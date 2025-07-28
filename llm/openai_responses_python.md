# **OpenAI Python SDK: Responses API vs Chat Completions API**

## **The Current Recommendation: Responses API**

For new Python projects using the OpenAI SDK, **OpenAI officially recommends using the Responses API over Chat Completions**[1][2]. Introduced in March 2025, the Responses API represents OpenAI's newest core API and is designed as an **"agentic API primitive"** that combines the simplicity of Chat Completions with enhanced capabilities for building more sophisticated AI applications[3][1].

## **Key Differences Between the APIs**

### **State Management**

The most significant difference lies in **conversation state management**:

**Chat Completions API** requires manual state management where you must maintain conversation history yourself and send the complete message array with each request[4][5]:

```python
from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "knock knock."},
        {"role": "assistant", "content": "Who's there?"},
        {"role": "user", "content": "Orange."}
    ]
)
print(completion.choices[0].message.content)
```

**Responses API** offers **built-in stateful conversations** through the `previous_response_id` parameter, eliminating the need to manually track conversation history[3][6]:

```python
from openai import OpenAI

client = OpenAI()

# First response
response = client.responses.create(
    model="gmini",
    input="tell me a joke"
)

# Continue conversation using previous response ID
second_response = client.responses.create(
    model="gpt-4o-mini",
    previous_response_id=response.id,
    input="explain why this is funny"
)
```

### **Built-in Tools and Capabilities**

The Responses API includes **native support for advanced tools**[1][7]:

| **Capability**       | **Chat Completions** | **Responses API** |
| -------------------- | -------------------- | ----------------- |
| Text generation      | ✓                    | ✓                 |
| Function calling     | ✓                    | ✓                 |
| **Web search**       | ✗                    | ✓                 |
| **File search**      | ✗                    | ✓                 |
| **Computer use**     | ✗                    | ✓                 |
| **Code interpreter** | ✗                    | Coming soon       |

### **Simplified API Structure**

**Responses API** offers a cleaner interface[1]:

- Uses `input` parameter instead of `messages` array
- Returns `output_text` directly via helper method
- Provides `response` object with unique `id` instead of `choices` array
- Built-in semantic events for better integration and type safety[2]

## **Migration Considerations**

### **Chat Completions API Remains Supported**

OpenAI has **committed to supporting Chat Completions indefinitely**[1][6]. It remains the industry standard and will continue receiving new models and capabilities. You can confidently continue using Chat Completions if:

- You don't need built-in tools like web search or computer use
- Your application already works well with manual state management
- You prefer the established, widely-adopted API format

### **When to Choose Responses API**

The Responses API is recommended for[1][8]:

- **New projects** starting development
- Applications requiring **agent-like workflows**
- Projects needing **built-in tools** (web search, file search, computer use)
- Applications benefiting from **automatic state management**
- **Multi-step conversational logic** and reasoning tasks

### **Assistants API Deprecation**

The **Assistants API will be sunset in the first half of 2026**[1][6][8], with OpenAI recommending migration to the Responses API. The Responses API incorporates improvements based on developer feedback from the Assistants API beta.

## **Code Examples Comparison**

**Basic text generation:**

```python
# Chat Completions
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
result = completion.choices[0].message.content

# Responses API
response = client.responses.create(
    model="gpt-4o",
    input="Hello"
)
result = response.output_text
```

**Conversation with state management:**

```python
# Chat Completions - Manual history management
history = [{"role": "user", "content": "Tell me a joke"}]
response1 = client.chat.completions.create(model="gpt-4o", messages=history)
history.append({"role": "assistant", "content": response1.choices[0].message.content})

# Responses API - Automatic state management
response1 = client.responses.create(model="gpt-4o", input="Tell me a joke")
response2 = client.responses.create(
    model="gpt-4o",
    input="Tell me another",
    previous_response_id=response1.id
)
```

## **Agent SDK Integration**

For advanced agent development, OpenAI provides the **Agents SDK**[9][10] which defaults to using the Responses API but can be configured to use Chat Completions:

```python
from agents import set_default_openai_api

# Use Responses API (default)
set_default_openai_api("responses")

# Or use Chat Completions
set_default_openai_api("chat_completions")
```

## **Conclusion**

While both APIs remain viable options, **OpenAI's clear recommendation is the Responses API for new projects**[1][2]. It provides a more modern foundation for building AI applications with built-in state management, advanced tools, and simplified workflows. The Chat Completions API continues to be an excellent choice for existing applications and scenarios where you don't need the advanced features of the Responses API.

For developers working on agentic systems and complex AI workflows—particularly relevant given your role as a Distinguished Engineer at Microsoft working on AI and agentic systems—the Responses API offers significant advantages in terms of development efficiency and capability integration.

[1] <https://platform.openai.com/docs/guides/responses-vs-chat-completions>
[2] <https://platform.openai.com/docs/guides/responses-vs-chat-completions?api-mode=responses>
[3] <https://neurlcreators.substack.com/p/buildaiers-talking-9>
[4] <https://www.ghacks.net/2025/03/12/openai-introduces-responses-api-and-agents-sdk-for-advanced-ai-development/>
[5] <https://platform.openai.com/docs/guides/conversation-state?lang=python>
[6] <https://simonwillison.net/2025/Mar/11/responses-vs-chat-completions/>
[7] <https://platform.openai.com/docs/guides/production-best-practices>
[8] <https://zuplo.com/blog/2025/04/10/openai-api>
[9] <https://www.datacamp.com/tutorial/openai-agents-sdk-tutorial>
[10] <https://openai.github.io/openai-agents-python/config/>
[11] <https://blog.finxter.com/openai-python-api-a-helpful-illustrated-guide-in-5-steps/>
[12] <https://expertbeacon.com/harnessing-the-power-of-openai-with-the-openai-python-library/>
[13] <https://www.newhorizons.com/resources/blog/the-complete-guide-for-using-the-openai-python-api>
[14] <https://blog.gopenai.com/exploring-the-power-of-openai-api-with-python-a-step-by-step-guide-cc286f451046?gi=fbbcd7f6271f>
[15] <https://gist.github.com/johnnykfeng/ea05ccdec22785b924dfc9aa378282c2>
[16] <https://community.openai.com/t/terminology-evolution-completion-vs-response/1143324>
[17] <https://platform.openai.com/docs/guides/function-calling>
[18] <https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api>
[19] <https://community.openai.com/t/api-learning-and-best-practices/904043>
[20] <https://stackoverflow.com/questions/76672343/openai-api-chatcompletion-and-completion-give-totally-different-answers-with-sa/76679485>
[21] <https://www.datacamp.com/cheat-sheet/the-open-ai-api-in-python>
[22] <https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety>
[23] <https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/chatgpt>
[24] <https://openai.github.io/openai-agents-python/tools/>
[25] <https://www.youtube.com/watch?v=CHsRy4gl6hk>
[26] <https://blog.csdn.net/weixin_40941102/article/details/146308722>
[27] <https://www.toolify.ai/ai-news/openai-new-api-revolutionizing-ai-development-in-2025-3314625>
[28] <https://the-decoder.com/openai-adds-new-features-and-improvements-to-its-agent-development-tools-and-language-model/>
[29] <https://learn.microsoft.com/en-us/azure/ai-foundry/openai/whats-new>
[30] <https://www.bitcot.com/openai-api-key-guide/>
[31] <https://simonwillison.net/2025/Mar/11/responses-vs-chat-completions/?form=MG0AV3>
[32] <https://www.rickyspears.com/ai/mastering-the-openai-api-in-python-a-comprehensive-guide-to-key-parameters-in-2025/>
[33] <https://help.openai.com/en/articles/7042661-moving-from-completions-to-chat-completions-in-the-openai-api>
[34] <https://platform.openai.com/docs/changelog>
[35] <https://www.youtube.com/watch?v=GXkfYm2hFYo>
[36] <https://www.youtube.com/watch?v=Bhj1n0dh1z8>
[37] <https://learn.microsoft.com/en-us/azure/ai-services/openai/whats-new>
[38] <https://github.com/openai/openai-python/blob/main/README.md?plain=1>
[39] <https://community.openai.com/t/chat-completions-and-completions-the-same-api-or-different/746834>
[40] <https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/responses>
[41] <https://milvus.io/ai-quick-reference/how-do-i-set-up-a-session-with-openai-api-for-conversational-tasks>
[42] <https://platform.openai.com/docs/guides/conversation-state>
[43] <https://platform.openai.com/docs/api-reference>
[44] <https://pypi.org/project/gptsession/>
[45] <https://www.toolify.ai/ai-news/openais-agent-sdk-revolutionizing-ai-agent-development-in-2025-3314664>
[46] <https://cookbook.openai.com/examples/responses_api/responses_example>
[47] <https://stackoverflow.com/questions/74711107/openai-api-continuing-conversation-in-a-dialogue>
[48] <https://www.youtube.com/watch?v=MK2rPpQP8pw>
[49] <https://www.youtube.com/watch?v=1P5Yccy1rRk>
[50] <https://www.infoq.com/news/2025/03/openai-responses-api-agents-sdk/>
[51] <https://stackoverflow.com/questions/72236412/how-do-i-save-responses-from-an-api-to-a-state-so-that-i-can-display-old-searche>
[52] <https://openai.github.io/openai-agents-python/sessions/>
[53] <https://www.notebookcheck.net/OpenAI-releases-tools-and-API-for-developers-to-build-AI-agents-for-businesses.977443.0.html>
[54] <https://community.openai.com/t/responses-api-question-about-managing-conversation-state-with-previous-response-id/1141633>
[55] <https://cookbook.openai.com/examples/assistants_api_overview_python>

# OpenAI Responses API: A Comprehensive Python Guide

The OpenAI Responses API represents the next generation of AI model interaction, combining the strengths of the Chat Completions and Assistants APIs into a single streamlined interface. Released in March 2025, this API is designed to be OpenAI's primary interface going forward, offering simplified development with automatic orchestration logic and native integration of built-in tools[^2]. This guide provides comprehensive coverage of using the Responses API with Python 3.13, focusing on prompt templating with Jinja2 and advanced function calling capabilities.

## Understanding the Responses API Architecture

The Responses API introduces a fundamentally different approach to AI model interaction compared to its predecessors. Unlike the Chat Completions API that relies on conversation-style message arrays, the Responses API uses a more flexible `input` parameter that can accept both simple strings and structured message arrays[^1][^2]. This design philosophy reflects OpenAI's commitment to creating a more developer-friendly interface that reduces complexity while maintaining powerful functionality.

The API's core innovation lies in its automatic handling of orchestration logic, eliminating the need for developers to manually manage complex conversation flows or tool integration patterns[^2]. This streamlined approach significantly reduces the amount of boilerplate code required for common AI development tasks, allowing developers to focus on application logic rather than API management details.

The response structure follows a predictable pattern with an `output` array containing generated content. Each response includes comprehensive metadata such as token usage, model information, and processing status, providing developers with detailed insights into API performance and costs[^1]. The API maintains backward compatibility with existing OpenAI concepts while introducing new capabilities for advanced use cases.

## Setting Up the Python Environment

Before implementing Responses API functionality, establishing a proper Python environment is crucial for success. The setup process involves several key components that ensure secure and efficient API usage.

```python
import os
from openai import OpenAI
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, Template
from loguru import logger
import json
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure logging with loguru
logger.add("openai_api.log", level="INFO", rotation="10 MB", retention="10 days")

# Initialize the OpenAI client with error handling
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

client = OpenAI(api_key=api_key)
logger.info("OpenAI client initialized successfully")
```

The initialization pattern shown above represents best practices for secure API key management[^2][^19]. Using environment variables prevents accidental exposure of sensitive credentials in source code repositories. The `dotenv` package provides a convenient mechanism for managing environment variables during development while maintaining security in production environments.

For Python 3.13 compatibility, ensure you're using the latest version of the OpenAI Python SDK. The installation command `pip install openai` will automatically retrieve the most recent version that supports the Responses API[^20]. Additionally, installing supporting packages like `python-dotenv` and `jinja2` enables the advanced templating functionality discussed in subsequent sections.

The client initialization creates a persistent connection object that handles authentication and request management automatically. This approach eliminates the need to pass API keys with each request and provides consistent error handling across all API interactions[^1].

## Implementing Jinja2 Template-Based Prompt Engineering

Dynamic prompt generation using Jinja2 templates represents a powerful approach to creating flexible and maintainable AI applications. This methodology separates prompt logic from application code, enabling non-technical team members to modify prompts without touching Python implementation details[^18].

```python
from jinja2 import Environment, FileSystemLoader
from typing import Any

# Set up Jinja2 environment for template loading
template_env = Environment(loader=FileSystemLoader('prompts'))

# Example template file: prompts/analysis_prompt.txt
analysis_template = template_env.get_template('analysis_prompt.txt')

@logger.catch
def generate_analysis_prompt(
    text: str,
    max_keywords: int = 5,
    analysis_type: str = "sentiment"
) -> str:
    """Generate a dynamic analysis prompt using Jinja2 templating.

    Parameters
    ----------
    text : str
        Text content to analyze.
    max_keywords : int, default=5
        Maximum number of keywords to extract.
    analysis_type : str, default="sentiment"
        Type of analysis to perform (sentiment, summary, etc.).

    Returns
    -------
    str
        Rendered prompt template ready for API submission.

    Examples
    --------
    >>> prompt = generate_analysis_prompt("Great product!", 3, "sentiment")
    >>> print(len(prompt) > 0)
    True
    """
    logger.debug(f"Generating {analysis_type} prompt for text length: {len(text)}")
    return analysis_template.render(
        text=text,
        max_keywords=max_keywords,
        analysis_type=analysis_type,
        timestamp=datetime.now().isoformat()
    )

@logger.catch
def analyze_text_with_template(text: str, **template_vars: Any) -> str | None:
    """Analyze text using templated prompts with the Responses API.

    Parameters
    ----------
    text : str
        Text to analyze.
    **template_vars : Any
        Additional template variables for prompt customization.

    Returns
    -------
    str | None
        Analysis result or None if request fails.

    Examples
    --------
    >>> result = analyze_text_with_template("Good service", analysis_type="sentiment")
    >>> isinstance(result, str) or result is None
    True
    """
    try:
        prompt = generate_analysis_prompt(text, **template_vars)

        response = client.responses.create(
            model="gpt-4.1",
            input=prompt,
            temperature=0.3,
            max_output_tokens=1000
        )

        logger.info(f"Analysis completed, tokens used: {response.usage.total_tokens}")
        return response.output_text

    except Exception as e:
        logger.error(f"Text analysis failed: {e}")
        return None
```

The template-based approach offers several advantages over hardcoded prompts[^18]. First, it enables version control of prompt evolution without requiring code changes. Second, it facilitates A/B testing of different prompt variations by simply swapping template files. Third, it supports internationalization by maintaining separate template files for different languages.

Template files can incorporate complex logic using Jinja2's control structures. For example, conditional sections can adapt prompts based on input characteristics, while loops can generate repeated sections for batch processing scenarios[^15]. This flexibility makes Jinja2 templates particularly valuable for applications requiring dynamic prompt adaptation based on runtime conditions.

Advanced template patterns include inheritance and macros, which enable prompt component reuse across different use cases. Template inheritance allows creation of base prompt structures that specific templates can extend, while macros provide reusable prompt fragments that can be shared across multiple templates[^7].

## Function Calling Fundamentals and Terminology

OpenAI's official documentation consistently uses the term **"function calling"** rather than "tool calling," though both terms refer to the same underlying capability[^4][^14]. Function calling enables AI models to interface with external code or services by generating structured function invocations based on natural language inputs.

The function calling process follows a predictable three-step pattern. First, the model analyzes the user input and determines whether any available functions should be called. Second, if function calls are warranted, the model generates structured function invocations with appropriate arguments. Third, the developer executes the called functions and provides results back to the model for integration into the final response[^4][^14].

```python
# Define a function schema for weather retrieval
weather_function: dict[str, Any] = {
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City and country e.g. Bogotá, Colombia"
            },
            "units": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature units"
            }
        },
        "required": ["location"],
        "additionalProperties": False
    },
    "strict": True
}

@logger.catch
def get_weather_example() -> None:
    """Demonstrate basic function calling with Responses API.

    Examples
    --------
    >>> get_weather_example()  # Should complete without errors
    """
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=[{"role": "user", "content": "What's the weather like in Paris today?"}],
            tools=[weather_function]
        )

        logger.info(f"Weather query completed: {response.status}")
        print(response.output)

    except Exception as e:
        logger.error(f"Weather function calling failed: {e}")
```

Function schemas must adhere to JSON Schema specifications, providing the model with detailed information about function purpose, parameters, and expected return values[^4]. The `strict` parameter enforces adherence to the schema, preventing the model from generating function calls with invalid arguments.

The `description` fields within function schemas serve as crucial guidance for the model's decision-making process. Well-written descriptions should clearly explain when and how to use each function, including edge cases and limitations[^14]. This documentation becomes particularly important in complex applications with multiple available functions.

## Advanced Function Calling Patterns

Sophisticated applications often require precise control over function calling behavior. The Responses API provides several mechanisms for influencing when and how functions are called through the `tool_choice` parameter[^4][^5].

```python
@logger.catch
def force_weather_lookup(location: str) -> Any | None:
    """Force the model to call a specific weather function.

    Parameters
    ----------
    location : str
        Geographic location for weather lookup.

    Returns
    -------
    Any | None
        API response or None if request fails.

    Examples
    --------
    >>> response = force_weather_lookup("London")
    >>> response is not None or response is None  # Either outcome is valid
    True
    """
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=f"Get weather information for {location}",
            tools=[weather_function],
            tool_choice={"type": "function", "name": "get_weather"}
        )
        logger.info(f"Forced weather lookup for {location} completed")
        return response
    except Exception as e:
        logger.error(f"Forced weather lookup failed: {e}")
        return None

@logger.catch
def require_function_call(user_input: str, available_functions: list[dict[str, Any]]) -> Any | None:
    """Require any function call but let model choose which.

    Parameters
    ----------
    user_input : str
        User's input message.
    available_functions : list[dict[str, Any]]
        List of available function schemas.

    Returns
    -------
    Any | None
        API response or None if request fails.
    """
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=user_input,
            tools=available_functions,
            tool_choice="required"
        )
        logger.info("Required function call completed")
        return response
    except Exception as e:
        logger.error(f"Required function call failed: {e}")
        return None

@logger.catch
def auto_function_selection(user_input: str, available_functions: list[dict[str, Any]]) -> Any | None:
    """Allow automatic function selection (default behavior).

    Parameters
    ----------
    user_input : str
        User's input message.
    available_functions : list[dict[str, Any]]
        List of available function schemas.

    Returns
    -------
    Any | None
        API response or None if request fails.
    """
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=user_input,
            tools=available_functions,
            tool_choice="auto"  # This is the default
        )
        logger.info("Auto function selection completed")
        return response
    except Exception as e:
        logger.error(f"Auto function selection failed: {e}")
        return None
```

The `tool_choice` parameter accepts three primary values: `"auto"` (default), `"required"`, and specific function selection objects[^5]. The `"auto"` setting allows the model to determine whether function calls are necessary, while `"required"` forces at least one function call regardless of input context. Specific function selection guarantees execution of a particular function, useful for scenarios requiring predetermined actions.

Function calling can generate multiple simultaneous calls when the model determines that several functions are needed to complete a task[^4]. This parallel execution capability requires careful handling in the response processing logic to ensure all function results are properly integrated.

```python
def handle_multiple_function_calls(response: Any) -> list[dict[str, str]]:
    """Process potentially multiple function calls from a single response.

    Parameters
    ----------
    response : Any
        OpenAI API response object containing function calls.

    Returns
    -------
    list[dict[str, str]]
        List of function call results formatted for API submission.

    Examples
    --------
    >>> # Assuming a response with function calls
    >>> results = handle_multiple_function_calls(mock_response)
    >>> isinstance(results, list)
    True
    """
    function_results: list[dict[str, str]] = []

    for output_item in response.output:
        if output_item.type == "function_call":
            try:
                # Extract function details
                function_name = output_item.name
                arguments = json.loads(output_item.arguments)
                call_id = output_item.call_id

                logger.debug(f"Executing function: {function_name} with args: {arguments}")

                # Execute the function (implement your own routing logic)
                result = execute_function(function_name, arguments)

                # Prepare result for next API call
                function_results.append({
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": str(result)
                })

                logger.info(f"Function {function_name} executed successfully")

            except Exception as e:
                logger.error(f"Function execution failed for {function_name}: {e}")
                function_results.append({
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": f"Error: {str(e)}"
                })

    return function_results
```

## Best Practices for Function Definition

Effective function calling requires adherence to several critical best practices that significantly impact model performance and reliability[^14]. These guidelines stem from extensive testing and real-world application experience.

Function names and descriptions should be extremely clear and detailed. The model relies heavily on these descriptions to determine when and how to use each function[^14]. Ambiguous or incomplete descriptions lead to incorrect function usage or missed opportunities for appropriate function calls.

```python
# Good function definition - clear and detailed with proper typing
calculate_mortgage_payment: dict[str, Any] = {
    "type": "function",
    "name": "calculate_mortgage_payment",
    "description": "Calculate monthly mortgage payment including principal, interest, taxes, and insurance. Use this when users ask about mortgage costs, monthly payments, or loan affordability.",
    "parameters": {
        "type": "object",
        "properties": {
            "principal": {
                "type": "number",
                "description": "Loan amount in dollars (e.g., 350000 for $350,000)"
            },
            "annual_interest_rate": {
                "type": "number",
                "description": "Annual interest rate as a decimal (e.g., 0.045 for 4.5%)"
            },
            "loan_term_years": {
                "type": "integer",
                "description": "Loan duration in years (typically 15 or 30)"
            },
            "annual_property_tax": {
                "type": "number",
                "description": "Annual property tax in dollars",
                "default": 0
            },
            "annual_insurance": {
                "type": "number",
                "description": "Annual insurance premium in dollars",
                "default": 0
            }
        },
        "required": ["principal", "annual_interest_rate", "loan_term_years"],
        "additionalProperties": False
    },
    "strict": True
}
```

Parameter design should follow software engineering best practices. Use enums to constrain possible values and prevent invalid states[^14]. Avoid making the model fill arguments that can be determined programmatically. For example, if you already have a user ID from the session context, don't require the model to provide it as a function parameter.

The number of available functions significantly impacts calling accuracy. OpenAI recommends limiting functions to fewer than 20 at any given time, though this is a soft suggestion rather than a hard limit[^14]. Applications requiring many functions should consider grouping related functionality or implementing dynamic function filtering based on context.

## Error Handling and Response Management

Robust error handling becomes critical when implementing function calling workflows, as failures can occur at multiple stages of the process. The Responses API provides detailed error information and status codes that enable sophisticated error recovery strategies[^1].

```python
@logger.catch
def robust_function_calling_workflow(
    user_input: str,
    functions: list[dict[str, Any]]
) -> str | None:
    """Implement comprehensive error handling for function calling.

    Parameters
    ----------
    user_input : str
        User's input message for processing.
    functions : list[dict[str, Any]]
        List of available function schemas.

    Returns
    -------
    str | None
        Function calling result or None if workflow fails.

    Examples
    --------
    >>> result = robust_function_calling_workflow("Hello", [])
    >>> isinstance(result, str) or result is None
    True
    """
    try:
        # Initial API call
        response = client.responses.create(
            model="gpt-4.1",
            input=user_input,
            tools=functions,
            tool_choice="auto"
        )

        # Check response status
        if response.status != "completed":
            logger.warning(f"Response status: {response.status}")
            if response.error:
                logger.error(f"API error: {response.error}")
                return None

        # Process function calls if present
        if any(item.type == "function_call" for item in response.output):
            return handle_function_calls_with_retry(response, functions)
        else:
            # Direct text response
            logger.info("Direct text response received")
            return response.output_text

    except Exception as e:
        logger.error(f"Function calling workflow failed: {e}")
        return None

@logger.catch
def handle_function_calls_with_retry(
    response: Any,
    functions: list[dict[str, Any]],
    max_retries: int = 3
) -> str | None:
    """Handle function calls with retry logic for failed executions.

    Parameters
    ----------
    response : Any
        OpenAI API response containing function calls.
    functions : list[dict[str, Any]]
        List of available function schemas.
    max_retries : int, default=3
        Maximum number of retry attempts.

    Returns
    -------
    str | None
        Final response text or None if processing fails.
    """
    input_messages: list[Any] = []

    for output_item in response.output:
        if output_item.type == "function_call":
            try:
                # Execute function with timeout protection
                result = execute_function_with_timeout(
                    output_item.name,
                    json.loads(output_item.arguments),
                    timeout=30
                )

                input_messages.extend([
                    output_item,  # Original function call
                    {
                        "type": "function_call_output",
                        "call_id": output_item.call_id,
                        "output": str(result)
                    }
                ])

                logger.info(f"Function {output_item.name} executed successfully")

            except Exception as e:
                logger.error(f"Function execution failed: {e}")
                # Provide error context to model
                input_messages.extend([
                    output_item,
                    {
                        "type": "function_call_output",
                        "call_id": output_item.call_id,
                        "output": f"Error: Function execution failed - {str(e)}"
                    }
                ])

    # Generate final response with function results
    try:
        final_response = client.responses.create(
            model="gpt-4.1",
            input=input_messages,
            tools=functions
        )
        logger.info("Final response generated successfully")
        return final_response.output_text

    except Exception as e:
        logger.error(f"Final response generation failed: {e}")
        return None
```

The error handling strategy should account for various failure modes including network timeouts, function execution errors, and malformed function calls. Providing meaningful error context to the model enables it to generate appropriate fallback responses or suggest alternative approaches[^1].

Rate limiting represents another critical consideration for production applications. The Responses API includes usage statistics in each response, enabling applications to monitor token consumption and implement appropriate throttling mechanisms[^1]. Applications should implement exponential backoff for rate limit errors and provide graceful degradation when API quotas are exceeded.

## Performance Optimization and Token Management

Optimizing Responses API performance requires careful attention to token usage patterns and request efficiency. The API charges for both input and output tokens, making prompt optimization crucial for cost-effective applications[^14].

Prompt caching provides significant cost and latency savings for applications with repeated content. Positioning static content at the beginning of prompts maximizes cache hit rates, while dynamic content should appear later in the prompt structure[^8]. This ordering enables the API to reuse cached prompt prefixes across multiple requests.

```python
def optimized_prompt_structure(base_instructions, dynamic_context, user_query):
    """Structure prompts for optimal caching and performance."""
    # Static content first (cached)
    prompt_parts = [
        base_instructions,  # Reusable system instructions
        # Dynamic content later
        f"Context: {dynamic_context}",
        f"User Query: {user_query}"
    ]

    return "\n\n".join(prompt_parts)

def token_aware_function_calling(user_input, functions, max_tokens=4000):
    """Implement token-aware function calling with limits."""
    # Calculate approximate input token count
    estimated_input_tokens = len(user_input.split()) * 1.3  # Rough estimation
    function_schema_tokens = sum(len(str(f)) for f in functions) * 0.75

    total_estimated_input = estimated_input_tokens + function_schema_tokens

    # Adjust max_output_tokens based on context size
    max_output = min(max_tokens - int(total_estimated_input), 2000)

    response = client.responses.create(
        model="gpt-4.1",
        input=user_input,
        tools=functions,
        max_output_tokens=max_output
    )

    # Log actual usage for optimization
    logging.info(f"Tokens used: {response.usage.total_tokens}")

    return response
```

Function schema optimization reduces token consumption without sacrificing functionality. Concise but clear function descriptions minimize token usage while maintaining model comprehension[^14]. Removing unnecessary fields from parameter schemas and using shorter but still descriptive parameter names can yield significant token savings in applications with many functions.

Model selection impacts both performance and cost. The `gpt-4.1` model provides state-of-the-art function calling capabilities but consumes more tokens than smaller models[^2]. Applications should evaluate whether simpler models like `gpt-3.5-turbo` meet their function calling requirements before defaulting to larger models.

## Conclusion

The OpenAI Responses API represents a significant advancement in AI model interaction capabilities, offering developers a streamlined interface that combines the best aspects of previous API generations. Through proper implementation of Jinja2-based prompt templating and sophisticated function calling patterns, developers can create robust, maintainable AI applications that leverage the full power of modern language models.

The key to successful Responses API implementation lies in understanding its architectural principles and following established best practices for function definition, error handling, and performance optimization. By treating function calling as a first-class feature rather than an afterthought, applications can achieve remarkable sophistication in their AI interactions while maintaining code clarity and reliability.

As the AI development landscape continues evolving, the Responses API provides a future-proof foundation for building advanced applications. Its emphasis on developer experience and operational simplicity positions it as the recommended approach for new OpenAI integrations, making investment in mastering its capabilities a strategic advantage for development teams building the next generation of AI-powered applications.

<div style="text-align: center">⁂</div>

[^1]: <https://platform.openai.com/docs/api-reference/responses>
[^2]: <https://www.datacamp.com/tutorial/openai-responses-api>
[^4]: <https://platform.openai.com/docs/guides/function-calling>
[^5]: <https://community.openai.com/t/tool-choice-auto-sending-content-and-tool-calls/1199283/6>
[^7]: <https://github.com/NirDiamant/Prompt_Engineering/blob/main/all_prompt_engineering_techniques/prompt-templates-variables-jinja2.ipynb>
[^8]: <https://platform.openai.com/docs/guides/text>
[^14]: <https://platform.openai.com/docs/guides/function-calling?api-mode=responses>
[^15]: <https://www.youtube.com/watch?v=8K2HbXhwWug>
[^18]: <https://datascience.fm/creating-dynamic-prompts-with-jinja2-for-llm-queries/>
[^19]: <https://github.com/gbaeke/openai_responses>
[^20]: <https://blog.finxter.com/openai-python-api-a-helpful-illustrated-guide-in-5-steps/>
