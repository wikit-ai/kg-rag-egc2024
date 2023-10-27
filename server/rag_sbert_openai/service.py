import time

from generator.openai_generator import OpenAIGenerator
from retriever.similarity_retriever import SimilarityRetriever
from rag_sbert_openai.schema import Output
from typing import Any, Dict, List


class RagSBertOpenAI:
    """Graph QA with similarity-based retriever and OpenAI model as generator."""

    def __init__(self) -> None:
        self.retriever = SimilarityRetriever()
        self.generator = OpenAIGenerator()

    def _format_output(
        self,
        execution_time: float,
        context: str,
        answer: str,
    ) -> Output:
        """Change the output format."""

        output = Output(
            execution_time=execution_time,
            context=context,
            answer=answer,
        )
        return output

    def run(self, question: str) -> Output:
        """Answer a question based on a knowledge graph."""
        start_time = time.time()
        context = self.retriever.run(question)
        answer = self.generator.run(context, question)
        execution_time = time.time() - start_time
        formatted_output = self._format_output(
            execution_time,
            context,
            answer,
        )
        return formatted_output
