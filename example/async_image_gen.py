import asyncio
from aio_straico import aio_straico_client
from pathlib import Path
from aio_straico.api.v0 import ImageSize

PROMPT_DESCRIPTION = "A cute cat"
SEED = 12345
# Applies only to flux and ideogram.
# The seed value controls result variability.
# Using the same seed and the same prompt with the same model version
# will produce the same image every time.
# The value must be between 0 and 2,147,483,647.

# Note:
# After some testing depending on the model used result may bot be the same!
# The image is equivalent or mostly the same.

# Same Result Models
# Flux
# Ideogram V1
# Ideogram V2
# Ideogram V2 Turbo
# Ideogram V2A

# Mostly the same
# Ideogram V1 Turbo
# Ideogram V2A Turbo


async def generate_image(image_model_id, description, output_directory):
    async with aio_straico_client(timeout=600) as client:
        image_paths = await client.image_generation_as_images(
            model=image_model_id,
            description=description,
            size=ImageSize.square,  # or ImageSize.portrait, ImageSize.landscape,
            variations=1,  # 1 to 4
            destination_directory_path=output_directory,
            seed=SEED,
        )
        print(image_model_id, image_paths)


async def async_main():
    async with aio_straico_client() as client:
        models_v1 = await client.models(v=1)
        parent_image_directory = Path("Images")
        for image_model in models_v1["image"][0]:
            image_model_id = image_model["model"]

            # dall-e-3 is does not support the seed parameter
            # hence only flux and ideogram models
            if image_model_id == "openai/dall-e-3":
                continue

            image_directory = parent_image_directory.joinpath(image_model["model"])
            image_directory.mkdir(parents=True, exist_ok=True)
            print(image_model_id)

            awaitables = []
            for retry_index in range(3):
                r = generate_image(image_model_id, PROMPT_DESCRIPTION, image_directory)
                awaitables.append(r)

            await asyncio.gather(*awaitables)


if __name__ == "__main__":
    asyncio.run(async_main())
