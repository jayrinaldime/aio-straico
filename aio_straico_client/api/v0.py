from aiohttp import FormData
from enum import Enum


async def aio_user(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v0/user"
    response = await session.get(url, headers=headers, **settings)
    return response


async def aio_models(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v0/models"
    response = await session.get(url, headers=headers, **settings)
    return response


async def aio_prompt_completion(
    session, base_url: str, headers: dict, model: str, message, **settings
):
    url = f"{base_url}/v0/prompt/completion"
    json_body = {"model": model, "message": message}
    response = await session.post(url, headers=headers, json=json_body, **settings)
    return response


async def aio_file_upload(
    session,
    base_url: str,
    headers: dict,
    *,
    filename: str,
    content_type: str,
    binary_data,
    **settings,
):
    data = FormData()
    data.add_field("file", binary_data, filename=filename, content_type=content_type)
    url = f"{base_url}/v0/file/upload"

    response = await session.post(url, headers=headers, data=data, **settings)
    return response


class ImageSize(Enum):
    square = "square"
    portrait = "portrait"
    landscape = "landscape"


def ImageSizer(size):
    lsize = size.lower()
    if lsize == ImageSize.square.value:
        return ImageSize.square
    elif lsize == ImageSize.portrait.value:
        return ImageSize.portrait
    elif lsize == ImageSize.landscape.value:
        return ImageSize.landscape

    raise Exception(f"Unknown Image Size {size}")


async def aio_image_generation(
    session,
    base_url: str,
    headers: dict,
    *,
    model: str,
    description: str,
    size: ImageSize | str,
    variations: int,
    **settings,
):
    url = f"{base_url}/v0/image/generation"

    if not (0 < variations <= 4):
        raise Exception(f"Error variation size should be 1 to 4 got {variations}")

    size_type = type(size)
    if size_type == str and size not in [
        ImageSize.square.value,
        ImageSize.portrait.value,
        ImageSize.landscape.value,
    ]:
        raise Exception(f"Unknown Image Size {size}")
    elif size_type == ImageSize:
        size = size.value

    json_body = {
        "model": model,
        "description": description,
        "size": size,
        "variations": variations,
    }
    response = await session.post(url, headers=headers, json=json_body, **settings)
    return response
