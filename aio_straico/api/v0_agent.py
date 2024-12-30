from enum import Enum
from pathlib import Path

from .v0_rag import SearchType
from ..utils.tracing import observe, tracing_context, TRACING_ENABLED


async def aio_create_agent(
    session,
    base_url: str,
    headers: dict,
    name: str,
    description: str,
    model: str,
    system_prompt: str,
    tags: [str],
    **settings,
):
    url = f"{base_url}/v0/agent"

    payload = {
        "name": name,
        "description": description,
        "default_llm": model,
        "custom_prompt": system_prompt,
        "tags": tags,
    }

    response = await session.post(url, headers=headers, data=payload, **settings)
    return response


async def aio_add_rag_to_agent(
    session,
    base_url: str,
    headers: dict,
    agent_id: str,
    rag_id: str,
    **settings,
):
    url = f"{base_url}/v0/agent/{agent_id}/rag"

    payload = {
        "rag": rag_id,
    }

    response = await session.post(url, headers=headers, data=payload, **settings)
    return response


async def aio_agents(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v0/agent"
    response = await session.get(url, headers=headers, **settings)
    return response


async def aio_agent(session, base_url: str, headers: dict, agent_id: str, **settings):
    url = f"{base_url}/v0/agent/{agent_id}"
    response = await session.get(url, headers=headers, **settings)
    return response


async def aio_agent_delete(
    session, base_url: str, headers: dict, agent_id: str, **settings
):
    url = f"{base_url}/v0/agent/{agent_id}"
    response = await session.delete(url, headers=headers, **settings)
    return response


@observe(as_type="generation")
async def aio_agent_prompt_completion(
    session,
    base_url: str,
    headers: dict,
    agent_id: str,
    message: str,
    search_type: [SearchType | str] = None,
    k: int = None,
    fetch_k: int = None,
    lambda_mult: float = None,
    score_threshold: float = None,
    **settings,
):
    url = f"{base_url}/v0/agent/{agent_id}/prompt"
    payload = {
        "prompt": message,
    }

    if "timeout" not in settings:
        settings["timeout"] = 600

    if search_type is not None:
        search_type = SearchType(search_type)
        payload["search_type"] = search_type.value

    if k is not None:
        payload["k"] = k

    if fetch_k is not None:
        payload["fetch_k"] = fetch_k

    if lambda_mult is not None:
        payload["lambda_mult"] = lambda_mult

    if score_threshold is not None:
        payload["score_threshold"] = score_threshold
    if TRACING_ENABLED:
        tracing = dict(payload)
        del tracing["prompt"]
        tracing.update(settings)
        tracing_context.update_current_observation(
            input=message, model=agent_id, model_parameters=tracing
        )
    response = await session.post(url, headers=headers, data=payload, **settings)
    if TRACING_ENABLED:
        if response.status_code == 200 and response.json()["success"]:
            json_data = response.json()
            meta = dict(json_data["response"])
            del meta["answer"]
            del meta["coins_used"]
            # del meta["overall_words"]
            # del meta["overall_price"]
            tracing_context.update_current_observation(
                output=json_data["response"]["answer"],
                usage_details={
                    "total_cost": json_data["response"]["coins_used"],
                },
                metadata=meta,
                status_message=str(response.status_code),
            )

        else:
            tracing_context.update_current_observation(
                output=response.text, status_message=str(response.status_code)
            )
    return response


async def aio_agent_update(
    session,
    base_url: str,
    headers: dict,
    agent_id: str,
    *,
    rag_id: str = None,
    name: str = None,
    description: str = None,
    model: str = None,
    system_prompt: str = None,
    tags: [str] = None,
    **settings,
):
    url = f"{base_url}/v0/agent/{agent_id}"

    payload = {}
    if rag_id is not None:
        payload["rag"] = rag_id
    if name is not None:
        payload["name"] = name
    if description is not None:
        payload["description"] = description
    if system_prompt is not None:
        payload["custom_prompt"] = system_prompt
    if model is not None:
        payload["default_llm"] = model
    if tags is not None:
        payload["tags"] = tags

    response = await session.put(url, headers=headers, data=payload, **settings)
    return response


def create_agent(
    session,
    base_url: str,
    headers: dict,
    name: str,
    description: str,
    model: str,
    system_prompt: str,
    tags: [str],
    **settings,
):
    url = f"{base_url}/v0/agent"

    payload = {
        "name": name,
        "description": description,
        "default_llm": model,
        "custom_prompt": system_prompt,
        "tags": tags,
    }

    response = session.post(url, headers=headers, data=payload, **settings)
    return response


def add_rag_to_agent(
    session,
    base_url: str,
    headers: dict,
    agent_id: str,
    rag_id: str,
    **settings,
):
    url = f"{base_url}/v0/agent/{agent_id}/rag"

    payload = {
        "rag": rag_id,
    }

    response = session.post(url, headers=headers, data=payload, **settings)
    return response


def agents(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v0/agent"
    response = session.get(url, headers=headers, **settings)
    return response


def agent(session, base_url: str, headers: dict, agent_id: str, **settings):
    url = f"{base_url}/v0/agent/{agent_id}"
    response = session.get(url, headers=headers, **settings)
    return response


def agent_delete(session, base_url: str, headers: dict, agent_id: str, **settings):
    url = f"{base_url}/v0/agent/{agent_id}"
    response = session.delete(url, headers=headers, **settings)
    return response


@observe(as_type="generation")
def agent_prompt_completion(
    session,
    base_url: str,
    headers: dict,
    agent_id: str,
    message: str,
    search_type: [SearchType | str] = None,
    k: int = None,
    fetch_k: int = None,
    lambda_mult: float = None,
    score_threshold: float = None,
    **settings,
):
    url = f"{base_url}/v0/agent/{agent_id}/prompt"
    payload = {
        "prompt": message,
    }

    if "timeout" not in settings:
        settings["timeout"] = 600

    if search_type is not None:
        search_type = SearchType(search_type)
        payload["search_type"] = search_type.value

    if k is not None:
        payload["k"] = k

    if fetch_k is not None:
        payload["fetch_k"] = fetch_k

    if lambda_mult is not None:
        payload["lambda_mult"] = lambda_mult

    if score_threshold is not None:
        payload["score_threshold"] = score_threshold
    if TRACING_ENABLED:
        tracing = dict(payload)
        del tracing["prompt"]
        tracing.update(settings)
        tracing_context.update_current_observation(
            input=message, model=agent_id, model_parameters=tracing
        )
    response = session.post(url, headers=headers, data=payload, **settings)
    if TRACING_ENABLED:
        if response.status_code == 200 and response.json()["success"]:
            json_data = response.json()
            meta = dict(json_data["response"])
            del meta["answer"]
            del meta["coins_used"]
            # del meta["overall_words"]
            # del meta["overall_price"]
            tracing_context.update_current_observation(
                output=json_data["response"]["answer"],
                usage_details={
                    "total_cost": json_data["response"]["coins_used"],
                },
                metadata=meta,
                status_message=str(response.status_code),
            )

        else:
            tracing_context.update_current_observation(
                output=response.text, status_message=str(response.status_code)
            )
    return response


def agent_update(
    session,
    base_url: str,
    headers: dict,
    agent_id: str,
    *,
    rag_id: str = None,
    name: str = None,
    description: str = None,
    model: str = None,
    system_prompt: str = None,
    tags: [str] = None,
    **settings,
):
    url = f"{base_url}/v0/agent/{agent_id}"

    payload = {}
    if rag_id is not None:
        payload["rag"] = rag_id
    if name is not None:
        payload["name"] = name
    if description is not None:
        payload["description"] = description
    if system_prompt is not None:
        payload["custom_prompt"] = system_prompt
    if model is not None:
        payload["default_llm"] = model
    if tags is not None:
        payload["tags"] = tags

    response = session.put(url, headers=headers, data=payload, **settings)
    return response
