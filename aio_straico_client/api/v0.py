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
