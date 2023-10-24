import os
import time

from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
from typing import Any, Dict


class LangChainGraphQA:
    def __init__(self) -> None:
        self.graph = Neo4jGraph(
            url=os.environ.get("GRAPH_URI"),
            username=os.environ.get("GRAPH_USER"),
            password=os.environ.get("GRAPH_PASSWORD"),
        )

        self.chain = GraphCypherQAChain.from_llm(
            ChatOpenAI(temperature=0),
            graph=self.graph,
            verbose=True,
            return_intermediate_steps=True,
        )

    def _format_output(
        self, model_answer: Dict[str, Any], execution_time: float
    ) -> Dict[str, Any]:
        output = {}
        output["execution_time"] = execution_time
        output["query"] = model_answer["intermediate_steps"][0]["query"]
        output["context"] = model_answer["intermediate_steps"][1]["context"]
        output["answer"] = model_answer["result"]
        return output

    def run(self, utterance: str) -> Dict[str, Any]:
        start_time = time.time()
        # TODO : Add error handling here but how ??
        results = self.chain(utterance)
        execution_time = time.time() - start_time
        formated_output = self._format_output(results, execution_time)
        return formated_output
