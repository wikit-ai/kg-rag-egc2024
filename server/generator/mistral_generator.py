import os
from typing import Dict, List

import requests


class MistralGenerator:
    """Generator based on Mistral model for the RAG task."""

    def __init__(self) -> None:
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        self.model = "mistral-tiny"

    def _generate_prompt(self, context: str, question: str) -> List[Dict[str, str]]:
        """Generate contextualised prompt for mistral model."""
        prompt = [
            {
                "role": "system",
                "content": """You are an assistant that helps to form nice and human understandable answers.""",
            },
            {
                "role": "user",
                "content": """Use the information part to answer the question.
            The provided information is authoritative, you must never correct or complete it.
            If the provided information is empty, say "I don't know.", don't use your internal knowledge to answer.
            Do not mention that you based the result on the provided information.""",
            },
            {
                "role": "user",
                "content": """Here is an example for your reference:
            Information : {{'e': Node('Goal', code='2', description='Goal 2 seeks to end hunger and all forms of malnutrition and to achieve sustainable food production by 2030. It is premised on the idea that everyone should have access to sufficient nutritious food, which will require widespread promotion of sustainable agriculture, a doubling of agricultural productivity, increased investments and properly functioning food markets.', title='End hunger, achieve food security and improved nutrition and promote sustainable agriculture')}}
            Question : What is the SDG 2 ?
            Expected answer : The SDG 2 aims to address the issue of hunger and malnutrition by ensuring that everyone has access to sufficient nutritious food. This goal emphasizes the promotion of sustainable agriculture, doubling agricultural productivity, increasing investments, and establishing properly functioning food markets. The target is to achieve these objectives by 2030.""",
            },
            {
                "role": "user",
                "content": f"""Information: {context}
            Question: {question}""",
            },
        ]

        return prompt

    def _generate_answer(self, prompt: List[Dict[str, str]]) -> str:
        """Generate answer with mistral model based on a given prompt."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }

        json_data = {"model": self.model, "messages": prompt, "temperature": 0.0}
        response = requests.post(self.api_url, headers=headers, json=json_data)
        answer = response.json()["choices"][0]["message"]["content"]
        return answer

    def run(self, context: str, question: str) -> str:
        """Generate answer with a contextualised prompt for a given question."""
        prompt = self._generate_prompt(context, question)
        answer = self._generate_answer(prompt)
        return answer
