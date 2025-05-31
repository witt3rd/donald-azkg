**Key Points:**

- Use built-in `list`, `dict` for type hints; `typing.List`, `typing.Dict` deprecated since Python 3.9.
- Adopt NumPy-style docstrings for clear, structured documentation.
- Manage configurations with `python-dotenv` for secure environment variables.
- Use `loguru` for simple, intuitive logging with customizable outputs.
- Write minimalist comments explaining "why," not "what," only when necessary.

**Type Hints**
Use `list`, `dict`, `set` directly in type annotations (e.g., `def func(items: list[int]) -> dict[str, int]:`). Avoid `typing.List`, `typing.Dict` as they’re deprecated ([PEP 585](https://peps.python.org/pep-0585/)).

**Docstrings**
Follow NumPy style for clarity, especially in scientific projects. Include summary, parameters, returns, and examples ([NumPy Docstring Guide](https://numpydoc.readthedocs.io/en/latest/format.html)).

**Configuration Management**
Use `python-dotenv` to load `.env` file variables. Add `.env` to `.gitignore` ([python-dotenv](https://pypi.org/project/python-dotenv/)).

**Logging**
Use `loguru` for easy logging. Configure handlers and use `@logger.catch` for exceptions ([Loguru Docs](https://loguru.readthedocs.io/en/stable/)).

**Comments**
Comment only to explain rationale or complex logic. Avoid obvious or historical comments.

```python
# Example demonstrating Python 3.13 best practices
from dotenv import load_dotenv
from loguru import logger
import os

load_dotenv()  # Load environment variables from .env

# Use built-in types for type hints
def process_data(items: list[str]) -> dict[str, int]:
    """Count occurrences of items in a list.

    Parameters
    ----------
    items : list[str]
        List of strings to count.

    Returns
    -------
    dict[str, int]
        Dictionary with item counts.

    Examples
    --------
    >>> process_data(["a", "b", "a"])
    {'a': 2, 'b': 1}
    """
    # Using dict for O(1) lookups to optimize counting
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    logger.info(f"Processed {len(items)} items")
    return counts

@logger.catch
def fetch_api_data(api_key: str) -> list[str]:
    """Fetch data from an API (mock example).

    Parameters
    ----------
    api_key : str
        API key for authentication.

    Returns
    -------
    list[str]
        List of data items.
    """
    # Simulate API call; in reality, use os.getenv("API_KEY")
    logger.debug("Fetching data with API key")
    return ["data1", "data2"]

if __name__ == "__main__":
    logger.add("app.log", level="INFO")
    api_key = os.getenv("API_KEY")
    data = fetch_api_data(api_key)
    result = process_data(data)
    logger.info(f"Result: {result}")
```

---

**Python 3.13 Best Practices Guide**

**1. Type Hints and Built-in Collections**
Since Python 3.9, built-in types like `list`, `dict`, and `set` support generic type annotations, making `typing.List`, `typing.Dict`, and similar aliases redundant ([PEP 585](https://peps.python.org/pep-0585/)). In Python 3.13, it’s best practice to use these built-in types directly in type hints to simplify code and align with modern standards. For example:

```python
def example(items: list[int]) -> dict[str, int]:
    return {str(i): i for i in items}
```

The `typing` module’s aliases (e.g., `typing.List`, `typing.Dict`) are deprecated and may trigger warnings in type checkers for Python 3.9+ projects. They are slated for removal in future versions, so avoid them. Additionally, Python 3.13 updates `locals()` to have defined mutation semantics in optimized scopes (e.g., functions, generators), ensuring consistent behavior with `exec()` and `eval()` ([PEP 667](https://peps.python.org/pep-0667/)).

**2. NumPy-Style Docstrings**
For clear and consistent documentation, especially in scientific or data science projects, adopt the NumPy docstring format ([NumPy Docstring Guide](https://numpydoc.readthedocs.io/en/latest/format.html)). This style uses reStructuredText (reST) and is compatible with Sphinx for generating documentation. Key sections include:

- **Summary:** A concise, one-line description.
- **Parameters:** List parameters with types and descriptions.
- **Returns:** Describe return values and types.
- **Examples:** Provide executable code examples.
- **Notes:** Optional for additional context.

Example:

```python
def calculate_mean(values: list[float]) -> float:
    """Calculate the arithmetic mean of a list of numbers.

    Parameters
    ----------
    values : list[float]
        List of numbers to average.

    Returns
    -------
    float
        The arithmetic mean.

    Examples
    --------
    >>> calculate_mean([1.0, 2.0, 3.0])
    2.0
    """
    return sum(values) / len(values)
```

Keep lines under 70 characters and avoid excessive markup to ensure readability in terminals.

**3. Configuration Management with `python-dotenv`**
The `python-dotenv` library is ideal for managing configuration settings, particularly sensitive data like API keys or database credentials, by loading them from a `.env` file ([python-dotenv](https://pypi.org/project/python-dotenv/)). Best practices include:

- Install: `pip install python-dotenv`
- Create a `.env` file in the project root:

  ```
  API_KEY=your_api_key_here
  DATABASE_URL=your_database_url
  ```

- Load variables in your script:

  ```python
  from dotenv import load_dotenv
  import os

  load_dotenv()
  api_key = os.getenv("API_KEY")
  ```

- Add `.env` to `.gitignore` to prevent committing sensitive data.
- Use `os.getenv()` to safely access variables, providing defaults if needed:

  ```python
  debug_mode = os.getenv("DEBUG", "False").lower() == "true"
  ```

This approach keeps configurations secure and separate from code, following the 12-factor app principles.

**4. Logging with `loguru`**
`Loguru` simplifies logging with a user-friendly API, offering features like colored output, file rotation, and exception handling ([Loguru Docs](https://loguru.readthedocs.io/en/stable/)). Best practices include:

- Install: `pip install loguru`
- Basic usage:

  ```python
  from loguru import logger

  logger.debug("Debug message")
  logger.info("Info message")
  ```

- Configure handlers for different outputs:

  ```python
  logger.add("app.log", level="INFO", rotation="1 MB")
  ```

- Use `@logger.catch` for automatic exception logging:

  ```python
  @logger.catch
  def risky_operation():
      return 1 / 0
  ```

- Customize log formats for clarity:

  ```python
  logger.add(sys.stderr, format="<green>{time}</green> <level>{message}</level>")
  ```

`Loguru` reduces boilerplate compared to Python’s `logging` module, making it ideal for debugging and monitoring.

**5. Minimalist Comment Style**
Comments should enhance code understanding by explaining the rationale behind decisions, not restating what the code does. Follow these guidelines:

- **Focus on "Why":** Comment only to clarify intent or trade-offs.
- **Avoid Obvious Comments:** Don’t repeat what clear code already conveys.
- **Use Sparingly:** Write self-documenting code with descriptive names and structures.
- **No Change History:** Use version control (e.g., Git) for tracking changes.

Good example:

```python
# Use set for O(1) membership testing to optimize performance
unique_items = set(data)
```

Bad example (avoid):

```python
# Create a list from data
items = list(data)
```

Only comment complex logic or non-obvious decisions, ensuring comments add value.

**Example Code**
Below is a sample script demonstrating these practices:

```python
# Example demonstrating Python 3.13 best practices
from dotenv import load_dotenv
from loguru import logger
import os

load_dotenv()  # Load environment variables from .env

# Use built-in types for type hints
def process_data(items: list[str]) -> dict[str, int]:
    """Count occurrences of items in a list.

    Parameters
    ----------
    items : list[str]
        List of strings to count.

    Returns
    -------
    dict[str, int]
        Dictionary with item counts.

    Examples
    --------
    >>> process_data(["a", "b", "a"])
    {'a': 2, 'b': 1}
    """
    # Using dict for O(1) lookups to optimize counting
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    logger.info(f"Processed {len(items)} items")
    return counts

@logger.catch
def fetch_api_data(api_key: str) -> list[str]:
    """Fetch data from an API (mock example).

    Parameters
    ----------
    api_key : str
        API key for authentication.

    Returns
    -------
    list[str]
        List of data items.
    """
    # Simulate API call; in reality, use os.getenv("API_KEY")
    logger.debug("Fetching data with API key")
    return ["data1", "data2"]

if __name__ == "__main__":
    logger.add("app.log", level="INFO")
    api_key = os.getenv("API_KEY")
    data = fetch_api_data(api_key)
    result = process_data(data)
    logger.info(f"Result: {result}")
```

**Summary Table**

| **Category**      | **Best Practice**                                                                    |
| ----------------- | ------------------------------------------------------------------------------------ |
| **Type Hints**    | Use `list`, `dict`, `set` directly; avoid `typing.List`, `typing.Dict` (deprecated). |
| **Docstrings**    | Use NumPy style with summary, parameters, returns, examples; keep lines <70 chars.   |
| **Configuration** | Use `python-dotenv` for `.env` files; add `.env` to `.gitignore`.                    |
| **Logging**       | Use `loguru` for simple logging; configure handlers, use `@logger.catch`.            |
| **Comments**      | Explain "why," not "what"; comment only for complex logic or rationale.              |

**Key Citations**

- [What’s New In Python 3.13](https://docs.python.org/3/whatsnew/3.13.html)
- [NumPy Docstring Style Guide](https://numpydoc.readthedocs.io/en/latest/format.html)
- [python-dotenv Package Documentation](https://pypi.org/project/python-dotenv/)
- [Loguru Logging Library Documentation](https://loguru.readthedocs.io/en/stable/)
- [PEP 585: Type Hinting Generics](https://peps.python.org/pep-0585/)
- [PEP 667: Consistent locals() Semantics](https://peps.python.org/pep-0667/)
