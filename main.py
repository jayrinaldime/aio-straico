import asyncio
from aio_straico_client.client import aio_straico_client
from pprint import pprint
from aio_straico_client.utils import (
    cheapest_model,
    to_model_mapping,
    to_model_mapping_by_name,
)

from pathlib import Path
from aio_straico_client.api.v0 import ImageSize


async def main():
    async with aio_straico_client(ssl=False) as client:
        # client.API_KEY = "helo"
        # print(client.API_KEY)

        # user_info = await client.user()
        # pprint(user_info)

        # models = await client.models()
        # pprint(models)

        # models_v1 = await client.models(v=1)
        # pprint(models_v1)

        models_v0 = await client.models(v=0)
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

        # cheapest_chat_model = cheapest_model(models_v1)
        # pprint(cheapest_chat_model)
        #
        # reply = await client.prompt_completion(cheapest_chat_model, "Hello there")
        # print(reply["completion"]["choices"][0]["message"]["content"])
        # # await asyncio.sleep(60)
        # reply = await client.prompt_completion("openai/gpt-4o-mini", "Hello there")
        # print(reply["completion"]["choices"][0]["message"]["content"])

        # model = models_v1["data"]["image"][0]
        # directory = Path(".")
        # # with tempfile.TemporaryDirectory() as temp_directory:
        # zip_file_path = await client.image_generation_as_zipfile(
        #     model=model,
        #     description="A cute cat",
        #     size=ImageSize.square,
        #     variations=1,
        #     destination_zip_path=directory,
        # )
        # if zip_file_path.exists():
        #     print("Image is downloaded")
        #
        # # with tempfile.TemporaryDirectory() as temp_directory:
        # image_paths = await client.image_generation_as_images(
        #     model=model,
        #     description="A cute cat",
        #     size=ImageSize.square,
        #     variations=1,
        #     destination_directory_path=directory,
        # )
        # for image_path in image_paths:
        #     if image_path.exists():
        #         print("Image is downloaded", image_path)

        mp3_files = [*Path("test_data/audio/").glob("*.mp3")]
        f = mp3_files[2]
        # response = await client.upload_file(f)
        # print(response)
        # print("test")

        file01 = "https://prompt-rack.s3.amazonaws.com/api/1722689225122_784%2520-%2520Aligning%2520Large%2520Language%2520Models%252C%2520with%2520Sinan%2520Ozdemir.mp3"
        response = await client.prompt_completion(
            "openai/gpt-4o-mini",
            "summarize the main points",
            files=mp3_files,
            display_transcripts=True,
        )

        print("## Summary")
        print(
            response["completions"]["openai/gpt-4o-mini"]["completion"]["choices"][0][
                "message"
            ]["content"]
        )

        print("## Transcript")
        for transcript in response["transcripts"]:
            print("Name:", transcript["name"])
            print("Transcript:", transcript["text"])
            print()


if __name__ == "__main__":
    asyncio.run(main())
