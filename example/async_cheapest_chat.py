import asyncio
from aio_straico import aio_straico_client
from aio_straico.utils import (
    to_features,
    filter_chat_models,
    cheapest_models,
)


async def async_main():
    async with aio_straico_client() as client:
        models_v1 = await client.models(v=1)
        capabilities, features, applications = to_features(models_v1)

        content_models = filter_chat_models(
            models_v1["chat"], applications=[applications.social_chat]
        )
        cheapest_model, _2nd_best, _3rd_best, _4th, *the_rest = cheapest_models(
            content_models
        )
        models = [cheapest_model, _2nd_best, _3rd_best, _4th]
        reply = await client.prompt_completion(
            models,
            "Tell me a joke in English.",
            temperature=0.6,
            max_tokens=100,
        )
        for model in models:
            model_id = model["model"]
            model_name = model["name"]
            print(model_name, model["pricing"])
            if "choices" in reply["completions"][model_id]["completion"]:
                print(
                    reply["completions"][model_id]["completion"]["choices"][0][
                        "message"
                    ]["content"]
                )
            else:
                print(reply["completions"][model_id]["completion"]["error"])


if __name__ == "__main__":
    asyncio.run(async_main())
