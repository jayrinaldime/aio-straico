async def aio_models(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v1/models"
    response = await session.get(url, headers=headers, **settings)
    return response
