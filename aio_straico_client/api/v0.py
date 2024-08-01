async def aio_user(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v0/user"
    response = await session.get(url, headers=headers, **settings)
    return response

async def aio_models(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v0/models"
    response = await session.get(url, headers=headers, **settings)
    return response
