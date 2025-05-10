import asyncio
from aio_straico import aio_straico_client
from pprint import pprint
from aio_straico.utils import (
    to_features,
    filter_chat_models,
    cheapest_models,
)
from pathlib import Path


async def async_main():
    async with aio_straico_client() as client:
        models_v1 = await client.models(v=1)
        capabilities, features, applications = to_features(models_v1)
        image_input_models = filter_chat_models(
            models_v1["chat"], features=[features.image_input]
        )

        cheap_models = cheapest_models(image_input_models)
        for cheap_model in cheap_models:
            model_name = cheap_model["name"]
            model_price = cheap_model["pricing"]["coins"]
            print(f"{model_name=} {model_price=}")

            img = Path("..") / "test_data" / "image" / "sample.jpeg"
            reply = await client.prompt_completion(
                cheap_model,
                "describe the image",
                temperature=2.0,
                max_tokens=100,
                images=[img],
            )
            if reply is None:
                print("Unable to process request")
                continue

            model_id = cheap_model["model"]
            if "choices" in reply["completions"][model_id]["completion"]:
                print(
                    reply["completions"][model_id]["completion"]["choices"][0][
                        "message"
                    ]["content"]
                )
            else:
                print(reply["completions"][model_id]["completion"]["error"])
            break


if __name__ == "__main__":
    asyncio.run(async_main())
