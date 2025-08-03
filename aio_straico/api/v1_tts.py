from typing import List
from enum import Enum


class TTSModel(Enum):
    eleven_multilingual_v2 = "eleven_multilingual_v2"
    tts_1 = "tts-1"


class TTS1Voices(Enum):
    alloy = "alloy"
    echo = "echo"
    fable = "fable"
    onxy = "onyx"
    nova = "nova"
    shimmer = "shimmer"


async def aio_elevenlabs_voices(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v1/tts/elevenlabslist"
    response = await session.get(url, headers=headers, **settings)
    return response


def elevenlabs_voices(session, base_url: str, headers: dict, **settings):
    url = f"{base_url}/v1/tts/elevenlabslist"
    response = session.get(url, headers=headers, **settings)
    return response


async def aio_tts(
    session,
    base_url: str,
    headers: dict,
    model: str,
    text: str,
    voice_id: str,
    **settings,
):
    url = f"{base_url}/v1/tts/create"
    payload = {"model": model, "text": text, "voice_id": voice_id}
    response = await session.post(url, headers=headers, data=payload, **settings)
    return response


def tts(
    session,
    base_url: str,
    headers: dict,
    model: str,
    text: str,
    voice_id: str,
    **settings,
):
    url = f"{base_url}/v1/tts/create"
    payload = {"model": model, "text": text, "voice_id": voice_id}
    response = session.post(url, headers=headers, data=payload, **settings)
    return response
