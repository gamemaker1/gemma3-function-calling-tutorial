"""
This module exports prompts that enable various function calling
capabilities based on the model being used. The prompts are stored in
markdown files, one per model, in the `prompts/` directory.
"""

import re


def function_calling(model: str) -> str:
    model, *tags = model.split(":")
    try:
        with open(f"prompts/function-calling/{model}.md", encoding="utf-8") as file:
            contents = file.read()
            return contents
    except FileNotFoundError:
        print(f"Function calling with {model} is not yet supported.")


def function_writing(model: str) -> str:
    with open("schemas/function.schema.json", encoding="utf-8") as file:
        schema = file.read()

    model, *tags = model.split(":")
    try:
        with open(f"prompts/function-writing/{model}.md", encoding="utf-8") as file:
            contents = re.sub(r"{schema}", schema, file.read())
            return contents

    except FileNotFoundError:
        print(f"Function writing with {model} is not yet supported.")
