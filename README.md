# JanjIA - Chatbot Satírico e Absurdo (Paródia)

O **JanjIA** é um sistema de chatbot conversacional satírico e bem-humorado, desenvolvido no estilo do ChatGPT, mas com uma personalidade única, teimosa e intencionalmente absurda. O projeto orquestra uma stack moderna completa usando Docker Compose.

---

## 🚀 Tecnologias Utilizadas

### Frontend
- **Vue 3** (Composition API)
- **Vite** (Build tool rápido)
- **Pinia** (Gerenciamento de estado global)
- **Vue Router** (Roteamento de views dinâmicas)
- **Axios** (Comunicação HTTP com interceptors para JWT)
- **TailwindCSS v3** (Estilização premium com suporte nativo a tema escuro/claro)

### Backend
- **Python 3.12**
- **FastAPI** (API assíncrona, robusta e tipada)
- **SQLAlchemy** (ORM assíncrono e síncrono com pool pré-ping)
- **Alembic** (Orquestração e versionamento de migrações SQL)
- **SlowAPI** (Rate limiting por IP usando Redis)
- **Uvicorn** (Servidor de aplicação ASGI de alta performance)

### Banco de Dados & Cache
- **PostgreSQL 16** (Armazenamento persistente de usuários, chats e mensagens)
- **Redis 7** (Cache para controle de taxa e persistência rápida de estados)

### Modelo de Linguagem (LLM)
- **Ollama** (Servidor local de inferência)
- **Qwen3:8b** (Modelo padrão leve de alta qualidade para texto em português)

### Proxy & Servidor Web
- **Nginx** (Proxy reverso centralizado, gzip, segurança e suporte a Server-Sent Events)

---

## 📂 Estrutura de Diretórios

```text
/janjia
├── backend/
│   ├── app/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── admin.py
│   │   │   └── observability.py
│   │   ├── services/
│   │   │   ├── llm.py
│   │   │   └── satire_engine.py
│   │   └── utils/
│   │       └── security.py
│   ├── migrations/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── stores/
│   │   ├── utils/
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── vite.config.js
│   └── Dockerfile
├── nginx/
│   ├── nginx.conf
│   └── Dockerfile
├── prompts/
│   └── system.txt
├── scripts/
│   ├── bootstrap.py
│   └── entrypoint.sh
├── docker-compose.yml
├── .env.example
├── .env
└── README.md
```

---

## 🛠️ Instalação e Execução

### Pré-requisitos
- Docker e Docker Compose instalados no sistema.

### Passo 1: Configurar Variáveis de Ambiente
Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```
Ajuste os segredos do JWT e as senhas conforme necessário.

### Passo 2: Iniciar a Stack Completa
Apenas execute o comando padrão do Compose na raiz:
```bash
docker compose up -d
```

Este comando irá subir todos os containers. O container do `backend` irá aguardar o banco estar online e automaticamente verificará se o modelo `qwen3:8b` (ou o especificado em `.env`) existe no Ollama. Caso não exista, o container **baixará o modelo automaticamente** (Pulling) antes de executar as migrações do banco (`alembic upgrade head`) e iniciar a API.

Acompanhe o progresso de download com:
```bash
docker compose logs -f backend
```

---

## 🖥️ Portas e Endpoints Locais

- **Frontend & API Gateway**: `http://localhost` (Porta 80 mapeada pelo Nginx)
- **API FastAPI (Direto)**: `http://localhost:8000` (Para desenvolvimento/depuração)
- **Painel Administrativo**: `http://localhost/admin`
- **Métricas do Prometheus**: `http://localhost/metrics`
- **Health Check**: `http://localhost/health`
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`

---

## ⚙️ Configurações do Motor de Satirização

O motor de satirização altera as respostas do LLM em tempo real no streaming SSE. O nível de satirização é passado a cada envio de mensagem pelo usuário:

- **Nível 0**: Resposta direta do LLM, sem alterações humorísticas.
- **Nível 1 (Leve)**: Introduz erros ocasionais e leves de português (ex: "comcerteza", "mais" no lugar de "mas") e 10% de chance de anexar piadas rápidas no final de sentenças.
- **Nível 2 (Moderado)**: Erros de português adicionais, analogias absurdas (ex: "isso faz tanto sentido quanto colocar uma capota em um submarino") e tom de autoconfiança exagerado.
- **Nível 3 (Totalmente Nonsense)**: Mudanças abruptas de assunto (ex: discutir capivaras julgadoras ou tomada de três pinos) e distorções completas do sentido original mantendo a estrutura da resposta.

---

## 🛡️ Usuário Administrador Inicial

Ao iniciar pela primeira vez, o backend insere automaticamente um usuário administrador no banco de dados baseado nos valores do `.env`:
- **Usuário**: `admin`
- **E-mail**: `admin@janjia.local`
- **Senha**: `admin_senha_secreta_123`

Entre com essa conta e navegue até `/admin` no navegador para visualizar o painel do dashboard administrativo.

---

## 💾 Rotinas de Backup

### Backup do Banco de Dados PostgreSQL
Para realizar o backup manual dos dados de conversas e usuários:
```bash
docker compose exec -t postgres pg_dumpall -c -U janjia_user > backup_janjia.sql
```

### Restauração do Banco de Dados
Para restaurar o backup gerado:
```bash
cat backup_janjia.sql | docker compose exec -T postgres psql -U janjia_user -d janjia_db
```

---

## ☁️ Oracle Cloud ARM64 Deployment (Ampere)

A stack do JanjIA é **totalmente compatível** com arquiteturas ARM64 (Oracle Cloud Ampere A1).

### 1. Imagens Multi-arch
Todas as imagens base utilizadas nos `Dockerfiles` (`python:3.12-slim`, `node:20-alpine`, `nginx:alpine`, `postgres:16-alpine`, `redis:7-alpine`) possuem suporte oficial nativo a ARM64. O build local compilará para a arquitetura nativa da máquina.

### 2. Compilação para ARM64 (Buildx)
Caso você esteja compilando as imagens a partir de uma máquina local AMD64 (Intel/AMD) para subir na nuvem ARM64, utilize o `docker buildx`:
```bash
docker buildx build --platform linux/arm64 -t seu-usuario/janjia-backend:latest ./backend --push
docker buildx build --platform linux/arm64 -t seu-usuario/janjia-frontend:latest ./frontend --push
```

### 3. Otimizações de CPU no ARM64 para Ollama
Para instâncias Oracle Ampere rodando Ollama sem GPU dedicada:
- Garanta que a VM tenha no mínimo **4 Cores e 8GB de RAM** (A1 Flex).
- O modelo `qwen3:8b` (ou `qwen2.5:7b`/`qwen2.5:3b`) roda perfeitamente em CPU ARM64 usando otimizações GGML nativas do Ollama.
- O tempo médio de início de geração (Time-to-first-token) na CPU ARM64 é de ~1.5s, o que é otimizado no JanjIA devido ao nosso processamento de sentenças assíncrono.
