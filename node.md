---
tags: [nodejs, javascript, typescript, runtime, performance, security]
---
# Node.js 24 Features & Best Practices Guide

## Overview

Node.js 24 represents a significant milestone in the evolution of server-side JavaScript, introducing native TypeScript support, enhanced security controls, and substantial performance improvements. Released in 2024-2025, this version solidifies Node.js as a high-performance runtime for modern web applications.

## Performance Enhancements

### V8 Engine 13.6 Upgrade

The updated V8 engine brings substantial performance improvements:

- **30% faster HTTP request handling** in production benchmarks
- **Improved memory optimization** through enhanced pointer compression
- **Enhanced JavaScript promise handling** with optimized microtask queues

### Undici v7 Integration

Node.js 24 includes Undici v7 for superior HTTP performance:

```javascript
import { request } from "undici";

// HTTP/2 multiplexing example
const { body } = await request("http://localhost:3000", {
  method: "GET",
  headers: { Accept: "application/json" },
});

console.log(await body.json());
```

**Key improvements:**

- **40% faster connection pooling** compared to previous versions
- **Automated load balancing** across HTTP/2 streams
- **Smart retry mechanisms** for failed requests
- **Connection multiplexing** support

### Stream Optimization

Enhanced stream processing delivers:

- **25% throughput increase** in I/O-heavy operations
- **Reduced latency** through rewritten scheduler core
- **Zero-copy buffer handling** for large datasets

```javascript
import { createReadStream } from "fs";
import { pipeline } from "stream/promises";

// Optimized stream processing
await pipeline(
  createReadStream("large-file.txt"),
  new TransformStream(),
  process.stdout
);
```

## Native TypeScript Integration

### Lightweight Type Stripping

Node.js 24 can execute TypeScript files directly by stripping type annotations:

```typescript
// app.mts - runs directly with node app.mts
interface User {
  id: number;
  name: string;
  email: string;
}

function greet(user: User): void {
  console.log(`Hello ${user.name}!`);
}

const user: User = { id: 1, name: "Alice", email: "alice@example.com" };
greet(user);
```

**File extensions supported:**

- `.mts` - TypeScript ES modules
- `.cts` - TypeScript CommonJS modules
- `.ts` - Standard TypeScript files

### Full TypeScript Support

For complete TypeScript features including `tsconfig.json` support:

```bash
# Install tsx for full TypeScript support
npm install --save-dev tsx

# Run with full type checking
node --import=tsx app.ts
```

```typescript
// tsconfig.json integration
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true
  }
}
```

**Benefits:**

- Eliminates separate compilation steps
- Native ES Modules support for TypeScript
- Direct execution of TypeScript test files
- Maintains full type safety during development

## Security Features

### Permission Model

Node.js 24 introduces a production-ready permission system for enhanced security:

```bash
# Restrict file system access
node --allow-fs-read=/safe/directory --allow-fs-write=/logs app.js

# Control network access
node --allow-net=example.com:443 app.js

# Combine multiple permissions
node --allow-fs-read=/data --allow-net --allow-env app.js
```

**Permission Categories:**

| Permission Flag           | Functionality                        | Example                       |
| ------------------------- | ------------------------------------ | ----------------------------- |
| `--allow-fs-read=<path>`  | Read access to specific directories  | `--allow-fs-read=/app/config` |
| `--allow-fs-write=<path>` | Write access to specific directories | `--allow-fs-write=/app/logs`  |
| `--allow-net[=<host>]`    | Network access control               | `--allow-net=api.example.com` |
| `--allow-child`           | Child process creation               | For build tools               |
| `--allow-env[=<var>]`     | Environment variable access          | `--allow-env=NODE_ENV`        |

### Runtime Permission Checks

```typescript
import permission from "node:permission";

// Check permissions at runtime
if (permission.has("fs.write", "/app/logs")) {
  await writeLog("Application started");
}

// Graceful degradation
if (permission.has("net.outbound", "api.example.com")) {
  await fetchExternalData();
} else {
  console.warn("External API access restricted");
}
```

## Modern JavaScript Features

### Stable Fetch API

Browser-compatible fetch is now stable and optimized:

```typescript
// Modern ESM-compatible fetch
const response = await fetch("https://api.example.com/data", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: "example" }),
});

// Stream processing
const reader = response.body?.getReader();
while (true) {
  const { done, value } = await reader!.read();
  if (done) break;
  console.log(new TextDecoder().decode(value));
}
```

**Performance benefits:**

- **15% faster JSON parsing** than legacy `http` module
- Native support for chunked data processing
- Seamless integration with ESM module system

### Global URLPattern

Unified route matching across server and client:

```typescript
// Route pattern matching
const pattern = new URLPattern({
  pathname: "/users/:id/posts/:postId",
});

// Test URLs
console.log(pattern.test("https://example.com/users/123/posts/456")); // true

// Extract parameters
const match = pattern.exec("https://example.com/users/123/posts/456");
console.log(match?.pathname.groups); // { id: '123', postId: '456' }
```

### Enhanced WebStreams

```typescript
// Readable stream from async generator
async function* generateData() {
  for (let i = 0; i < 1000; i++) {
    yield `data-${i}\n`;
  }
}

const stream = new ReadableStream({
  async start(controller) {
    for await (const chunk of generateData()) {
      controller.enqueue(new TextEncoder().encode(chunk));
    }
    controller.close();
  },
});
```

## AsyncLocalStorage

Enhanced asynchronous context management with improved performance:

```typescript
import { AsyncLocalStorage } from "async_hooks";

interface RequestContext {
  requestId: string;
  userId?: string;
  startTime: number;
}

const requestContext = new AsyncLocalStorage<RequestContext>();

// Express middleware example
function contextMiddleware(req: Request, res: Response, next: NextFunction) {
  const context: RequestContext = {
    requestId: crypto.randomUUID(),
    startTime: Date.now(),
  };

  requestContext.run(context, () => {
    next();
  });
}

// Use context anywhere in the request lifecycle
function logOperation(operation: string) {
  const context = requestContext.getStore();
  if (context) {
    console.log(
      `[${context.requestId}] ${operation} at ${
        Date.now() - context.startTime
      }ms`
    );
  }
}

// Database query with automatic context
async function findUser(id: string) {
  logOperation("Database query started");
  const user = await db.users.findById(id);
  logOperation("Database query completed");
  return user;
}
```

**Performance improvements:**

- **60% reduction in context propagation latency**
- Enhanced async stack traces for debugging
- Backward-compatible API for existing applications

## Built-in Module Enhancements

### Enhanced Test Runner

The `node:test` module now supports TypeScript and advanced testing patterns:

```typescript
import { test, describe, beforeEach, afterEach } from "node:test";
import assert from "node:assert";

describe("User Service", () => {
  let userService: UserService;

  beforeEach(() => {
    userService = new UserService();
  });

  test("should create user with valid data", async (t) => {
    const userData = { name: "Alice", email: "alice@example.com" };
    const user = await userService.createUser(userData);

    assert.strictEqual(user.name, userData.name);
    assert.strictEqual(user.email, userData.email);
    assert.ok(user.id);
  });

  test("should validate email format", async (t) => {
    await assert.rejects(
      () => userService.createUser({ name: "Bob", email: "invalid" }),
      { name: "ValidationError" }
    );
  });
});
```

### File System Enhancements

Improved `fs/promises` with better TypeScript support:

```typescript
import { readFile, writeFile, watch } from "fs/promises";
import { join } from "path";

// Type-safe file operations
interface ConfigFile {
  apiUrl: string;
  timeout: number;
  features: string[];
}

async function loadConfig(): Promise<ConfigFile> {
  const configPath = join(process.cwd(), "config.json");
  const content = await readFile(configPath, "utf-8");
  return JSON.parse(content) as ConfigFile;
}

// File watching with async iteration
for await (const event of watch("./src", { recursive: true })) {
  if (event.filename?.endsWith(".ts")) {
    console.log(`TypeScript file changed: ${event.filename}`);
  }
}
```

### Crypto Module Updates

Enhanced cryptographic operations:

```typescript
import { webcrypto } from "crypto";

// Web Crypto API integration
async function generateKeyPair() {
  return await webcrypto.subtle.generateKey(
    {
      name: "RSA-OAEP",
      modulusLength: 2048,
      publicExponent: new Uint8Array([1, 0, 1]),
      hash: "SHA-256",
    },
    true,
    ["encrypt", "decrypt"]
  );
}

// Modern hashing
async function hashPassword(password: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await webcrypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(hashBuffer))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}
```

## Ecosystem Updates

### npm 11 Integration

Node.js 24 ships with npm 11, providing:

- **35% faster dependency installation** through parallel resolution
- **Improved TypeScript declaration file handling**
- **Smart peer dependency conflict resolution**
- **Enhanced security audit capabilities**

```bash
# Faster installation with parallel processing
npm install --parallel

# Better TypeScript integration
npm install @types/node --save-dev

# Security improvements
npm audit --audit-level=moderate
```

### ES Modules First

Default module system optimizations:

```typescript
// package.json
{
  "type": "module",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  }
}
```

## Migration Guide

### From Node.js 20/22 to 24

**1. Update Dependencies:**

```bash
# Update Node.js
nvm install 24
nvm use 24

# Update package.json
npm update

# Update TypeScript if using
npm install typescript@latest @types/node@latest
```

**2. Enable Native TypeScript:**

```bash
# Option 1: Direct execution (lightweight)
node app.mts

# Option 2: Full TypeScript support
npm install --save-dev tsx
node --import=tsx app.ts
```

**3. Adopt Permission Model:**

```bash
# Development
node --allow-fs-read=. --allow-net app.js

# Production
node --allow-fs-read=/app --allow-fs-write=/logs --allow-net=api.internal app.js
```

**4. Update Fetch Usage:**

```typescript
// Replace node-fetch with native fetch
// Before
import fetch from "node-fetch";

// After (built-in)
// No import needed - fetch is global
```

### Breaking Changes Checklist

- [ ] **Windows Build Tools**: Requires ClangCL instead of MSVC
- [ ] **Legacy HTTP**: Consider migrating to fetch for new code
- [ ] **CommonJS**: Plan migration to ESM where possible
- [ ] **Security**: Review file system access patterns for permission model

## Best Practices

### TypeScript Development

```typescript
// Use strict TypeScript configuration
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}

// Leverage native types
interface ServerConfig {
  readonly port: number;
  readonly host: string;
  readonly features: readonly string[];
}
```

### Performance Optimization

```typescript
// Use AsyncLocalStorage for request context
const requestContext = new AsyncLocalStorage<RequestContext>();

// Prefer fetch over legacy HTTP
const response = await fetch(url, {
  signal: AbortSignal.timeout(5000),
});

// Leverage streams for large data
async function* processLargeFile(filename: string) {
  const stream = createReadStream(filename);
  for await (const chunk of stream) {
    yield processChunk(chunk);
  }
}
```

### Security Implementation

```typescript
// Runtime permission checks
function secureFileOperation(path: string) {
  if (!permission.has("fs.write", path)) {
    throw new Error("Insufficient permissions for file write");
  }
  return writeFile(path, data);
}

// Environment variable validation
const config = {
  apiKey:
    process.env.API_KEY ||
    (() => {
      if (!permission.has("env.read", "API_KEY")) {
        throw new Error("API_KEY access denied");
      }
      return undefined;
    })(),
};
```

## Browser Compatibility

Node.js 24 features align closely with modern browser APIs:

- **93% coverage of browser API surface** for isomorphic JavaScript
- **Native fetch compatibility** with browser implementations
- **WebCrypto API alignment** for consistent cryptographic operations
- **URL and URLPattern compatibility** for universal routing

## Key Benefits Summary

- **40% reduction in TypeScript build complexity** through native support
- **30% faster HTTP operations** with Undici v7 integration
- **Enhanced security** through granular permission controls
- **Improved developer experience** with better error messages and debugging
- **Future-proof architecture** with modern JavaScript standard alignment

Node.js 24 represents a significant step forward in server-side JavaScript development, offering improved performance, enhanced security, and native TypeScript support that reduces toolchain complexity while maintaining enterprise-grade capabilities.

## Related Concepts

### Related Topics
- [[typescript]] - Node.js 24 provides native TypeScript support
- [[react_framework]] - Node.js provides runtime for React development
- [[vite]] - Vite runs on Node.js runtime

### Extended By
- [[react_framework]] - Node.js provides runtime environment for React development
- [[vite]] - Vite runs on Node.js runtime
- [[motion_canvas_cheatsheet]] - Motion Canvas runs on Node.js runtime