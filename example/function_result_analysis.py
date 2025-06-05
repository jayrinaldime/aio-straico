import asyncio
import json
from aio_straico import aio_straico_client, ModelSelector


request_data = json.dumps(
    [
        {
            "role": "system",
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "calculator",
                        "description": "Useful for getting the result of a math expression. The input to this tool should be a valid mathematical expression that could be executed by a simple calculator.",
                        "parameters": {
                            "type": "object",
                            "properties": {"input": {"type": "string"}},
                            "additionalProperties": False,
                            "$schema": "http://json-schema.org/draft-07/schema#",
                        },
                    },
                }
            ],
            "content": """
If you need to use a tool to answer please use the defined tools.
Assuming the function is 
```
{"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather for a location","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The location to get the weather for, e.g. San Francisco, CA"},"format":{"type":"string","description":"The format to return the weather in, e.g. 'celsius' or 'fahrenheit'","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
```
When you do use a function your output should be like
``` 
{"tool_calls":[{"function":{"name":"get_current_weather","arguments":{"format":"celsius","location":"Paris, FR"}}}]}
``` 
You must answer by exactly following the provided instructions. Do not add any additional comments or explanations.
Do not add "Here is..." or anything like that.
Act like a script, you are given an optional input and the instructions to perform, you answer with the output of the requested task.
You must respond in valid JSON. Don't wrap the response in a markdown code.
""".strip(),
        },
        {"role": "user", "content": "what is 5+ 133922"},
        {"role": "assistant", "content": ""},
        {"role": "tool", "content": "133927"},
        {
            "role": "user",
            "content": "If this completely answers the request, please use the tool's result to respond.",
        },
    ]
)


async def async_auto_chat_v0():
    async with aio_straico_client() as client:
        reply = await client.prompt_completion(
            "openai/gpt-4.1-mini",
            request_data,
        )
        if reply is None:
            print("Could not process request")
            return
        print(reply["completion"]["choices"][0]["message"]["content"])


if __name__ == "__main__":
    asyncio.run(async_auto_chat_v0())
