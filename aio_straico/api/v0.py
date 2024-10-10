from enum import Enum


async def aio_user(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v0/user"
    response = await session.get(url, headers=headers, **settings)
    return response


def user(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v0/user"
    response = session.get(url, headers=headers, **settings)
    return response


async def aio_models(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v0/models"
    response = await session.get(url, headers=headers, **settings)
    return response


def models(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v0/models"
    response = session.get(url, headers=headers, **settings)
    return response


async def aio_prompt_completion(
    session,
    base_url: str,
    headers: dict,
    model: str,
    message,
    temperature: float = None,
    max_tokens: float = None,
    **settings,
):
    url = f"{base_url}/v0/prompt/completion"
    json_body = {"model": model, "message": message}

    if "timeout" not in settings:
        settings["timeout"] = 60

    if temperature is not None:
        temperature = max(min(temperature, 2), 0)
        json_body["temperature"] = temperature

    if max_tokens is not None:
        max_tokens = max(max_tokens, 0)
        if max_tokens > 0:
            json_body["max_tokens"] = max_tokens

    response = await session.post(url, headers=headers, json=json_body, **settings)
    return response


def prompt_completion(
    session,
    base_url: str,
    headers: dict,
    model: str,
    message,
    temperature: float = None,
    max_tokens: float = None,
    **settings,
):
    url = f"{base_url}/v0/prompt/completion"
    json_body = {"model": model, "message": message}

    if "timeout" not in settings:
        settings["timeout"] = 60

    if temperature is not None:
        temperature = max(min(temperature, 2), 0)
        json_body["temperature"] = temperature

    if max_tokens is not None:
        max_tokens = max(max_tokens, 0)
        if max_tokens > 0:
            json_body["max_tokens"] = max_tokens

    response = session.post(url, headers=headers, json=json_body, **settings)
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
    files = {"file": (filename, binary_data, content_type)}

    url = f"{base_url}/v0/file/upload"
    if "timeout" not in settings:
        settings["timeout"] = 150
    response = await session.post(url, headers=headers, files=files, **settings)
    return response


def file_upload(
    session,
    base_url: str,
    headers: dict,
    *,
    filename: str,
    content_type: str,
    binary_data,
    **settings,
):
    files = {"file": (filename, binary_data, content_type)}

    url = f"{base_url}/v0/file/upload"
    if "timeout" not in settings:
        settings["timeout"] = 150
    response = session.post(url, headers=headers, files=files, **settings)
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
    if "timeout" not in settings:
        settings["timeout"] = 300
    response = await session.post(url, headers=headers, json=json_body, **settings)
    return response


def image_generation(
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
    if "timeout" not in settings:
        settings["timeout"] = 300
    response = session.post(url, headers=headers, json=json_body, **settings)
    return response
