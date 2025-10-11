Yes—OpenRouter exposes an OpenAI-compatible /v1 endpoint, so the official Python OpenAI SDK works by pointing the client’s base_url to OpenRouter and providing an OpenRouter API key. This lets the same SDK code call hundreds of models routed through OpenRouter without changing calling patterns beyond configuration.[1][4][5]

### How to use

Configure the OpenAI client with OpenRouter’s v1 endpoint and an OpenRouter API key, then call chat.completions as usual.[5][1]

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
    default_headers={
        # OpenRouter recommends providing a referer for app attribution
        "HTTP-Referer": "http://localhost:3000"
    },
)

resp = client.chat.completions.create(
    model="meta-llama/llama-3.1-8b-instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about observability."},
    ],
)

print(resp.choices[0].message.content)
```

OpenRouter mirrors OpenAI’s schema on its /v1 endpoint, so the same client and method signatures work; instrumentation that hooks the OpenAI SDK also works unchanged when base_url is set to OpenRouter. The example above uses a standard chat.completions call, which is supported by OpenRouter’s OpenAI-compatible interface.[1][5]

### Model IDs

Model identifiers use provider/model-name, allowing selection of OpenAI, Anthropic, Google, Meta, and many others via one client configuration. Examples include openai/gpt-4o-2024-11-20, anthropic/claude-sonnet-4, google/gemini-2.5-pro-preview, and meta-llama/llama-4-maverick, all selected by setting model in the SDK call.[2]

### Routing and options

OpenRouter supports advanced routing preferences via extra_body, including provider ordering, quantization preferences for open‑source models, allow_fallbacks, and data_collection controls. For example, extra_body={"provider":{"order":["together","fireworks"],"allow_fallbacks":True}} can steer which backend serves the request and whether failover is allowed.[2]

### Instrumentation and ecosystem

Because the API mirrors OpenAI’s schema, OpenAI SDK auto-instrumentation used by observability tools can be applied directly by repointing the SDK to OpenRouter’s endpoint. This enables reuse of the same tracing and monitoring setup when switching from direct OpenAI calls to OpenRouter.[5]

### Notes on Agents SDK

Community reports indicate the OpenAI Agents SDK can be wired to OpenRouter by configuring the client to use OpenRouter’s endpoint, though integration specifics may require adjustments and results can vary across versions. For most applications, the core OpenAI Python SDK path shown above is the most straightforward way to access OpenRouter models.[3][1][5]

[1](https://openrouter.ai/docs/community/open-ai-sdk)
[2](https://snyk.io/articles/openrouter-in-python-use-any-llm-with-one-api-key/)
[3](https://www.reddit.com/r/openrouter/comments/1jcrejo/has_anybody_gotten_the_openai_agents_sdk_working/)
[4](https://openrouter.ai/openai/gpt-5/api)
[5](https://arize.com/docs/ax/integrations/llm-providers/openrouter/openrouter-tracing)
[6](https://www.youtube.com/watch?v=mtnoR2lQOI8)
[7](https://ai.pydantic.dev/models/openai/)
[8](https://openrouter.ai/openai/o3/api)
[9](https://www.reddit.com/r/ollama/comments/1hske56/can_openai_sdk_be_used_with_locally_hosted/)
[10](https://openrouter.ai/docs/quickstart)
[11](https://docs.letta.com/guides/server/providers/openai-proxy)
[12](https://www.reddit.com/r/LangChain/comments/1kcudql/using_langchain_chatopenai_with_openrouter_how_to/)
[13](https://gist.github.com/rbiswasfc/f38ea50e1fa12058645e6077101d55bb)
[14](https://langfuse.com/integrations/gateways/openrouter)
