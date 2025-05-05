import asyncio
from aio_straico import aio_straico_client
from pprint import pprint
from aio_straico.utils import (
    to_model_mapping_by_name,
    to_model_enum,
)


async def async_main():
    async with aio_straico_client() as client:
        models_v1 = await client.models(v=1)
        chat_models, image_models = to_model_enum(models_v1)

        pprint(models_v1)

        print(chat_models.openai.gpt_4o_mini)
        print(image_models.openai.dall_e_3)


if __name__ == "__main__":
    asyncio.run(async_main())
