import asyncio
from aio_straico import aio_straico_client, straico_client
from pprint import pprint
from aio_straico.utils import (
    cheapest_model,
    to_model_mapping,
    to_model_mapping_by_name,
    to_model_enum,
)


from aio_straico.utils.transcript_utils import youtube_trasncript_to_plain_text
from pathlib import Path
from aio_straico.api.v0 import ImageSize


async def async_main():
    async with aio_straico_client() as client:
        # r = await client.create_rag("Test1", "Test Rag",
        #                   Path("./aio_straico/utils/models.py"),
        #                   Path("./aio_straico/utils/models_to_enum.py"),
        #                   Path("./aio_straico/utils/transcript_utils.py"),
        #                   Path("./aio_straico/api/v0_rag.py"),
        #                   )
        # pprint(r)

        r = await client.rags()
        pprint(r)
        print(r["data"][0]["_id"])

        rag_id = r["data"][0]["_id"]
        # r = await client.rag(rag_id)
        # pprint(r)

        # r = await client.rag_delete(rag_id)
        # pprint(r)
        models = await client.models()
        cheapest_chat_model = cheapest_model(models)
        r = await client.rag_prompt_completion(rag_id, cheapest_chat_model, "How to get the cheapest Model ?" )
        pprint(r)
if __name__ == "__main__":
    asyncio.run(async_main())
