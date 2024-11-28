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


def get_directory_files(path):
    for p in path.glob("*.py"):
        yield p


async def async_main():
    async with aio_straico_client() as client:
        # api_files = list(get_directory_files(Path("./aio_straico/api")))[-4:]
        # utils_files = list(get_directory_files(Path("./aio_straico/utils")))[-4:]
        # client_files = list(get_directory_files(Path("./aio_straico")))[-4:]
        #
        # api_rag = await client.create_rag("API", "API Files",
        #                  *api_files
        #                   )
        #
        # utils_rag = await client.create_rag("Utils", "Util Files",
        #                                   *utils_files
        #                                   )
        #
        # client_rag = await client.create_rag("Client", "Client Files",
        #                                     *client_files
        #                                     )

        *_, api_rag, utils_rag, client_rag = await client.rags()
        models = await client.models()
        cheapest_chat_model = cheapest_model(models)
        r = await client.create_agent(
            "AIO Straico Python Agent",
            "An Agent that understand the code for aio-straico library",
            cheapest_chat_model,
            "You are helpful **Python** coding assistant for the library aio-straico. Always answer using the context provided. Please do not answer if no information is available for the user question.",
            ["Python", "aio-straico"],
        )
        pprint(r)
        agent_id = r["_id"]

        r = await client.agents()
        pprint(r)

        r = await client.agent(agent_id)
        pprint(r)

        r = await client.agent_add_rag(agent_id, api_rag)
        pprint(r)

        r = await client.agent_add_rag(agent_id, utils_rag)
        pprint(r)

        r = await client.agent_add_rag(agent_id, client_rag)
        pprint(r)
        # agent_id = "67482c8e5962c57393ecb173"

        r = await client.agent_prompt_completion(
            agent_id, "How to get the cheapest Model ?"
        )
        pprint(r)

        # r = await client.agent_delete(agent_id)
        # pprint(r)


if __name__ == "__main__":
    asyncio.run(async_main())
