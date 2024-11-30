from .api.v0_rag import SearchType
from .async_client_rag import AsyncStraicoRAG


class AsyncStraicoAgent:
    def __init__(self, client, data):
        self.client = client
        self._data = data
        self.agent_id = data["_id"]

    @property
    def data(self):
        return self._data

    async def refresh(self):
        self._data = await self.client.agent(self.agent_id)

    async def delete(self) -> dict:
        return await self.client.agent_delete(self.agent_id)

    async def set_rag(self, rag: [AsyncStraicoRAG | dict | str]):
        return await self.client.agent_add_rag(self.agent_id, rag)

    async def prompt_completion(
        self,
        message: str,
        search_type: [SearchType | str] = None,
        k: int = None,
        fetch_k: int = None,
        lambda_mult: float = None,
        score_threshold: float = None,
    ) -> dict:
        return await self.client.agent_prompt_completion(
            self.agent_id,
            message,
            search_type=search_type,
            k=k,
            fetch_k=fetch_k,
            lambda_mult=lambda_mult,
            score_threshold=score_threshold,
        )

    async def update(
        self,
        *,
        rag: [AsyncStraicoRAG | dict | str] = None,
        name: str = None,
        description: str = None,
        model: str = None,
        system_prompt: str = None,
        tags: [str] = None,
    ):
        return await self.client.agent_update(
            self.agent_id,
            name=name,
            rag=rag,
            description=description,
            model=model,
            system_prompt=system_prompt,
            tags=tags,
        )
