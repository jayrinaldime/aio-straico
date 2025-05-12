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
from aio_straico import straico_client, ModelSelector

def main():
    with straico_client(API_KEY="ko-11111111111111111111111111") as client:
        user_info = client.user()
        print(user_info)
        """
        {'coins': 100000.00,
          'first_name': 'User',
          'last_name': 'Name',
          'plan': 'License Tier 1'}
        """
        
        reply = client.prompt_completion(ModelSelector.budget(), 
                                         "Hello there")
        print(reply["completion"]["choices"][0]["message"]["content"])
        """
        General Kenobi! 👋 

        What can I do for you today? 😊
        """
if __name__=="__main__":
    main()
```

### Async Basic Prompt Completion 
```python
from aio_straico import aio_straico_client
from aio_straico.utils import cheapest_model 

async def main():
    async with aio_straico_client(API_KEY="ko-11111111111111111111111111") as client:
        user_info = await client.user()
        print(user_info)
        """
        {'coins': 100000.00,
          'first_name': 'User',
          'last_name': 'Name',
          'plan': 'License Tier 1'}
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

### Example Async Code 

While the code below is async code, it can also be executed in a non-async mode by removing "await" and using the code with `straico_client` as shown in the "Basic Prompt Completion" section.

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

#### Add Image File and describe the image
```python
images = [Path("test_data/image/sample.jpeg")]

response = await client.prompt_completion(
    "openai/gpt-4o-mini",
    "describe the image",
    images=images
)

print("## Image Description")
print(
    response["completions"]["openai/gpt-4o-mini"]["completion"]["choices"][0][
        "message"
    ]["content"]
)

"""
## Image Description 
The . . .
"""
```

### Image Generation 

#### Generate images and download zip file to local directory 
```python
model ="openai/dall-e-3"
directory = Path(".")
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
image_paths = await client.image_generation_as_images(
    model=model,
    description="A cute cat",
    size=ImageSize.landscape,
    variations=4,
    destination_zip_path=directory,
)
```


### RAG (Retrieval Augmented Generation)

#### Creating a RAG

##### Async Example
```python
from aio_straico import aio_straico_client
from pathlib import Path

async def main():
    async with aio_straico_client() as client:
        # Create a RAG by providing a name, description, and files to index
        rag = await client.create_rag(
            "My Code RAG", 
            "RAG for my project files",
            Path("./my_project/utils.py"),
            Path("./my_project/main.py")
        )
        print(rag)  # Print RAG details

        # Alternatively, create a new RAG object
        rag_obj = await client.new_rag(
            "My Code RAG", 
            "RAG for my project files",
            Path("./my_project/utils.py"),
            Path("./my_project/main.py")
        )
        print(rag_obj.data)
```

##### Synchronous Example
```python
from aio_straico import straico_client
from pathlib import Path

def main():
    with straico_client() as client:
        # Create a RAG by providing a name, description, and files to index
        rag = client.create_rag(
            "My Code RAG", 
            "RAG for my project files",
            Path("./my_project/utils.py"),
            Path("./my_project/main.py")
        )
        print(rag)  # Print RAG details

        # Alternatively, create a new RAG object
        rag_obj = client.new_rag(
            "My Code RAG", 
            "RAG for my project files",
            Path("./my_project/utils.py"),
            Path("./my_project/main.py")
        )
        print(rag_obj.data)
```

#### Deleting a RAG

##### Async Example
```python
async def delete_rag():
    async with aio_straico_client() as client:
        # Get existing RAGs
        rags = await client.rags()
        rag_id = rags[0]['_id']  # Get ID of first RAG

        # Delete RAG by ID
        await client.rag_delete(rag_id)

        # Or delete RAG object directly
        rag_obj = await client.rag(rag_id)
        await rag_obj.delete()
```

##### Synchronous Example
```python
def delete_rag():
    with straico_client() as client:
        # Get existing RAGs
        rags = client.rags()
        rag_id = rags[0]['_id']  # Get ID of first RAG

        # Delete RAG by ID
        client.rag_delete(rag_id)

        # Or delete RAG object directly
        rag_obj = client.rag(rag_id)
        rag_obj.delete()
```

#### RAG Prompt Completion

##### Async Example
```python
async def rag_prompt():
    async with aio_straico_client() as client:
        # Get existing RAGs
        rags = await client.rags()
        rag_id = rags[0]['_id']  # Get ID of first RAG

        # Get available models
        models = await client.models()
        cheapest_model = cheapest_model(models)

        # Perform RAG prompt completion
        response = await client.rag_prompt_completion(
            rag_id, 
            cheapest_model, 
            "Explain the main functionality of my project"
        )
        print(response)

        # Alternatively, with RAG object
        rag_obj = await client.rag(rag_id)
        response = await rag_obj.prompt_completion(
            cheapest_model, 
            "Explain the main functionality of my project"
        )
        print(response)
```

##### Synchronous Example
```python
def rag_prompt():
    with straico_client() as client:
        # Get existing RAGs
        rags = client.rags()
        rag_id = rags[0]['_id']  # Get ID of first RAG

        # Get available models
        models = client.models()
        cheapest_model = cheapest_model(models)

        # Perform RAG prompt completion
        response = client.rag_prompt_completion(
            rag_id, 
            cheapest_model, 
            "Explain the main functionality of my project"
        )
        print(response)

        # Alternatively, with RAG object
        rag_obj = client.rag(rag_id)
        response = rag_obj.prompt_completion(
            cheapest_model, 
            "Explain the main functionality of my project"
        )
        print(response)
```


### Agents

#### Creating an Agent

##### Async Example
```python
from aio_straico import aio_straico_client
from aio_straico.utils import cheapest_model

async def create_agent():
    async with aio_straico_client() as client:
        # Get available models
        models = await client.models()
        cheapest_chat_model = cheapest_model(models)

        # Create a new agent
        agent = await client.create_agent(
            "My Project Agent", 
            "An agent to help with my project",
            cheapest_chat_model,
            "You are a helpful assistant for my project.",
            ["Python", "Project"]
        )
        print(agent)  # Print agent details

        # Alternatively, create a new agent object
        agent_obj = await client.new_agent(
            "My Project Agent", 
            "An agent to help with my project",
            cheapest_chat_model,
            "You are a helpful assistant for my project.",
            ["Python", "Project"]
        )
        print(agent_obj.data)
```

##### Synchronous Example
```python
from aio_straico import straico_client
from aio_straico.utils import cheapest_model

def create_agent():
    with straico_client() as client:
        # Get available models
        models = client.models()
        cheapest_chat_model = cheapest_model(models)

        # Create a new agent
        agent = client.create_agent(
            "My Project Agent", 
            "An agent to help with my project",
            cheapest_chat_model,
            "You are a helpful assistant for my project.",
            ["Python", "Project"]
        )
        print(agent)  # Print agent details

        # Alternatively, create a new agent object
        agent_obj = client.new_agent(
            "My Project Agent", 
            "An agent to help with my project",
            cheapest_chat_model,
            "You are a helpful assistant for my project.",
            ["Python", "Project"]
        )
        print(agent_obj.data)
```

#### Adding a RAG to an Agent

##### Async Example
```python
async def add_rag_to_agent():
    async with aio_straico_client() as client:
        # Get existing RAGs and Agents
        rags = await client.rags()
        rag_id = rags[0]['_id']  # Get ID of first RAG

        agents = await client.agents()
        agent_id = agents[0]['_id']  # Get ID of first agent

        # Add RAG to agent by ID
        await client.agent_add_rag(agent_id, rag_id)

        # Or add RAG to agent object directly
        agent_obj = await client.agent(agent_id)
        await agent_obj.update(rag=rag_id)
```

##### Synchronous Example
```python
def add_rag_to_agent():
    with straico_client() as client:
        # Get existing RAGs and Agents
        rags = client.rags()
        rag_id = rags[0]['_id']  # Get ID of first RAG

        agents = client.agents()
        agent_id = agents[0]['_id']  # Get ID of first agent

        # Add RAG to agent by ID
        client.agent_add_rag(agent_id, rag_id)

        # Or add RAG to agent object directly
        agent_obj = client.agent(agent_id)
        agent_obj.update(rag=rag_id)
```

#### Updating an Agent

##### Async Example
```python
async def update_agent():
    async with aio_straico_client() as client:
        # Get an existing agent
        agents = await client.agents()
        agent_id = agents[0]['_id']

        # Update agent details
        await client.agent_update(
            agent_id, 
            name="Updated Agent Name",
            description="Updated description",
            system_prompt="You are an updated helpful assistant."
        )

        # Or update agent object directly
        agent_obj = await client.agent(agent_id)
        await agent_obj.update(
            name="Updated Agent Name",
            description="Updated description",
            system_prompt="You are an updated helpful assistant."
        )
```

##### Synchronous Example
```python
def update_agent():
    with straico_client() as client:
        # Get an existing agent
        agents = client.agents()
        agent_id = agents[0]['_id']

        # Update agent details
        client.agent_update(
            agent_id, 
            name="Updated Agent Name",
            description="Updated description",
            system_prompt="You are an updated helpful assistant."
        )

        # Or update agent object directly
        agent_obj = client.agent(agent_id)
        agent_obj.update(
            name="Updated Agent Name",
            description="Updated description",
            system_prompt="You are an updated helpful assistant."
        )
```

#### Agent Prompt Completion

##### Async Example
```python
async def agent_prompt():
    async with aio_straico_client() as client:
        # Get existing agents
        agents = await client.agents()
        agent_id = agents[0]['_id']  # Get ID of first agent

        # Perform agent prompt completion
        response = await client.agent_prompt_completion(
            agent_id, 
            "Explain the main functionality of my project"
        )
        print(response)

        # Alternatively, with agent object
        agent_obj = await client.agent(agent_id)
        response = await agent_obj.prompt_completion(
            "Explain the main functionality of my project"
        )
        print(response)
```

##### Synchronous Example
```python
def agent_prompt():
    with straico_client() as client:
        # Get existing agents
        agents = client.agents()
        agent_id = agents[0]['_id']  # Get ID of first agent

        # Perform agent prompt completion
        response = client.agent_prompt_completion(
            agent_id, 
            "Explain the main functionality of my project"
        )
        print(response)

        # Alternatively, with agent object
        agent_obj = client.agent(agent_id)
        response = agent_obj.prompt_completion(
            "Explain the main functionality of my project"
        )
        print(response)
```

#### Deleting an Agent

##### Async Example
```python
async def delete_agent():
    async with aio_straico_client() as client:
        # Get existing agents
        agents = await client.agents()
        agent_id = agents[0]['_id']  # Get ID of first agent

        # Delete agent by ID
        await client.agent_delete(agent_id)

        # Or delete agent object directly
        agent_obj = await client.agent(agent_id)
        await agent_obj.delete()
```

##### Synchronous Example
```python
def delete_agent():
    with straico_client() as client:
        # Get existing agents
        agents = client.agents()
        agent_id = agents[0]['_id']  # Get ID of first agent

        # Delete agent by ID
        client.agent_delete(agent_id)

        # Or delete agent object directly
        agent_obj = client.agent(agent_id)
        agent_obj.delete()
```