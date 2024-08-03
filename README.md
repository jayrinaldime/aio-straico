## Async Client Libary for the Straico API

A client side implementation of Straico API. 




### Installation

```commandline
# install from PyPI
pip install aio-straico
```

### Usage

Please see the official Straico API documentation 
https://documenter.getpostman.com/view/5900072/2s9YyzddrR

### Basic Prompt Completion 
```python
from aio_straico.client import aio_straico_client
from aio_straico.utils import cheapest_model 

async def main():
    async with aio_straico_client(API_KEY="ko-11111111111111111111111111", ssl=False) as client:
        user_info = await client.user()
        print(user_info)
        """
        {'data': {'coins': 100000.00,
          'first_name': 'User',
          'last_name': 'Name',
          'plan': 'License Tier 1'},
        """
        
        models = await client.models()
        cheapest_chat_model = cheapest_model(models)
        print(cheapest_chat_model)
        """
        {'name': 'Google: Gemma 2 27B',  
         'model': 'google/gemma-2-27b-it',
         'word_limit': 3072,
         'pricing': {'coins': 0.4, 
                     'words': 100}}
        """
        
        reply = await client.prompt_completion(cheapest_chat_model, "Hello there")
        print(reply["completion"]["choices"][0]["message"]["content"])
        """
        General Kenobi! 👋 

        What can I do for you today? 😊
        """
asyncio.run(main())
```

when `API_KEY` is not set in aio_straico_client, it will use the value from environment variable `STRAICO_API_KEY`.
If no environment variable is found the program will raise an error.


You can also set the model name manually

```python
reply = await client.prompt_completion("openai/gpt-4o-mini", "Hello there")
print(reply["completion"]["choices"][0]["message"]["content"])
"""
General Kenobi! 👋 

What can I do for you today? 😊
"""
```

#### Add file attachment and Transcript
```python
mp3_files = [*Path("test_data/audio/").glob("*.mp3")]
response = await client.prompt_completion(
    "openai/gpt-4o-mini",
    "summarize the main points",
    files=mp3_files,
    display_transcripts=True,
)

print("## Summary")
print(
    response["completions"]["openai/gpt-4o-mini"]["completion"]["choices"][0][
        "message"
    ]["content"]
)

print("## Transcript")
for transcript in response["transcripts"]:
    print("Name:", transcript["name"])
    print("Transcript:", transcript["text"])
    print()

"""
## Summary 
The . . .

## Transcript
Name:  . . .
Transcript: . . .
"""
```

#### Add Youtube URL and Transcript
```python
youtube_url = "https://www.youtube.com/watch?v=zWPe_CUR4yU"

response = await client.prompt_completion(
    "openai/gpt-4o-mini",
    "summarize the main points",
    youtube_urls=youtube_url,
    display_transcripts=True,
)

print("## Summary")
print(
    response["completions"]["openai/gpt-4o-mini"]["completion"]["choices"][0][
        "message"
    ]["content"]
)

print("## Transcript")
for transcript in response["transcripts"]:
    print("Name:", transcript["name"])
    print("Transcript:", youtube_trasncript_to_plain_text(transcript["text"]))
    print()

"""
## Summary 
The . . .

## Transcript
Name:  . . .
Transcript: . . .
"""
```


### Image Generation 

#### Generate images and download zip file to local directory 
```python
model ="openai/dall-e-3"
directory = Path(".")
# with tempfile.TemporaryDirectory() as temp_directory:
zip_file_path = await client.image_generation_as_zipfile(
    model=model,
    description="A cute cat",
    size=ImageSize.square,
    variations=4,
    destination_zip_path=directory,
)
```

#### Generate images and download image files to local directory 
```python
model ="openai/dall-e-3"
directory = Path(".")
# with tempfile.TemporaryDirectory() as temp_directory:
image_paths = await client.image_generation_as_images(
    model=model,
    description="A cute cat",
    size=ImageSize.landscape,
    variations=4,
    destination_zip_path=directory,
)
```
