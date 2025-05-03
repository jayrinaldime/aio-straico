import asyncio
from aio_straico import aio_straico_client

async def async_main():
    async with aio_straico_client() as client:
        reply = await client.prompt_completion(
            "amazon/nova-lite-v1",
            "Tell me a joke",
            temperature=2.0,
            max_tokens=100,
        )
        print(reply["completion"]["choices"][0]["message"]["content"])

if __name__ == "__main__":
    asyncio.run(async_main())
