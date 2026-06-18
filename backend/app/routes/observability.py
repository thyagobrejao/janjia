import time
import httpx
import redis
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Gauge, Counter
from app.database import get_db, engine
from app.config import settings
from app.models import User, Conversation, Message

router = APIRouter(tags=["observability"])

# Definição de métricas do Prometheus
METRICS_PREFIX = "janjia_"

# Gauges dinâmicos para estatísticas do sistema
users_gauge = Gauge(f"{METRICS_PREFIX}users_total", "Total de usuários registrados no sistema")
conversations_gauge = Gauge(f"{METRICS_PREFIX}conversations_total", "Total de conversas criadas")
messages_gauge = Gauge(f"{METRICS_PREFIX}messages_total", "Total de mensagens registradas", ["role"])
tokens_gauge = Gauge(f"{METRICS_PREFIX}tokens_total", "Total de tokens consumidos", ["type"])
service_health_gauge = Gauge(f"{METRICS_PREFIX}service_health", "Status de saúde do serviço (1 = OK, 0 = Erro)", ["service"])

# Contadores de requisições
http_requests_total = Counter(f"{METRICS_PREFIX}http_requests_total", "Total de requisições HTTP", ["method", "endpoint"])

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Verifica a integridade do banco de dados, Redis e Ollama."""
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "postgres": "unhealthy",
            "redis": "unhealthy",
            "ollama": "unhealthy"
        }
    }
    
    # 1. Testa Postgres
    try:
        db.execute(text("SELECT 1"))
        health_status["services"]["postgres"] = "healthy"
        service_health_gauge.labels(service="postgres").set(1)
    except Exception as e:
        health_status["status"] = "degraded"
        service_health_gauge.labels(service="postgres").set(0)

    # 2. Testa Redis
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, socket_timeout=2)
        r.ping()
        health_status["services"]["redis"] = "healthy"
        service_health_gauge.labels(service="redis").set(1)
    except Exception as e:
        health_status["status"] = "degraded"
        service_health_gauge.labels(service="redis").set(0)

    # 3. Testa Ollama
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/")
            if response.status_code == 200:
                health_status["services"]["ollama"] = "healthy"
                service_health_gauge.labels(service="ollama").set(1)
            else:
                health_status["status"] = "degraded"
                service_health_gauge.labels(service="ollama").set(0)
    except Exception as e:
        health_status["status"] = "degraded"
        service_health_gauge.labels(service="ollama").set(0)

    return health_status

@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    """
    Expõe métricas do sistema no formato Prometheus.
    Atualiza gauges dinâmicos lendo do banco de dados.
    """
    # Atualiza usuários
    try:
        total_users = db.query(func.count(User.id)).scalar() or 0
        users_gauge.set(total_users)
    except Exception:
        pass

    # Atualiza conversas
    try:
        total_conversations = db.query(func.count(Conversation.id)).scalar() or 0
        conversations_gauge.set(total_conversations)
    except Exception:
        pass

    # Atualiza mensagens
    try:
        user_msgs = db.query(func.count(Message.id)).filter(Message.role == "user").scalar() or 0
        assistant_msgs = db.query(func.count(Message.id)).filter(Message.role == "assistant").scalar() or 0
        messages_gauge.labels(role="user").set(user_msgs)
        messages_gauge.labels(role="assistant").set(assistant_msgs)
    except Exception:
        pass

    # Atualiza tokens
    try:
        tokens_query = db.query(
            func.sum(Message.tokens_prompt).label("prompt"),
            func.sum(Message.tokens_completion).label("completion")
        ).filter(Message.role == "assistant").first()
        
        prompt_tokens = int(tokens_query.prompt or 0) if tokens_query else 0
        completion_tokens = int(tokens_query.completion or 0) if tokens_query else 0
        
        tokens_gauge.labels(type="prompt").set(prompt_tokens)
        tokens_gauge.labels(type="completion").set(completion_tokens)
    except Exception:
        pass

    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
