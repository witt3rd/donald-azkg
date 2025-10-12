---
tags: [python, programming, async, types, guide, best-practices]
---
# Python 3.13+ Coding Standards

## Core Language Standards

### Type Hints - Modern Python 3.13 Approach

**Use built-in types directly** - `typing.List`, `typing.Dict` are deprecated since Python 3.9:

```python
# ✅ Correct - Use built-in types
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# ❌ Avoid - Deprecated typing aliases
from typing import List, Dict
def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}
```

**Required type annotations:**

- All function parameters and return types
- Class attributes with non-obvious types
- Complex data structures
- Public API interfaces

### Documentation Standards - NumPy Style

**Use NumPy-style docstrings** for all functions, classes, and modules:

```python
def extract_transcript(video_id: str, languages: list[str] = None) -> dict[str, str]:
    """Extract transcript from a YouTube video.

    Parameters
    ----------
    video_id : str
        YouTube video identifier.
    languages : list[str], optional
        Preferred language codes in priority order.
        Defaults to ['en'] if not provided.

    Returns
    -------
    dict[str, str]
        Dictionary containing transcript text and metadata.

    Raises
    ------
    TranscriptNotAvailableError
        When no transcript is available for the video.
    APIQuotaExceededError
        When YouTube API quota is exceeded.

    Examples
    --------
    >>> transcript = extract_transcript("dQw4w9WgXcQ", ["en", "es"])
    >>> transcript["text"][:50]
    "Never gonna give you up, never gonna let you down"
    """
```

**Docstring requirements:**

- Keep lines under 70 characters for terminal readability
- Include all parameters with types and descriptions
- Document return values and types
- List possible exceptions
- Provide realistic examples
- Use present tense ("Extract transcript" not "Extracts transcript")

### Configuration Management

**Use `python-dotenv` for environment variables:**

```python
from dotenv import load_dotenv
import os

# Load at module level
load_dotenv()

# Access with defaults
api_key = os.getenv("OPENAI_API_KEY")
debug_mode = os.getenv("DEBUG", "False").lower() == "true"
max_tokens = int(os.getenv("MAX_TOKENS", "4000"))
```

**Configuration patterns:**

- Always use `.env` files for secrets and configuration
- Add `.env` to `.gitignore`
- Provide `.env.example` with dummy values
- Use `os.getenv()` with sensible defaults
- Convert environment strings to appropriate types

### Logging with Loguru

**Use `loguru` for all logging needs:**

```python
from loguru import logger

# Configure at application startup
logger.add("app.log", level="INFO", rotation="10 MB")
logger.add("debug.log", level="DEBUG", rotation="1 day")

# Use throughout application
@logger.catch
def risky_operation(data: dict[str, str]) -> str:
    """Process data with automatic exception logging."""
    logger.debug(f"Processing {len(data)} items")
    result = process_data(data)
    logger.info(f"Successfully processed data: {len(result)} chars")
    return result
```

**Logging standards:**

- Use `@logger.catch` for automatic exception handling
- Log at appropriate levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Include context in log messages (counts, IDs, relevant data)
- Configure file rotation and retention
- Use structured logging for complex data

### Error Handling Patterns

**Comprehensive error handling with context:**

```python
from loguru import logger
from typing import Optional

class TranscriptError(Exception):
    """Base exception for transcript operations."""
    pass

class TranscriptNotAvailableError(TranscriptError):
    """Raised when transcript is not available for a video."""
    pass

@logger.catch
def safe_extract_transcript(video_id: str) -> Optional[str]:
    """Extract transcript with comprehensive error handling.

    Parameters
    ----------
    video_id : str
        YouTube video identifier.

    Returns
    -------
    Optional[str]
        Transcript text or None if extraction fails.
    """
    try:
        transcript = extract_transcript(video_id)
        logger.info(f"Successfully extracted transcript for {video_id}")
        return transcript
    except TranscriptNotAvailableError:
        logger.warning(f"No transcript available for video {video_id}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error extracting transcript for {video_id}: {e}")
        raise TranscriptError(f"Failed to extract transcript: {e}") from e
```

## uv Workspace Standards

### Project Structure

**Follow uv workspace patterns for modular design:**

```
project-root/
├── pyproject.toml            # Workspace root
├── uv.lock                   # Shared lockfile
├── common/                   # Shared utilities
│   ├── pyproject.toml
│   └── src/common/
├── package1/                 # Feature package
│   ├── pyproject.toml
│   └── src/package1/
└── package2/                 # Feature package
    ├── pyproject.toml
    └── src/package2/
```

**Workspace root `pyproject.toml`:**

```toml
[tool.uv.workspace]
members = [
    "common",
    "transcript",
    "summarize",
    # Add new packages here
]

[tool.uv.sources]
common = { workspace = true }
```

**Package-level `pyproject.toml`:**

```toml
[project]
name = "transcript"
version = "0.1.0"
dependencies = [
    "common",
    "youtube-transcript-api>=0.6.0",
    "loguru>=0.7.0",
]

[tool.uv.sources]
common = { workspace = true }
```

### Command Patterns

**Use uv commands consistently:**

```bash
# Install/sync all workspace dependencies
uv sync

# Run specific package
uv run --package transcript yt-transcript VIDEO_ID

# Run with specific Python version
uv run --python 3.13 --package summarize summarize content.txt

# Add dependency to specific package
uv add --package transcript requests

# Development workflows
uv run pytest                    # Run tests
uv run mypy src/                # Type checking
uv run ruff check src/          # Linting
```

## Code Style and Comments

### Commenting Philosophy

**Comment only to explain "why," not "what":**

```python
# ✅ Good - Explains rationale
# Use dict for O(1) lookups to optimize repeated membership testing
cache = {}

# ✅ Good - Explains business logic
# YouTube API has strict rate limits, so we batch requests
batch_size = 50

# ❌ Avoid - States the obvious
# Create a dictionary
cache = {}

# ❌ Avoid - Historical comments
# TODO: Fix this later (use Git for history)
```

### Naming Conventions

**Use descriptive, clear names:**

```python
# ✅ Clear and descriptive
def extract_youtube_transcript(video_id: str) -> dict[str, str]:
    """Extract transcript from YouTube video."""

def calculate_content_similarity_score(text1: str, text2: str) -> float:
    """Calculate semantic similarity between two text passages."""

# ❌ Unclear abbreviations
def ext_yt_trans(vid: str) -> dict:
    """Extract transcript."""
```

### Import Organization

**Follow standard import ordering:**

```python
# Standard library imports
import os
import sys
from pathlib import Path
from typing import Optional

# Third-party imports
import click
from loguru import logger
from dotenv import load_dotenv

# Local imports
from common.config import get_api_key
from common.logger import setup_logging
from .extractor import YouTubeExtractor
```

## CLI Development Standards

### Click Framework Patterns

**Use Click for CLI interfaces with proper error handling:**

```python
import click
from loguru import logger
from typing import Optional

@click.command()
@click.argument("video_id")
@click.option("--languages", "-l", multiple=True, default=["en"],
              help="Language codes in priority order")
@click.option("--output", "-o", type=click.Path(),
              help="Output file path")
@click.option("--format", "output_format", type=click.Choice(["text", "json", "srt"]),
              default="text", help="Output format")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def extract_transcript(
    video_id: str,
    languages: tuple[str, ...],
    output: Optional[str],
    output_format: str,
    verbose: bool
) -> None:
    """Extract transcript from YouTube video.

    VIDEO_ID is the YouTube video identifier (e.g., 'dQw4w9WgXcQ').
    """
    if verbose:
        logger.add(sys.stderr, level="DEBUG")

    try:
        result = perform_extraction(video_id, list(languages), output_format)

        if output:
            Path(output).write_text(result, encoding="utf-8")
            logger.info(f"Transcript saved to {output}")
        else:
            click.echo(result)

    except Exception as e:
        logger.error(f"Failed to extract transcript: {e}")
        raise click.ClickException(f"Extraction failed: {e}")
```

## Testing Standards

### Test Structure with pytest

**Comprehensive test coverage following AAA pattern:**

```python
import pytest
from unittest.mock import Mock, patch
from pathlib import Path

from transcript.extractor import YouTubeExtractor
from transcript.exceptions import TranscriptNotAvailableError

class TestYouTubeExtractor:
    """Test suite for YouTube transcript extraction."""

    @pytest.fixture
    def extractor(self):
        """Create extractor instance for testing."""
        return YouTubeExtractor()

    @pytest.fixture
    def sample_transcript(self):
        """Sample transcript data for testing."""
        return [
            {"text": "Hello world", "start": 0.0, "duration": 2.0},
            {"text": "This is a test", "start": 2.0, "duration": 3.0},
        ]

    def test_extract_transcript_success(self, extractor, sample_transcript):
        """Test successful transcript extraction."""
        # Arrange
        video_id = "test_video_123"

        with patch("youtube_transcript_api.YouTubeTranscriptApi.get_transcript") as mock_get:
            mock_get.return_value = sample_transcript

            # Act
            result = extractor.extract_transcript(video_id)

            # Assert
            assert result["video_id"] == video_id
            assert "Hello world" in result["text"]
            assert len(result["segments"]) == 2
            mock_get.assert_called_once_with(video_id, languages=["en"])

    def test_extract_transcript_not_available(self, extractor):
        """Test handling of unavailable transcript."""
        # Arrange
        video_id = "no_transcript_video"

        with patch("youtube_transcript_api.YouTubeTranscriptApi.get_transcript") as mock_get:
            mock_get.side_effect = Exception("No transcript available")

            # Act & Assert
            with pytest.raises(TranscriptNotAvailableError):
                extractor.extract_transcript(video_id)
```

## Performance and Optimization

### Efficient Data Processing

**Use appropriate data structures and algorithms:**

```python
from collections import defaultdict, Counter
from typing import Iterator

def analyze_word_frequency(text: str) -> dict[str, int]:
    """Analyze word frequency using efficient Counter.

    Parameters
    ----------
    text : str
        Input text to analyze.

    Returns
    -------
    dict[str, int]
        Word frequency mapping.
    """
    # Use Counter for O(n) frequency counting
    words = text.lower().split()
    return dict(Counter(words))

def batch_process_videos(video_ids: list[str], batch_size: int = 10) -> Iterator[list[dict]]:
    """Process videos in batches to manage memory usage.

    Parameters
    ----------
    video_ids : list[str]
        List of video IDs to process.
    batch_size : int, default 10
        Number of videos to process per batch.

    Yields
    ------
    list[dict]
        Batch of processed video data.
    """
    for i in range(0, len(video_ids), batch_size):
        batch = video_ids[i:i + batch_size]
        yield [process_single_video(vid) for vid in batch]
```

## Security Standards

### Input Validation and Sanitization

**Validate all external inputs:**

```python
import re
from typing import Optional

def validate_youtube_video_id(video_id: str) -> str:
    """Validate and sanitize YouTube video ID.

    Parameters
    ----------
    video_id : str
        Raw video ID input.

    Returns
    -------
    str
        Validated video ID.

    Raises
    ------
    ValueError
        If video ID format is invalid.
    """
    if not video_id:
        raise ValueError("Video ID cannot be empty")

    # YouTube video IDs are 11 characters, alphanumeric plus _ and -
    pattern = r"^[a-zA-Z0-9_-]{11}$"
    if not re.match(pattern, video_id):
        raise ValueError(f"Invalid YouTube video ID format: {video_id}")

    return video_id

def sanitize_file_path(path: str, allowed_extensions: set[str]) -> Path:
    """Sanitize file path for safe file operations.

    Parameters
    ----------
    path : str
        Raw file path input.
    allowed_extensions : set[str]
        Set of allowed file extensions (e.g., {'.txt', '.json'}).

    Returns
    -------
    Path
        Sanitized Path object.

    Raises
    ------
    ValueError
        If path is invalid or extension not allowed.
    """
    file_path = Path(path).resolve()

    if file_path.suffix.lower() not in allowed_extensions:
        raise ValueError(f"File extension not allowed: {file_path.suffix}")

    return file_path
```

## Restrictions and Requirements

### What You MUST Do

- **Type hints**: Every function parameter and return value
- **Docstrings**: NumPy-style for all public functions and classes
- **Error handling**: Use `@logger.catch` and specific exception types
- **Configuration**: Use `python-dotenv` and environment variables
- **Logging**: Use `loguru` with appropriate levels and context
- **Testing**: Write pytest tests for all new functionality
- **Validation**: Sanitize and validate all external inputs

### What You MUST NOT Do

- **Never** use deprecated `typing.List`, `typing.Dict` etc.
- **Never** commit sensitive data like API keys to version control
- **Never** use bare `except:` clauses without specific exception handling
- **Never** ignore type checker warnings without justification
- **Never** write obvious comments that restate code
- **Never** modify `pyproject.toml` workspace configuration without approval
- **Never** install new dependencies without discussing alternatives

### Safe Operations (Auto-approve)

- Reading files for analysis
- Running tests (`uv run pytest`)
- Type checking (`uv run mypy`)
- Linting (`uv run ruff check`)
- Creating new modules following existing patterns
- Adding logging statements
- Writing documentation

### Require Approval

- Installing new dependencies (`uv add`)
- Modifying workspace configuration
- Changing API interfaces
- Adding new environment variables
- Modifying error handling patterns
- Creating new CLI commands

## Development Workflow

### Standard Development Process

1. **Analyze requirements** and existing code patterns
2. **Propose implementation plan** with file changes
3. **Wait for approval** before making changes
4. **Implement** following all coding standards
5. **Add comprehensive tests** with good coverage
6. **Run quality checks** (tests, types, linting)
7. **Update documentation** if needed

### Quality Assurance Commands

```bash
# Run full quality check suite
uv run pytest --cov=src/
uv run mypy src/
uv run ruff check src/
uv run ruff format src/

# Package-specific checks
uv run --package transcript pytest
uv run --package summarize mypy src/
```

This comprehensive guide ensures high-quality, maintainable Python code that follows modern best practices and integrates seamlessly with the uv workspace architecture.

## Related Concepts

### Related Topics
- [[python_role]] - Role-specific guidance applies Python standards
- [[typescript]] - Alternative language with similar async patterns
- [[cpp_spec]] - C++23 formatting inspired by Python f-strings
- [[onnx_runtime]] - ONNX Runtime available for Python
- [[python3_13]] - Shares Python 3.13 coding standards content
- [[uv]] - uv is used for Python workspace management
- [[tenacity]] - Tenacity is a Python library following Python best practices
- [[click_repl]] - click-repl is a Python CLI library
- [[bayes_theory]] - Python tools (PyMC, Stan) used for Bayesian inference
- [[type_theory]] - Python 3.13+ uses type hints based on type theory principles
- [[chromadb]] - ChromaDB provides Python SDK
- [[firecrawl]] - Firecrawl provides Python SDK
- [[marker]] - Marker provides Python SDK
- [[numpy_pytorch_rust_guide]] - NumPy and PyTorch are Python libraries

### Extended By
- [[python_role]] - Role applies Python standards to specific context
- [[python3_13]] - Specific Python 3.13 features and enhancements
- [[python_mcp_sdk]] - MCP SDK uses Python for implementation
- [[openai_embeddings_python]] - Need Python knowledge to use OpenAI Python SDK
- [[openai_responses_python]] - Need Python knowledge to use OpenAI Python SDK
- [[openrouter_openai_python_sdk]] - Need Python knowledge to use SDK
- [[youtube_transcript_api]] - Need Python knowledge to use YouTube Transcript API
- [[type_theory]] - Python type hints are practical application of type theory
- [[numpy_pytorch_rust_guide]] - Need Python knowledge for NumPy/PyTorch sections

### Alternatives
- [[typescript]] - TypeScript alternative for similar use cases
- [[dotnet]] - .NET/C# alternative for development
