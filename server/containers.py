from dependency_injector import containers, providers
from entity_linking_mistralai.service import ELMistral
from entity_linking_openai.service import ELOpenAI
from langchain_custom_openai.service import LangChainCustom
from langchain_graph_qa_openai.service import LangChainGraphQA
from rag_sbert_openai.service import RagSBertOpenAI


class ApplicationContainer(containers.DeclarativeContainer):
    """The ApplicationContainer provides integration of services,
    databases and other main components into the application.
    It's an easy way to configure the wiring and dependencies of the application.
    It provides features such as service registration and access, configuration,
    database access and integration of third-party components."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "entity_linking_mistralai.router",
            "entity_linking_openai.router",
            "langchain_custom_openai.router",
            "langchain_graph_qa_openai.router",
            "rag_sbert_openai.router"
        ]
    )
    configuration = providers.Configuration()

    # Singleton without dependency injection
    el_mistralai_service = providers.Singleton(ELMistral)
    el_openai_service = providers.Singleton(ELOpenAI)
    langchain_graphqa_service = providers.Singleton(LangChainGraphQA)
    langchain_custom_service = providers.Singleton(LangChainCustom)
    rag_sbert_openai_service = providers.Singleton(RagSBertOpenAI)
