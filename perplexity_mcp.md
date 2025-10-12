---
tags: [guide, api]
---

https://docs.perplexity.ai/guides/mcp-server

https://github.com/perplexityai/modelcontextprotocol



{
  "mcpServers": {
    "perplexity-ask": {
      "command": "npx",
      "args": [
        "-y",
        "server-perplexity-ask"
      ],
      "env": {
        "PERPLEXITY_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}

## Related Concepts

### Related Topics
- [[openai_responses_python]] - Perplexity uses OpenAI-compatible API format
- [[openrouter_openai_python_sdk]] - Both provide OpenAI-compatible endpoints for alternative models

### Alternatives
- [[openrouter_openai_python_sdk]] - OpenRouter for broader model access without built-in search