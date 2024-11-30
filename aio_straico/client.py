from os import environ
from contextlib import contextmanager
from functools import wraps
from httpx import Client
from .api.v0 import user
from .api.v0_agent import (
    create_agent as api_create_agent,
    agents as api_agents,
    agent as api_agent,
    agent_delete as api_agent_delete,
    agent_prompt_completion as api_agent_prompt_completion,
    agent_update as api_agent_update,
    add_rag_to_agent as api_add_rag_to_agent,
)
from .client_agent import StraicoAgent
from .api.v0 import models as model0
from .api.v1 import models as model1
from .api.v0 import prompt_completion as prompt_completion0
from .api.v1 import prompt_completion as prompt_completion1
from .api.v0 import file_upload
from .api.v0 import image_generation, ImageSize, ImageSizer
from .api.v0_rag import (
    ChunkingMethod,
    BreakpointThresholdType,
    SearchType,
    create_rag as api_create_rag,
    rags as api_rags,
    rag as api_rag,
    rag_delete as api_rag_delete,
    rag_prompt_completion as api_rag_prompt_completion,
)
from httpx import RemoteProtocolError
from pathlib import Path
from .utils.models_to_enum import Model
from .utils import is_listable_not_string

from .client_agent import StraicoAgent
from .client_rag import StraicoRAG


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
        raw_output=False,
    ):

        if type(model) == dict and "model" in model:
            model = model["model"]
        elif type(model) == Model:
            model = model.model

        if len(files) > 0 or len(youtube_urls) > 0:
            if is_listable_not_string(files) and len(files) > 4:
                raise Exception(
                    f"Too many attached files. API is limited to 4 File attachments"
                )
            if is_listable_not_string(youtube_urls) and len(youtube_urls) > 4:
                raise Exception(
                    f"Too many youtube_urls files. API is limited to 4 Youtube URL attachments"
                )
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
            if raw_output:
                return response.json()
            else:
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

        file_extension = file_to_upload.name.split(".")[-1].strip().lower()

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

    #################################
    # Image Generation API
    ##############################
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

    def close(self):
        self._session.close()

    #################################
    # RAG API
    ##############################
    @retry_on_disconnect
    def create_rag(
        self,
        name: str,
        description: str,
        *file_to_uploads: [Path | str],
        chunking_method: [ChunkingMethod | str] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 50,
        breakpoint_threshold_type: [
            BreakpointThresholdType | str
        ] = BreakpointThresholdType.percentile,
        buffer_size: int = 500,
    ) -> str:
        if len(file_to_uploads) > 4:
            raise Exception(
                "Too many files, Only accepts up to 4 Files per RAG Instance"
            )
        if len(file_to_uploads) == 0:
            raise Exception("Requires at least 1 File per RAG Instance")

        response = api_create_rag(
            self._session,
            self.BASE_URL,
            self._header,
            name=name,
            description=description,
            chunking_method=chunking_method,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            breakpoint_threshold_type=breakpoint_threshold_type,
            buffer_size=buffer_size,
            files=file_to_uploads,
            **self._client_settings,
        )
        if response.status_code == 201 and response.json()["success"]:
            return response.json()["data"]

    @retry_on_disconnect
    def rags(self) -> str:
        response = api_rags(
            self._session,
            self.BASE_URL,
            self._header,
            **self._client_settings,
        )
        if response.status_code == 200 and response.json()["success"]:
            return response.json()["data"]

    @retry_on_disconnect
    def rag(self, rag_id: str) -> str:
        response = api_rag(
            self._session,
            self.BASE_URL,
            self._header,
            rag_id,
            **self._client_settings,
        )
        if response.status_code == 200 and response.json()["success"]:
            return response.json()["data"]

    @retry_on_disconnect
    def rag_delete(self, rag_id: str) -> str:
        response = api_rag_delete(
            self._session,
            self.BASE_URL,
            self._header,
            rag_id,
            **self._client_settings,
        )
        if response.status_code == 200 and response.json()["success"]:
            return response.json()

    @retry_on_disconnect
    def rag_prompt_completion(
        self,
        rag_id: str,
        model: str,
        message: str,
        search_type: [SearchType | str] = None,
        k: int = None,
        fetch_k: int = None,
        lambda_mult: float = None,
        score_threshold: float = None,
    ) -> str:
        if type(model) == dict and "model" in model:
            model = model["model"]
        elif type(model) == Model:
            model = model.model

        response = api_rag_prompt_completion(
            self._session,
            self.BASE_URL,
            self._header,
            rag_id,
            model,
            message,
            search_type,
            k,
            fetch_k,
            lambda_mult,
            score_threshold,
            **self._client_settings,
        )
        if response.status_code == 200 and response.json()["success"]:
            return response.json()["response"]

    #################################
    # RAG object factory methods
    ##############################
    def rag_object(self, rag_id):
        data = self.rag(rag_id=rag_id)
        agent_obj = StraicoAgent(self, data)
        return agent_obj

    def rag_objects(self):
        _rags = self.rags()
        return [StraicoRAG(self, rag) for rag in _rags]

    def new_rag(
        self,
        name: str,
        description: str,
        *file_to_uploads: [Path | str],
        chunking_method: [ChunkingMethod | str] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 50,
        breakpoint_threshold_type: [
            BreakpointThresholdType | str
        ] = BreakpointThresholdType.percentile,
        buffer_size: int = 500,
    ) -> str:
        _rag = self.create_rag(
            name,
            description,
            *file_to_uploads,
            chunking_method=chunking_method,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            breakpoint_threshold_type=breakpoint_threshold_type,
            buffer_size=buffer_size,
        )
        return StraicoRAG(self, _rag)

    #################################
    # Agent API
    ##############################
    @retry_on_disconnect
    def create_agent(
        self,
        name: str,
        description: str,
        model: str,
        system_prompt: str,
        tags: [str] = [],
        rag: [StraicoRAG | dict | str] = None,
    ) -> str:
        if type(model) == dict and "model" in model:
            model = model["model"]
        elif type(model) == Model:
            model = model.model

        response = api_create_agent(
            self._session,
            self.BASE_URL,
            self._header,
            name=name,
            description=description,
            model=model,
            system_prompt=system_prompt,
            tags=tags,
            **self._client_settings,
        )
        if response.status_code == 201 and response.json()["success"]:
            _agent = response.json()["data"]
            if rag is not None:
                rag_type = type(rag)
                if rag_type == dict and "_id" in rag:
                    rag = rag["_id"]
                if rag_type == StraicoRAG:
                    rag = rag.data["_id"]
                return self.agent_add_rag(_agent["_id"], rag)
            return _agent

    @retry_on_disconnect
    def agents(self, *, with_tag: str = None) -> str:
        response = api_agents(
            self._session,
            self.BASE_URL,
            self._header,
            **self._client_settings,
        )
        if response.status_code == 200 and response.json()["success"]:
            _agents = response.json()["data"]
            if with_tag is None:
                return _agents
            return [agent for agent in _agents if with_tag in agent["tag"]]

    @retry_on_disconnect
    def agent(self, agent_id: str) -> str:
        response = api_agent(
            self._session,
            self.BASE_URL,
            self._header,
            agent_id,
            **self._client_settings,
        )
        if response.status_code == 200 and response.json()["success"]:
            return response.json()["data"]

    @retry_on_disconnect
    def agent_delete(self, agent_id: str) -> dict:
        response = api_agent_delete(
            self._session,
            self.BASE_URL,
            self._header,
            agent_id,
            **self._client_settings,
        )
        if response.status_code == 200 and response.json()["success"]:
            return response.json()

    @retry_on_disconnect
    def agent_add_rag(self, agent_id: str, rag_id: [StraicoRAG | dict | str]) -> dict:
        rag_type = type(rag_id)
        if rag_type == dict and "_id" in rag_id:
            rag_id = rag_id["_id"]
        elif rag_type == StraicoRAG:
            rag_id = rag_id.data["_id"]

        response = api_add_rag_to_agent(
            self._session,
            self.BASE_URL,
            self._header,
            agent_id,
            rag_id,
            **self._client_settings,
        )

        if response.status_code == 200 and response.json()["success"]:
            return response.json()["data"]

    @retry_on_disconnect
    def agent_prompt_completion(
        self,
        agent_id: str,
        message: str,
        search_type: [SearchType | str] = None,
        k: int = None,
        fetch_k: int = None,
        lambda_mult: float = None,
        score_threshold: float = None,
    ) -> dict:
        response = api_agent_prompt_completion(
            self._session,
            self.BASE_URL,
            self._header,
            agent_id,
            message,
            search_type,
            k,
            fetch_k,
            lambda_mult,
            score_threshold,
            **self._client_settings,
        )
        if response.status_code == 200 and response.json()["success"]:
            return response.json()["response"]

    @retry_on_disconnect
    def agent_update(
        self,
        agent_id: str,
        rag: [StraicoRAG | dict | str] = None,
        name: str = None,
        description: str = None,
        model: str = None,
        system_prompt: str = None,
        tags: [str] = None,
    ) -> str:
        if rag is not None:
            rag_type = type(rag)
            if rag_type == dict and "_id" in rag:
                rag = rag["_id"]
            elif rag_type == StraicoRAG:
                rag = rag.data["_id"]

        if type(model) == dict and "model" in model:
            model = model["model"]
        elif type(model) == Model:
            model = model.model

        response = api_agent_update(
            self._session,
            self.BASE_URL,
            self._header,
            agent_id,
            rag_id=rag,
            name=name,
            description=description,
            model=model,
            system_prompt=system_prompt,
            tags=tags,
            **self._client_settings,
        )
        if response.status_code == 200 and response.json()["success"]:
            return response.json()["data"]

    #################################
    # Agent object factory methods
    ##############################
    def agent_object(self, agent_id):
        data = self.agent(agent_id=agent_id)
        agent_obj = StraicoAgent(self, data)
        return agent_obj

    def agent_objects(self, *, with_tag: str = None):
        _agents = self.agents(with_tag=with_tag)
        return [StraicoAgent(self, agent) for agent in _agents]

    def new_agent(
        self,
        name: str,
        description: str,
        model: str,
        system_prompt: str,
        tags: [str] = [],
        rag: [StraicoRAG | dict | str] = None,
    ) -> str:
        _agent = self.create_agent(
            name=name,
            description=description,
            model=model,
            system_prompt=system_prompt,
            tags=tags,
            rag=rag,
        )
        return StraicoAgent(self, _agent)


@contextmanager
def straico_client(API_KEY: str = None, STRAICO_BASE_URL: str = None, **settings: dict):
    try:
        client = StraicoClient(
            API_KEY=API_KEY, STRAICO_BASE_URL=STRAICO_BASE_URL, **settings
        )
        yield client
    finally:
        client.close()
