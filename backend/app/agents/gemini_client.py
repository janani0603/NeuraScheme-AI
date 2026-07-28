from groq import AsyncGroq
from app.config.settings import settings

_client: AsyncGroq | None = None


def get_groq_client() -> AsyncGroq:
    global _client
    if _client is None:
        _client = AsyncGroq(api_key=settings.GROQ_API_KEY)
    return _client


async def generate(prompt: str, temperature: float = 0.3) -> str:
    """
    Send a prompt to Groq (Llama) and return the text response.
    Raises RuntimeError on API failure.
    """
    client = get_groq_client()
    try:
        response = await client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Groq API error: {e}") from e
