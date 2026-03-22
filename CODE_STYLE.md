# Python Coding Standards and Best Practices

## Naming Conventions
- Use `snake_case` for variable and function names.
- Use `CamelCase` for class names.
- Constants should be written in `UPPER_SNAKE_CASE`.

## Formatting
- Use 4 spaces per indentation level.
- Limit all lines to a maximum of 79 characters.
- Use blank lines to separate functions and classes.

## Imports
- Import standard libraries first, followed by third-party libraries, and then local application/library imports.
- Group imports and use one import per line.

## Type Hints
- Use type hints for function parameters and return types to indicate expected types.

```python
def add(a: int, b: int) -> int:
    return a + b
```

## Docstrings
- All public modules, functions, classes, and methods should have docstrings to describe their purpose and usage.
- Use triple quotes for multi-line docstrings.

```python
def function_name(param1: str) -> None:
    """Description of function.

    Args:
        param1 (str): Parameter description.
    """
```

## Comments
- Use comments to explain complex code and logic.
- Comments should be clear and concise.

## Error Handling
- Use exceptions to handle errors and avoid using return codes.
- Always specify the exception type when catching exceptions.

## Testing Standards
- Use `unittest` or `pytest` for writing tests.
- Tests should be organized in a separate directory (e.g., `tests`).
- Ensure that tests cover both normal cases and edge cases.