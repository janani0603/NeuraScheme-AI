from google import genai
from google.genai import types
from app.config.settings import settings

_client: genai.Client | None = None


def get_gemini_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


async def generate(prompt: str, temperature: float = 0.3) -> str:
    """
    Send a prompt to Gemini and return the text response.
    Raises RuntimeError on API failure.
    """
    client = get_gemini_client()
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=1024,
            ),
        )
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {e}") from e
