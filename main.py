import asyncio
from aio_straico import aio_straico_client, straico_client
from pprint import pprint
from aio_straico.utils import (
    cheapest_model,
    to_model_mapping,
    to_model_mapping_by_name,
    to_model_enum,
)


from aio_straico.utils.transcript_utils import youtube_trasncript_to_plain_text
from pathlib import Path
from aio_straico.api.v0 import ImageSize


async def async_main():
    async with aio_straico_client() as client:
        # client.API_KEY = "helo"
        # print(client.API_KEY)

        # user_info = await client.user()
        # pprint(user_info)

        # models = await client.models()
        # pprint(models)

        models_v1 = await client.models(v=1)
        chat_models, image_models = to_model_enum(models_v1)
        print("Model V1")
        pprint(models_v1)
        #
        # models_v0 = await client.models(v=0)
        # print("Model V0")
        # pprint(models_v0)
        #
        # model_mapping = to_model_mapping(models_v0)
        # pprint(model_mapping)
        #
        # model_mapping = to_model_mapping_by_name(models_v0)
        # pprint(model_mapping)

        # cheapest_chat_model = cheapest_model(models_v0)
        # pprint(cheapest_chat_model)

        # cheapest_chat_model = cheapest_model(models_v1)
        # pprint(cheapest_chat_model)
        #
        # reply = await client.prompt_completion(cheapest_chat_model, "Hello there")
        # print(reply["completion"]["choices"][0]["message"]["content"])

        reply = await client.prompt_completion(
            chat_models.openai.gpt_4o_mini,
            "Tell me a joke",
            temperature=2,
            max_tokens=100,
        )
        print(reply["completion"]["choices"][0]["message"]["content"])
        # await asyncio.sleep(60)

        # model = models_v1["image"][0]
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

        # mp3_files = [*Path("test_data/audio/").glob("*.mp3")]
        # f = mp3_files[3]
        # response = await client.upload_file(f)
        # print(response)
        # print("test")

        file01 = "https://prompt-rack.s3.amazonaws.com/api/1722689225122_784%2520-%2520Aligning%2520Large%2520Language%2520Models%252C%2520with%2520Sinan%2520Ozdemir.mp3"
        # response = await client.prompt_completion(
        #     "openai/gpt-4o-mini",
        #     "summarize the main points",
        #     files=mp3_files,
        #     display_transcripts=True,
        # )
        # #
        # print("## Summary")
        # print(
        #     response["completions"]["openai/gpt-4o-mini"]["completion"]["choices"][0][
        #         "message"
        #     ]["content"]
        # )
        #
        # print("## Transcript")
        # for transcript in response["transcripts"]:
        #     print("Name:", transcript["name"])
        #     print("Transcript:", transcript["text"])
        #     print()

        # youtube_url = "https://www.youtube.com/watch?v=zWPe_CUR4yU"
        #
        # response = await client.prompt_completion(
        #     chat_models.openai.gpt_4o_mini,
        #     "summarize the main points",
        #     youtube_urls=youtube_url,
        #     display_transcripts=True,
        # )
        #
        # print("## Summary")
        # print(
        #     response["completions"][chat_models.openai.gpt_4o_mini.model]["completion"][
        #         "choices"
        #     ][0]["message"]["content"]
        # )
        #
        # print("## Transcript")
        # for transcript in response["transcripts"]:
        #     print("Name:", transcript["name"])
        #     print("Transcript:", youtube_trasncript_to_plain_text(transcript["text"]))
        #     print()


def main():

    with straico_client() as client:
        user_info = client.user()
        pprint(user_info)

        models = client.models(v=1)
        pprint(models)
        cheapest_chat_model = cheapest_model(models)
        # # pprint(cheapest_chat_model)
        #
        # reply =  client.prompt_completion(cheapest_chat_model, "Hello there")
        # print(reply["completion"]["choices"][0]["message"]["content"])
        #
        #
        reply = client.prompt_completion(
            cheapest_chat_model, "tell me a joke", temperature=2.0, max_tokens=100
        )
        print(reply["completion"]["choices"][0]["message"]["content"])

        # model = models["image"][0]
        # directory = Path(".")
        # # with tempfile.TemporaryDirectory() as temp_directory:
        # zip_file_path =  client.image_generation_as_zipfile(
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
        # image_paths =  client.image_generation_as_images(
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

        file01 = "https://prompt-rack.s3.amazonaws.com/api/1722689225122_784%2520-%2520Aligning%2520Large%2520Language%2520Models%252C%2520with%2520Sinan%2520Ozdemir.mp3"
        # response =  client.prompt_completion(
        #     "openai/gpt-4o-mini",
        #     "summarize the main points",
        #     files=mp3_files,
        #     display_transcripts=True,
        # )
        # print("## Summary")
        # print(
        #     response["completions"]["openai/gpt-4o-mini"]["completion"]["choices"][0][
        #         "message"
        #     ]["content"]
        # )
        #
        # print("## Transcript")
        # for transcript in response["transcripts"]:
        #     print("Name:", transcript["name"])
        #     print("Transcript:", transcript["text"])
        #     print()

        # youtube_url = "https://www.youtube.com/watch?v=zWPe_CUR4yU"
        #
        # response = client.prompt_completion(
        #     "openai/gpt-4o-mini",
        #     "summarize the main points",
        #     youtube_urls=youtube_url,
        #     display_transcripts=True,
        # )
        # print("## Summary")
        # print(
        #     response["completions"]["openai/gpt-4o-mini"]["completion"]["choices"][0][
        #         "message"
        #     ]["content"]
        # )
        #
        # print("## Transcript")
        # for transcript in response["transcripts"]:
        #     print("Name:", transcript["name"])
        #     print("Transcript:", transcript["text"])
        #     print()


async def async_upload_image():
    img = Path(".") / "test_data" / "image" / "sample.jpeg"
    async with aio_straico_client() as client:
        reply = await client.prompt_completion(
            "openai/gpt-4o-mini",
            "describe the image",
            temperature=2.0,
            max_tokens=100,
            images=[img],
        )
        pprint(reply)


def upload_image():
    img = Path(".") / "test_data" / "image" / "sample.jpeg"
    with straico_client() as client:
        reply = client.prompt_completion(
            "openai/gpt-4o-mini",
            "describe the image",
            temperature=2.0,
            max_tokens=100,
            images=[img],
        )
        pprint(reply)


if __name__ == "__main__":
    asyncio.run(async_upload_image())
    # upload_image()
