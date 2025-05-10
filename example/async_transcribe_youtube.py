import asyncio
from aio_straico import aio_straico_client
from aio_straico.utils import to_model_enum


async def async_youtube_transcribe():
    async with aio_straico_client() as client:
        models_v1 = await client.models(v=1)
        chat_models, image_models = to_model_enum(models_v1)
        model = chat_models.amazon.nova_lite_1_0
        question = "What is Zuck’s Stunning Claim About Meta’s Self-Improving AI"
        reply = await client.prompt_completion(
            model,
            question,
            temperature=0.2,
            youtube_urls=["https://youtube.com/watch?v=2o5V6SVl7k0"],
            display_transcripts=True,
        )
        transcript = reply["transcripts"][0]["text"]
        answer = reply["completions"][model["model"]]["completion"]["choices"][0][
            "message"
        ]["content"]
        print("Question:", question)
        print("Answer:", answer)
        print("Whole Video Transcript:")
        print(transcript)


if __name__ == "__main__":
    asyncio.run(async_youtube_transcribe())
