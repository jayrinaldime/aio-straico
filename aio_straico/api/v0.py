from enum import Enum
from ..utils.tracing import observe, tracing_context, TRACING_ENABLED
from .smartllmselector import ModelSelector


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


@observe(as_type="generation")
async def aio_prompt_completion(
    session,
    base_url: str,
    headers: dict,
    model: [str | ModelSelector],
    message,
    temperature: float = None,
    max_tokens: float = None,
    **settings,
):
    url = f"{base_url}/v0/prompt/completion"
    json_body = {"message": message}

    if isinstance(model, ModelSelector):
        json_body["smart_llm_selector"] = model.pricing_method.value
    else:
        json_body["model"] = model

    if "timeout" not in settings:
        settings["timeout"] = 60

    if temperature is not None:
        temperature = max(min(temperature, 2), 0)
        json_body["temperature"] = temperature

    if max_tokens is not None:
        max_tokens = max(max_tokens, 0)
        if max_tokens > 0:
            json_body["max_tokens"] = max_tokens

    if TRACING_ENABLED:
        tracing = dict(json_body)
        if "model" in tracing:
            del tracing["model"]
        if "smart_llm_selector" in tracing:
            del tracing["smart_llm_selector"]
        del tracing["message"]
        tracing.update(settings)
        if "model" in tracing:
            tracing_context.update_current_observation(
                input=message, model=model, model_parameters=tracing
            )
        else:
            tracing_context.update_current_observation(
                input=message, model_parameters=tracing
            )
    response = await session.post(url, headers=headers, json=json_body, **settings)
    if TRACING_ENABLED:
        if response.status_code == 201 and response.json()["success"]:
            json_data = response.json()
            meta = dict(json_data["data"]["completion"])
            del meta["choices"]
            tracing_context.update_current_observation(
                output=json_data["data"]["completion"]["choices"],
                usage_details={
                    "input": json_data["data"]["words"]["input"],
                    "output": json_data["data"]["words"]["output"],
                    "total": json_data["data"]["words"]["total"],
                    "input_cost": json_data["data"]["price"]["input"],
                    "output_cost": json_data["data"]["price"]["output"],
                    "total_cost": json_data["data"]["price"]["total"],
                },
                metadata=meta,
                status_message=str(response.status_code),
            )

        else:
            tracing_context.update_current_observation(
                output=response.text, status_message=str(response.status_code)
            )

    return response


@observe(as_type="generation")
def prompt_completion(
    session,
    base_url: str,
    headers: dict,
    model: [str | ModelSelector],
    message,
    temperature: float = None,
    max_tokens: float = None,
    **settings,
):
    url = f"{base_url}/v0/prompt/completion"
    json_body = {"message": message}

    if isinstance(model, ModelSelector):
        json_body["smart_llm_selector"] = model.pricing_method.value
    else:
        json_body["model"] = model

    if "timeout" not in settings:
        settings["timeout"] = 60

    if temperature is not None:
        temperature = max(min(temperature, 2), 0)
        json_body["temperature"] = temperature

    if max_tokens is not None:
        max_tokens = max(max_tokens, 0)
        if max_tokens > 0:
            json_body["max_tokens"] = max_tokens
    if TRACING_ENABLED:
        tracing = dict(json_body)
        if "model" in tracing:
            del tracing["model"]
        if "smart_llm_selector" in tracing:
            del tracing["smart_llm_selector"]
        del tracing["message"]
        tracing.update(settings)
        if "model" in tracing:
            tracing_context.update_current_observation(
                input=message, model=model, model_parameters=tracing
            )
        else:
            tracing_context.update_current_observation(
                input=message, model_parameters=tracing
            )
    response = session.post(url, headers=headers, json=json_body, **settings)
    if TRACING_ENABLED:
        if response.status_code == 201 and response.json()["success"]:
            json_data = response.json()
            meta = dict(json_data["data"]["completion"])
            del meta["choices"]
            tracing_context.update_current_observation(
                output=json_data["data"]["completion"]["choices"],
                usage_details={
                    "input": json_data["data"]["words"]["input"],
                    "output": json_data["data"]["words"]["output"],
                    "total": json_data["data"]["words"]["total"],
                    "input_cost": json_data["data"]["price"]["input"],
                    "output_cost": json_data["data"]["price"]["output"],
                    "total_cost": json_data["data"]["price"]["total"],
                },
                metadata=meta,
                status_message=str(response.status_code),
            )

        else:
            tracing_context.update_current_observation(
                output=response.text, status_message=str(response.status_code)
            )
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


@observe(as_type="generation")
async def aio_image_generation(
    session,
    base_url: str,
    headers: dict,
    *,
    model: str,
    description: str,
    size: ImageSize | str,
    variations: int,
    seed: int = None,
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

    if seed is not None:
        json_body["seed"] = seed

    if "timeout" not in settings:
        settings["timeout"] = 300

    if TRACING_ENABLED:
        tracing = {"size": size, "variations": variations, **settings}
        tracing_context.update_current_observation(
            input=description, model=model, model_parameters=tracing
        )
    response = await session.post(url, headers=headers, json=json_body, **settings)
    if TRACING_ENABLED:
        if response.status_code == 201 and response.json()["success"]:
            json_data = response.json()
            output = dict(json_data["data"])
            del output["price"]
            tracing_context.update_current_observation(
                output=output,
                usage_details={
                    "total_cost": json_data["data"]["price"]["total"],
                },
                status_message=str(response.status_code),
            )

        else:
            tracing_context.update_current_observation(
                output=response.text, status_message=str(response.status_code)
            )
    return response


@observe(as_type="generation")
def image_generation(
    session,
    base_url: str,
    headers: dict,
    *,
    model: str,
    description: str,
    size: ImageSize | str,
    variations: int,
    seed: int = None,
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
    if seed is not None:
        json_body["seed"] = seed

    if "timeout" not in settings:
        settings["timeout"] = 300

    if TRACING_ENABLED:
        tracing = {"size": size, "variations": variations, **settings}
        tracing_context.update_current_observation(
            input=description, model=model, model_parameters=tracing
        )
    response = session.post(url, headers=headers, json=json_body, **settings)
    if TRACING_ENABLED:
        if response.status_code == 201 and response.json()["success"]:
            json_data = response.json()
            output = dict(json_data["data"])
            del output["price"]
            tracing_context.update_current_observation(
                output=output,
                usage_details={
                    "total_cost": json_data["data"]["price"]["total"],
                },
                status_message=str(response.status_code),
            )

        else:
            tracing_context.update_current_observation(
                output=response.text, status_message=str(response.status_code)
            )
    return response
