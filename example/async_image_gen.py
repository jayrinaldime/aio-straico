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


async def generate_image(image_model_id, description, output_directory):
    async with aio_straico_client(timeout=600) as client:
        image_paths = await client.image_generation_as_images(
            model=image_model_id,
            description=description,
            size=ImageSize.square,
            variations=1,
            destination_directory_path=output_directory,
            seed=12345,
        )
        print(image_model_id, image_paths)


async def async_main():

    async with aio_straico_client() as client:
        models_v1 = await client.models(v=1)
        parent_image_directory = Path("Images")

        for image_model in models_v1["image"][0]:

            image_model_id = image_model["model"]
            # if image_model_id == "openai/dall-e-3":
            #     continue

            image_directory = parent_image_directory.joinpath(image_model["model"])
            image_directory.mkdir(parents=True, exist_ok=True)
            print(image_model_id)

            awaitables = []
            for retry_index in range(3):
                r = generate_image(image_model_id, "A cute cat", image_directory)
                awaitables.append(r)

            await asyncio.gather(*awaitables)


if __name__ == "__main__":
    asyncio.run(async_main())
