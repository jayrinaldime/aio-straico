from .api.v0_rag import SearchType
from .client_rag import StraicoRAG


class StraicoAgent:
    def __init__(self, client, data):
        self.client = client
        self._data = data
        self.agent_id = data["_id"]

    @property
    def data(self):
        return self._data

    def refresh(self):
        self._data = self.client.agent(self.agent_id)

    def delete(self) -> dict:
        return self.client.agent_delete(self.agent_id)

    def set_rag(self, rag: [StraicoRAG | dict | str]):
        return self.client.agent_add_rag(self.agent_id, rag)

    def prompt_completion(
        self,
        message: str,
        search_type: [SearchType | str] = None,
        k: int = None,
        fetch_k: int = None,
        lambda_mult: float = None,
        score_threshold: float = None,
    ) -> dict:
        return self.client.agent_prompt_completion(
            self.agent_id,
            message,
            search_type=search_type,
            k=k,
            fetch_k=fetch_k,
            lambda_mult=lambda_mult,
            score_threshold=score_threshold,
        )

    def update(
        self,
        *,
        rag: [StraicoRAG | dict | str] = None,
        name: str = None,
        description: str = None,
        model: str = None,
        system_prompt: str = None,
        tags: [str] = None,
    ):
        return self.client.agent_update(
            self.agent_id,
            name=name,
            rag=rag,
            description=description,
            model=model,
            system_prompt=system_prompt,
            tags=tags,
        )
