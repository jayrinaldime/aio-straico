import asyncio
from aio_straico import aio_straico_client
from pprint import pprint
from aio_straico.utils import (
    to_features,
    filter_chat_models,
    cheapest_models,
)


async def async_main():
    async with aio_straico_client() as client:
        models_v1 = await client.models(v=1)
        capabilities, features, applications = to_features(models_v1)

        image_input_models = filter_chat_models(
            models_v1["chat"], features=[features.image_input]
        )
        print("Image Input Models", len(image_input_models))

        web_browsing_models = filter_chat_models(
            models_v1["chat"], capabilities=[capabilities.web_browsing]
        )
        print("Web Browsing Models", len(web_browsing_models))
        # pprint(web_browsing_models)

        web_search_models = filter_chat_models(
            models_v1["chat"], features=[features.web_search]
        )
        print("Web Search Models", len(web_search_models))
        # pprint(web_search_models)

        image_input_coding_models = filter_chat_models(
            models_v1["chat"],
            applications=[applications.coding],
            features=[features.image_input],
        )
        print("Image Input Coding Models", len(image_input_coding_models))
        pprint(cheapest_models(image_input_coding_models))


if __name__ == "__main__":
    asyncio.run(async_main())
