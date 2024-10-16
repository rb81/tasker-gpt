import os, httpx
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class LLMOpenAI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        self.client = OpenAI(api_key=self.api_key)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.RequestError))
    )
    def call(self, messages: list, response_format: BaseModel):
        try:
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=messages,
                response_format=response_format,
                timeout=60  # Set a 60-second timeout
            )
            return completion.choices[0].message.content
        except httpx.TimeoutException:
            raise Exception("Request to OpenAI API timed out")
        except httpx.RequestError as e:
            raise Exception(f"Request to OpenAI API failed: {str(e)}")
