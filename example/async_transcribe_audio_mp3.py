import asyncio
from aio_straico import aio_straico_client
from aio_straico.utils import to_model_enum
from pathlib import Path

async def async_audio_transcribe():
    async with aio_straico_client() as client:
        models_v1 = await client.models(v=1)
        chat_models, image_models = to_model_enum(models_v1)
        model = chat_models.amazon.nova_lite_1_0

        mp3_file = [*Path("../test_data/audio/").glob("*.mp3")][0]

        response = await client.prompt_completion(
            model,
            "summarize the main points",
            files=[mp3_file],
            display_transcripts=True,
        )
        print("## Summary")
        print(
            response["completions"][model["model"]]["completion"]["choices"][0][
                "message"
            ]["content"]
        )

        print("## Transcript")
        for transcript in response["transcripts"]:
            print("Name:", transcript["name"])
            print("Transcript:", transcript["text"])
            print()

if __name__ == "__main__":
    asyncio.run(async_audio_transcribe())
