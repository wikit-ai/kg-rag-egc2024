import os
import requests


class MistralGenerator:
    def __init__(self) -> None:
        self.model_api_url = os.environ.get("MODEL_API_URL")
        self.model_token = os.environ.get("MODEL_TOKEN")

    def _generate_prompt(self, context: str, question: str) -> str:
        prompt = f"""<s> [INST] You are an assistant that helps to form nice and human understandable answers.
        Use the information part to answer the question. 
        The provided information is authoritative, you must never correct or complete it.
        Do not mention that you based the result on the given information.
        If the provided information is empty, say that you don't know the answer, don't use your internal knowledge.
        Your answer must start with a [ANSWER] tag and end with a [/ANSWER] tag.

        Here is an example for your reference:
        Information : {{'e': Node('Goal', code='2', description='Goal 2 seeks to end hunger and all forms of malnutrition and to achieve sustainable food production by 2030. It is premised on the idea that everyone should have access to sufficient nutritious food, which will require widespread promotion of sustainable agriculture, a doubling of agricultural productivity, increased investments and properly functioning food markets.', title='End hunger, achieve food security and improved nutrition and promote sustainable agriculture')}}
        Question : What is the SDG 2 ?
        Expected answer : [ANSWER] The SDG 2 aims to address the issue of hunger and malnutrition by ensuring that everyone has access to sufficient nutritious food. This goal emphasizes the promotion of sustainable agriculture, doubling agricultural productivity, increasing investments, and establishing properly functioning food markets. The target is to achieve these objectives by 2030. [/ANSWER]

        Information:
        {context}

        Question: 
        {question}[/INST]"""

        return prompt

    def _generate_answer(self, prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self.model_token}"}
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 1024, "temperature": 0.1},
        }

        response = requests.post(self.model_api_url, headers=headers, json=payload)
        answer = response.json()[0]["generated_text"]
        extracted_answer = answer[answer.find("[/INST]") :]
        if "[ANSWER]" in extracted_answer:
            extracted_answer = extracted_answer[extracted_answer.find("[ANSWER]") :]
            extracted_answer = extracted_answer.replace("[/ANSWER]", "")
            extracted_answer = extracted_answer.replace("[ANSWER]", "")
        else:
            extracted_answer = "I don't know."
        return extracted_answer

    def run(self, context: str, question: str) -> str:
        prompt = self._generate_prompt(context, question)
        answer = self._generate_answer(prompt)
        return answer
