import os

from langchain_deepseek import ChatDeepSeek

from deer_code.config.config import get_config_section


def init_chat_model():
    settings = get_config_section(["models", "chat_model"])
    if not settings:
        raise ValueError(
            "The `models/chat_model` section in `config.yaml` is not found"
        )
    model = settings.get("model")
    if not model:
        raise ValueError("The `model` in `config.yaml` is not found")
    api_key = settings.get("api_key")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    elif api_key.startswith("$"):
        api_key = os.getenv(api_key[1:])
    rest_settings = settings.copy()
    del rest_settings["model"]
    del rest_settings["api_key"]
    model = ChatDeepSeek(model=model, api_key=api_key, **rest_settings)
    return model


if __name__ == "__main__":
    chat_model = init_chat_model()
    print(chat_model.invoke("What is the capital of France?"))
