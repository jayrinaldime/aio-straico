import asyncio
from aio_straico import aio_straico_client
from pprint import pprint
from aio_straico.utils import (
    to_model_enum,
)


async def async_main():
    async with aio_straico_client() as client:
        models_v0 = await client.models(v=0)
        chat_models = to_model_enum(models_v0)

        pprint(models_v0)

        print(chat_models.openai.gpt_4o_mini)


if __name__ == "__main__":
    asyncio.run(async_main())
