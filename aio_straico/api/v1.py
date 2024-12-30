from ..utils.tracing import observe, tracing_context, TRACING_ENABLED


async def aio_models(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v1/models"
    response = await session.get(url, headers=headers, **settings)
    return response


def models(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v1/models"
    response = session.get(url, headers=headers, **settings)
    return response


@observe(as_type="generation")
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
    temperature: float = None,
    max_tokens: float = None,
    **settings,
):
    if isinstance(models, str):
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

    if temperature is not None:
        temperature = max(min(temperature, 2), 0)
        json_body["temperature"] = temperature

    if max_tokens is not None:
        max_tokens = max(max_tokens, 0)
        if max_tokens > 0:
            json_body["max_tokens"] = max_tokens
    if TRACING_ENABLED:
        tracing = dict(json_body)
        del tracing["models"]
        del tracing["message"]
        tracing.update(settings)
        tracing_context.update_current_observation(
            input=message, model=", ".join(models), model_parameters=tracing
        )
    response = await session.post(url, headers=headers, json=json_body, **settings)
    if TRACING_ENABLED:
        if response.status_code == 201 and response.json()["success"]:
            json_data = response.json()
            meta = dict(json_data["data"])
            del meta["completions"]
            del meta["overall_words"]
            del meta["overall_price"]
            tracing_context.update_current_observation(
                output=json_data["data"]["completions"],
                usage_details={
                    "input": json_data["data"]["overall_words"]["input"],
                    "output": json_data["data"]["overall_words"]["output"],
                    "total": json_data["data"]["overall_words"]["total"],
                    "input_cost": json_data["data"]["overall_price"]["input"],
                    "output_cost": json_data["data"]["overall_price"]["output"],
                    "total_cost": json_data["data"]["overall_price"]["total"],
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
    models,
    message,
    *,
    file_urls=[],
    youtube_urls=[],
    display_transcripts=False,
    temperature: float = None,
    max_tokens: float = None,
    **settings,
):
    if isinstance(models, str):
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

    if temperature is not None:
        temperature = max(min(temperature, 2), 0)
        json_body["temperature"] = temperature

    if max_tokens is not None:
        max_tokens = max(max_tokens, 0)
        if max_tokens > 0:
            json_body["max_tokens"] = max_tokens
    if TRACING_ENABLED:
        tracing = dict(json_body)
        del tracing["models"]
        del tracing["message"]
        tracing.update(settings)
        tracing_context.update_current_observation(
            input=message, model=", ".join(models), model_parameters=tracing
        )
    response = session.post(url, headers=headers, json=json_body, **settings)
    if TRACING_ENABLED:
        if response.status_code == 201 and response.json()["success"]:
            json_data = response.json()
            meta = dict(json_data["data"])
            del meta["completions"]
            del meta["overall_words"]
            del meta["overall_price"]
            tracing_context.update_current_observation(
                output=json_data["data"]["completions"],
                usage_details={
                    "input": json_data["data"]["overall_words"]["input"],
                    "output": json_data["data"]["overall_words"]["output"],
                    "total": json_data["data"]["overall_words"]["total"],
                    "input_cost": json_data["data"]["overall_price"]["input"],
                    "output_cost": json_data["data"]["overall_price"]["output"],
                    "total_cost": json_data["data"]["overall_price"]["total"],
                },
                metadata=meta,
                status_message=str(response.status_code),
            )

        else:
            tracing_context.update_current_observation(
                output=response.text, status_message=str(response.status_code)
            )
    return response
