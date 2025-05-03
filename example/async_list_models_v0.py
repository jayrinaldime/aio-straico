import asyncio
from aio_straico import aio_straico_client
from pprint import pprint
from aio_straico.utils import (
    to_model_mapping_by_name,
    to_model_enum,
)


async def async_main():
    async with aio_straico_client() as client:
        models_v1 = await client.models()
        chat_models, image_models = to_model_enum(models_v1)

        pprint(dir(image_models.flux))
        # image_models.flux.flux_1_1

        pprint(dir(image_models.ideogram))
        # image_models.ideogram.flux_1_1
        # image_models.ideogram.ideogram_v_1
        # image_models.ideogram.ideogram_v_1_turbo
        # image_models.ideogram.ideogram_v_2
        # image_models.ideogram.ideogram_v_2_turbo
        # image_models.ideogram.ideogram_v_2a
        # image_models.ideogram.ideogram_v_2a_turbo

        pprint(dir(image_models.openai))
        # image_models.openai.dall_e_3

        image_model_names = to_model_mapping_by_name(models_v1["image"][0])
        pprint(image_model_names)


if __name__ == "__main__":
    asyncio.run(async_main())
