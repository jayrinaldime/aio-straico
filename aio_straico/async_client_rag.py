from .api.v0_rag import SearchType


class AsyncStraicoRAG:
    def __init__(self, client, data):
        self.client = client
        self._data = data
        self.rag_id = data["_id"]

    @property
    def data(self):
        return self._data

    async def refresh(self):
        self._data = await self.client.rag(self.rag_id)

    async def delete(self) -> dict:
        return await self.client.rag_delete(self.rag_id)

    async def prompt_completion(
        self,
        model: str,
        message: str,
        search_type: [SearchType | str] = None,
        k: int = None,
        fetch_k: int = None,
        lambda_mult: float = None,
        score_threshold: float = None,
    ) -> dict:
        return await self.client.rag_prompt_completion(
            self.rag_id,
            model,
            message,
            search_type=search_type,
            k=k,
            fetch_k=fetch_k,
            lambda_mult=lambda_mult,
            score_threshold=score_threshold,
        )
