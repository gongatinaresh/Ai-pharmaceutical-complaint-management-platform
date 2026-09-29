from groq import Groq

from app.core.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def generate_ai_response(user_text: str) -> str:
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI assistant for a pharmaceutical "
                    "customer complaint management system."
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content