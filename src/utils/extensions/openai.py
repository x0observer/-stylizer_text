from sqlmodel import Session
from fastapi import Depends
# from engine import get_db
from setup import settings
# from register import MessageResponse
from typing import List
import openai
import os

#openai.api_key = os.environ["OPENAI_API_KEY"]#settings["openai"]["api_key"]


class OpenAIService:
    # def __init__(self, db: Session = Depends(get_db)):
    #     self.db = db
    
    def generate_response_by_prompt(prompt: str, openai_key: str = os.environ["OPENAI_API_KEY"]) -> str:
        prompt = f"{prompt}\n"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=len(prompt),
            n=1,
            temperature=0.7,
            api_key=openai_key
        )

        print("OPEN_AI_RESPONSE: ", response, type(response))
        return response['choices'][0]["text"]


