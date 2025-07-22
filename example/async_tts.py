import asyncio
from aio_straico import aio_straico_client, TTSModel, TTS1Voices
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


if __name__ == "__main__":
    asyncio.run(async_tts_elevenlabs())
