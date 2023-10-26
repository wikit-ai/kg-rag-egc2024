import os
import time

from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
from langchain_graph_qa_openai.schema import Output
from typing import Any, Dict

from langchain_custom_openai.schema import CYPHER_GENERATION_PROMPT, CYPHER_QA_PROMPT


class LangChainCustom:
    """LangChain Graph QA for Neo4j graph with custom prompt."""

    def __init__(self) -> None:
        self.graph = Neo4jGraph(
            url=os.environ.get("GRAPH_URI"),
            username=os.environ.get("GRAPH_USER"),
            password=os.environ.get("GRAPH_PASSWORD"),
        )

        self.chain = GraphCypherQAChain.from_llm(
            ChatOpenAI(temperature=0),
            graph=self.graph,
            cypher_prompt=CYPHER_GENERATION_PROMPT, 
            qa_prompt=CYPHER_QA_PROMPT,
            return_intermediate_steps=True,
        )

    def _format_output(
        self, model_answer: Dict[str, Any], execution_time: float
    ) -> Output:
        """Change the output format."""

        output = Output(
            execution_time=execution_time,
            query=model_answer["intermediate_steps"][0]["query"],
            context=str(model_answer["intermediate_steps"][1]["context"]),
            answer=model_answer["result"],
        )
        return output

    def run(self, utterance: str) -> Output:
        """Answer a question based on a knowledge graph."""
        start_time = time.time()
        # TODO : Add error handling here
        results = self.chain(utterance)
        execution_time = time.time() - start_time
        formated_output = self._format_output(results, execution_time)
        return formated_output