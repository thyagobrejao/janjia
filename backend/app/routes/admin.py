from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import User, Conversation, Message
from app.schemas import AdminUserDetail, AdminStatsDashboard
from app.utils.security import get_current_admin
from app.config import settings

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[AdminUserDetail])
def list_admin_users(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Retorna a lista detalhada de usuários com a contagem de suas conversas."""
    # Realiza query com join para contar as conversas
    results = (
        db.query(
            User.id,
            User.username,
            User.email,
            User.is_admin,
            User.created_at,
            func.count(Conversation.id).label("conversation_count")
        )
        .outerjoin(Conversation, User.id == Conversation.user_id)
        .group_by(User.id)
        .order_by(User.created_at.desc())
        .all()
    )
    
    users_list = []
    for r in results:
        users_list.append(
            AdminUserDetail(
                id=r.id,
                username=r.username,
                email=r.email,
                is_admin=r.is_admin,
                created_at=r.created_at,
                conversation_count=r.conversation_count
            )
        )
        
    return users_list

@router.get("/stats", response_model=AdminStatsDashboard)
def get_dashboard_stats(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Calcula estatísticas de uso para o painel administrativo."""
    # Total de usuários
    total_users = db.query(func.count(User.id)).scalar() or 0
    
    # Usuários ativos nas últimas 24 horas (que criaram/atualizaram conversas ou mandaram mensagens)
    time_24h_ago = datetime.now(timezone.utc) - timedelta(hours=24)
    active_users_24h = (
        db.query(func.count(User.id.distinct()))
        .join(Conversation, User.id == Conversation.user_id)
        .filter(Conversation.updated_at >= time_24h_ago)
        .scalar()
    ) or 0
    
    # Total de conversas
    total_conversations = db.query(func.count(Conversation.id)).scalar() or 0
    
    # Total de perguntas (role = user) e respostas (role = assistant)
    total_questions = (
        db.query(func.count(Message.id))
        .filter(Message.role == "user")
        .scalar()
    ) or 0
    
    total_answers = (
        db.query(func.count(Message.id))
        .filter(Message.role == "assistant")
        .scalar()
    ) or 0
    
    # Total de tokens
    tokens_query = (
        db.query(
            func.sum(Message.tokens_prompt).label("prompt"),
            func.sum(Message.tokens_completion).label("completion")
        )
        .filter(Message.role == "assistant")
        .first()
    )
    
    total_prompt_tokens = int(tokens_query.prompt or 0) if tokens_query else 0
    total_completion_tokens = int(tokens_query.completion or 0) if tokens_query else 0
    
    return AdminStatsDashboard(
        total_users=total_users,
        active_users_24h=active_users_24h,
        total_conversations=total_conversations,
        total_questions=total_questions,
        total_answers=total_answers,
        total_prompt_tokens=total_prompt_tokens,
        total_completion_tokens=total_completion_tokens,
        model_name=settings.OLLAMA_MODEL
    )
