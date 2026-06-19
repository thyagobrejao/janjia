import json
import logging
import httpx
import asyncio
from typing import AsyncGenerator, Dict, Any, List
from app.config import settings

logger = logging.getLogger("janjia.llm")

class LLMService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT
        self.max_retries = settings.OLLAMA_MAX_RETRIES

    async def get_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def check_model_exists(self) -> bool:
        """Verifica se o modelo configurado existe localmente no Ollama."""
        try:
            async with await self.get_client() as client:
                response = await client.get("/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [m.get("name") for m in models]
                    # Também checa variações (ex: sem tag ':latest' ou ':8b')
                    return any(self.model in name or name in self.model for name in model_names)
        except Exception as e:
            logger.error(f"Erro ao verificar modelo no Ollama: {e}")
        return False

    async def pull_model(self) -> bool:
        """Faz download do modelo configurado no Ollama."""
        logger.info(f"Iniciando download do modelo '{self.model}' no Ollama...")
        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=None) as client:
                async with client.stream("POST", "/api/pull", json={"name": self.model}) as response:
                    if response.status_code == 200:
                        async for line in response.aiter_lines():
                            if line:
                                data = json.loads(line)
                                status = data.get("status", "")
                                completed = data.get("completed", 0)
                                total = data.get("total", 0)
                                if total > 0:
                                    percent = (completed / total) * 100
                                    logger.info(f"Pulling {self.model}: {status} ({percent:.2f}%)")
                                else:
                                    logger.info(f"Pulling {self.model}: {status}")
                        logger.info(f"Modelo '{self.model}' baixado com sucesso.")
                        return True
        except Exception as e:
            logger.error(f"Falha ao baixar modelo '{self.model}': {e}")
        return False

    async def chat_stream(self, messages: List[Dict[str, str]]) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Envia histórico de mensagens para o Ollama e retorna gerador com pedaços do texto e estatísticas.
        Implementa retentativas em caso de falha de conexão inicial.
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True
        }

        retries = 0
        backoff = 1.0

        while retries <= self.max_retries:
            try:
                async with await self.get_client() as client:
                    # Abre conexão em stream
                    request = client.build_request("POST", "/api/chat", json=payload)
                    response = await client.send(request, stream=True)
                    
                    try:
                        if response.status_code != 200:
                            await response.aread()
                            raise httpx.HTTPStatusError(
                                f"Ollama respondeu com status {response.status_code}",
                                request=request,
                                response=response
                            )
                        
                        # Sucesso ao conectar: lê a stream
                        async for line in response.aiter_lines():
                            if not line:
                                continue
                            try:
                                chunk = json.loads(line)
                                yield chunk
                            except json.JSONDecodeError:
                                logger.warning(f"Falha ao decodificar chunk: {line}")
                        
                        # Finaliza com sucesso
                        return
                    finally:
                        await response.aclose()

            except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPStatusError) as e:
                retries += 1
                logger.warning(f"Tentativa {retries} falhou ao conectar ao Ollama ({type(e).__name__}: {e}).")
                if retries > self.max_retries:
                    logger.error("Número máximo de retentativas atingido para o Ollama.")
                    raise e
                await asyncio.sleep(backoff)
                backoff *= 2.0  # Backoff exponencial

