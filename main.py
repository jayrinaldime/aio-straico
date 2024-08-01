import asyncio
from aio_straico_client.client import aio_straico_client
from pprint import pprint


async def main():
    async with aio_straico_client(ssl=False) as client:
        # client.API_KEY = "helo"
        # print(client.API_KEY)

        user_info = await client.user()
        pprint(user_info)


if __name__ == "__main__":
    asyncio.run(main())
