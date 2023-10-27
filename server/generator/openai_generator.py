import openai
import os


class OpenAIGenerator:
    """Generator based on Mistral model for the RAG task."""

    def __init__(self) -> None:
        openai.organization = os.getenv("OPENAI_ORG")
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def _generate_prompt(self, context: str) -> str:
        """Generate contextualised prompt for OpenAI model."""
        prompt = f"""You are an assistant that helps to form nice and human understandable answers.
        The information part contains the provided information that you must use to construct an answer.
        The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
        Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
        If the provided information is empty, say that you don't know the answer.
        Information:
        {context}"""

        return prompt

    def _generate_answer(self, prompt: str, question: str) -> str:
        """Generate answer with OpenAI model based on a given prompt."""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
            ]
            )
        answer = response['choices'][0]['message']['content']
        return answer

    def run(self, context: str, question: str) -> str:
        """Generate answer with a contextualised prompt for a given question."""
        prompt = self._generate_prompt(context)
        answer = self._generate_answer(prompt, question)
        return answer
