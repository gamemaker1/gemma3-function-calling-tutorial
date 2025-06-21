"""
This module exports utility functions that parse function definitions
and calls, and handle the execution lifecycle of the actual functions.
"""

import re
import json
import asyncio
import inspect

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


def register(func: Callable, spec: FunctionSpec) -> None:
    functions[spec["name"]] = {"spec": spec, "func": func}


def specify() -> str:
    return "\n".join(
        [
            f"```function_spec\n{json.dumps(x['spec'], indent=4)}\n```\n"
            for x in functions.values()
        ]
    )


def parse_funcs(message: str) -> list[str]:
    regex = re.compile(code_block_regex, re.VERBOSE | re.DOTALL)

    definitions = []
    for match in regex.finditer(message):
        if match.group("code_class") == "python":
            definitions.append(match.group("code_content"))

    return definitions


def parse_specs(message: str) -> list[FunctionSpec]:
    regex = re.compile(code_block_regex, re.VERBOSE | re.DOTALL)

    specifications = []
    for match in regex.finditer(message):
        if match.group("code_class") == "function_spec":
            specifications.append(json.loads(match.group("code_content")))

    return specifications


def parse_calls(message: str) -> list[FunctionCall]:
    regex = re.compile(code_block_regex, re.VERBOSE | re.DOTALL)

    invocations = []
    for match in regex.finditer(message):
        if match.group("code_class") == "function_call":
            invocations.append(json.loads(match.group("code_content")))

    return invocations


async def execute_call(invocation: FunctionCall) -> str:
    name, args = invocation["function"], invocation["parameters"]
    func = functions[name]["func"]

    try:
        if inspect.iscoroutinefunction(func):
            output = await func(**args)
        else:
            output = {"result": func(**args)}

        response = json.dumps({"id": invocation["id"], **output}, indent=4)

    except Exception as error:
        error = {"name": type(error).__name__, "message": str(error)}
        response = json.dumps({"id": invocation["id"], "error": error}, indent=4)

    return f"```function_output\n{response}\n```\n"


async def execute_calls(invocations: list[FunctionCall]) -> str:
    tasks = [asyncio.create_task(execute_call(inv)) for inv in invocations]
    results = []

    for task in asyncio.as_completed(tasks):
        results.append(await task)

    return "\n".join(results)
