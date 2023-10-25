from dependency_injector import containers, providers
from langchain_graph_qa_openai.service import LangChainGraphQA


class ApplicationContainer(containers.DeclarativeContainer):
    """The ApplicationContainer provides integration of services,
    databases and other main components into the application.
    It's an easy way to configure the wiring and dependencies of the application.
    It provides features such as service registration and access, configuration,
    database access and integration of third-party components."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "langchain_graph_qa_openai.router",
        ]
    )
    configuration = providers.Configuration()

    # Singleton without dependency injection
    langchain_graphqa_service = providers.Singleton(LangChainGraphQA)
