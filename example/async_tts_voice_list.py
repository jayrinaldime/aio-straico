import asyncio
from aio_straico import aio_straico_client
from aio_straico.utils import to_voices_enum
from pprint import pprint


async def async_main():
    async with aio_straico_client() as client:
        models = await client.elevenlabs_voices()
        pprint(models)


async def async_enum_main():
    async with aio_straico_client() as client:
        models = await client.elevenlabs_voices()
        voices = to_voices_enum(models)
        pprint(voices.sarah)


if __name__ == "__main__":
    asyncio.run(async_enum_main())
