import asyncio
from aio_straico import aio_straico_client, ModelSelector


async def async_auto_chat_v0():
    async with aio_straico_client() as client:
        reply = await client.prompt_completion(
            ModelSelector.budget(),
            "Tell me a joke",
            temperature=2.0,
            max_tokens=100,
        )
        if reply is None:
            print("Could not process request")
        print(reply["completion"]["choices"][0]["message"]["content"])


async def async_auto_chat_v1():
    async with aio_straico_client() as client:
        reply = await client.prompt_completion(
            ModelSelector.balance(4),
            "Tell me a joke",
            temperature=2.0,
            max_tokens=100,
        )
        if reply is None:
            print("Could not process request")

        for model, response in reply["completions"].items():
            print("-------------------------------------")
            print(model)
            print("-------------------------------------")
            if "choices" in response["completion"]:
                print(response["completion"]["choices"][0]["message"]["content"])
            else:
                print(response["completion"]["error"])


if __name__ == "__main__":
    asyncio.run(async_auto_chat_v0())
    asyncio.run(async_auto_chat_v1())
