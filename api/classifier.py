from pydantic import BaseModel
from api.models import Categories
from openai import OpenAI


class Classification(BaseModel):
    category: Categories
    explanation: str


SYSTEM_PROMPT ="""
Please classify the following software license into one of these categories:

- **Productivity**
- **Design**
- **Communication**
- **Development**
- **Finance**
- **Marketing**

Write a 150-character explanation of why you choose this category
"""


class LicenseClassifier:
    def __init__(
            self, 
            api_key: int,
            system_prompt: str = SYSTEM_PROMPT,
            model_name: str = "gpt-4o-mini"):

        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def run(
            self,
            query: str) -> Classification:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": query},
        ]
        completion = self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=messages,
            response_format=Classification,
                )
        output = completion.choices[0].message.parsed
        return output
