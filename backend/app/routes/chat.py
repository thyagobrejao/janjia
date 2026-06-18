import json
import logging
import re
import os
from functools import lru_cache
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.database import get_db, SessionLocal
from app.models import Conversation, Message, User
from app.schemas import ConversationCreate, ConversationResponse, ConversationUpdate, MessageCreate, MessageResponse
from app.utils.security import get_current_user
from app.services.llm import LLMService
from app.services.satire_engine import SatireEngine

logger = logging.getLogger("janjia.chat")
router = APIRouter(prefix="/conversations", tags=["chat"])

# Caminho do prompt do sistema
SYSTEM_PROMPT_PATH = "/app/prompts/system.txt"

@lru_cache(maxsize=1)
def load_system_prompt() -> str:
    """Lê o prompt do sistema configurado. Resultado é cacheado (requer restart para atualizar)."""
    if os.path.exists(SYSTEM_PROMPT_PATH):
        try:
            with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Erro ao carregar prompts/system.txt: {e}")
    
    # Fallback caso o arquivo falhe
    return (
        "Você é JanjIA. Uma inteligência artificial humorística. "
        "Seu objetivo é responder perguntas normalmente, porém introduzindo elementos satíricos, absurdos e nonsense."
    )

@router.get("", response_model=List[ConversationResponse])
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todas as conversas do usuário ordenadas por atualização recente."""
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )
    return conversations

@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(
    conv_in: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria uma nova conversa."""
    conversation = Conversation(
        title=conv_in.title,
        user_id=current_user.id
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

@router.patch("/{conversation_id}", response_model=ConversationResponse)
def rename_conversation(
    conversation_id: int,
    conv_in: ConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Renomeia uma conversa existente."""
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id)
        .first()
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversa não encontrada"
        )
    
    conversation.title = conv_in.title
    db.commit()
    db.refresh(conversation)
    return conversation

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Exclui uma conversa e todas as suas mensagens."""
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id)
        .first()
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversa não encontrada"
        )
    
    db.delete(conversation)
    db.commit()
    return

@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
def list_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém o histórico de mensagens de uma conversa específica."""
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id)
        .first()
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversa não encontrada"
        )
    
    return conversation.messages

@router.post("/{conversation_id}/messages")
async def send_message(
    conversation_id: int,
    msg_in: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Envia uma pergunta, salva o input do usuário e inicia
    a stream SSE da resposta gerada pelo LLM e satirizada.
    """
    # Valida a posse da conversa
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id)
        .first()
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversa não encontrada"
        )

    # 1. Salva a mensagem do usuário no DB
    user_message = Message(
        conversation_id=conversation_id,
        role="user",
        content=msg_in.content,
        satire_level=0
    )
    db.add(user_message)
    
    # Atualiza timestamp da conversa
    conversation.updated_at = func.now()
    db.commit()

    # 2. Prepara o histórico de mensagens para enviar ao Ollama
    # Carrega as últimas 20 mensagens para contexto de chat (busca desc e inverte)
    past_messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(20)
        .all()
    )[::-1]  # Reverte para ordem cronológica

    llm_messages = []
    # Injeta System Prompt original
    llm_messages.append({"role": "system", "content": load_system_prompt()})
    
    for msg in past_messages:
        llm_messages.append({"role": msg.role, "content": msg.content})

    # 3. Define gerador assíncrono para o streaming SSE
    async def sse_generator():
        # Cria uma sessão exclusiva para o ciclo de vida da stream as síncrona
        async_db = SessionLocal()
        llm = LLMService()
        
        current_sentence = ""
        accumulated_raw = []
        accumulated_satirized = []
        prompt_tokens = 0
        completion_tokens = 0
        
        try:
            async for chunk in llm.chat_stream(llm_messages):
                msg = chunk.get("message", {})
                content = msg.get("content", "")
                
                if chunk.get("done", False):
                    prompt_tokens = chunk.get("prompt_eval_count", 0)
                    completion_tokens = chunk.get("eval_count", 0)
                
                if content:
                    current_sentence += content
                    
                    # Identifica limites de sentenças para satirização fluida (. ! ? \n)
                    matches = list(re.finditer(r'[.!?\n]+', current_sentence))
                    if matches:
                        last_idx = matches[-1].end()
                        to_process = current_sentence[:last_idx]
                        current_sentence = current_sentence[last_idx:]
                        
                        # Aplica o Motor de Satirização
                        satirized = SatireEngine.satirize_text(to_process, msg_in.satire_level)
                        accumulated_raw.append(to_process)
                        accumulated_satirized.append(satirized)
                        
                        yield {"event": "message", "data": json.dumps({"content": satirized})}
            
            # Processa o restante final se houver
            if current_sentence.strip():
                satirized = SatireEngine.satirize_text(current_sentence, msg_in.satire_level)
                accumulated_raw.append(current_sentence)
                accumulated_satirized.append(satirized)
                yield {"event": "message", "data": json.dumps({"content": satirized})}
            
            # Monta o texto completo satirizado
            final_content = "".join(accumulated_satirized)
            if not final_content.strip():
                final_content = "Os abacates confabulavam em silêncio... (Erro de geração)"

            # 4. Salva a resposta da IA no banco
            assistant_message = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=final_content,
                satire_level=msg_in.satire_level,
                tokens_prompt=prompt_tokens,
                tokens_completion=completion_tokens
            )
            async_db.add(assistant_message)
            
            # Atualiza também a conversa
            conv = async_db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if conv:
                conv.updated_at = func.now()
                
            async_db.commit()
            async_db.refresh(assistant_message)
            
            # Envia o evento de encerramento com os dados salvos da mensagem
            yield {
                "event": "done",
                "data": json.dumps({
                    "id": assistant_message.id,
                    "conversation_id": assistant_message.conversation_id,
                    "role": assistant_message.role,
                    "content": assistant_message.content,
                    "satire_level": assistant_message.satire_level,
                    "tokens_prompt": assistant_message.tokens_prompt,
                    "tokens_completion": assistant_message.tokens_completion,
                    "created_at": assistant_message.created_at.isoformat()
                })
            }
            
        except Exception as e:
            logger.error(f"Erro na stream SSE da conversa {conversation_id}: {e}")
            yield {"event": "error", "data": json.dumps({"detail": f"Erro interno na stream: {str(e)}"}) }
        finally:
            async_db.close()

    return EventSourceResponse(sse_generator())
