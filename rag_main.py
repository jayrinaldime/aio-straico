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


async def async_main_obj():
    async with aio_straico_client() as client:
        rag_obj_new = await client.new_rag(
            "Test1",
            "Test Rag",
            Path("./aio_straico/utils/models.py"),
            Path("./aio_straico/utils/models_to_enum.py"),
            Path("./aio_straico/utils/transcript_utils.py"),
            Path("./aio_straico/api/v0_rag.py"),
        )
        pprint(rag_obj_new.data)
        r = await rag_obj_new.delete()
        pprint(r)

        rag_obj, *_ = await client.rag_objects()
        pprint(rag_obj.data)

        await rag_obj.refresh()
        pprint(rag_obj.data)

        models = await client.models()
        cheapest_chat_model = cheapest_model(models)
        r = await rag_obj.prompt_completion(
            cheapest_chat_model, "How to get the cheapest Model ?"
        )

        pprint(r)


async def async_main():
    async with aio_straico_client() as client:
        # r = await client.create_rag("Test1", "Test Rag",
        #                   Path("./aio_straico/utils/models.py"),
        #                   Path("./aio_straico/utils/models_to_enum.py"),
        #                   Path("./aio_straico/utils/transcript_utils.py"),
        #                   Path("./aio_straico/api/v0_rag.py"),
        #                   )
        # pprint(r)

        r, *_ = await client.rags()
        pprint(r)
        print(r["_id"])

        rag_id = r["_id"]
        # r = await client.rag(rag_id)
        # pprint(r)

        # r = await client.rag_delete(rag_id)
        # pprint(r)
        models = await client.models()
        cheapest_chat_model = cheapest_model(models)
        r = await client.rag_prompt_completion(
            rag_id, cheapest_chat_model, "How to get the cheapest Model ?"
        )

        pprint(r)


def main_obj():
    with straico_client() as client:
        rag_obj_new = client.new_rag(
            "Test1",
            "Test Rag",
            Path("./aio_straico/utils/models.py"),
            Path("./aio_straico/utils/models_to_enum.py"),
            Path("./aio_straico/utils/transcript_utils.py"),
            Path("./aio_straico/api/v0_rag.py"),
        )
        pprint(rag_obj_new.data)
        r = rag_obj_new.delete()
        pprint(r)

        rag_obj, *_ = client.rag_objects()
        pprint(rag_obj.data)

        rag_obj.refresh()
        pprint(rag_obj.data)

        models = client.models()
        cheapest_chat_model = cheapest_model(models)
        r = rag_obj.prompt_completion(
            cheapest_chat_model, "How to get the cheapest Model ?"
        )

        pprint(r)

if __name__ == "__main__":
    main_obj()
