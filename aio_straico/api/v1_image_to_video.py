from typing import List
from enum import Enum


class ImageToVideoModel(Enum):
    fal_ai_kling_video_v2_1 = "fal-ai/kling-video/v2.1/master/image-to-video"
    fal_ai_veo2 = "fal-ai/veo2/image-to-video"
    fal_ai_vidu_q1 = "fal-ai/vidu/q1/image-to-video"
    gen3a_turbo = "gen3a_turbo"
    gen4_turbo = "gen4_turbo"


class VideoSize(Enum):
    square = "square"
    landscape = "landscape"
    portrait = "portrait"


async def aio_image_to_video(
    session,
    base_url: str,
    headers: dict,
    model: str,
    description: str,
    size: str,
    duration: int,
    image_url: str,
    **settings,
):
    url = f"{base_url}/v1/image/tovideo"
    payload = {
        "model": model,
        "description": description,
        "size": size,
        "duration": duration,
        "image_url": image_url,
    }
    if "timeout" not in settings:
        settings["timeout"] = 300
    response = await session.post(url, headers=headers, json=payload, **settings)
    return response


def image_to_video(
    session,
    base_url: str,
    headers: dict,
    model: str,
    description: str,
    size: str,
    duration: int,
    image_url: str,
    **settings,
):
    url = f"{base_url}/v1/image/tovideo"
    payload = {
        "model": model,
        "description": description,
        "size": size,
        "duration": duration,
        "image_url": image_url,
    }
    if "timeout" not in settings:
        settings["timeout"] = 300
    response = session.post(url, headers=headers, data=payload, **settings)
    return response
