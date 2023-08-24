from typing import List, Optional
import openai
import os

#TO GETTING VARIABLES
from setup import settings

class OpenAIService:
    def generate_response_by_prompt(prompt: str, openai_key: str = os.environ["OPENAI_API_KEY"], unicode: Optional[str] = 'utf-8') -> str:
        prompt = f"{prompt}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=len(prompt),
            n=1,
            temperature=0.7,
            api_key=openai_key
        )

        out_response = response['choices'][0]["text"]
        return out_response if not unicode else out_response.encode('utf-8').decode()


