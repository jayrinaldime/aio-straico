import asyncio
from aio_straico import aio_straico_client
from aio_straico.utils import to_model_enum


async def async_main():
    async with aio_straico_client() as client:
        reply = await client.prompt_completion(
            "amazon/nova-lite-v1",
            "Tell me a joke",
            temperature=2.0,
            max_tokens=100,
        )
        print(reply["completion"]["choices"][0]["message"]["content"])


async def async_main_enum_model():
    async with aio_straico_client() as client:
        models_v1 = await client.models(v=1)
        chat_models, image_models = to_model_enum(models_v1)
        reply = await client.prompt_completion(
            chat_models.amazon.nova_lite_1_0,
            "Tell me a joke",
            temperature=2.0,
            max_tokens=100,
        )
        print(reply["completion"]["choices"][0]["message"]["content"])


if __name__ == "__main__":
    asyncio.run(async_main())
    asyncio.run(async_main_enum_model())
