import asyncio
from aio_straico_client.client import aio_straico_client
from pprint import pprint


async def main():
    async with aio_straico_client(ssl=False) as client:
        # client.API_KEY = "helo"
        # print(client.API_KEY)

        user_info = await client.user()
        pprint(user_info)

        models = await client.models()
        pprint(models)

        models_v0 = await client.models(v=0)
        pprint(models_v0)

        models_v1 = await client.models(v=1)
        pprint(models_v1)


if __name__ == "__main__":
    asyncio.run(main())
