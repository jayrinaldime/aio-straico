import asyncio
from aio_straico import aio_straico_client, ImageToVideoModel, VideoSize
from pathlib import Path
from pprint import pprint


async def async_main():
    async with aio_straico_client(timeout=600) as client:
        tts = await client.image_to_video_as_file(
            ImageToVideoModel.gen3a_turbo,
            VideoSize.landscape,
            5,
            "https://prompt-rack.s3.amazonaws.com/api/1753611904762_1746108434390_5RIVUXvT.png",  # Path("./images_0/ideogram/V_2A/1746108434390_5RIVUXvT.png"),
            "A resting cat happily sleeping.",
            destination_directory_path="./Video",
        )
        pprint(tts)


if __name__ == "__main__":
    asyncio.run(async_main())
