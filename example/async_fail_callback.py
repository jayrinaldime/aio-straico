import asyncio
from aio_straico import aio_straico_client
from aio_straico.utils import to_model_enum


async def async_main():
    def on_fail(request_type, response):
        import pprint

        print("Failed on request:", request_type.value)
        print("HTTP status code:", response.status_code)
        print("Response body:")
        pprint.pprint(response.json())

    async with aio_straico_client(
        STRAICO_REQUEST_RETRY_COUNT=3, timeout=1, on_request_failure_callback=on_fail
    ) as client:
        reply = await client.prompt_completion(
            "amazon/nova-lite-v1",
            "Tell me a joke about a pope and buddha",
            temperature=2.0,
            max_tokens=100,
            replace_failed_models=True,
        )
        if reply is None:
            print("Could not process request")
            return
        print(reply["completion"]["choices"][0]["message"]["content"])


if __name__ == "__main__":
    asyncio.run(async_main())
