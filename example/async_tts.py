import asyncio
from aio_straico import aio_straico_client, TTSModel, TTS1Voices
from aio_straico.utils import to_voices_enum
from pprint import pprint


async def async_main():
    async with aio_straico_client() as client:
        tts = await client.tts(
            TTSModel.tts_1, TTS1Voices.alloy, text="Hello world from alloy"
        )
        pprint(tts)


async def async_tts_elevenlabs():
    async with aio_straico_client() as client:
        tts = await client.tts(
            TTSModel.eleven_multilingual_v2,
            "9BWtsMINqrJLrRacOk9x",
            text="Hello world from eleven labs",
        )
        pprint(tts)


async def async_tts_elevenlabs2():
    async with aio_straico_client() as client:
        models = await client.elevenlabs_voices()
        voices = to_voices_enum(models)
        sarah_voice = voices.sarah
        tts = await client.tts(
            TTSModel.eleven_multilingual_v2,
            sarah_voice,
            text=f"Hello world from eleven labs model {sarah_voice.name}",
        )
        pprint(tts)


async def async_tts_as_zip():
    async with aio_straico_client() as client:
        tts_zip_path = await client.tts_as_zipfile(
            TTSModel.eleven_multilingual_v2,
            "9BWtsMINqrJLrRacOk9x",
            text="Hello world from eleven labs",
            destination_zip_path="./Audio",
        )
        print(tts_zip_path)


async def async_tts_as_audio():
    async with aio_straico_client() as client:
        tts_zip_path = await client.tts_as_audio(
            TTSModel.eleven_multilingual_v2,
            "9BWtsMINqrJLrRacOk9x",
            text="Hello world from eleven labs",
            destination_directory_path="./Audio",
        )
        print(tts_zip_path)


if __name__ == "__main__":
    asyncio.run(async_tts_elevenlabs2())
