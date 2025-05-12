from aio_straico import straico_client, ModelSelector


def auto_chat_v0():
    with straico_client() as client:
        reply = client.prompt_completion(
            ModelSelector.quality(),
            "Tell me a joke",
            temperature=2.0,
            max_tokens=100,
        )
        if reply is None:
            print("Could not process request")
        print(reply["completion"]["choices"][0]["message"]["content"])


def auto_chat_v1():
    with straico_client() as client:
        reply = client.prompt_completion(
            ModelSelector.balance(4),
            "Tell me a joke",
            temperature=2.0,
            max_tokens=100,
        )
        if reply is None:
            print("Could not process request")

        for model, response in reply["completions"].items():
            print("-------------------------------------")
            print(model)
            print("-------------------------------------")
            if "choices" in response["completion"]:
                print(response["completion"]["choices"][0]["message"]["content"])
            else:
                print(response["completion"]["error"])


if __name__ == "__main__":
    auto_chat_v0()
    auto_chat_v1()
