import asyncio
from aio_straico import aio_straico_client
from pathlib import Path
from aio_straico.api.v0 import ImageSize
from aio_straico.utils import (
    to_model_enum,
)


async def async_main():
    PROMPT_DESCRIPTION = "A cute cat"
    SEED = 12345

    async with aio_straico_client() as client:
        models_v1 = await client.models(v=1)
        _, image_models = to_model_enum(models_v1)

        image_directory = Path("Images")
        image_directory.mkdir(parents=True, exist_ok=True)

        image_paths = await client.image_generation_as_images(
            model=image_models.ideogram.ideogram_v_2a,
            description=PROMPT_DESCRIPTION,
            size=ImageSize.square,  # or ImageSize.portrait, ImageSize.landscape,
            variations=1,  # 1 to 4
            destination_directory_path=image_directory,
            seed=SEED,
            enhancement_instruction="make it gothic",
        )
        print(image_models.ideogram.ideogram_v_2a["model"], image_paths)


if __name__ == "__main__":
    asyncio.run(async_main())
