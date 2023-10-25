from langchain.prompts.prompt import PromptTemplate
from pydantic import BaseModel


class Output(BaseModel):
    execution_time: float
    query: str
    context: str
    answer: str

CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided labels, properties and relationship types in the schema.
Do not use any other label, property or relationship types that are not provided.
Schema:
Node labels and properties :
Label Goal has properties title, description and code
Label Target has properties title, description and code
Label Indicator has properties code and decription
Label Transformation has properties code and title
Label IntermediateOutput has property title
Label Intervention has property title
Label Ministry has property title
All properties are string.
Relationships :
Goal - HAS_INDICATOR -> Indicator
Goal - HAS_TARGET -> Target
Target - HAS-INDICATOR -> Indicator
Transformation - COMPRISES -> Intervention
IntermediateOutput - ASSOCIATED_WITH -> Goal
Intervention - CONTRIBUTES_TO -> IntermediateOutput
Ministry - OVERSEE_THE_IMPLEMENTATION_OF -> Transformation
Note: Do not include any explanations or apologies in your responses.
Do not include any text except the generated Cypher statement.
Examples: Here are an example of generated Cypher statement for a particular question:
# What are the targets of the SDG 1 ?
MATCH (g:Goal {{code:"1"}})-[:HAS_TARGET]->(t:Target)
RETURN t

Question: {question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["question"], template=CYPHER_GENERATION_TEMPLATE
)

CYPHER_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
If the provided information is empty, say that you don't know the answer.
Information:
{context}

Question: {question}
Helpful Answer:"""

CYPHER_QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE
)