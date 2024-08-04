async def aio_models(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v1/models"
    response = await session.get(url, headers=headers, **settings)
    return response


def models(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v1/models"
    response = session.get(url, headers=headers, **settings)
    return response


async def aio_prompt_completion(
    session,
    base_url: str,
    headers: dict,
    models,
    message,
    *,
    file_urls=[],
    youtube_urls=[],
    display_transcripts=False,
    **settings,
):
    if type(models) == str:
        models = [models]
    url = f"{base_url}/v1/prompt/completion"
    json_body = {"models": models, "message": message}

    if 0 < len(file_urls) <= 4:
        json_body["file_urls"] = file_urls
    if 0 < len(youtube_urls) <= 4:
        json_body["youtube_urls"] = youtube_urls
    if display_transcripts:
        json_body["display_transcripts"] = True
    if "timeout" not in settings:
        settings["timeout"] = 300
    response = await session.post(url, headers=headers, json=json_body, **settings)
    return response


def prompt_completion(
    session,
    base_url: str,
    headers: dict,
    models,
    message,
    *,
    file_urls=[],
    youtube_urls=[],
    display_transcripts=False,
    **settings,
):
    if type(models) == str:
        models = [models]
    url = f"{base_url}/v1/prompt/completion"
    json_body = {"models": models, "message": message}

    if 0 < len(file_urls) <= 4:
        json_body["file_urls"] = file_urls
    if 0 < len(youtube_urls) <= 4:
        json_body["youtube_urls"] = youtube_urls
    if display_transcripts:
        json_body["display_transcripts"] = True
    if "timeout" not in settings:
        settings["timeout"] = 300
    response = session.post(url, headers=headers, json=json_body, **settings)
    return response
