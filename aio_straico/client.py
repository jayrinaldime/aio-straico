from os import environ
from contextlib import contextmanager
from functools import wraps
from httpx import Client
from .api.v0 import user
from .api.v0 import models as model0
from .api.v1 import models as model1
from .api.v0 import prompt_completion as prompt_completion0
from .api.v1 import prompt_completion as prompt_completion1
from .api.v0 import file_upload
from .api.v0 import image_generation, ImageSize, ImageSizer
from httpx import RemoteProtocolError
from pathlib import Path
from .utils.models_to_enum import Model


def retry_on_disconnect(func):
    @wraps(func)
    def retry_func(self, *args, **kwargs):
        for i in range(1):
            try:
                r = func(self, *args, **kwargs)
                return r
            except RemoteProtocolError as e:
                print("REconnect")
                self._reconnect()

    return retry_func


class StraicoClient:
    def __init__(
        self, API_KEY: str = None, STRAICO_BASE_URL: str = None, **settings: dict
    ):
        self._client_settings = settings

        if API_KEY is None:
            API_KEY = environ.get("STRAICO_API_KEY")
            if API_KEY is None:
                raise Exception("Straico API Key is not defined")
            API_KEY = str(API_KEY)

        self._api_key = API_KEY

        if STRAICO_BASE_URL is None:
            STRAICO_BASE_URL = environ.get(
                "STRAICO_BASE_URL", "https://api.straico.com"
            )

        self.BASE_URL = STRAICO_BASE_URL

        self._session = Client()
        self.__prepare_header()

    async def _reconnect(self):
        self._session.close()
        self._session = Client()

    def __prepare_header(self):
        self._header = {"Authorization": f"Bearer {self._api_key}"}

    @property
    def API_KEY(self):
        return self._api_key

    @API_KEY.setter
    def API_KEY(self, API_KEY):
        self._api_key = API_KEY
        self.__prepare_header()

    @retry_on_disconnect
    def user(self):
        response = user(
            self._session, self.BASE_URL, self._header, **self._client_settings
        )
        if response.status_code == 200 and response.json()["success"]:
            return response.json()["data"]

    @retry_on_disconnect
    def models(self, v=1):
        if v == 0:
            response = model0(
                self._session, self.BASE_URL, self._header, **self._client_settings
            )
        elif v == 1:
            response = model1(
                self._session, self.BASE_URL, self._header, **self._client_settings
            )
        else:
            raise Exception(f"Unsupported model api version {v}")

        if response.status_code == 200 and response.json()["success"]:
            return response.json()["data"]

    @retry_on_disconnect
    def prompt_completion(
        self,
        model,
        message,
        *,
        files: [Path | str] = [],
        youtube_urls: [str] = [],
        temperature: float = None,
        max_tokens: float = None,
        display_transcripts=False,
    ):

        if type(model) == dict and "model" in model:
            model = model["model"]
        elif type(model) == Model:
            model = model.model

        if len(files) > 0 or len(youtube_urls) > 0:
            v = 1
        else:
            v = 0

        if v == 0:
            response = prompt_completion0(
                self._session,
                self.BASE_URL,
                self._header,
                model,
                message,
                temperature=temperature,
                max_tokens=max_tokens,
                **self._client_settings,
            )
        elif v == 1:
            if isinstance(youtube_urls, str):
                youtube_urls = [youtube_urls]

            if isinstance(files, str):
                files = [files]

            file_urls = []
            for file in files:
                if isinstance(file, str):
                    if not file.strip().lower().startswith("http"):
                        file_path = Path(file)
                        if file_path.exist():
                            file_url = self.upload_file(file)
                        else:
                            raise Exception(f"Unknown file {file}")
                    else:
                        file_url = file
                elif isinstance(file, Path):
                    file_url = self.upload_file(file)
                else:
                    raise Exception(f"Unknown file type {type(file)} for file {file}")
                file_urls.append(file_url)

            response = prompt_completion1(
                self._session,
                self.BASE_URL,
                self._header,
                model,
                message,
                file_urls=file_urls,
                youtube_urls=youtube_urls,
                display_transcripts=display_transcripts,
                temperature=temperature,
                max_tokens=max_tokens,
                **self._client_settings,
            )
        if response.status_code == 201 and response.json()["success"]:
            return response.json()["data"]

    @retry_on_disconnect
    def upload_file(self, file_to_upload: Path | str) -> str:
        if type(file_to_upload) == str:
            file_to_upload = Path(file_to_upload)
        # pdf, docx, pptx, txt, xlsx, mp3, mp4, html, csv, json
        content_type_mapping = {
            "mp3": "audio/mpeg",
            "mp4": "video/mp4",
            "pdf": "application/pdf",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "txt": "text/plain",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "html": "text/html",
            "htm": "text/html",
            "csv": "text/csv",
            "json": "application/json",
        }
        if not file_to_upload.exists():
            raise Exception(f"Cannot find file {file_to_upload}")

        if not file_to_upload.is_file() or file_to_upload.is_dir():
            raise Exception(f"Not a FILE {file_to_upload}")

        with file_to_upload.open("rb") as binary_reader:
            content = binary_reader.read(-1)

        file_extension = file_to_upload.name.split(".")[-1].lower()

        content_type = content_type_mapping.get(
            file_extension, "application/octet-stream"
        )
        response = file_upload(
            self._session,
            self.BASE_URL,
            self._header,
            filename=file_to_upload.name,
            content_type=content_type,
            binary_data=content,
            **self._client_settings,
        )
        if response.status_code == 201 and response.json()["success"]:
            return response.json()["data"]["url"]

    @retry_on_disconnect
    def image_generation(
        self, model, description: str, size: ImageSize | str, variations: int
    ):
        if type(model) == dict and "model" in model:
            model = model["model"]
        elif type(model) == Model:
            model = model.model

        response = image_generation(
            self._session,
            self.BASE_URL,
            self._header,
            model=model,
            description=description,
            size=size,
            variations=variations,
            **self._client_settings,
        )
        if response.status_code == 201 and response.json()["success"]:
            return response.json()["data"]

    def image_generation_as_zipfile(
        self,
        model,
        description: str,
        size: ImageSize | str,
        variations: int,
        destination_zip_path: Path | str,
    ) -> Path:
        if type(destination_zip_path) == str:
            destination_zip_path = Path(destination_zip_path)

        image_details = self.image_generation(model, description, size, variations)

        zip_url = image_details["zip"]

        response = self._session.get(zip_url, **self._client_settings)
        content = response.read()

        if destination_zip_path.is_dir():
            zip_name = zip_url.split("/")[-1]
            destination_zip_path = destination_zip_path / zip_name

        with destination_zip_path.open("wb") as file_writer:
            file_writer.write(content)

        return destination_zip_path

    def close(self):
        self._session.close()

    def image_generation_as_images(
        self,
        model,
        description: str,
        size: ImageSize | str,
        variations: int,
        destination_directory_path: Path | str,
    ) -> [Path]:
        if type(destination_directory_path) == str:
            destination_directory_path = Path(destination_directory_path)

        if not destination_directory_path.is_dir():
            raise Exception("Destination path is not a directory")

        image_details = self.image_generation(model, description, size, variations)

        image_urls = image_details["images"]
        image_paths = []
        for image_url in image_urls:
            response = self._session.get(image_url, **self._client_settings)
            content = response.read()

            image_name = image_url.split("/")[-1]
            destination_image_path = destination_directory_path / image_name

            with destination_image_path.open("wb") as file_writer:
                file_writer.write(content)

            image_paths.append(destination_image_path)

        return image_paths


@contextmanager
def straico_client(API_KEY: str = None, STRAICO_BASE_URL: str = None, **settings: dict):
    try:
        client = StraicoClient(
            API_KEY=API_KEY, STRAICO_BASE_URL=STRAICO_BASE_URL, **settings
        )
        yield client
    finally:
        client.close()
