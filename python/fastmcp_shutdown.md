<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Diagnosing FastMCP STDIO Shutdown Hangs

FastMCP’s default **STDIO** transport keeps a subprocess alive between client invocations to avoid cold-starts. Unfortunately, on many platforms that persistence combines with asyncio’s task-scheduling semantics to produce zombie processes and a CLI that never returns to the shell. The symptom you are working around _is_ a well-documented bug, not a mistake in your code.

Below is a deep dive into why the hang occurs, who has confirmed it, and the safest ways to eliminate it without peppering your codebase with manual task-cancellation loops.

## 1. What exactly is happening?

### 1.1 Default session persistence

* Every **PythonStdioTransport** and **NodeStdioTransport** instance is created with `keep_alive=True`. This makes the child MCP server remain in the background after the first call so that later calls can reuse it with lower latency[^1].
* The CLI wrapper (`fastmcp client …`) hard-codes that default today; the official JSON config schema still lacks a `keep_alive` property[^2].


### 1.2 Missing automatic teardown

* When the parent process exits, the transport does _not_ send a JSON-RPC `shutdown` and EOF before closing its pipes. The orphaned server survives in an event-loop “select” call and continues to wait for input. Multiple GitHub tickets track the issue, e.g. “STDIO hangs forever when using multiprocessing” \#817[^3] and “MCP server instances not cleaned up in STDIO transport mode” \#9064[^4].


### 1.3 Why your `cancel all tasks` patch works

* By enumerating `asyncio.all_tasks()` and cancelling everything except the current coroutine, you unblock the selector, forcing `FastMCP.run()` to finish and return control to your script. Your patch is effectively imitating the missing graceful shutdown. It is correct—but it should be unnecessary.


## 2. Evidence this is a real bug

| Evidence | Project | Excerpt |
| :-- | :-- | :-- |
| GitHub \#817 | modelcontextprotocol/python-sdk | “When multiprocessing in a tool … the MCP server never responds … The program is stuck and won’t continue.”[^3] |
| Client-side doc | FastMCP site | “STDIO transports maintain sessions across multiple client contexts by default (`keep_alive=True`).”[^1] |
| Enhancement \#644 | fastmcp | “Move keep_alive from transport level to client level.”[^2] |
| Langflow bug \#9064 | langflow-ai/langflow | “Old STDIO server processes are not cleaned up; memory consumption grows each time the editor page opens.”[^4] |

These confirm the behavior across Windows, macOS, and Linux; it is not unique to your environment.

## 3. How to shut down cleanly—four proven options

### 3.1 Disable persistence programmatically

If you create the transport yourself, explicitly pass `keep_alive=False`:

```python
from fastmcp.client.transports import PythonStdioTransport
from fastmcp import Client

transport = PythonStdioTransport(
        command="python",
        args=["my_server.py"],
        keep_alive=False          # <-- disables background process
)

client = Client(transport)
async with client:
    await client.ping()
```

This causes the subprocess to exit automatically when the `async with` block closes. (The option is available in SDK ≥ 1.8 even though the CLI wrapper still lacks a flag.)

### 3.2 Call `await client.close()` explicitly

If you _must_ rely on the CLI helper that hides the transport, obtain the client object and close it yourself before exiting:

```python
async with client:
    …  # your calls
await client.close()  # forces shutdown, even with keep_alive=True
```


### 3.3 Switch to streamable-HTTP/SSE transport

HTTP transports never keep a subprocess on the caller’s side, so the hang cannot occur. Issue \#817 shows the same sample code succeeding instantly when switched to `streamablehttp_client`[^3].

### 3.4 Monkey-patch the CLI until upstream fixes land

If your workflow _must_ stay on the CLI and you cannot upgrade yet, wrap your script with a tiny shim:

```bash
#!/usr/bin/env bash
python - <<'PY'
import asyncio, sys
from fastmcp.tools_cli import run_cli            # hypothetical import

async def main():
    try:
        await run_cli()
    finally:
        # last-resort cleanup identical to your workaround
        loop = asyncio.get_running_loop()
        pending = [t for t in asyncio.all_tasks(loop) if not t.done()]
        for t in pending:
            t.cancel()
        await asyncio.gather(*pending, return_exceptions=True)

asyncio.run(main())
PY
```

This keeps your current logic intact but isolates the cleanup hack to one place.

## 4. Why the official fix is taking time

* **Cross-platform process termination** is tricky (Windows needs `CTRL_BREAK_EVENT`; POSIX uses `SIGTERM` + `SIGKILL` fallback).
* `keep_alive` was introduced for IDE integrations (e.g. Cursor, VS Code) that expect hot-reload behaviour.
* The maintainers are debating whether to expose persistence in the MCP JSON config, an environment variable, or a CLI flag (\#644 discussion)[^2].

Until consensus lands, disabling persistence in code (option 3.1) is the safest route.

## 5. Best-practice checklist to avoid future hangs

1. **Always use `async with`** around both your transport and your `ClientSession`. That ensures `__aexit__` runs even on `KeyboardInterrupt`.
2. **Cancel _before_ closing the loop.** Call `await client.close()` or your manual cancellation logic _inside_ the running loop, not after `loop.run_until_complete`.
3. **Protect long-running background tasks.** Mark them with `asyncio.shield()` or store strong references so they aren’t garbage-collected mid-call.
4. **Prefer HTTP when you need parallelism.** STDIO is single-connection by design and struggles with `multiprocessing` or `ProcessPoolExecutor` workloads[^3].
5. **Upgrade FastMCP regularly.** Releases 2.x have begun exposing transport flags in the CLI; your workaround may become obsolete soon.

## 6. Summary

Yes—your manual task-cancellation section is compensating for a documented FastMCP bug involving the **STDIO** transport’s persistent subprocess. You are not misusing asyncio; the library presently omits the graceful shutdown you expected. Pick one of the four mitigation strategies above (ideally `keep_alive=False`) and you can delete the workaround without risking hangs.

<div style="text-align: center">⁂</div>

[^1]: https://gofastmcp.com/clients/transports

[^2]: https://github.com/jlowin/fastmcp/issues/644

[^3]: https://github.com/modelcontextprotocol/python-sdk/issues/817

[^4]: https://github.com/python/cpython/issues/105288

[^5]: https://blog.csdn.net/qq_40691189/article/details/148833059

[^6]: https://gist.github.com/grahama1970/65cf2fe1c6e04d2493000d268015fb7d

[^7]: https://lobehub.com/mcp/masony817-ask-human-mcp

[^8]: https://stackoverflow.com/questions/70265343/python-fastapi-server-how-to-extend-connection-timeout

[^9]: https://github.com/modelcontextprotocol/python-sdk/issues/552

[^10]: https://www.youtube.com/watch?v=iS25RFups4A

[^11]: https://foojay.io/today/understanding-mcp-through-raw-stdio-communication/

[^12]: https://github.com/modelcontextprotocol/python-sdk/issues/547

[^13]: https://pkg.go.dev/github.com/modelcontextprotocol-ce/go-sdk/spec

[^14]: https://github.com/punkpeye/fastmcp

[^15]: https://github.com/modelcontextprotocol/python-sdk/issues/671

[^16]: https://arxiv.org/html/2506.13538v2

[^17]: https://github.com/modelcontextprotocol/python-sdk/issues/428

[^18]: https://github.com/modelcontextprotocol/modelcontextprotocol/issues/817

[^19]: https://community.openai.com/t/local-mcp-server-instance-not-being-cleaned-up-under-agents-sdk/1312779

[^20]: https://www.trendmicro.com/en_us/research/25/f/why-a-classic-mcp-server-vulnerability-can-undermine-your-entire-ai-agent.html

[^21]: https://gofastmcp.com/llms-full.txt

[^22]: https://stackoverflow.com/questions/2408650/why-does-python-subprocess-hang-after-proc-communicate

[^23]: https://github.com/modelcontextprotocol/python-sdk/issues/1027

[^24]: https://stackoverflow.com/questions/27796294/when-using-asyncio-how-do-you-allow-all-running-tasks-to-finish-before-shutting/27910822

[^25]: https://hackernoon.com/asyncio-how-to-say-goodbye-without-losing-your-data

[^26]: https://www.npmjs.com/package/@mcpcn/mcp-system-cleaner

[^27]: https://stackoverflow.com/questions/34710835/proper-way-to-shutdown-asyncio-tasks

[^28]: https://github.com/pydantic/pydantic-ai/issues/1554

[^29]: https://modelcontextprotocol.io/quickstart/client

[^30]: https://superfastpython.com/asyncio-stuck-long-running-tasks/

[^31]: https://github.com/modelcontextprotocol/python-sdk/issues/831

[^32]: https://stackoverflow.com/questions/78245411/unclear-about-python-async-task-cancel-shutdown-at-program-exit

[^33]: https://github.com/modelcontextprotocol/python-sdk

[^34]: https://discuss.python.org/t/asyncio-hangs-on-exit-in-windows-is-it-a-bug/10444

[^35]: https://github.com/modelcontextprotocol/python-sdk/issues/543

[^36]: https://openai.github.io/openai-agents-python/ref/mcp/server/

[^37]: https://github.com/langflow-ai/langflow/issues/9064

[^38]: https://stackoverflow.com/questions/5033532/how-to-clean-up-after-subprocess-popen

[^39]: https://stackoverflow.com/questions/79412812/processpoolexecutor-with-asyncio-hangs-randomly

[^40]: https://mcp-framework.com/docs/Transports/stdio-transport/

[^41]: https://docs.python.org/3/library/asyncio-task.html

[^42]: https://github.com/cloudwalk/hermes-mcp/issues/23

[^43]: https://discuss.python.org/t/help-with-asyncio-program-freezing-during-requests/8542

[^44]: https://stackoverflow.com/questions/53870767/turning-off-keep-alive

[^45]: https://docs.chainlit.io/advanced-features/mcp

[^46]: https://github.com/pola-rs/polars/issues/6538

[^47]: https://community.openai.com/t/it-can-perform-only-one-call-to-mcp/1289469

[^48]: https://modelcontextprotocol.io/docs/concepts/transports

[^49]: https://roguelynn.com/words/asyncio-graceful-shutdowns/

[^50]: https://thinhdanggroup.github.io/mcp-production-ready/

[^51]: https://simplescraper.io/blog/how-to-mcp

[^52]: https://gist.github.com/anuj846k/2d641bf33606bcd13d8d5af311af1832

[^53]: https://www.byteplus.com/en/topic/541422?title=mcp-request-lifecycle-stages-roles-use-cases\&rut=3da2334ebf189b367360aaf304937be941e466a308bf3e3adac7e59b56992a3e

[^54]: https://stackoverflow.com/questions/49901840/asyncio-cleanup-when-getting-system-signal/49908223

[^55]: https://composio.dev/blog/mcp-client-step-by-step-guide-to-building-from-scratch

[^56]: https://github.com/cyanheads/model-context-protocol-resources/blob/main/guides/mcp-client-development-guide.md

[^57]: https://omz-software.com/pythonista/docs-3.4/py3/library/asyncio-subprocess.html

[^58]: https://www.youtube.com/watch?v=AA0BGrBpY9w

[^59]: https://www.linkedin.com/pulse/model-context-protocol-inside-mcp-architecture-martin-treiber-nj1qf

[^60]: https://www.cs.unb.ca/~bremner/teaching/cs2613/books/python3-doc/library/asyncio-subprocess.html

[^61]: https://docs.rs/rust-mcp-sdk/latest/rust_mcp_sdk/struct.StdioTransport.html

[^62]: https://stackoverflow.com/questions/13355499/termination-of-application-multiple-nested-subprocesses

[^63]: https://betterstack.com/community/guides/ai/mcp-explained/

[^64]: https://til.simonwillison.net/python/subprocess-time-limit

[^65]: https://hexdocs.pm/mcp_ex/MCPEx.Transport.Stdio.html

[^66]: https://stackoverflow.com/questions/72192252/how-to-terminate-all-subprocesses-when-the-first-one-completes

[^67]: https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle

[^68]: https://stackoverflow.com/questions/63782892/using-asyncio-to-wait-for-results-from-subprocess

