from enum import Enum
from pathlib import Path

from .v0_rag import SearchType


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
    url = f"{base_url}/v0/agent/"
    response = await session.get(url, headers=headers, **settings)
    return response


async def aio_agent(session, base_url: str, headers: dict, agent_id: str, **settings):
    url = f"{base_url}/v0/agent/{agent_id}"
    response = await session.get(url, headers=headers, **settings)
    return response


async def aio_rag_delete(
    session, base_url: str, headers: dict, agent_id: str, **settings
):
    url = f"{base_url}/v0/agent/{agent_id}"
    response = await session.delete(url, headers=headers, **settings)
    return response


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
    if search_type is not None:
        search_type = SearchType(search_type)
        payload["search_type"] = search_type

    if k is not None:
        payload["k"] = k

    if fetch_k is not None:
        payload["fetch_k"] = fetch_k

    if lambda_mult is not None:
        payload["lambda_mult"] = lambda_mult

    if score_threshold is not None:
        payload["score_threshold"] = score_threshold

    response = await session.post(url, headers=headers, data=payload, **settings)
    return response
