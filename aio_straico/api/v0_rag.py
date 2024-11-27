from enum import Enum
from pathlib import Path

valid_file_types = ("pdf", "docx", "csv", "txt", "xlsx", "py")


class ChunkingMethod(Enum):
    fixed_size = "fixed_size"
    # chunk_size = 1000
    # chunk_overlap = 50
    recursive = "recursive"
    # chunk_size = 1000
    # chunk_overlap = 50
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
    **settings,
):
    url = f"{base_url}/v0/rag"

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
                ('files', (file.name, content, 'application/octet-stream'))

            )

    payload = {"name": name, "description": description}

    if chunking_method is not None:
        try:
            chunking_method = ChunkingMethod(chunking_method)
        except:
            raise Exception(f"Unexpected Chunking Method value {chunking_method}")

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
