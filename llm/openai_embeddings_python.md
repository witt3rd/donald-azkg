<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Comprehensive Guide to OpenAI Python SDK for Text Embeddings

This guide provides a practical introduction to using the OpenAI Python SDK for generating text embeddings, covering essential setup steps, preferred models, implementation examples, and optimization strategies. Text embeddings are numerical representations of text that capture semantic meaning, enabling applications such as semantic search, document clustering, and recommendation systems. The OpenAI Python SDK offers a streamlined interface for accessing state-of-the-art embedding models, making it accessible for developers to integrate advanced natural language processing capabilities into their applications.

## Understanding the OpenAI Python SDK

The OpenAI Python SDK serves as a comprehensive library that facilitates seamless interaction with OpenAI's API services from Python applications[^1][^3]. This SDK abstracts the complexity of direct API calls, providing developers with an intuitive interface for accessing powerful AI models including embeddings, chat completions, and other language processing capabilities[^17]. The library is designed with production environments in mind, offering robust error handling, automatic retry mechanisms, and built-in authentication management that simplifies the development process significantly[^1].

The SDK follows modern Python development practices, supporting both synchronous and asynchronous operations, and provides comprehensive type hints for enhanced development experience[^1]. It automatically handles API key management from environment variables, reducing security risks associated with hardcoded credentials[^1]. The library's architecture allows for easy scaling from prototype to production, making it suitable for both experimental projects and enterprise-level applications[^17].

## Installation and Setup

### Installing Required Dependencies

Getting started with the OpenAI Python SDK requires installing the core library along with recommended dependencies for production-ready applications[^1][^2]:

```bash
pip install openai python-dotenv loguru tiktoken
```

For projects using virtual environments, which is considered a best practice, you should first create and activate your virtual environment before installation[^2]:

```bash
mkdir my_project
cd my_project
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install openai python-dotenv loguru tiktoken
```

### Environment Configuration

Create a `.env` file in your project root to securely manage configuration variables:

```bash
# .env
OPENAI_API_KEY=your_api_key_here
LOG_LEVEL=INFO
DEFAULT_MODEL=text-embedding-3-small
```

Add `.env` to your `.gitignore` file to prevent committing sensitive data:

```bash
# .gitignore
.env
*.log
__pycache__/
```

### Basic Setup Module

Create a configuration module that follows Python 3.13 best practices:

```python
"""Configuration and setup for OpenAI embeddings."""

import os
from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logger.add(
    "embeddings.log",
    level=os.getenv("LOG_LEVEL", "INFO"),
    rotation="10 MB",
    retention="10 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuration constants
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "text-embedding-3-small")
MAX_TOKENS = 8000
MAX_RETRIES = 3
```

## Preferred Embedding Models

### Current Model Landscape

OpenAI offers several embedding models, with the newest generation providing significant improvements in both performance and cost-effectiveness[^16]. The current model hierarchy includes:

- **text-embedding-3-large**: The most powerful model with 3,072 dimensions, offering superior performance for complex tasks[^6][^16]
- **text-embedding-3-small**: A highly efficient model with 1,536 dimensions, providing excellent performance-to-cost ratio[^6][^16]
- **text-embedding-ada-002**: The legacy model, still functional but superseded by the newer generation[^6][^15]

### Recommended Model Selection

For most applications, **text-embedding-3-small** represents the optimal choice, offering substantial improvements over the legacy ada-002 model while maintaining cost efficiency[^16]. According to benchmark comparisons, text-embedding-3-small achieves a 44.0% average score on the MIRACL benchmark compared to ada-002's 31.4%, representing a significant performance improvement[^16]. The model also provides better English task performance, with MTEB benchmark scores increasing from 61.0% to 62.3%[^16].

For applications requiring maximum performance and having sufficient computational resources, text-embedding-3-large offers superior capabilities with its larger dimensionality, though at a higher cost per token[^16]. The choice between these models should consider the specific requirements of your application, including accuracy needs, latency constraints, and budget considerations[^6].

## Implementation Examples

### Basic Embedding Generation

The fundamental pattern for generating embeddings involves creating an OpenAI client instance and calling the embeddings endpoint[^1][^5]:

```python
from openai import OpenAI
from loguru import logger

client = OpenAI()

@logger.catch
def get_embedding(text: str, model: str = DEFAULT_MODEL) -> list[float]:
    """Generate embedding for a single text input.

    Parameters
    ----------
    text : str
        Input text to generate embedding for.
    model : str, optional
        OpenAI embedding model to use, by default DEFAULT_MODEL.

    Returns
    -------
    list[float]
        Vector representation of the input text.

    Examples
    --------
    >>> embedding = get_embedding("Hello world")
    >>> len(embedding)
    1536
    """
    response = client.embeddings.create(input=text, model=model)
    logger.info(f"Generated embedding for text of length {len(text)}")
    return response.data[0].embedding

# Example usage
text = "The quick brown fox jumps over the lazy dog"
embedding = get_embedding(text)
logger.info(f"Embedding dimension: {len(embedding)}")
```

### Batch Processing Multiple Texts

For efficiency when processing multiple texts, the API supports batch operations that can handle multiple inputs in a single request[^5][^19]:

```python
@logger.catch
def get_multiple_embeddings(
    texts: list[str],
    model: str = DEFAULT_MODEL
) -> list[list[float]]:
    """Generate embeddings for multiple texts efficiently.

    Parameters
    ----------
    texts : list[str]
        List of input texts to generate embeddings for.
    model : str, optional
        OpenAI embedding model to use, by default DEFAULT_MODEL.

    Returns
    -------
    list[list[float]]
        List of vector representations for each input text.

    Examples
    --------
    >>> texts = ["Hello", "World", "Example"]
    >>> embeddings = get_multiple_embeddings(texts)
    >>> len(embeddings)
    3
    """
    response = client.embeddings.create(input=texts, model=model)
    logger.info(f"Generated {len(texts)} embeddings in batch")
    return [data.embedding for data in response.data]

# Example with multiple texts
texts = [
    "Machine learning is a subset of artificial intelligence",
    "Natural language processing enables computers to understand text",
    "Deep learning uses neural networks with multiple layers"
]

embeddings = get_multiple_embeddings(texts)
logger.info(f"Generated {len(embeddings)} embeddings")
```

### Advanced Configuration with Dimensions

The newer embedding models support dimension reduction, allowing you to trade off between performance and resource usage[^5][^16]:

```python
@logger.catch
def get_custom_embedding(
    text: str,
    model: str = DEFAULT_MODEL,
    dimensions: int | None = None
) -> list[float]:
    """Generate embedding with custom dimensions.

    Parameters
    ----------
    text : str
        Input text to generate embedding for.
    model : str, optional
        OpenAI embedding model to use, by default DEFAULT_MODEL.
    dimensions : int or None, optional
        Number of dimensions for the output embedding. If None,
        uses model default.

    Returns
    -------
    list[float]
        Vector representation with specified dimensions.

    Examples
    --------
    >>> embedding = get_custom_embedding("Test", dimensions=512)
    >>> len(embedding)
    512
    """
    params = {"input": text, "model": model}
    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)
    logger.info(f"Generated {len(response.data[0].embedding)}-dimensional embedding")
    return response.data[0].embedding

# Generate compact embedding for storage efficiency
compact_embedding = get_custom_embedding(
    "This is a test sentence",
    dimensions=512
)
logger.info(f"Custom embedding dimension: {len(compact_embedding)}")
```

## Best Practices and Optimization Tips

### Token Management and Limits

Understanding token limitations is crucial for effective embedding generation[^19]. All embedding models have a maximum input limit of 8,192 tokens, and any single request cannot exceed 300,000 tokens total across all inputs[^19]:

```python
import tiktoken

def count_tokens(text: str, model: str = DEFAULT_MODEL) -> int:
    """Count tokens in text for the specified model.

    Parameters
    ----------
    text : str
        Input text to count tokens for.
    model : str, optional
        Model to use for tokenization, by default DEFAULT_MODEL.

    Returns
    -------
    int
        Number of tokens in the text.

    Examples
    --------
    >>> count_tokens("Hello world")
    2
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def prepare_text_for_embedding(text: str, max_tokens: int = MAX_TOKENS) -> str:
    """Truncate text if it exceeds token limits.

    Parameters
    ----------
    text : str
        Input text to prepare.
    max_tokens : int, optional
        Maximum number of tokens allowed, by default MAX_TOKENS.

    Returns
    -------
    str
        Text truncated to fit within token limits.

    Examples
    --------
    >>> prepare_text_for_embedding("Very long text...", max_tokens=10)
    'Truncated text'
    """
    token_count = count_tokens(text)
    if token_count <= max_tokens:
        return text

    # Truncate while preserving word boundaries
    encoding = tiktoken.encoding_for_model(DEFAULT_MODEL)
    tokens = encoding.encode(text)
    truncated_tokens = tokens[:max_tokens]
    return encoding.decode(truncated_tokens)
```

### Text Preprocessing for Better Results

Proper text preprocessing can significantly improve embedding quality[^5][^15]:

```python
def preprocess_text(text: str) -> str:
    """Clean and prepare text for optimal embedding generation.

    Parameters
    ----------
    text : str
        Raw input text to preprocess.

    Returns
    -------
    str
        Cleaned and normalized text.

    Examples
    --------
    >>> preprocess_text("  Multiple   spaces\\n\\nand linebreaks  ")
    'Multiple spaces and linebreaks'
    """
    # Normalize whitespace and line breaks
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())
    return text.strip()

@logger.catch
def get_optimized_embedding(text: str, model: str = DEFAULT_MODEL) -> list[float]:
    """Generate embedding with preprocessing and optimization.

    Parameters
    ----------
    text : str
        Raw input text.
    model : str, optional
        OpenAI embedding model to use, by default DEFAULT_MODEL.

    Returns
    -------
    list[float]
        Optimized vector representation.

    Examples
    --------
    >>> embedding = get_optimized_embedding("  Messy   text\\n\\n")
    >>> len(embedding) > 0
    True
    """
    processed_text = preprocess_text(text)
    processed_text = prepare_text_for_embedding(processed_text)
    return get_embedding(processed_text, model)
```

### Performance and Cost Optimization

Several strategies can optimize both performance and cost when working with embeddings[^16][^6]:

**Dimension Optimization**: Use the dimensions parameter to reduce embedding size when full dimensionality isn't required[^16]. Research shows that text-embedding-3-large can be shortened to 256 dimensions while still outperforming full-sized ada-002 embeddings[^16].

**Batch Processing**: Process multiple texts in single API calls rather than individual requests to reduce latency and improve throughput[^5][^19].

**Caching Strategy**: Implement caching for frequently requested embeddings to avoid redundant API calls:

```python
import hashlib
import json

class EmbeddingCache:
    """Cache for storing and retrieving embeddings to reduce API calls."""

    def __init__(self) -> None:
        """Initialize empty cache."""
        self.cache: dict[str, list[float]] = {}

    def _get_cache_key(
        self,
        text: str,
        model: str,
        dimensions: int | None = None
    ) -> str:
        """Generate cache key for text and model parameters.

        Parameters
        ----------
        text : str
            Input text.
        model : str
            Model name.
        dimensions : int or None, optional
            Number of dimensions, by default None.

        Returns
        -------
        str
            MD5 hash for use as cache key.
        """
        key_data = {"text": text, "model": model, "dimensions": dimensions}
        return hashlib.md5(
            json.dumps(key_data, sort_keys=True).encode()
        ).hexdigest()

    @logger.catch
    def get_embedding_cached(
        self,
        text: str,
        model: str = DEFAULT_MODEL,
        dimensions: int | None = None
    ) -> list[float]:
        """Get embedding with caching support.

        Parameters
        ----------
        text : str
            Input text to generate embedding for.
        model : str, optional
            OpenAI embedding model to use, by default DEFAULT_MODEL.
        dimensions : int or None, optional
            Number of dimensions for output, by default None.

        Returns
        -------
        list[float]
            Cached or newly generated embedding vector.

        Examples
        --------
        >>> cache = EmbeddingCache()
        >>> embedding = cache.get_embedding_cached("Hello world")
        >>> len(embedding) > 0
        True
        """
        cache_key = self._get_cache_key(text, model, dimensions)

        if cache_key in self.cache:
            logger.debug("Cache hit for embedding")
            return self.cache[cache_key]

        # Generate new embedding
        params = {"input": text, "model": model}
        if dimensions is not None:
            params["dimensions"] = dimensions

        response = client.embeddings.create(**params)
        embedding = response.data[0].embedding

        # Cache the result
        self.cache[cache_key] = embedding
        logger.info(f"Cached new embedding with {len(embedding)} dimensions")
        return embedding
```

### Error Handling and Robustness

Implement proper error handling to manage API limitations and network issues[^12]:

```python
import time
from openai import RateLimitError, APIError

@logger.catch
def robust_get_embedding(
    text: str,
    model: str = DEFAULT_MODEL,
    max_retries: int = MAX_RETRIES
) -> list[float]:
    """Get embedding with retry logic and error handling.

    Parameters
    ----------
    text : str
        Input text to generate embedding for.
    model : str, optional
        OpenAI embedding model to use, by default DEFAULT_MODEL.
    max_retries : int, optional
        Maximum number of retry attempts, by default MAX_RETRIES.

    Returns
    -------
    list[float]
        Vector representation of input text.

    Raises
    ------
    Exception
        If all retry attempts fail.

    Examples
    --------
    >>> embedding = robust_get_embedding("Test text")
    >>> len(embedding) > 0
    True
    """
    for attempt in range(max_retries):
        try:
            response = client.embeddings.create(input=text, model=model)
            logger.info(f"Successfully generated embedding on attempt {attempt + 1}")
            return response.data[0].embedding

        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(f"Rate limit hit, waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            logger.error("Rate limit exceeded after all retries")
            raise

        except APIError as e:
            logger.error(f"API error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            raise

    raise Exception("Failed to get embedding after all retries")
```

### Complete Production Example

Here's a comprehensive example that combines all best practices:

```python
"""Production-ready OpenAI embeddings module."""

import os
import time
import hashlib
import json
from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI, RateLimitError, APIError
import tiktoken

# Load environment variables
load_dotenv()

# Configure logging
logger.add(
    "embeddings.log",
    level=os.getenv("LOG_LEVEL", "INFO"),
    rotation="10 MB",
    retention="10 days"
)

class ProductionEmbeddings:
    """Production-ready embeddings client with caching and error handling."""

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        max_tokens: int = 8000,
        max_retries: int = 3
    ) -> None:
        """Initialize embeddings client.

        Parameters
        ----------
        model : str, optional
            Default embedding model, by default "text-embedding-3-small".
        max_tokens : int, optional
            Maximum tokens per request, by default 8000.
        max_retries : int, optional
            Maximum retry attempts, by default 3.
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.cache: dict[str, list[float]] = {}

    @logger.catch
    def get_embedding(
        self,
        text: str,
        use_cache: bool = True,
        dimensions: int | None = None
    ) -> list[float]:
        """Generate embedding with full production features.

        Parameters
        ----------
        text : str
            Input text to generate embedding for.
        use_cache : bool, optional
            Whether to use caching, by default True.
        dimensions : int or None, optional
            Custom embedding dimensions, by default None.

        Returns
        -------
        list[float]
            Vector representation of input text.

        Examples
        --------
        >>> embedder = ProductionEmbeddings()
        >>> embedding = embedder.get_embedding("Hello world")
        >>> len(embedding) > 0
        True
        """
        # Preprocess and validate input
        processed_text = self._preprocess_text(text)
        processed_text = self._prepare_text_for_embedding(processed_text)

        # Check cache if enabled
        if use_cache:
            cache_key = self._get_cache_key(processed_text, dimensions)
            if cache_key in self.cache:
                logger.debug("Cache hit for embedding")
                return self.cache[cache_key]

        # Generate embedding with retry logic
        embedding = self._robust_get_embedding(processed_text, dimensions)

        # Cache result if enabled
        if use_cache:
            cache_key = self._get_cache_key(processed_text, dimensions)
            self.cache[cache_key] = embedding

        return embedding

    def _preprocess_text(self, text: str) -> str:
        """Clean and normalize input text."""
        text = text.replace('\n', ' ').replace('\r', ' ')
        return ' '.join(text.split()).strip()

    def _prepare_text_for_embedding(self, text: str) -> str:
        """Truncate text to fit within token limits."""
        encoding = tiktoken.encoding_for_model(self.model)
        tokens = encoding.encode(text)

        if len(tokens) <= self.max_tokens:
            return text

        truncated_tokens = tokens[:self.max_tokens]
        return encoding.decode(truncated_tokens)

    def _get_cache_key(self, text: str, dimensions: int | None) -> str:
        """Generate cache key for text and parameters."""
        key_data = {"text": text, "model": self.model, "dimensions": dimensions}
        return hashlib.md5(
            json.dumps(key_data, sort_keys=True).encode()
        ).hexdigest()

    def _robust_get_embedding(
        self,
        text: str,
        dimensions: int | None
    ) -> list[float]:
        """Generate embedding with retry logic."""
        for attempt in range(self.max_retries):
            try:
                params = {"input": text, "model": self.model}
                if dimensions is not None:
                    params["dimensions"] = dimensions

                response = self.client.embeddings.create(**params)
                return response.data[0].embedding

            except RateLimitError:
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Rate limit hit, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise

            except APIError as e:
                logger.error(f"API error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise

        raise Exception("Failed to get embedding after all retries")
```

## Conclusion

The OpenAI Python SDK provides a powerful and accessible interface for generating text embeddings that can enhance various natural language processing applications. By following the practices outlined in this guide—from proper setup and model selection to optimization strategies and error handling—developers can effectively integrate embedding capabilities into their projects. The combination of the efficient text-embedding-3-small model, proper preprocessing techniques, and thoughtful resource management creates a foundation for building robust, scalable applications that leverage the semantic understanding capabilities of modern embedding models.

<div style="text-align: center">⁂</div>

[^1]: https://platform.openai.com/docs/libraries

[^2]: https://openai.github.io/openai-agents-python/quickstart/

[^3]: https://www.newhorizons.com/resources/blog/the-complete-guide-for-using-the-openai-python-api

[^4]: https://stackoverflow.com/questions/77435356/openai-api-new-version-v1-of-the-openai-python-package-appears-to-contain-bre

[^5]: https://platform.openai.com/docs/guides/embeddings

[^6]: https://zilliz.com/ai-models/text-embedding-ada-002

[^7]: https://platform.openai.com/docs/guides/embeddings/embedding-models

[^8]: https://platform.openai.com/docs/guides/batch

[^9]: https://platform.openai.com/docs/api-reference?lang=python

[^10]: https://cheapwindowsvps.com/blog/step-by-step-guide-to-installing-python-openai-sdk-on-windows-and-macos/

[^11]: https://python.langchain.com/docs/integrations/text_embedding/openai/

[^12]: https://learn.microsoft.com/en-us/answers/questions/1525849/why-is-the-response-unstable-when-i-use-text-embed

[^13]: https://www.reddit.com/r/MachineLearning/comments/13aaj2w/d_is_openai_textembeddingada002_the_best/

[^14]: https://openai.github.io/openai-agents-python/

[^15]: https://www.educative.io/answers/how-to-generate-text-embeddings-with-openais-api-in-python

[^16]: https://openai.com/index/new-embedding-models-and-api-updates/

[^17]: https://www.byteplus.com/en/topic/415518

[^18]: https://www.datacamp.com/tutorial/introduction-to-text-embeddings-with-the-open-ai-api

[^19]: https://github.com/openai/openai-python/blob/main/src/openai/resources/embeddings.py

[^20]: https://stackoverflow.com/questions/77943395/openai-embeddings-api-how-to-extract-the-embedding-vector

[^21]: https://platform.openai.com/docs/api-reference/introduction?lang=python

[^22]: https://github.com/openai/openai-python

[^23]: https://platform.openai.com/docs/api-reference/embeddings/create

[^24]: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/embeddings

[^25]: https://www.timescale.com/blog/which-openai-embedding-model-is-best

[^26]: https://iamnotarobot.substack.com/p/should-you-use-openais-embeddings

[^27]: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-batch-model-openai-embeddings?view=azureml-api-2

[^28]: https://help.openai.com/en/articles/9197833-batch-api-faq

[^29]: https://community.openai.com/t/is-there-a-way-to-call-embeddings-batch-api-synchronously/886940

[^30]: https://community.openai.com/t/best-practice-for-writing-category-descriptions-for-embeddings/976489

[^31]: https://www.pinecone.io/learn/series/rag/embedding-models-rundown/

[^32]: https://www.reddit.com/r/OpenAI/comments/18p5kj5/embeddings_best_practices/

[^33]: https://community.openai.com/t/how-to-structure-the-embeddings/184576

[^34]: https://community.openai.com/t/best-practices-for-reliable-embeddings-pipeline/294985

[^35]: https://community.openai.com/t/embeddings-api-max-batch-size/655329

[^36]: https://stackoverflow.com/questions/74907244/how-can-i-use-batch-embeddings-using-openais-api

[^37]: https://www.pinecone.io/learn/openai-embeddings-v3/
