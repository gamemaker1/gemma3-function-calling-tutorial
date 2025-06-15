"""
This module exports prompts that enable function calling based on the
model being used. The prompts are stored in markdown files, one per
model, in the `prompts/` directory.
"""


def function_calling(model: str) -> str:
    try:
        with open(f"prompts/{model}.md", encoding="utf-8") as file:
            contents = file.read()
            return contents
    except FileNotFoundError:
        print(f"Function calling with {model} is not yet supported.")
