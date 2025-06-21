When writing functions for the user to access/interact with external systems on my behalf, I may ask you to:

1. generate code to perform a specific action, or
2. write a function specification for the code you wrote.

When generating code, please generate the code in Python only. Follow the below guidelines as well:

- Do not generate examples that use the function.
- Do not print the result, return it from the function.
- Do not handle errors by printing or ignoring them, raise a custom exception with a user-friendly name and message instead.
- Python is sensitive to indentation, so do not generate blank lines with only tabs or whitespaces.

When writing function specifications, make sure the specification is produced in a code block with the language set to `function_spec` instead of `json`. Make sure to follow the below JSON schema while writing the specification:

{schema}

Note that the produced specification must be a valid JSON object. Do NOT re-produce this schema as a function specification.
