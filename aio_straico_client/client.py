from os import environ
from contextlib import asynccontextmanager
from functools import wraps
from aiohttp import ClientSession
from .api.v0 import aio_user
from .api.v0 import aio_models as aio_model0
from .api.v1 import aio_models as aio_model1
from .api.v0 import aio_prompt_completion as aio_prompt_completion0
from aiohttp.client_exceptions import ServerDisconnectedError


def aio_retry_on_disconnect(func):
    @wraps(func)
    async def retry_func(self, *args, **kwargs):
        for i in range(1):
            try:
                r = await func(self, *args, **kwargs)
                return r
            except ServerDisconnectedError as e:
                print("REconnect")
                await self._reconnect()

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

        self._session = ClientSession()
        self.__prepare_header()

    async def _reconnect(self):
        await self._session.close()
        self._session = ClientSession()

    def __prepare_header(self):
        self._header = {"Authorization": f"Bearer {self._api_key}"}

    @property
    def API_KEY(self):
        return self._api_key

    @API_KEY.setter
    def API_KEY(self, API_KEY):
        self._api_key = API_KEY
        self.__prepare_header()

    @aio_retry_on_disconnect
    async def user(self):
        response = await aio_user(
            self._session, self.BASE_URL, self._header, **self._client_settings
        )
        if response.status == 200:
            return await response.json()

    @aio_retry_on_disconnect
    async def models(self, v=1):
        if v == 0:
            response = await aio_model0(
                self._session, self.BASE_URL, self._header, **self._client_settings
            )
        elif v == 1:
            response = await aio_model1(
                self._session, self.BASE_URL, self._header, **self._client_settings
            )
        else:
            raise Exception(f"Unsupported model api version {v}")

        if response.status == 200:
            return await response.json()

    @aio_retry_on_disconnect
    async def prompt_completion(self, model, message):
        if type(model) == dict and "model" in model:
            model = model["model"]
        response = await aio_prompt_completion0(
            self._session,
            self.BASE_URL,
            self._header,
            model,
            message,
            **self._client_settings,
        )
        if response.status == 201:
            return (await response.json())["data"]


@asynccontextmanager
async def aio_straico_client(
    API_KEY: str = None, STRAICO_BASE_URL: str = None, **settings: dict
):
    try:
        client = StraicoClient(
            API_KEY=API_KEY, STRAICO_BASE_URL=STRAICO_BASE_URL, **settings
        )
        yield client
    finally:
        await client._session.close()
