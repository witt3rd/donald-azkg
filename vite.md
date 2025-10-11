---
tags: [vite, build-tools, react, typescript, tailwind, configuration]
---

# Vite 6 Best Practices & Configuration Guide

## Overview

Vite 6 represents the latest evolution of the build tool, introducing enhanced performance optimizations, improved developer experience, and streamlined integrations with modern frameworks. This guide covers current best practices for React + TypeScript + Tailwind CSS projects in 2024-2025.

## Core Setup & Configuration

### Basic Vite 6 + React + TypeScript Configuration

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { visualizer } from "rollup-plugin-visualizer";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss({
      nesting: true, // Enable CSS nesting
    }),
    visualizer({ open: true }), // Bundle analysis
  ],
  build: {
    target: "esnext", // 18-25% smaller bundles
    minify: "esbuild",
    sourcemap: false, // Faster production builds
    terserOptions: {
      compress: { drop_console: true },
    },
  },
  server: {
    middlewareMode: "ssr", // Enhanced HMR performance
  },
  worker: {
    format: "es", // 30% faster builds in large projects
  },
});
```

### Package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "analyze": "vite build --mode production --profile"
  }
}
```

## Tailwind CSS 4 Integration

### Modern Plugin-First Architecture

The `@tailwindcss/vite` plugin eliminates the need for separate PostCSS configuration:

```bash
npm install -D tailwindcss @tailwindcss/vite
```

```typescript
// vite.config.ts
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss({
      config: "./tailwind.config.js", // Optional custom config
      nesting: true,
      analyzer: true, // Enable bundle analyzer
    }),
  ],
});
```

### CSS Layer Structure

```css
/* src/index.css */
@import "tailwindcss";

@layer base {
  /* Custom base styles */
  html {
    scroll-behavior: smooth;
  }
}

@layer components {
  /* Custom components */
  .btn-primary {
    @apply bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
  }
}

@layer utilities {
  /* Custom utilities */
  .text-shadow {
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  }
}
```

### Tailwind Configuration

```javascript
// tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      // Custom theme extensions
    },
  },
};
```

## Performance Optimization

### Bundle Analysis & Optimization

```bash
# Install bundle analyzer
npm install -D rollup-plugin-visualizer
```

Key strategies:

- **Target Modern Browsers**: Use `esnext` to skip legacy polyfills (18-25% size reduction)
- **Tree Shaking**: Use ESM imports (`lodash-es` instead of `lodash`)
- **Code Splitting**: Implement dynamic imports for large components
- **Plugin Efficiency**: Limit non-essential plugins (each adds 15-20% startup time)

### Development Performance

```typescript
export default defineConfig({
  server: {
    middlewareMode: "ssr", // 40% faster HMR in large projects
    hmr: {
      overlay: true,
    },
  },
  optimizeDeps: {
    include: ["react", "react-dom"], // Pre-bundle dependencies
  },
});
```

### Caching Strategies

Vite 6 enhances browser caching:

- Automatic module reload optimization
- Persistent dependency caching
- Smart cache invalidation

## TypeScript Configuration

### Recommended tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "module": "ESNext",
    "skipLibCheck": true,
    "allowJs": false,
    "esModuleInterop": false,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src", "vite.config.ts"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### TypeScript Node Configuration

```json
// tsconfig.node.json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}
```

## Scaling Strategies

### Large Project Optimizations

For projects with 1000+ modules:

1. **Environment API**: Use Vite 6's new environments API for conditional configs
2. **Worker Parallelism**: Configure worker format for faster builds
3. **Selective Processing**: Implement conditional plugin loading

```typescript
export default defineConfig(({ mode }) => ({
  plugins: [
    react(),
    tailwindcss(),
    ...(mode === "development" ? [visualizer()] : []),
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          utils: ["lodash-es"],
        },
      },
    },
  },
}));
```

## Production Build Configuration

### Optimized Production Settings

```typescript
export default defineConfig({
  build: {
    target: "esnext",
    minify: "esbuild", // Faster than terser
    sourcemap: false, // 15-20% faster builds
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          if (id.includes("node_modules")) {
            return "vendor";
          }
        },
      },
    },
  },
});
```

### Migration from Tailwind 3

When upgrading:

1. Remove `postcss.config.js` (handled by `@tailwindcss/vite`)
2. Update content glob patterns
3. Convert `@apply` rules to layered syntax
4. Migrate custom utilities to `@layer` directives

## Key Benefits

- **15-20% faster HMR** compared to previous setups
- **Zero-runtime CSS generation** with Tailwind 4
- **Automatic template scanning** without manual configuration
- **40% reduced initial build times** with hybrid JIT mode
- **30% faster builds** in enterprise-scale applications
- **Built-in PostCSS compatibility** without separate configuration

## Common Pitfalls to Avoid

1. **Plugin Overload**: Each plugin adds 15-20% to startup time
2. **Legacy Targets**: Using older build targets increases bundle size unnecessarily
3. **Sourcemap in Production**: Slows deployment without user benefit
4. **Disabled Caching**: Never disable dev server caching mechanisms
5. **Manual PostCSS**: Let `@tailwindcss/vite` handle CSS processing

This configuration provides an optimal balance between performance, developer experience, and scalability for modern React + TypeScript + Tailwind CSS applications using Vite 6.


## Related Concepts

### Prerequisites

- [[node]] - Vite runs on Node.js
- [[typescript]] - TypeScript configuration knowledge needed

### Related Topics

- [[react_framework]] - Vite commonly used with React
- [[tailwind]] - Guide covers Tailwind integration with Vite