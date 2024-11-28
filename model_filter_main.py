import asyncio
from aio_straico import aio_straico_client, straico_client
from pprint import pprint
from aio_straico.utils import (
    cheapest_model,
    to_model_mapping,
    to_model_mapping_by_name,
    to_model_enum,
)

def model_filter_enums(models):
    # provider =  openai, anthropic . . .
    # features
    # capabilitys =
    # application
    # others =
    providers = []
    features = []
    capabilities = []
    applications = []
    others = []

    for model in models["chat"]:
        metadata = model["metadata"]
        applications += metadata["applications"]
        capabilities += metadata["capabilities"]
        features += metadata["features"]
        others += metadata["other"]
        providers.append(model["model"].split("/")[0])

    print()
    print("applications")
    applications = set(map(str.upper, applications))
    pprint(applications)

    print()
    print("capabilities")
    capabilities = set(map(str.upper, capabilities))
    pprint(capabilities)

    print()
    print("features")
    features = set(map(str.upper, features))
    pprint(features)

    print()
    print("providers")
    providers = set(map(str.upper, providers))
    pprint(providers)

    print()
    print("others")
    others = set(map(str.upper, others))
    pprint(others)

async def async_main():
    async with aio_straico_client() as client:
        # client.API_KEY = "helo"
        # print(client.API_KEY)

        # user_info = await client.user()
        # pprint(user_info)

        models = await client.models()

        model_filter_enums(models)
        #
        #
        # models_v1 = await client.models(v=1)
        # chat_models, image_models = to_model_enum(models_v1)
        # pprint(chat_models.openai.gpt_4o_mini)
        # print("Model V1")
        # pprint(models_v1)

if __name__ == "__main__":
    asyncio.run(async_main())