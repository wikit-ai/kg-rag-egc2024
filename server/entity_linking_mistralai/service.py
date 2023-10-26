import time

from entity_linking_mistralai.generator import MistralGenerator
from entity_linking_mistralai.retriever import ELRetriever
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
        context = self.retriever.run(question)
        answer = self.generator.run(context, question)
        execution_time = time.time() - start_time
        formatted_output = self._format_output(
            execution_time,
            self.retriever.el.question_entities,
            self.retriever.qp.queries,
            context,
            answer,
        )
        return formatted_output
