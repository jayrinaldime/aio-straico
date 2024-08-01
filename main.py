import asyncio
from aio_straico_client.client import aio_straico_client
from pprint import pprint
from aio_straico_client.utils import (
    cheapest_model,
    to_model_mapping,
    to_model_mapping_by_name,
)


async def main():
    async with aio_straico_client(ssl=False) as client:
        # client.API_KEY = "helo"
        # print(client.API_KEY)

        user_info = await client.user()
        pprint(user_info)

        # models = await client.models()
        # pprint(models)

        models_v1 = await client.models(v=1)
        # pprint(models_v1)

        # models_v0 = await client.models(v=0)
        # pprint(models_v0)
        #
        # model_mapping = to_model_mapping(models_v0)
        #
        # pprint(model_mapping)
        #
        # model_mapping = to_model_mapping_by_name(models_v0)
        #
        # pprint(model_mapping)

        # cheapest_chat_model = cheapest_model(models_v0)
        # pprint(cheapest_chat_model)

        cheapest_chat_model = cheapest_model(models_v1)
        pprint(cheapest_chat_model)


if __name__ == "__main__":
    asyncio.run(main())
