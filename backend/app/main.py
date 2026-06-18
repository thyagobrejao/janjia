import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.database import SessionLocal, Base, engine
from app.models import User
from app.utils.security import get_password_hash
from app.routes import auth, chat, admin, observability

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("janjia.main")

# Inicialização do Rate Limiter baseado em Redis
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
)

def create_initial_admin():
    """Garante a existência de um usuário administrador no banco de dados."""
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
        if not admin_user:
            hashed_pwd = get_password_hash(settings.ADMIN_PASSWORD)
            new_admin = User(
                username=settings.ADMIN_USERNAME,
                email=settings.ADMIN_EMAIL,
                hashed_password=hashed_pwd,
                is_admin=True
            )
            db.add(new_admin)
            db.commit()
            logger.info(f"Usuário Admin '{settings.ADMIN_USERNAME}' criado com sucesso.")
        else:
            logger.info("Usuário Admin já existe.")
    except Exception as e:
        logger.error(f"Erro ao criar usuário administrador inicial: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Iniciando JanjIA Backend API...")
    create_initial_admin()
    yield
    # Shutdown
    logger.info("Parando JanjIA Backend API...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend para o JanjIA Chatbot Conversacional Satírico",
    version="1.0.0",
    lifespan=lifespan
)

# Configuração do Rate Limiter na app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware de CORS
cors_origins = ["*"] if settings.ENV == "development" else settings.ALLOWED_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Interceptor global para logar requisições e alimentar métricas de requisição
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Ignora logs e métricas nos endpoints de observabilidade
    if request.url.path in ["/metrics", "/health"]:
        return await call_next(request)
        
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Incrementa contador do Prometheus
    try:
        from app.routes.observability import http_requests_total
        http_requests_total.labels(method=request.method, endpoint=request.url.path).inc()
    except Exception:
        pass
        
    response = await call_next(request)
    return response

# Inclusão de Rotas
app.include_router(auth.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(observability.router)
