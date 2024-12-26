import pytest
from .utils import make_temp_file
from aio_straico import straico_client, aio_straico_client
from aio_straico.api.v0_rag import ChunkingMethod


@pytest.mark.asyncio
async def test_basic_rag_aio():
    rag_name = "testrag"
    rag_description = "this is only a basic test"
    test_filename = "test.py"
    async with aio_straico_client() as client:
        with make_temp_file(test_filename, "this is a test") as file:
            s = await client.create_rag(rag_name, rag_description, file)
            assert s["name"] == rag_name
            assert s["description"] == rag_description
            assert s["original_filename"] == test_filename
            assert s["chunking_method"] == "fixed_size"
            assert s["chunk_size"] == 1000
            assert s["chunk_overlap"] == 50


@pytest.mark.asyncio
async def test_customize_rag_fixed_size_aio():
    rag_name = "testrag"
    rag_description = "this is only a basic test"
    test_filename = "test.py"
    async with aio_straico_client() as client:
        with make_temp_file(test_filename, "this is a test") as file:
            s = await client.create_rag(
                rag_name,
                rag_description,
                file,
                chunk_size=1001,
                chunk_overlap=55,
                separator="a",
            )
            assert s["name"] == rag_name
            assert s["description"] == rag_description
            assert s["original_filename"] == test_filename
            assert s["chunking_method"] == "fixed_size"
            assert s["chunk_size"] == 1001
            assert s["chunk_overlap"] == 55
            assert s["separator"] == "a"


@pytest.mark.asyncio
async def test_customize_rag_fixed_size_explicit_str_aio():
    rag_name = "testrag"
    rag_description = "this is only a basic test"
    test_filename = "test.py"
    async with aio_straico_client() as client:
        with make_temp_file(test_filename, "this is a test") as file:
            s = await client.create_rag(
                rag_name,
                rag_description,
                file,
                chunking_method="fixed_size",
                chunk_size=1001,
                chunk_overlap=55,
                separator="a",
            )
            assert s["name"] == rag_name
            assert s["description"] == rag_description
            assert s["original_filename"] == test_filename
            assert s["chunking_method"] == "fixed_size"
            assert s["chunk_size"] == 1001
            assert s["chunk_overlap"] == 55
            assert s["separator"] == "a"


@pytest.mark.asyncio
async def test_customize_rag_fixed_size_explicit_enum_aio():
    rag_name = "testrag"
    rag_description = "this is only a basic test"
    test_filename = "test.py"
    async with aio_straico_client() as client:
        with make_temp_file(test_filename, "this is a test") as file:
            s = await client.create_rag(
                rag_name,
                rag_description,
                file,
                chunking_method=ChunkingMethod.fixed_size,
                chunk_size=1001,
                chunk_overlap=55,
                separator="a",
            )
            assert s["name"] == rag_name
            assert s["description"] == rag_description
            assert s["original_filename"] == test_filename
            assert s["chunking_method"] == ChunkingMethod.fixed_size.value
            assert s["chunk_size"] == 1001
            assert s["chunk_overlap"] == 55
            assert s["separator"] == "a"


@pytest.mark.asyncio
async def test_customize_rag_recursive_explicit_str_aio():
    rag_name = "testrag"
    rag_description = "this is only a basic test"
    test_filename = "test.py"
    async with aio_straico_client() as client:
        with make_temp_file(test_filename, "this is a test") as file:
            s = await client.create_rag(
                rag_name,
                rag_description,
                file,
                chunking_method="recursive",
                chunk_size=1001,
                chunk_overlap=55,
                separator=["a"],
            )
            assert s["name"] == rag_name
            assert s["description"] == rag_description
            assert s["original_filename"] == test_filename
            assert s["chunking_method"] == "recursive"
            assert s["chunk_size"] == 1001
            assert s["chunk_overlap"] == 55
            assert s["separators"] == ["a"]


@pytest.mark.asyncio
async def test_customize_rag_recursive_explicit_enum_aio():
    rag_name = "testrag"
    rag_description = "this is only a basic test"
    test_filename = "test.py"
    async with aio_straico_client() as client:
        with make_temp_file(test_filename, "this is a test") as file:
            s = await client.create_rag(
                rag_name,
                rag_description,
                file,
                chunking_method=ChunkingMethod.recursive,
                chunk_size=1001,
                chunk_overlap=55,
                separator=["a"],
            )
            assert s["name"] == rag_name
            assert s["description"] == rag_description
            assert s["original_filename"] == test_filename
            assert s["chunking_method"] == ChunkingMethod.recursive.value
            assert s["chunk_size"] == 1001
            assert s["chunk_overlap"] == 55
            assert s["separators"] == ["a"]
