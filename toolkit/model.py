"""
This module exports functions used to communicate with the model via
the Ollama REST API.
"""

import json
import base64
import requests

from typing import TypedDict, Generator
from enum import StrEnum

Role = StrEnum("Role", [("User", "user"), ("Model", "assistant")])

Message = TypedDict("Message", {"role": Role, "content": str, "images": list[str]})


def encode_image(path: str) -> str:
    try:
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file: {path}")
    except Exception as error:
        raise Exception(f"Failed to encode image {path}: {str(error)}")


def get_response(
    model: str, messages: list[Message], ollama_url="http://localhost:11434"
) -> Generator[str, None, None]:
    messages = [
        {**message, "images": [encode_image(image) for image in message["images"]]}
        if "images" in message
        else message
        for message in messages
    ]

    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "num_ctx": 8192,
            "top_p": 0.95,
        },
    }

    response = requests.post(
        f"{ollama_url}/api/chat", json=payload, stream=True, timeout=300
    )
    response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue

        try:
            data = json.loads(line.decode("utf-8"))
            if "message" in data and "content" in data["message"]:
                yield data["message"]["content"]

            if data.get("done", False):
                break
        except json.JSONDecodeError:
            continue
