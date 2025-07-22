import asyncio
from aio_straico import aio_straico_client
from pprint import pprint


async def async_main():
    async with aio_straico_client() as client:
        models = await client.elevenlabs_voices()
        pprint(models)


if __name__ == "__main__":
    asyncio.run(async_main())
