<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# ChromaDB Python SDK: Comprehensive Guide for Text Embeddings

ChromaDB has emerged as a leading open-source vector database specifically designed for building applications with long-term memory capabilities using embeddings[^1]. This comprehensive guide explores the ChromaDB Python SDK, covering fundamental concepts, practical implementation strategies, and optimization techniques for creating and managing text embeddings. The platform distinguishes itself through its simplicity, offering a core API with just four essential functions while supporting both in-memory prototyping and persistent storage solutions[^1]. Whether you're building retrieval-augmented generation systems, semantic search applications, or any LLM-powered solution requiring vector similarity search, ChromaDB provides the infrastructure to efficiently store, query, and manage embedding vectors at scale.

## Understanding ChromaDB and Core Concepts

ChromaDB represents a specialized vector database engineered to handle the unique requirements of embedding-based applications[^5]. At its foundation, the platform manages vector embeddings—numerical representations of data that capture semantic relationships and enable similarity-based operations[^11]. The database architecture follows a hierarchical structure consisting of tenants, databases, collections, and documents, where tenants represent logical groupings for organizations or users, databases model individual applications or projects, and collections serve as the primary mechanism for grouping embeddings, documents, and metadata[^11].

The concept of documents within ChromaDB differs from traditional file-based systems. Here, documents refer to chunks of text that fit within an embedding model's context window, making them the fundamental units for vector generation and retrieval[^11]. Each document can be associated with metadata—key-value pairs supporting strings, integers, floats, and booleans—which enables sophisticated filtering and organization capabilities[^11]. The system supports multiple distance functions including cosine similarity for text applications, Euclidean distance for noise-sensitive scenarios, and inner product for recommendation systems[^11].

Embedding functions serve as the bridge between raw text and vector representations, providing consistent interfaces for generating embeddings from documents or queries[^11]. ChromaDB supports various embedding approaches, from built-in functions utilizing pre-trained models to custom implementations that accommodate specific domain requirements or external embedding services[^3]. This flexibility allows developers to choose the most appropriate embedding strategy for their particular use case while maintaining consistent API interactions.

## Installation and Environment Setup

ChromaDB installation involves two primary packages designed for different deployment scenarios[^12]. The core `chromadb` package provides full database functionality suitable for local development and testing, while the `chromadb-client` package offers a lightweight client for interacting with remote ChromaDB instances[^12]. Installation can be accomplished through multiple methods, including direct PyPI installation, GitHub repository cloning, or specific version targeting for compatibility requirements[^12].

```python
# Basic installation
pip install chromadb python-dotenv loguru

# For client-only functionality
pip install chromadb-client python-dotenv loguru

# Installing specific versions
pip install chromadb==0.5.0

# Installing from development branch
pip install git+https://github.com/chroma-core/chroma.git@main
```

The installation process requires consideration of backward compatibility, as certain releases introduce breaking changes and irreversible database migrations[^12]. For production environments, careful version management ensures application stability and prevents compatibility issues during updates[^12]. Additionally, ChromaDB offers JavaScript and TypeScript client packages for cross-language integration scenarios[^12].

Environment configuration involves setting up persistent storage and client connections. The platform supports both in-memory operations for rapid prototyping and persistent storage for production applications[^13]. Configuration parameters include database implementation backends, persistence directories, and various client settings that optimize performance for specific deployment scenarios[^13].

## Getting Started with Basic Operations

ChromaDB operations begin with client initialization and collection management[^1]. The core workflow involves creating a client instance, establishing collections with appropriate embedding functions, adding documents with their associated embeddings, and performing similarity-based queries[^1]. This fundamental pattern scales from simple prototypes to complex production systems while maintaining consistent API interactions.

```python
"""ChromaDB basic operations with Python 3.13 best practices."""

import os
from dotenv import load_dotenv
from loguru import logger
import chromadb
from chromadb.utils import embedding_functions
from chromadb.api.models.Collection import Collection

# Load environment variables
load_dotenv()

def initialize_chroma_client() -> chromadb.Client:
    """Initialize ChromaDB client with configuration.

    Returns
    -------
    chromadb.Client
        Configured ChromaDB client instance.

    Examples
    --------
    >>> client = initialize_chroma_client()
    >>> isinstance(client, chromadb.Client)
    True
    """
    persist_directory = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    logger.info(f"Initializing ChromaDB client with persistence: {persist_directory}")

    return chromadb.PersistentClient(path=persist_directory)

def create_document_collection(
    client: chromadb.Client,
    collection_name: str,
    embedding_model: str = "all-MiniLM-L6-v2"
) -> Collection:
    """Create or retrieve a document collection with embedding function.

    Parameters
    ----------
    client : chromadb.Client
        ChromaDB client instance.
    collection_name : str
        Name for the collection.
    embedding_model : str, optional
        Name of the sentence transformer model, by default "all-MiniLM-L6-v2".

    Returns
    -------
    Collection
        ChromaDB collection instance.

    Examples
    --------
    >>> client = initialize_chroma_client()
    >>> collection = create_document_collection(client, "test-docs")
    >>> collection.name == "test-docs"
    True
    """
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=embedding_model
    )

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )

    logger.info(f"Created collection '{collection_name}' with model '{embedding_model}'")
    return collection

@logger.catch
def add_documents_to_collection(
    collection: Collection,
    documents: list[str],
    metadatas: list[dict[str, str | int | float | bool]] | None = None,
    ids: list[str] | None = None
) -> None:
    """Add documents to a ChromaDB collection.

    Parameters
    ----------
    collection : Collection
        ChromaDB collection to add documents to.
    documents : list[str]
        List of document texts to add.
    metadatas : list[dict[str, str | int | float | bool]] | None, optional
        List of metadata dictionaries for each document, by default None.
    ids : list[str] | None, optional
        List of unique identifiers for documents, by default None.

    Examples
    --------
    >>> client = initialize_chroma_client()
    >>> collection = create_document_collection(client, "test")
    >>> docs = ["First document", "Second document"]
    >>> add_documents_to_collection(collection, docs)
    """
    if ids is None:
        ids = [f"doc-{i}" for i in range(len(documents))]

    if metadatas is None:
        metadatas = [{"source": "api"} for _ in documents]

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    logger.info(f"Added {len(documents)} documents to collection '{collection.name}'")

def query_collection(
    collection: Collection,
    query_texts: list[str],
    n_results: int = 5,
    where: dict | None = None,
    where_document: dict | None = None
) -> dict:
    """Query a ChromaDB collection for similar documents.

    Parameters
    ----------
    collection : Collection
        ChromaDB collection to query.
    query_texts : list[str]
        List of query texts for similarity search.
    n_results : int, optional
        Maximum number of results to return, by default 5.
    where : dict | None, optional
        Metadata filter conditions, by default None.
    where_document : dict | None, optional
        Document content filter conditions, by default None.

    Returns
    -------
    dict
        Query results containing documents, distances, and metadata.

    Examples
    --------
    >>> client = initialize_chroma_client()
    >>> collection = create_document_collection(client, "test")
    >>> results = query_collection(collection, ["search query"])
    >>> "documents" in results
    True
    """
    logger.debug(f"Querying collection '{collection.name}' with {len(query_texts)} queries")

    results = collection.query(
        query_texts=query_texts,
        n_results=n_results,
        where=where,
        where_document=where_document
    )

    logger.info(f"Query returned {len(results['documents'][0])} results")
    return results

# Example usage
if __name__ == "__main__":
    logger.add("chromadb.log", level="INFO", rotation="10 MB")

    # Initialize client and collection
    client = initialize_chroma_client()
    collection = create_document_collection(client, "my-documents")

    # Add sample documents
    sample_docs = [
        "This is the first document about machine learning",
        "Here is another document discussing natural language processing",
        "A third document covering vector databases and embeddings"
    ]

    sample_metadata = [
        {"category": "ml", "priority": 1},
        {"category": "nlp", "priority": 2},
        {"category": "vectordb", "priority": 3}
    ]

    add_documents_to_collection(collection, sample_docs, sample_metadata)

    # Query the collection
    results = query_collection(
        collection,
        ["Find documents about artificial intelligence"],
        n_results=2
    )

    logger.info(f"Query results: {results}")
```

Collection management extends beyond basic creation to include retrieval, updating, and deletion operations[^2]. The `get_collection`, `get_or_create_collection`, and `delete_collection` methods provide comprehensive collection lifecycle management[^1]. These operations support various metadata filtering and document-based filtering capabilities, enabling precise control over data retrieval and manipulation[^7].

Document operations support both individual and batch processing patterns[^2]. The `add` method accommodates documents, embeddings, metadata, and unique identifiers, while `update` and `delete` methods enable dynamic content management[^2]. For large-scale operations, ChromaDB provides batching utilities that respect database limitations while optimizing throughput[^8].

## Embedding Function Strategies

ChromaDB supports multiple embedding function approaches, each suited to different requirements and deployment scenarios[^3]. The default embedding functions provide immediate functionality using pre-trained models, while custom implementations enable domain-specific optimizations or integration with external embedding services[^3]. Understanding these options allows developers to select the most appropriate strategy for their specific use cases.

Default embedding functions include sentence transformers, OpenAI embeddings, and ONNX-based implementations[^1][^16][^20]. These functions handle tokenization, embedding generation, and indexing automatically, reducing implementation complexity while providing robust performance[^1]. The sentence transformer implementation supports GPU acceleration for improved throughput in high-volume scenarios[^20].

```python
"""Advanced embedding function strategies for ChromaDB."""

import os
from typing import Any
from dotenv import load_dotenv
from loguru import logger
from chromadb.utils import embedding_functions
from chromadb.api.types import EmbeddingFunction, Documents
import chromadb

load_dotenv()

class CustomEmbeddingFunction(EmbeddingFunction[Documents]):
    """Custom embedding function implementing domain-specific logic.

    This example demonstrates how to create custom embedding functions
    for specialized use cases or integration with external services.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        """Initialize custom embedding function.

        Parameters
        ----------
        model_name : str, optional
            Name of the underlying model, by default "all-MiniLM-L6-v2".
        """
        self.model_name = model_name
        logger.info(f"Initialized custom embedding function with model: {model_name}")

    def __call__(self, input: Documents) -> list[list[float]]:
        """Generate embeddings for input documents.

        Parameters
        ----------
        input : Documents
            Documents to generate embeddings for.

        Returns
        -------
        list[list[float]]
            List of embedding vectors.
        """
        # Custom preprocessing logic here
        processed_docs = [doc.lower().strip() for doc in input]

        # Use sentence transformer for actual embedding generation
        sentence_transformer = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.model_name
        )

        embeddings = sentence_transformer(processed_docs)
        logger.debug(f"Generated embeddings for {len(input)} documents")

        return embeddings

def create_sentence_transformer_collection(
    client: chromadb.Client,
    collection_name: str,
    model_name: str = "all-MiniLM-L6-v2",
    device: str = "cpu"
) -> chromadb.Collection:
    """Create collection with sentence transformer embedding function.

    Parameters
    ----------
    client : chromadb.Client
        ChromaDB client instance.
    collection_name : str
        Name for the collection.
    model_name : str, optional
        Sentence transformer model name, by default "all-MiniLM-L6-v2".
    device : str, optional
        Device for model execution ('cpu' or 'cuda'), by default "cpu".

    Returns
    -------
    chromadb.Collection
        Collection with sentence transformer embeddings.

    Examples
    --------
    >>> client = chromadb.Client()
    >>> collection = create_sentence_transformer_collection(client, "st-docs")
    >>> collection.name == "st-docs"
    True
    """
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=model_name,
        device=device
    )

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )

    logger.info(f"Created collection '{collection_name}' with {model_name} on {device}")
    return collection

def create_openai_collection(
    client: chromadb.Client,
    collection_name: str,
    model_name: str = "text-embedding-3-large"
) -> chromadb.Collection:
    """Create collection with OpenAI embedding function.

    Parameters
    ----------
    client : chromadb.Client
        ChromaDB client instance.
    collection_name : str
        Name for the collection.
    model_name : str, optional
        OpenAI embedding model name, by default "text-embedding-3-large".

    Returns
    -------
    chromadb.Collection
        Collection with OpenAI embeddings.

    Examples
    --------
    >>> client = chromadb.Client()
    >>> collection = create_openai_collection(client, "openai-docs")
    >>> collection.name == "openai-docs"
    True
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name=model_name
    )

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )

    logger.info(f"Created collection '{collection_name}' with OpenAI {model_name}")
    return collection

def create_custom_collection(
    client: chromadb.Client,
    collection_name: str,
    custom_function: EmbeddingFunction[Documents]
) -> chromadb.Collection:
    """Create collection with custom embedding function.

    Parameters
    ----------
    client : chromadb.Client
        ChromaDB client instance.
    collection_name : str
        Name for the collection.
    custom_function : EmbeddingFunction[Documents]
        Custom embedding function implementation.

    Returns
    -------
    chromadb.Collection
        Collection with custom embeddings.

    Examples
    --------
    >>> client = chromadb.Client()
    >>> custom_ef = CustomEmbeddingFunction()
    >>> collection = create_custom_collection(client, "custom-docs", custom_ef)
    >>> collection.name == "custom-docs"
    True
    """
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=custom_function
    )

    logger.info(f"Created collection '{collection_name}' with custom embedding function")
    return collection

@logger.catch
def add_precomputed_embeddings(
    collection: chromadb.Collection,
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict[str, Any]] | None = None,
    ids: list[str] | None = None
) -> None:
    """Add documents with precomputed embeddings to collection.

    Parameters
    ----------
    collection : chromadb.Collection
        Target collection for documents.
    documents : list[str]
        Document texts.
    embeddings : list[list[float]]
        Precomputed embedding vectors.
    metadatas : list[dict[str, Any]] | None, optional
        Document metadata, by default None.
    ids : list[str] | None, optional
        Document identifiers, by default None.

    Examples
    --------
    >>> collection = chromadb.Client().create_collection("test")
    >>> docs = ["test doc"]
    >>> embeddings = [[0.1, 0.2, 0.3]]
    >>> add_precomputed_embeddings(collection, docs, embeddings)
    """
    if ids is None:
        ids = [f"precomputed-{i}" for i in range(len(documents))]

    if metadatas is None:
        metadatas = [{"source": "precomputed"} for _ in documents]

    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    logger.info(f"Added {len(documents)} documents with precomputed embeddings")

# Example usage comparing embedding strategies
if __name__ == "__main__":
    logger.add("embedding_strategies.log", level="INFO", rotation="10 MB")

    client = chromadb.Client()

    # Create collections with different embedding strategies
    st_collection = create_sentence_transformer_collection(
        client, "sentence-transformer", "all-MiniLM-L6-v2"
    )

    # Only create OpenAI collection if API key is available
    if os.getenv("OPENAI_API_KEY"):
        openai_collection = create_openai_collection(client, "openai-embeddings")

    custom_ef = CustomEmbeddingFunction()
    custom_collection = create_custom_collection(client, "custom-embeddings", custom_ef)

    # Test documents
    test_docs = [
        "Machine learning algorithms process data efficiently",
        "Natural language processing enables text understanding",
        "Vector databases store high-dimensional embeddings"
    ]

    # Add documents to sentence transformer collection
    st_collection.add(
        documents=test_docs,
        ids=[f"st-{i}" for i in range(len(test_docs))]
    )

    logger.info("Embedding strategy comparison complete")
```

Custom embedding functions require implementing the `EmbeddingFunction` interface, enabling integration with proprietary models or specialized embedding services[^3]. This approach provides maximum flexibility for organizations with specific embedding requirements or existing model infrastructure[^14]. The implementation involves creating a class that inherits from `EmbeddingFunction[Documents]` and implements the required methods for embedding generation[^3].

For scenarios involving pre-computed embeddings, ChromaDB supports direct embedding insertion without requiring embedding function execution[^14][^18]. This capability enables integration with external embedding pipelines or batch processing workflows where embeddings are generated separately from storage operations[^14].

## Advanced Querying and Filtering

ChromaDB provides sophisticated querying capabilities that extend beyond basic similarity search to include metadata filtering, document content filtering, and complex boolean operations[^7]. These features enable precise data retrieval and support complex application requirements while maintaining query performance at scale.

Metadata filtering utilizes a MongoDB-style query syntax supporting equality, inequality, range, and inclusion operations[^7]. The filtering system accommodates nested boolean logic through `$and` and `$or` operators, enabling complex query conditions that combine multiple metadata criteria[^7]. This functionality proves essential for multi-tenant applications or scenarios requiring fine-grained access control.

```python
"""Advanced querying and filtering patterns for ChromaDB."""

import os
from typing import Any
from dotenv import load_dotenv
from loguru import logger
from chromadb.api.models.Collection import Collection
import chromadb

load_dotenv()

def execute_metadata_query(
    collection: Collection,
    query_texts: list[str],
    metadata_filters: dict[str, Any],
    n_results: int = 5
) -> dict:
    """Execute query with metadata filtering.

    Parameters
    ----------
    collection : Collection
        ChromaDB collection to query.
    query_texts : list[str]
        Query texts for similarity search.
    metadata_filters : dict[str, Any]
        MongoDB-style metadata filter conditions.
    n_results : int, optional
        Maximum results to return, by default 5.

    Returns
    -------
    dict
        Query results with documents, distances, and metadata.

    Examples
    --------
    >>> collection = chromadb.Client().create_collection("test")
    >>> filters = {"category": "technical"}
    >>> results = execute_metadata_query(collection, ["query"], filters)
    >>> "documents" in results
    True
    """
    logger.debug(f"Executing metadata query with filters: {metadata_filters}")

    results = collection.query(
        query_texts=query_texts,
        where=metadata_filters,
        n_results=n_results
    )

    total_results = len(results['documents'][0]) if results['documents'] else 0
    logger.info(f"Metadata query returned {total_results} results")

    return results

def execute_content_query(
    collection: Collection,
    query_texts: list[str],
    content_filters: dict[str, Any],
    n_results: int = 5
) -> dict:
    """Execute query with document content filtering.

    Parameters
    ----------
    collection : Collection
        ChromaDB collection to query.
    query_texts : list[str]
        Query texts for similarity search.
    content_filters : dict[str, Any]
        Document content filter conditions.
    n_results : int, optional
        Maximum results to return, by default 5.

    Returns
    -------
    dict
        Query results filtered by document content.

    Examples
    --------
    >>> collection = chromadb.Client().create_collection("test")
    >>> filters = {"$contains": "important"}
    >>> results = execute_content_query(collection, ["query"], filters)
    >>> "documents" in results
    True
    """
    logger.debug(f"Executing content query with filters: {content_filters}")

    results = collection.query(
        query_texts=query_texts,
        where_document=content_filters,
        n_results=n_results
    )

    total_results = len(results['documents'][0]) if results['documents'] else 0
    logger.info(f"Content query returned {total_results} results")

    return results

def execute_complex_query(
    collection: Collection,
    query_texts: list[str],
    metadata_filters: dict[str, Any] | None = None,
    content_filters: dict[str, Any] | None = None,
    n_results: int = 10
) -> dict:
    """Execute complex query combining metadata and content filtering.

    Parameters
    ----------
    collection : Collection
        ChromaDB collection to query.
    query_texts : list[str]
        Query texts for similarity search.
    metadata_filters : dict[str, Any] | None, optional
        Metadata filter conditions, by default None.
    content_filters : dict[str, Any] | None, optional
        Content filter conditions, by default None.
    n_results : int, optional
        Maximum results to return, by default 10.

    Returns
    -------
    dict
        Query results with combined filtering.

    Examples
    --------
    >>> collection = chromadb.Client().create_collection("test")
    >>> meta_filters = {"priority": {"$gte": 3}}
    >>> content_filters = {"$contains": "machine learning"}
    >>> results = execute_complex_query(collection, ["AI"], meta_filters, content_filters)
    >>> "documents" in results
    True
    """
    logger.debug("Executing complex query with metadata and content filters")

    results = collection.query(
        query_texts=query_texts,
        where=metadata_filters,
        where_document=content_filters,
        n_results=n_results
    )

    total_results = len(results['documents'][0]) if results['documents'] else 0
    logger.info(f"Complex query returned {total_results} results")

    return results

def demonstrate_filter_patterns(collection: Collection) -> None:
    """Demonstrate various filtering patterns with ChromaDB.

    Parameters
    ----------
    collection : Collection
        Collection to demonstrate filtering patterns with.

    Examples
    --------
    >>> collection = chromadb.Client().create_collection("demo")
    >>> demonstrate_filter_patterns(collection)
    """
    query_text = ["machine learning applications"]

    # Equality filtering
    logger.info("=== Equality Filtering ===")
    equality_results = execute_metadata_query(
        collection, query_text, {"category": "technical"}
    )

    # Range filtering
    logger.info("=== Range Filtering ===")
    range_results = execute_metadata_query(
        collection, query_text, {"priority": {"$gte": 3}}
    )

    # Boolean logic filtering
    logger.info("=== Boolean Logic Filtering ===")
    boolean_results = execute_metadata_query(
        collection,
        query_text,
        {
            "$and": [
                {"category": "technical"},
                {"priority": {"$lte": 5}}
            ]
        }
    )

    # Inclusion filtering
    logger.info("=== Inclusion Filtering ===")
    inclusion_results = execute_metadata_query(
        collection,
        query_text,
        {"status": {"$in": ["active", "pending"]}}
    )

    # Content filtering
    logger.info("=== Content Filtering ===")
    content_results = execute_content_query(
        collection, query_text, {"$contains": "algorithm"}
    )

    # Combined filtering
    logger.info("=== Combined Filtering ===")
    combined_results = execute_complex_query(
        collection,
        query_text,
        metadata_filters={"category": "technical"},
        content_filters={"$contains": "deep learning"}
    )

    logger.info("Filter pattern demonstration complete")

@logger.catch
def setup_demo_collection() -> Collection:
    """Set up demonstration collection with sample data.

    Returns
    -------
    Collection
        Collection populated with sample documents for filtering demos.
    """
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="filter-demo")

    # Sample documents with varied metadata
    documents = [
        "Machine learning algorithms enable pattern recognition in large datasets",
        "Deep learning neural networks process complex hierarchical features",
        "Natural language processing transforms text into structured information",
        "Computer vision systems interpret visual data for autonomous vehicles",
        "Reinforcement learning agents optimize decision-making strategies"
    ]

    metadatas = [
        {"category": "technical", "priority": 5, "status": "active"},
        {"category": "technical", "priority": 4, "status": "pending"},
        {"category": "research", "priority": 3, "status": "active"},
        {"category": "application", "priority": 2, "status": "completed"},
        {"category": "research", "priority": 1, "status": "active"}
    ]

    ids = [f"demo-{i}" for i in range(len(documents))]

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    logger.info(f"Set up demo collection with {len(documents)} documents")
    return collection

# Example usage of advanced querying
if __name__ == "__main__":
    logger.add("advanced_querying.log", level="INFO", rotation="10 MB")

    # Set up demonstration collection
    demo_collection = setup_demo_collection()

    # Run filtering demonstrations
    demonstrate_filter_patterns(demo_collection)

    logger.info("Advanced querying demonstration complete")
```

Document filtering operates on text content rather than metadata, enabling searches based on document content patterns[^7]. This capability complements metadata filtering and embedding similarity to provide comprehensive query flexibility. The combination of these filtering mechanisms supports complex retrieval scenarios while maintaining query performance through optimized indexing strategies.

Range queries and numerical filtering support various comparison operators including greater than, less than, and inclusion tests[^7]. These operations enable time-based queries, priority-based filtering, and other numerical criteria that enhance application functionality beyond simple similarity search.

## Performance Optimization and Best Practices

ChromaDB performance optimization encompasses several key areas including embedding function selection, batch processing strategies, storage configuration, and query optimization techniques[^8][^20]. Understanding these optimization opportunities enables applications to scale effectively while maintaining responsive user experiences.

Embedding function performance varies significantly based on implementation and hardware configuration[^20]. GPU-accelerated sentence transformers typically outperform ONNX implementations for large-scale operations, with performance differences measured in orders of magnitude for substantial document volumes[^20]. The choice between local and remote embedding services involves balancing latency, throughput, and operational complexity considerations.

```python
"""Performance optimization strategies for ChromaDB applications."""

import os
import time
from typing import Iterator
from dotenv import load_dotenv
from loguru import logger
from chromadb.utils import embedding_functions
from chromadb.utils.batch_utils import create_batches
import chromadb

load_dotenv()

def create_optimized_collection(
    client: chromadb.Client,
    collection_name: str,
    use_gpu: bool = False,
    model_name: str = "thenlper/gte-small"
) -> chromadb.Collection:
    """Create optimized collection with performance-tuned embedding function.

    Parameters
    ----------
    client : chromadb.Client
        ChromaDB client instance.
    collection_name : str
        Name for the collection.
    use_gpu : bool, optional
        Whether to use GPU acceleration, by default False.
    model_name : str, optional
        Model name optimized for performance, by default "thenlper/gte-small".

    Returns
    -------
    chromadb.Collection
        Performance-optimized collection.

    Examples
    --------
    >>> client = chromadb.Client()
    >>> collection = create_optimized_collection(client, "fast-docs", True)
    >>> collection.name == "fast-docs"
    True
    """
    device = "cuda" if use_gpu else "cpu"

    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=model_name,
        device=device
    )

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )

    logger.info(f"Created optimized collection '{collection_name}' on {device}")
    return collection

@logger.catch
def batch_add_documents(
    collection: chromadb.Collection,
    documents: list[str],
    metadatas: list[dict] | None = None,
    ids: list[str] | None = None,
    batch_size: int | None = None
) -> None:
    """Add documents to collection using optimized batching.

    Parameters
    ----------
    collection : chromadb.Collection
        Target collection for documents.
    documents : list[str]
        Documents to add.
    metadatas : list[dict] | None, optional
        Document metadata, by default None.
    ids : list[str] | None, optional
        Document identifiers, by default None.
    batch_size : int | None, optional
        Override default batch size, by default None.

    Examples
    --------
    >>> collection = chromadb.Client().create_collection("test")
    >>> docs = [f"Document {i}" for i in range(100)]
    >>> batch_add_documents(collection, docs)
    """
    if ids is None:
        ids = [f"batch-{i}" for i in range(len(documents))]

    if metadatas is None:
        metadatas = [{"batch_added": True} for _ in documents]

    # Use ChromaDB's batch utilities for optimal performance
    if batch_size is None:
        batch_size = getattr(collection._client, 'max_batch_size', 5461)

    start_time = time.time()

    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i + batch_size]
        batch_meta = metadatas[i:i + batch_size] if metadatas else None
        batch_ids = ids[i:i + batch_size]

        collection.add(
            documents=batch_docs,
            metadatas=batch_meta,
            ids=batch_ids
        )

        logger.debug(f"Added batch {i//batch_size + 1}, documents {i}-{min(i+batch_size, len(documents))}")

    elapsed = time.time() - start_time
    logger.info(f"Batch added {len(documents)} documents in {elapsed:.2f} seconds")

def benchmark_embedding_functions(
    sample_documents: list[str],
    models: list[str] = None
) -> dict[str, float]:
    """Benchmark different embedding functions for performance comparison.

    Parameters
    ----------
    sample_documents : list[str]
        Sample documents for benchmarking.
    models : list[str] | None, optional
        List of model names to benchmark, by default None.

    Returns
    -------
    dict[str, float]
        Benchmark results mapping model names to processing times.

    Examples
    --------
    >>> docs = ["Sample document for testing performance"]
    >>> results = benchmark_embedding_functions(docs)
    >>> isinstance(results, dict)
    True
    """
    if models is None:
        models = ["all-MiniLM-L6-v2", "thenlper/gte-small"]

    results = {}

    for model_name in models:
        logger.info(f"Benchmarking model: {model_name}")

        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name
        )

        start_time = time.time()
        embeddings = embedding_function(sample_documents)
        elapsed = time.time() - start_time

        results[model_name] = elapsed
        logger.info(f"{model_name}: {elapsed:.3f}s for {len(sample_documents)} documents")

    return results

def optimize_query_performance(
    collection: chromadb.Collection,
    query_text: str,
    n_results: int = 10
) -> dict:
    """Execute optimized query with performance monitoring.

    Parameters
    ----------
    collection : chromadb.Collection
        Collection to query.
    query_text : str
        Query text for similarity search.
    n_results : int, optional
        Number of results to return, by default 10.

    Returns
    -------
    dict
        Query results with performance metrics.

    Examples
    --------
    >>> collection = chromadb.Client().create_collection("test")
    >>> results = optimize_query_performance(collection, "test query")
    >>> "query_time" in results
    True
    """
    start_time = time.time()

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )

    query_time = time.time() - start_time

    # Add performance metrics to results
    results["query_time"] = query_time
    results["documents_per_second"] = n_results / query_time if query_time > 0 else 0

    logger.info(f"Query completed in {query_time:.3f}s, {results['documents_per_second']:.1f} docs/sec")

    return results

# Example usage for performance optimization
if __name__ == "__main__":
    logger.add("performance.log", level="INFO", rotation="10 MB")

    client = chromadb.Client()

    # Create optimized collection
    optimized_collection = create_optimized_collection(
        client, "performance-test", use_gpu=False
    )

    # Generate test documents
    test_documents = [f"Performance test document number {i} with varied content" for i in range(1000)]

    # Benchmark batch adding
    logger.info("Starting batch add benchmark")
    batch_add_documents(optimized_collection, test_documents)

    # Benchmark embedding functions
    sample_docs = test_documents[:10]
    benchmark_results = benchmark_embedding_functions(sample_docs)

    # Test query performance
    query_results = optimize_query_performance(
        optimized_collection, "performance test", n_results=5
    )

    logger.info("Performance optimization demonstration complete")
```

Storage configuration impacts both performance and persistence characteristics[^13]. Persistent clients enable data durability across application restarts while in-memory clients maximize performance for temporary operations[^13]. The choice between SQLite and alternative backends affects concurrency, storage capacity, and query performance characteristics[^13].

Memory management becomes critical for applications processing large document volumes or maintaining extensive collections[^4]. ChromaDB provides guidance on memory optimization strategies including collection partitioning, embedding dimension selection, and garbage collection practices that maintain system stability under load.

## Integration Patterns and Ecosystem Compatibility

ChromaDB integrates seamlessly with popular machine learning and data processing frameworks, particularly LangChain, which provides extensive integration capabilities for building complex AI applications[^9]. The integration patterns enable developers to leverage existing workflows while incorporating vector database capabilities for enhanced application functionality.

LangChain integration involves adapter patterns that bridge ChromaDB's embedding functions with LangChain's embedding interfaces[^9]. This compatibility enables developers to utilize either framework's embedding implementations while maintaining consistent interfaces across application components[^9]. The built-in adapters handle the conversion complexity while preserving the functionality of both platforms.

```python
"""Integration patterns for ChromaDB with popular frameworks."""

import os
from typing import Any
from dotenv import load_dotenv
from loguru import logger
import chromadb
from chromadb.utils import embedding_functions

# LangChain integration (requires langchain-huggingface)
try:
    from chromadb.utils.embedding_functions import create_langchain_embedding
    from langchain_huggingface import HuggingFaceEmbeddings
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger.warning("LangChain integration not available. Install langchain-huggingface to enable.")

load_dotenv()

def create_langchain_integrated_collection(
    client: chromadb.Client,
    collection_name: str,
    model_name: str = "all-MiniLM-L6-v2"
) -> chromadb.Collection | None:
    """Create collection using LangChain embedding integration.

    Parameters
    ----------
    client : chromadb.Client
        ChromaDB client instance.
    collection_name : str
        Name for the collection.
    model_name : str, optional
        HuggingFace model name, by default "all-MiniLM-L6-v2".

    Returns
    -------
    chromadb.Collection | None
        Collection with LangChain embeddings, or None if unavailable.

    Examples
    --------
    >>> client = chromadb.Client()
    >>> collection = create_langchain_integrated_collection(client, "langchain-docs")
    >>> collection is not None or not LANGCHAIN_AVAILABLE
    True
    """
    if not LANGCHAIN_AVAILABLE:
        logger.warning("LangChain integration not available")
        return None

    langchain_embeddings = HuggingFaceEmbeddings(model_name=model_name)
    embedding_function = create_langchain_embedding(langchain_embeddings)

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )

    logger.info(f"Created LangChain integrated collection '{collection_name}'")
    return collection

def implement_rag_pattern(
    collection: chromadb.Collection,
    knowledge_documents: list[str],
    query: str,
    context_limit: int = 3
) -> dict[str, Any]:
    """Implement Retrieval-Augmented Generation pattern with ChromaDB.

    Parameters
    ----------
    collection : chromadb.Collection
        Collection containing knowledge base documents.
    knowledge_documents : list[str]
        Documents to add to knowledge base.
    query : str
        User query for RAG pattern.
    context_limit : int, optional
        Maximum context documents to retrieve, by default 3.

    Returns
    -------
    dict[str, Any]
        RAG results with retrieved context and metadata.

    Examples
    --------
    >>> collection = chromadb.Client().create_collection("rag-test")
    >>> docs = ["Knowledge document 1", "Knowledge document 2"]
    >>> results = implement_rag_pattern(collection, docs, "test query")
    >>> "context" in results
    True
    """
    # Add knowledge documents to collection
    doc_ids = [f"kb-{i}" for i in range(len(knowledge_documents))]
    collection.add(
        documents=knowledge_documents,
        ids=doc_ids,
        metadatas=[{"source": "knowledge_base"} for _ in knowledge_documents]
    )

    # Retrieve relevant context
    search_results = collection.query(
        query_texts=[query],
        n_results=context_limit
    )

    # Extract context documents
    context_documents = search_results["documents"][0] if search_results["documents"] else []
    distances = search_results["distances"][0] if search_results["distances"] else []

    rag_result = {
        "query": query,
        "context": context_documents,
        "relevance_scores": [1 - d for d in distances],  # Convert distance to similarity
        "metadata": search_results.get("metadatas", []),
        "num_context_docs": len(context_documents)
    }

    logger.info(f"RAG pattern retrieved {len(context_documents)} context documents")
    return rag_result

def implement_semantic_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:
    """Implement semantic text chunking for optimal embedding generation.

    Parameters
    ----------
    text : str
        Text to chunk semantically.
    chunk_size : int, optional
        Target chunk size in characters, by default 500.
    overlap : int, optional
        Character overlap between chunks, by default 50.

    Returns
    -------
    list[str]
        List of semantically chunked text segments.

    Examples
    --------
    >>> text = "This is a test document. " * 100
    >>> chunks = implement_semantic_chunking(text)
    >>> len(chunks) > 1
    True
    """
    # Simple sentence-aware chunking implementation
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Check if adding sentence exceeds chunk size
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Start new chunk with overlap
            overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
            current_chunk = overlap_text + " " + sentence
        else:
            current_chunk += sentence + ". " if not sentence.endswith('.') else sentence + " "

    # Add final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    logger.debug(f"Chunked text into {len(chunks)} segments")
    return chunks

@logger.catch
def create_multi_modal_collection(
    client: chromadb.Client,
    collection_name: str
) -> chromadb.Collection:
    """Create collection for multi-modal data (text, metadata, etc.).

    Parameters
    ----------
    client : chromadb.Client
        ChromaDB client instance.
    collection_name : str
        Name for the multi-modal collection.

    Returns
    -------
    chromadb.Collection
        Collection configured for multi-modal data.

    Examples
    --------
    >>> client = chromadb.Client()
    >>> collection = create_multi_modal_collection(client, "multimodal")
    >>> collection.name == "multimodal"
    True
    """
    # Use default embedding function for text
    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )

    logger.info(f"Created multi-modal collection '{collection_name}'")
    return collection

def add_multi_modal_documents(
    collection: chromadb.Collection,
    texts: list[str],
    image_paths: list[str] | None = None,
    audio_metadata: list[dict] | None = None
) -> None:
    """Add multi-modal documents with various data types.

    Parameters
    ----------
    collection : chromadb.Collection
        Target collection for multi-modal data.
    texts : list[str]
        Text content for documents.
    image_paths : list[str] | None, optional
        Paths to associated images, by default None.
    audio_metadata : list[dict] | None, optional
        Audio file metadata, by default None.

    Examples
    --------
    >>> collection = chromadb.Client().create_collection("test")
    >>> texts = ["Document with image"]
    >>> add_multi_modal_documents(collection, texts)
    """
    metadatas = []

    for i, text in enumerate(texts):
        metadata = {"content_type": "text", "index": i}

        if image_paths and i < len(image_paths):
            metadata["image_path"] = image_paths[i]
            metadata["has_image"] = True

        if audio_metadata and i < len(audio_metadata):
            metadata.update(audio_metadata[i])
            metadata["has_audio"] = True

        metadatas.append(metadata)

    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=[f"multimodal-{i}" for i in range(len(texts))]
    )

    logger.info(f"Added {len(texts)} multi-modal documents")

# Example usage for integration patterns
if __name__ == "__main__":
    logger.add("integration.log", level="INFO", rotation="10 MB")

    client = chromadb.Client()

    # Test LangChain integration if available
    if LANGCHAIN_AVAILABLE:
        langchain_collection = create_langchain_integrated_collection(
            client, "langchain-test"
        )

    # Demonstrate RAG pattern
    rag_collection = client.get_or_create_collection("rag-demo")
    knowledge_docs = [
        "ChromaDB is a vector database for embeddings",
        "Vector databases enable semantic search capabilities",
        "Embeddings represent text as numerical vectors"
    ]

    rag_results = implement_rag_pattern(
        rag_collection, knowledge_docs, "What is ChromaDB?"
    )

    # Test semantic chunking
    long_text = "This is a long document that needs to be chunked. " * 50
    chunks = implement_semantic_chunking(long_text)

    # Create multi-modal collection
    multimodal_collection = create_multi_modal_collection(client, "multimodal-demo")
    add_multi_modal_documents(
        multimodal_collection,
        ["Document with multimedia content"],
        image_paths=["path/to/image.jpg"],
        audio_metadata=[{"duration": 30, "format": "mp3"}]
    )

    logger.info("Integration patterns demonstration complete")
```

Text chunking strategies significantly impact embedding quality and retrieval performance[^6][^15]. ChromaDB supports various chunking approaches including semantic chunking, cluster-based chunking, and LLM-guided chunking that optimize text segmentation for specific domains or applications[^6]. The evaluation framework provided by ChromaDB enables systematic comparison of chunking strategies to identify optimal approaches for particular use cases[^6].

Multi-modal capabilities extend ChromaDB beyond text embeddings to support image, audio, and other data types[^11]. This extensibility enables applications that combine multiple data modalities while maintaining consistent vector operations and query interfaces. The embedding function framework accommodates these scenarios through type-generic implementations that handle various input formats.

## Conclusion

ChromaDB represents a mature and flexible solution for implementing vector database capabilities in Python applications, offering a comprehensive SDK that balances simplicity with advanced functionality. The platform's four-function core API provides immediate productivity while supporting sophisticated use cases through extensive customization options. From basic document storage and retrieval to complex multi-modal applications with custom embedding functions, ChromaDB accommodates diverse requirements while maintaining consistent performance characteristics.

The key to successful ChromaDB implementation lies in understanding the relationship between embedding functions, chunking strategies, and query patterns that optimize for specific application requirements. By leveraging GPU acceleration, implementing appropriate batching strategies, and utilizing metadata filtering effectively, developers can build scalable vector database applications that handle substantial document volumes while maintaining responsive query performance. The platform's integration capabilities with frameworks like LangChain further enhance its utility in modern AI application development workflows.

The adoption of Python 3.13 best practices throughout ChromaDB implementations ensures code maintainability, type safety, and operational reliability. Using built-in type hints, NumPy-style documentation, environment-based configuration, and structured logging creates robust applications that scale effectively. As vector databases become increasingly central to AI applications, ChromaDB's minimal yet powerful approach positions it as an essential tool for developers building the next generation of intelligent systems.

<div style="text-align: center">⁂</div>

## References

[^1]: https://pypi.org/project/chromadb/

[^2]: https://github.com/neo-con/chromadb-tutorial

[^3]: https://cookbook.chromadb.dev/embeddings/bring-your-own-embeddings/

[^4]: https://cookbook.chromadb.dev

[^5]: https://airbyte.com/data-engineering-resources/chroma-db-vector-embeddings

[^6]: https://github.com/brandonstarxel/chunking_evaluation

[^7]: https://cookbook.chromadb.dev/core/filters/

[^8]: https://cookbook.chromadb.dev/strategies/batching/

[^9]: https://cookbook.chromadb.dev/integrations/langchain/embeddings/

[^10]: https://go-client.chromadb.dev/client/

[^11]: https://cookbook.chromadb.dev/core/concepts/

[^12]: https://cookbook.chromadb.dev/core/install/

[^13]: https://anderfernandez.com/en/blog/chroma-vector-database-tutorial/

[^14]: https://stackoverflow.com/questions/78662101/chroma-db-using-embedding-values

[^15]: https://www.youtube.com/watch?v=JjSCezpZbI0

[^16]: https://github.com/chroma-core/chroma/blob/main/chromadb/utils/embedding_functions/openai_embedding_function.py

[^17]: https://www.youtube.com/watch?v=cm2Ze2n9lxw

[^18]: https://www.reddit.com/r/vectordatabase/comments/1f2hgbd/chromadb_custom_embedding_functions/

[^19]: https://stackoverflow.com/questions/77004874/chromadb-langchain-sentencetransformerembeddingfunction-throwing-sentencetr

[^20]: https://cookbook.chromadb.dev/embeddings/gpu-support/

[^21]: https://docs.trychroma.com/getting-started

[^22]: https://www.datacamp.com/tutorial/chromadb-tutorial-step-by-step-guide

[^23]: https://github.com/chroma-core/chroma

[^24]: https://realpython.com/chromadb-vector-database/

[^25]: https://docs.trychroma.com/docs/embeddings/embedding-functions

[^26]: https://github.com/chroma-core/chroma/blob/main/chromadb/utils/embedding_functions/chroma_langchain_embedding_function.py

[^27]: https://cookbook.chromadb.dev/core/api/
