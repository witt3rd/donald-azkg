---
tags: [api, best-practices, python]
---

# Best Practices for Using Tenacity in Python

## Overview

Tenacity is a Python library for retrying operations with configurable strategies, ideal for handling transient failures. Below are best practices for effective use.

## Installation

Install via pip:

```bash
pip install tenacity
```

## Core Best Practices

### 1. Use Decorators for Simplicity

Apply the `@retry` decorator to functions for clean, reusable retry logic:

```python
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_data():
    # API call or operation
    pass
```

### 2. Choose Appropriate Stop Conditions

Define when to stop retrying to avoid infinite loops:

- `stop_after_attempt(n)`: Stop after `n` attempts.
- `stop_after_delay(seconds)`: Stop after a total delay.
- Combine with `stop_any` or `stop_all`:

```python
from tenacity import stop_any, stop_after_attempt, stop_after_delay

@retry(stop=stop_any(stop_after_attempt(5), stop_after_delay(30)))
def operation():
    pass
```

### 3. Implement Backoff Strategies

Use exponential backoff to reduce load on systems:

- `wait_exponential(multiplier=1, min=1, max=10)`: Delays grow exponentially (e.g., 1s, 2s, 4s), capped at `max`.
- `wait_random_exponential(min=1, max=10)`: Adds jitter to prevent thundering herd.
  Example:

```python
from tenacity import wait_exponential

@retry(wait=wait_exponential(multiplier=1, min=2, max=60))
def connect_to_service():
    pass
```

### 4. Specify Retry Conditions

Retry only on specific exceptions to avoid masking unrelated errors:

```python
from tenacity import retry_if_exception_type
import requests

@retry(retry=retry_if_exception_type(requests.ConnectionError))
def make_request():
    response = requests.get("https://api.example.com")
    response.raise_for_status()
    return response
```

### 5. Log Retry Attempts

Use `after` callbacks to log retries for debugging:

```python
from tenacity import after_log
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@retry(after=after_log(logger, logging.INFO))
def risky_operation():
    pass
```

### 6. Handle Results Conditionally

Retry based on result conditions with `retry_if_result`:

```python
from tenacity import retry_if_result

def is_failed(result):
    return result.get("status") == "failed"

@retry(retry=retry_if_result(is_failed))
def poll_status():
    return {"status": "failed"}  # Example
```

### 7. Use Async Support

For async functions, use `@retry` with async/await:

```python
import asyncio
from tenacity import retry, AsyncRetrying

@retry(stop=stop_after_attempt(3))
async def async_operation():
    await asyncio.sleep(1)
    raise ValueError("Failed")

# Manual retry for more control
async def manual_retry():
    async for attempt in AsyncRetrying(stop=stop_after_attempt(3)):
        with attempt:
            await async_operation()
```

### 8. Avoid Over-Retrying

- Set reasonable attempt limits (e.g., 3–5).
- Use `max` in `wait_exponential` to cap delays.
- Monitor performance to avoid excessive delays.

### 9. Test Retry Logic

Simulate failures in tests to ensure retry behavior:

```python
import pytest
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(2))
def flaky_function(counter=[0]):
    counter[0] += 1
    if counter[0] < 2:
        raise ValueError("Not yet")
    return "Success"

def test_retry():
    result = flaky_function()
    assert result == "Success"
    assert flaky_function.__closure__[0].cell_contents[0] == 2
```

### 10. Combine with Context Managers

For manual control, use `Retrying` or `AsyncRetrying`:

```python
from tenacity import Retrying, stop_after_attempt

def complex_operation():
    for attempt in Retrying(stop=stop_after_attempt(3)):
        with attempt:
            # Custom logic
            pass
```

## Advanced Tips

- **Thread Safety**: Tenacity is thread-safe, but ensure your operation is too.
- **Custom Callbacks**: Use `before`, `after`, or `retry_error_callback` for custom behavior.
- **Metrics**: Track retry metrics (e.g., attempts, duration) for observability.
- **Documentation**: Review Tenacity’s API docs for advanced features like `wait_chain`.

## Common Pitfalls to Avoid

- **Catching All Exceptions**: Always specify exception types to avoid masking bugs.
- **Infinite Retries**: Always set a `stop` condition.
- **Ignoring Performance**: Monitor retry impact on system load and latency.
- **Not Testing**: Unverified retry logic can fail silently in production.

## Example: Comprehensive Setup

```python
import logging
import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    after_log,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((requests.ConnectionError, requests.Timeout)),
    after=after_log(logger, logging.INFO),
)
def robust_request(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
```

## Related Concepts

### Related Topics
- [[python_coding_standards]] - Tenacity is a Python library following Python best practices