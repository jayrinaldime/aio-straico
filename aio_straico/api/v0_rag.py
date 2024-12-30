from enum import Enum
from pathlib import Path
from typing import List
from ..utils.tracing import observe, tracing_context, TRACING_ENABLED

valid_file_types = ("pdf", "docx", "csv", "txt", "xlsx", "py")


class ChunkingMethod(Enum):
    fixed_size = "fixed_size"
    # chunk_size = 1000
    # chunk_overlap = 50
    # separator = "\n" only single value is accepted
    recursive = "recursive"
    # chunk_size = 1000
    # chunk_overlap = 50
    # separator = ["\n\n", "\n", " ", ""] multiple values are accepted
    markdown = "markdown"
    # chunk_size = 1000
    # chunk_overlap = 50
    python = "python"
    # chunk_size = 1000
    # chunk_overlap = 50
    semantic = "semantic"
    # breakpoint_threshold_type: BreakpointThresholdType = percentile
    # buffer_size = 500


class BreakpointThresholdType(Enum):
    percentile = "percentile"
    interquartile = "interquartile"
    standard_deviation = "standard_deviation"
    gradient = "gradient"


class SearchType(Enum):
    similarity = "similarity"
    mmr = "mmr"
    similarity_score_threshold = "similarity_score_threshold"


async def aio_create_rag(
    session,
    base_url: str,
    headers: dict,
    name: str,
    description: str,
    files: [Path | str] = None,
    chunking_method: [ChunkingMethod | str] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 50,
    breakpoint_threshold_type: [
        BreakpointThresholdType | str
    ] = BreakpointThresholdType.percentile,
    buffer_size: int = 500,
    separator: [List[str] | str] = None,
    **settings,
):
    url = f"{base_url}/v0/rag"

    if "timeout" not in settings:
        settings["timeout"] = 600

    filepaths = [file if isinstance(file, Path) else Path(file) for file in files]
    files_parameter = []

    for index, file in enumerate(filepaths):
        extension = file.name.split(".")[-1].strip().lower()
        if extension not in valid_file_types:
            raise Exception(
                f"Unsupported file type {extension} for file {str(file)}. Only the following file types are supported {valid_file_types}"
            )

        if not file.exists():
            raise FileNotFoundError(str(file))

        if not file.is_file() or file.is_dir():
            raise Exception(f"Not a FILE {file}")

        with file.open("rb") as reader:
            content = reader.read(-1)
            files_parameter.append(
                ("files", (file.name, content, "application/octet-stream"))
            )

    payload = {"name": name, "description": description}
    if chunking_method is None:
        chunking_method = ChunkingMethod.fixed_size

    try:
        chunking_method = ChunkingMethod(chunking_method)
    except:
        raise Exception(f"Unexpected Chunking Method value {chunking_method}")

    if chunking_method == ChunkingMethod.fixed_size and separator is not None:
        if isinstance(separator, str):
            payload["separator"] = separator
        else:
            raise Exception(
                "Invalid value for separator. For Chunking method fixed size, only string is valid."
            )

    if chunking_method == ChunkingMethod.recursive and separator is not None:
        if isinstance(separator, list) or isinstance(separator, tuple):
            payload["separators"] = separator
        else:
            raise Exception(
                "Invalid value for separator. For Chunking method recursive, only list type is valid."
            )

    if chunking_method in (
        ChunkingMethod.fixed_size,
        ChunkingMethod.recursive,
        ChunkingMethod.markdown,
        ChunkingMethod.python,
    ):
        payload["chunk_size"] = chunk_size
        payload["chunk_overlap"] = chunk_overlap

    elif chunking_method == ChunkingMethod.semantic:
        payload["breakpoint_threshold_type"] = breakpoint_threshold_type
        payload["buffer_size"] = buffer_size

    payload["chunking_method"] = chunking_method.value

    response = await session.post(
        url, headers=headers, files=files_parameter, data=payload, **settings
    )
    return response


async def aio_rags(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v0/rag/user"
    response = await session.get(url, headers=headers, **settings)
    return response


async def aio_rag(session, base_url: str, headers: dict, rag_id: str, **settings):
    url = f"{base_url}/v0/rag/{rag_id}"
    response = await session.get(url, headers=headers, **settings)
    return response


async def aio_rag_delete(
    session, base_url: str, headers: dict, rag_id: str, **settings
):
    url = f"{base_url}/v0/rag/{rag_id}"
    response = await session.delete(url, headers=headers, **settings)
    return response


@observe(as_type="generation")
async def aio_rag_prompt_completion(
    session,
    base_url: str,
    headers: dict,
    rag_id: str,
    model: str,
    message: str,
    search_type: [SearchType | str] = None,
    k: int = None,
    fetch_k: int = None,
    lambda_mult: float = None,
    score_threshold: float = None,
    **settings,
):
    url = f"{base_url}/v0/rag/{rag_id}/prompt"
    payload = {
        "prompt": message,
        "model": model,
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
        del tracing["model"]
        del tracing["prompt"]
        tracing.update(settings)
        tracing_context.update_current_observation(
            input=message, model=model, model_parameters=tracing
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


###########################
# Non Async Functions
#########################


def create_rag(
    session,
    base_url: str,
    headers: dict,
    name: str,
    description: str,
    files: [Path | str] = None,
    chunking_method: [ChunkingMethod | str] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 50,
    breakpoint_threshold_type: [
        BreakpointThresholdType | str
    ] = BreakpointThresholdType.percentile,
    buffer_size: int = 500,
    separator: [List[str] | str] = None,
    **settings,
):
    url = f"{base_url}/v0/rag"

    if "timeout" not in settings:
        settings["timeout"] = 600

    filepaths = [file if isinstance(file, Path) else Path(file) for file in files]
    if not all((file.exists() for file in filepaths)):
        pass

    files_parameter = []

    for index, file in enumerate(filepaths):
        extension = file.name.split(".")[-1].strip().lower()
        if extension not in valid_file_types:
            raise Exception(
                f"Unsupported file type {extension} for file {str(file)}. Only the following file types are supported {valid_file_types}"
            )

        if not file.exists():
            raise FileNotFoundError(str(file))

        if not file.is_file() or file.is_dir():
            raise Exception(f"Not a FILE {file}")

        with file.open("rb") as reader:
            content = reader.read(-1)
            files_parameter.append(
                ("files", (file.name, content, "application/octet-stream"))
            )

    payload = {"name": name, "description": description}

    if chunking_method is None:
        chunking_method = ChunkingMethod.fixed_size

    try:
        chunking_method = ChunkingMethod(chunking_method)
    except:
        raise Exception(f"Unexpected Chunking Method value {chunking_method}")

    if chunking_method == ChunkingMethod.fixed_size and separator is not None:
        if isinstance(separator, str):
            payload["separator"] = separator
        else:
            raise Exception(
                "Invalid value for separator. For Chunking method fixed size, only string is valid."
            )

    if chunking_method == ChunkingMethod.recursive and separator is not None:
        if isinstance(separator, list) or isinstance(separator, tuple):
            payload["separators"] = separator
        else:
            raise Exception(
                "Invalid value for separator. For Chunking method recursive, only list type is valid."
            )

    if chunking_method in (
        ChunkingMethod.fixed_size,
        ChunkingMethod.recursive,
        ChunkingMethod.markdown,
        ChunkingMethod.python,
    ):
        payload["chunk_size"] = chunk_size
        payload["chunk_overlap"] = chunk_overlap

    elif chunking_method == ChunkingMethod.semantic:
        payload["breakpoint_threshold_type"] = breakpoint_threshold_type
        payload["buffer_size"] = buffer_size

    payload["chunking_method"] = chunking_method.value

    response = session.post(
        url, headers=headers, files=files_parameter, data=payload, **settings
    )
    return response


def rags(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v0/rag/user"
    response = session.get(url, headers=headers, **settings)
    return response


def rag(session, base_url: str, headers: dict, rag_id: str, **settings):
    url = f"{base_url}/v0/rag/{rag_id}"
    response = session.get(url, headers=headers, **settings)
    return response


def rag_delete(session, base_url: str, headers: dict, rag_id: str, **settings):
    url = f"{base_url}/v0/rag/{rag_id}"
    response = session.delete(url, headers=headers, **settings)
    return response


@observe(as_type="generation")
def rag_prompt_completion(
    session,
    base_url: str,
    headers: dict,
    rag_id: str,
    model: str,
    message: str,
    search_type: [SearchType | str] = None,
    k: int = None,
    fetch_k: int = None,
    lambda_mult: float = None,
    score_threshold: float = None,
    **settings,
):
    url = f"{base_url}/v0/rag/{rag_id}/prompt"
    payload = {
        "prompt": message,
        "model": model,
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
        del tracing["model"]
        del tracing["prompt"]
        tracing.update(settings)
        tracing_context.update_current_observation(
            input=message, model=model, model_parameters=tracing
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
