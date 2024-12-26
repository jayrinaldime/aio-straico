import pytest
from .utils import make_temp_file
from aio_straico import straico_client, aio_straico_client


@pytest.mark.parametrize(
    "unsupported_file_name, content",
    [
        ("test.htm", """<html><body><p>Hello, World!</p></body></html"""),
        ("test.perl", """print "Hello, World!\n";"""),
    ],
)
def test_unsupported_file_upload(unsupported_file_name, content):
    with make_temp_file(unsupported_file_name, content) as file:
        with straico_client() as client:
            with pytest.raises(Exception, match="Unsupported File Type"):
                s = client.upload_file(file)


@pytest.mark.parametrize(
    "file_name, content",
    [
        # ('test.htm', """<html><body><p>Hello, World!</p></body></html"""),
        ("test.html", """<html><body><p>Hello, World!</p></body></html"""),
        ("test.json", """{"text": "Hello, World!"}"""),
        ("test.txt", """Hello, World!"""),
        ("test.csv", """Hello, World)"""),
        ("test.py", """print("Hello, World!")"""),
        ("test.php", """<?php echo "Hello, World!"; ?>"""),
        (
            "test.js",
            """function sayHello(): void { \nconsole.log("Hello, World!");\n}""",
        ),
        (
            "test.css",
            """body { \n    background-color: #f0f0f0; \n    font-family: Arial, sans-serif; \n}""",
        ),
        ("test.cs", """Console.WriteLine("Hello, World!");"""),
        ("test.swift", """import Foundation\n\nprint("Hello, World!")"""),
        ("test.kt", """fun main() {\n    println("Hello, World!")\n}"""),
        ("test.xml", """<test> hello world </test>"""),
        (
            "test.ts",
            """function sayHello(): void { \nconsole.log("Hello, World!");\n}""",
        ),
    ],
)
def test_supported_file_upload(file_name, content):
    with make_temp_file(file_name, content) as file:
        with straico_client() as client:
            s = client.upload_file(file)
            assert s is not None
            assert s.endswith("_" + file_name)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "unsupported_file_name, content",
    [
        ("test.htm", """<html><body><p>Hello, World!</p></body></html"""),
        ("test.perl", """print "Hello, World!\n";"""),
    ],
)
async def test_unsupported_file_upload_aio(unsupported_file_name, content):
    with make_temp_file(unsupported_file_name, content) as file:
        async with aio_straico_client() as client:
            with pytest.raises(Exception, match="Unsupported File Type"):
                s = await client.upload_file(file)
                print(s)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "file_name, content",
    [
        # ('test.htm', """<html><body><p>Hello, World!</p></body></html"""),
        ("test.html", """<html><body><p>Hello, World!</p></body></html"""),
        ("test.json", """{"text": "Hello, World!"}"""),
        ("test.txt", """Hello, World!"""),
        ("test.csv", """Hello, World)"""),
        ("test.py", """print("Hello, World!")"""),
        ("test.php", """<?php echo "Hello, World!"; ?>"""),
        (
            "test.js",
            """function sayHello(): void { \nconsole.log("Hello, World!");\n}""",
        ),
        (
            "test.css",
            """body { \n    background-color: #f0f0f0; \n    font-family: Arial, sans-serif; \n}""",
        ),
        ("test.cs", """Console.WriteLine("Hello, World!");"""),
        ("test.swift", """import Foundation\n\nprint("Hello, World!")"""),
        ("test.kt", """fun main() {\n    println("Hello, World!")\n}"""),
        ("test.xml", """<test> hello world </test>"""),
        (
            "test.ts",
            """function sayHello(): void { \nconsole.log("Hello, World!");\n}""",
        ),
    ],
)
async def test_supported_file_upload_aio(file_name, content):
    with make_temp_file(file_name, content) as file:
        async with aio_straico_client() as client:
            s = await client.upload_file(file)
            assert s is not None
            assert s.endswith("_" + file_name)
