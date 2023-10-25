import time

from entity_linking_mistralai.generator import MistralGenerator
from entity_linking_mistralai.retriever import ELRetriever
from entity_linking_mistralai.router import Output
from typing import Any, Dict, List


class ELMistral:
    def __init__(self) -> None:
        self.retriever = ELRetriever()
        self.generator = MistralGenerator()

    def _format_output(
        self,
        entities: Dict[str, Any],
        queries: List[str],
        context: str,
        answer: str,
        execution_time: float,
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
        start_time = time.time()
        self.retriever.run(question)
        answer = self.generator.run(self.retriever.context, question)
        execution_time = time.time() - start_time
        formated_output = self._format_output(
            execution_time,
            self.retriever.el.entities,
            self.retriever.qp.queries,
            self.retriever.context,
            answer,
        )
        return formated_output
