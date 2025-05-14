import asyncio
from aio_straico import async_managed_client, SwitchModelOnUnavailable

from aio_straico.utils import (
    to_model_enum,
    cheapest_models,
)

async def async_main():
    async with async_managed_client(api_keys=[
        "XX-YYyyy00000000zzzzzz111111", #Account 1 API Key
        "XX-YYyyy00000000zzzzzz222222", #Account 2 API Key
        "XX-YYyyy00000000zzzzzz333333", #Account 3 API Key
    ]) as client:
        # when error is reached
            # 50,000 daily limit error
            # OR
            # 100 image generation daily limit error
            # b'{"error":"The number of images requested will exceed the flux and ideogram daily generation limit","success":false}'
        # then use the next account



        models_v1 = await client.models(v=1)
        chat_models, image_models = to_model_enum(models_v1)
        cheapest_model, _2nd_best, _3rd_best, _4th, *the_rest = cheapest_models(
            chat_models
        )

        reply = await client.prompt_completion(
            SwitchModelOnUnavailable(cheapest_model, _2nd_best, _3rd_best, _4th),
            "Tell me a joke",
            temperature=2.0,
            max_tokens=100,
            replace_failed_models=True,
        )
        # SwitchModelOnUnavailable will iterate on the listed model when model is unable to respond.
        """
**Warning:** It seems we couldn't process your request this time, and rest assured, no coins were deducted. This might be due to:
* Moderation of specific content.
* Excessively large context for the LLM (context length: 131000).
* High demands on our LLM providers.

Our tip? Switching LLMs might just solve it.
        """
        if reply is None:
            print("Could not process request")
            # This can only happen when all 4 listed models are unable to respond.
            return
        print(reply["completion"]["choices"][0]["message"]["content"])



if __name__ == "__main__":
    asyncio.run(async_main())
