import asyncio
import time


async def aio_download_asset(session, asset_url, destination_path, **client_settings):
    content = None
    for i in range(5):
        try:
            response = await session.get(asset_url, **client_settings)
            content = response.read()
        except:
            await asyncio.sleep(1)
    if content is None:
        raise Exception(f"Unable to download asset URL {asset_url}")

    if destination_path.is_dir():
        filename = asset_url.split("/")[-1]
        destination_file_path = destination_path / filename
    else:
        destination_file_path = destination_path

    with destination_file_path.open("wb") as file_writer:
        file_writer.write(content)

    return destination_file_path


def download_asset(session, asset_url, destination_path, **client_settings):
    content = None
    for i in range(5):
        try:
            response = session.get(asset_url, **client_settings)
            content = response.read()
        except:
            time.sleep(1)
    if content is None:
        raise Exception(f"Unable to download asset URL {asset_url}")

    if destination_path.is_dir():
        filename = asset_url.split("/")[-1]
        destination_file_path = destination_path / filename
    else:
        destination_file_path = destination_path

    with destination_file_path.open("wb") as file_writer:
        file_writer.write(content)

    return destination_file_path
