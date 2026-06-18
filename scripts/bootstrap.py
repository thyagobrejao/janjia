import socket
import time
import sys
import asyncio
import httpx
import redis

# Ajusta path para importar do backend app
sys.path.append("/app")

from app.config import settings
from app.services.llm import LLMService

def wait_for_port(host: str, port: int, name: str):
    """Loop de espera até que a porta de rede do serviço esteja aberta."""
    print(f"Aguardando {name} ({host}:{port})...")
    start_time = time.time()
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((host, port))
            print(f"-> {name} está pronto!")
            break
        except Exception:
            time.sleep(2)
            if time.time() - start_time > 120:
                print(f"AVISO: Tempo de espera limite excedido para {name}. Continuando...")
                break

def wait_for_redis():
    """Loop de espera pela inicialização do Redis."""
    print(f"Aguardando Redis ({settings.REDIS_HOST}:{settings.REDIS_PORT})...")
    start_time = time.time()
    while True:
        try:
            r = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                socket_timeout=2
            )
            r.ping()
            print("-> Redis está pronto!")
            break
        except Exception:
            time.sleep(2)
            if time.time() - start_time > 60:
                print("AVISO: Tempo limite excedido para o Redis. Continuando...")
                break

def wait_for_ollama():
    """Loop de espera pela inicialização do Ollama."""
    print(f"Aguardando Ollama ({settings.OLLAMA_BASE_URL})...")
    start_time = time.time()
    while True:
        try:
            r = httpx.get(f"{settings.OLLAMA_BASE_URL}/", timeout=2)
            if r.status_code == 200:
                print("-> Ollama está pronto!")
                break
        except Exception:
            time.sleep(2)
            if time.time() - start_time > 60:
                print("AVISO: Tempo limite excedido para o Ollama. Continuando...")
                break

async def ensure_llm_model():
    """Verifica e faz o download do modelo configurado se necessário."""
    llm = LLMService()
    try:
        model_exists = await llm.check_model_exists()
        if not model_exists:
            print(f"Modelo '{llm.model}' não encontrado no Ollama. Iniciando o pull...")
            success = await llm.pull_model()
            if success:
                print(f"-> Modelo '{llm.model}' baixado com sucesso!")
            else:
                print(f"-> AVISO: Falha ao baixar o modelo '{llm.model}'. Verifique sua conexão de internet.")
        else:
            print(f"-> Modelo '{llm.model}' já está disponível no Ollama.")
    except Exception as e:
        print(f"Erro durante a verificação/pull do modelo no Ollama: {e}")

if __name__ == "__main__":
    print("Iniciando verificação de dependências...")
    
    # 1. Espera Postgres
    wait_for_port(settings.POSTGRES_SERVER, settings.POSTGRES_PORT, "PostgreSQL")
    
    # 2. Espera Redis
    wait_for_redis()
    
    # 3. Espera Ollama
    wait_for_ollama()
    
    # 4. Certifica o modelo no Ollama
    asyncio.run(ensure_llm_model())
    
    print("Verificação de dependências concluída!")
