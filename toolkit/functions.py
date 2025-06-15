"""
This module exports utility functions that parse function definitions
and calls, and handle the execution lifecycle of the actual functions.
"""

import re
import json

from typing import TypedDict
from collections.abc import Callable

FunctionSpec = TypedDict(
    "FunctionSpec",
    {
        "name": str,
        "description": str,
        "parameters": TypedDict(
            "FunctionParams",
            {"type": "object", "properties": dict, "required": list[str]},
        ),
        "responses": list,
        "errors": list[TypedDict("FunctionError", {"name": str, "description": str})],
        "examples": list[
            TypedDict("InvocationExample", {"prompt": str, "parameters": dict})
        ],
    },
)

FunctionCall = TypedDict(
    "FunctionCall", {"id": str, "function": str, "parameters": dict}
)

code_block_regex = r"""
(?:\n+|\A)?
(?P<code_all>
    (?P<code_start>
        [ ]{0,3}
        `{3,}
    )
    [ \t]*
    (?:
        (?:
            (?P<code_class>[\w\-\.]+)
            (?:
                [ \t]*
                \{(?P<code_def_a>[^\}]+)\}
            )?
        )
        |
        (?:
            [ \t]*
            \{(?P<code_def_b>[^\}]+)\}
        )
    )?
    \n+
    (?P<code_content>.*?)
    \n+
    (?<!`)
    (?P=code_start)
    (?!`)
)
(?:\n|\Z)
"""

functions = {}


def register(spec: FunctionSpec, func: Callable) -> None:
    functions[spec["name"]] = {"spec": spec, "func": func}


def specify() -> str:
    return "\n".join(
        [
            f"```function_spec\n{json.dumps(x['spec'], indent=2)}\n```\n"
            for x in functions.values()
        ]
    )


def parse_calls(message: str) -> list[FunctionCall]:
    regex = re.compile(code_block_regex, re.VERBOSE | re.DOTALL)

    invocations = []
    for match in regex.finditer(message):
        if match.group("code_class") == "function_call":
            invocations.append(json.loads(match.group("code_content")))

    return invocations


def execute_call(invocation: FunctionCall, respond: Callable[[str], None]) -> None:
    name, args = invocation["function"], invocation["parameters"]

    try:
        result = functions[name]["func"](**args)
        response = json.dumps({"id": invocation["id"], "result": result}, indent=4)

    except Exception as error:
        response = json.dumps(
            {
                "id": invocation["id"],
                "error": {"name": type(error).__name__, "message": str(error)},
            },
            indent=4,
        )

    respond(f"```function_output\n{response}\n```")
