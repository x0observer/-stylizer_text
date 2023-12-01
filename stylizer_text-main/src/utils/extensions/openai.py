from typing import List, Optional
import openai
import os

#TO GETTING VARIABLES
from setup import settings

class OpenAIService:
    def generate_response_by_prompt(prompt: str, openai_key: str = os.environ["OPENAI_API_KEY"], unicode: Optional[str] = 'utf-8') -> str:
        prompt = f"{prompt}"
        max_tokens_for_response = min(1536, 4097 - len(prompt))
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens_for_response,
            n=1,
            temperature=0.7,
            api_key=openai_key
        )

        out_response = response['choices'][0]["text"]
        print("__out_response__", out_response.encode('utf-8').decode())
        return out_response if not unicode else out_response.encode('utf-8').decode()

    def generate_response_by_prompt_with_no_context(prompt: str, openai_key: str = os.environ["OPENAI_API_KEY"], unicode: Optional[str] = 'utf-8') -> str:
        prompt = f"{prompt}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=0,
            n=1,
            temperature=0.7,
            api_key=openai_key
        )

        out_response = response['choices'][0]["text"]
        return out_response if not unicode else out_response.encode('utf-8').decode()
    
    def summarize_news(news: str, summarize_prefix: str = "Пожалуйста, сократи новость и вырази ее суть в нескольких предложениях не теряя важную информацию", openai_key: str = os.environ["OPENAI_API_KEY"], unicode: Optional[str] = 'utf-8') -> str:
        max_tokens_limit = 2049  # Максимальное количество токенов, допустимое OpenAI
        total_length = len(summarize_prefix) + len(news)

        # Сокращение новости, если ее длина с префиксом превышает лимит
        if total_length > max_tokens_limit:
            sentences = news.split(".")
            summarized_news = ""
            current_length = len(summarize_prefix)

            for sentence in sentences:
                if current_length + len(sentence) + 1 <= max_tokens_limit:
                    summarized_news += sentence + ". "
                    current_length += len(sentence) + 1
                else:
                    break

            news = summarized_news.rstrip()

        finite_prompt = "%s: %s" % (summarize_prefix, news)

        # Устанавливаем максимальное количество токенов для ответа
        max_tokens_for_response = min(1025, 4097 - len(finite_prompt))  # Фиксированный лимит для ответа
        print("__finite_prompt__", len(finite_prompt))
        
        response = openai.Completion.create(
            model="text-davinci-003",  # При наличии более новой модели, обновите здесь
            prompt=finite_prompt,
            max_tokens=max_tokens_for_response,
            n=1,
            temperature=0.7,
            api_key=openai_key
        )

        out_response = response['choices'][0]["text"]
        return out_response if not unicode else out_response.encode('utf-8').decode()
    

    def summarize_news_conclusions(summarize_news_conclusions: [], stock_title: str, stock_ ,summarize_prefix: str = "Пожалуйста, сократи новость и вырази ее суть в нескольких предложениях не теряя важную информацию", openai_key: str = os.environ["OPENAI_API_KEY"], unicode: Optional[str] = 'utf-8') -> str:
        
        
        max_tokens_limit = 2049  # Максимальное количество токенов, допустимое OpenAI
        total_length = len(summarize_prefix) + len(news)

        # Сокращение новости, если ее длина с префиксом превышает лимит
        if total_length > max_tokens_limit:
            sentences = news.split(".")
            summarized_news = ""
            current_length = len(summarize_prefix)

            for sentence in sentences:
                if current_length + len(sentence) + 1 <= max_tokens_limit:
                    summarized_news += sentence + ". "
                    current_length += len(sentence) + 1
                else:
                    break

            news = summarized_news.rstrip()

        finite_prompt = "%s: %s" % (summarize_prefix, news)

        # Устанавливаем максимальное количество токенов для ответа
        max_tokens_for_response = min(1025, 4097 - len(finite_prompt))  # Фиксированный лимит для ответа
        print("__finite_prompt__", len(finite_prompt))
        
        response = openai.Completion.create(
            model="text-davinci-003",  # При наличии более новой модели, обновите здесь
            prompt=finite_prompt,
            max_tokens=max_tokens_for_response,
            n=1,
            temperature=0.7,
            api_key=openai_key
        )

        out_response = response['choices'][0]["text"]
        return out_response if not unicode else out_response.encode('utf-8').decode()