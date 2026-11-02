import httpx

from .config import settings


class OllamaError(Exception):
    """Raised when Ollama cannot generate a response."""


async def generate(
    prompt: str,
    system: str | None = None,
    temperature: float = 0.2,
) -> str:
    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    if system:
        payload["system"] = system

    url = f"{settings.ollama_base_url.rstrip('/')}/api/generate"

    try:
        async with httpx.AsyncClient(
            timeout=settings.ollama_timeout_seconds
        ) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()

    except httpx.TimeoutException as exc:
        raise OllamaError(
            "Ollama took too long to respond. Please try again."
        ) from exc

    except httpx.HTTPStatusError as exc:
        raise OllamaError(
            f"Ollama returned HTTP {exc.response.status_code}."
        ) from exc

    except httpx.RequestError as exc:
        raise OllamaError(
            "Cannot connect to Ollama. Make sure Ollama is running."
        ) from exc

    answer = result.get("response", "").strip()

    if not answer:
        raise OllamaError("Ollama returned an empty response.")

    return answer