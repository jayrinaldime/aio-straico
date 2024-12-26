import tempfile
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def make_temp_file(filename, content):
    with tempfile.TemporaryDirectory() as temp_directory:
        temp_file = Path(temp_directory) / filename
        with temp_file.open("w", encoding="utf-8") as writer:
            writer.write(content)
        yield temp_file
