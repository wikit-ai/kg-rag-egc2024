import time

from generator.mistral_generator import MistralGenerator
from retriever.el_retriever import ELRetriever
from entity_linking_mistralai.schema import Output
from typing import Any, Dict, List


class ELMistral:
    """Graph QA with entity linking-based retriever and mistral model as generator."""

    def __init__(self) -> None:
        self.retriever = ELRetriever()
        self.generator = MistralGenerator()

    def _format_output(
        self,
        execution_time: float,
        entities: Dict[str, Any],
        queries: List[str],
        context: str,
        answer: str,
    ) -> Output:
        """Change the output format."""

        output = Output(
            execution_time=execution_time,
            entities=entities,
            queries=queries,
            context=context,
            answer=answer,
        )
        return output

    def run(self, question: str) -> Output:
        """Answer a question based on a knowledge graph."""
        start_time = time.time()
        retriever_context = self.retriever.run(question)
        answer = self.generator.run(retriever_context["context"], question)
        execution_time = time.time() - start_time
        formatted_output = self._format_output(
            execution_time,
            retriever_context["question_entities"],
            retriever_context["queries"],
            retriever_context["context"],
            answer,
        )
        return formatted_output
