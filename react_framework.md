---
tags: [react, javascript, typescript, ui, framework, patterns]
---

# React 19 Best Practices & TypeScript Guide

## Overview

React 19 introduces significant advancements in developer experience, performance optimizations, and modernization of patterns. This guide covers key features, best practices, and TypeScript integration for modern React development in 2024-2025.

## Key New Features

### 1. Actions API - Async State Management

React 19 automatically handles async operations with built-in pending states and error handling:

```typescript
import { startTransition } from "react";

function SubmitButton() {
  async function handleSubmit() {
    startTransition(async () => {
      await submitForm(data); // Automatically shows loading state
    });
  }

  return <button onClick={handleSubmit}>Submit</button>;
}
```

**Benefits:**

- Eliminates manual loading state management
- Automatic error boundaries for failed operations
- Optimistic UI updates

### 2. Simplified Refs - No More forwardRef

Function components can now accept `ref` as a regular prop:

```typescript
// Before (React 18)
const MyInput = forwardRef<HTMLInputElement, InputProps>((props, ref) => {
  return <input ref={ref} {...props} />;
});

// After (React 19)
function MyInput({
  ref,
  ...props
}: { ref?: React.Ref<HTMLInputElement> } & InputProps) {
  return <input ref={ref} {...props} />;
}
```

**Migration:**

- Use the official codemod: `npx @react/codemod@canary replace-react-fc-typescript`
- `forwardRef` is deprecated but still works

### 3. Enhanced Context API

Simplified provider syntax and performance improvements:

```typescript
const ThemeContext = createContext<"light" | "dark">("light");

// Before
function App() {
  return (
    <ThemeContext.Provider value="dark">
      <ChildComponent />
    </ThemeContext.Provider>
  );
}

// After (React 19)
function App() {
  return (
    <ThemeContext value="dark">
      <ChildComponent />
    </ThemeContext>
  );
}
```

**Performance Optimization:**

```typescript
const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  // Memoize to prevent unnecessary re-renders
  const value = useMemo(() => ({ theme, setTheme }), [theme]);

  return <ThemeContext value={value}>{children}</ThemeContext>;
};
```

### 4. Improved Hydration Error Reporting

Enhanced dev tools show detailed diffs for hydration mismatches:

```typescript
// Server renders: "2024-06-07"
// Client renders: "2024-06-08"
// Console shows exact diff with line numbers

function DateDisplay() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <div>Loading...</div>; // Prevents hydration mismatch
  }

  return <div>{new Date().toLocaleDateString()}</div>;
}
```

### 5. Web Components Support

First-class integration with custom elements:

```typescript
// Type declaration for custom elements
declare global {
  namespace JSX {
    interface IntrinsicElements {
      "custom-button": React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & {
          label?: string;
          variant?: "primary" | "secondary";
        },
        HTMLElement
      >;
    }
  }
}

// Usage
function App() {
  return (
    <div>
      <custom-button label="Click me" variant="primary" />
    </div>
  );
}
```

## TypeScript Best Practices

### Component Props with Refs

```typescript
interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  ref?: React.Ref<HTMLButtonElement>;
}

function Button({ children, onClick, ref }: ButtonProps) {
  return (
    <button ref={ref} onClick={onClick}>
      {children}
    </button>
  );
}

// Usage with ref
function App() {
  const buttonRef = useRef<HTMLButtonElement>(null);

  return <Button ref={buttonRef}>Click me</Button>;
}
```

### Context Type Safety

```typescript
interface AppContextType {
  user: User | null;
  theme: "light" | "dark";
  updateUser: (user: User) => void;
  toggleTheme: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

// Custom hook with type safety
function useAppContext() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error("useAppContext must be used within AppProvider");
  }
  return context;
}

// Provider component
function AppProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [theme, setTheme] = useState<"light" | "dark">("light");

  const value = useMemo(
    () => ({
      user,
      theme,
      updateUser: setUser,
      toggleTheme: () =>
        setTheme((prev) => (prev === "light" ? "dark" : "light")),
    }),
    [user, theme]
  );

  return <AppContext value={value}>{children}</AppContext>;
}
```

### Async Components (Server Components)

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

// Server component
async function UserProfile({ userId }: { userId: string }) {
  const user = await fetchUser(userId); // Runs at build time or request time

  return (
    <div className="user-profile">
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}

// Client component that uses server component
function UserPage({ userId }: { userId: string }) {
  return (
    <div>
      <UserProfile userId={userId} />
      <UserActions userId={userId} /> {/* Client-side interactivity */}
    </div>
  );
}
```

## Performance Patterns

### 1. Optimized State Updates

```typescript
function OptimizedComponent() {
  const [state, setState] = useState({ count: 0, name: "" });

  // Good: Update only what changed
  const incrementCount = useCallback(() => {
    setState((prev) => ({ ...prev, count: prev.count + 1 }));
  }, []);

  // Good: Batch updates automatically handled in React 19
  const handleBatchedUpdates = () => {
    setState((prev) => ({ ...prev, count: prev.count + 1 }));
    setState((prev) => ({ ...prev, name: "Updated" }));
    // Both updates batched automatically
  };

  return (
    <div>
      <p>Count: {state.count}</p>
      <p>Name: {state.name}</p>
      <button onClick={incrementCount}>Increment</button>
      <button onClick={handleBatchedUpdates}>Batch Update</button>
    </div>
  );
}
```

### 2. Memoization Best Practices

```typescript
interface ExpensiveComponentProps {
  items: Item[];
  onItemClick: (id: string) => void;
}

const ExpensiveComponent = memo(
  ({ items, onItemClick }: ExpensiveComponentProps) => {
    const expensiveValue = useMemo(() => {
      return items.reduce((acc, item) => acc + item.value, 0);
    }, [items]);

    return (
      <div>
        <p>Total: {expensiveValue}</p>
        {items.map((item) => (
          <Item key={item.id} item={item} onClick={onItemClick} />
        ))}
      </div>
    );
  }
);
```

### 3. Error Boundaries for Async Operations

```typescript
class AsyncErrorBoundary extends Component<
  { children: React.ReactNode },
  { hasError: boolean; error?: Error }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Async operation failed:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h2>Something went wrong with async operation</h2>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Common Patterns

### 1. Custom Hooks with Actions

```typescript
function useAsyncAction<T>(
  action: () => Promise<T>
): [T | null, boolean, Error | null, () => void] {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const execute = useCallback(() => {
    startTransition(async () => {
      setLoading(true);
      setError(null);
      try {
        const result = await action();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err : new Error("Unknown error"));
      } finally {
        setLoading(false);
      }
    });
  }, [action]);

  return [data, loading, error, execute];
}

// Usage
function DataComponent() {
  const [data, loading, error, fetchData] = useAsyncAction(() =>
    fetch("/api/data").then((res) => res.json())
  );

  return (
    <div>
      <button onClick={fetchData} disabled={loading}>
        {loading ? "Loading..." : "Fetch Data"}
      </button>
      {error && <p>Error: {error.message}</p>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}
```

### 2. Form Handling with Actions

```typescript
interface FormData {
  email: string;
  password: string;
}

function LoginForm() {
  const [formData, setFormData] = useState<FormData>({
    email: "",
    password: "",
  });
  const [pending, setPending] = useState(false);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    startTransition(async () => {
      setPending(true);
      try {
        await submitLogin(formData);
        // Success handling
      } catch (error) {
        // Error handling
      } finally {
        setPending(false);
      }
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={formData.email}
        onChange={(e) =>
          setFormData((prev) => ({ ...prev, email: e.target.value }))
        }
        disabled={pending}
      />
      <input
        type="password"
        value={formData.password}
        onChange={(e) =>
          setFormData((prev) => ({ ...prev, password: e.target.value }))
        }
        disabled={pending}
      />
      <button type="submit" disabled={pending}>
        {pending ? "Signing in..." : "Sign in"}
      </button>
    </form>
  );
}
```

## Migration Strategy

### 1. Gradual Adoption

```typescript
// Feature flag approach
const FEATURES = {
  newRefSyntax: true,
  enhancedContext: true,
  serverComponents: false, // Gradually enable
};

function ConditionalComponent() {
  if (FEATURES.newRefSyntax) {
    return <NewRefComponent />;
  }
  return <LegacyRefComponent />;
}
```

### 2. Dependency Updates

```bash
# Update to React 19
npm install react@19 react-dom@19 @types/react@19 @types/react-dom@19

# Update related packages
npm install @vitejs/plugin-react@latest

# Run codemods for automatic migration
npx @react/codemod@canary replace-react-fc-typescript
```

### 3. Testing Strategy

```typescript
// Test async components
import { render, screen, waitFor } from "@testing-library/react";
import { act } from "react";

test("async component handles loading states", async () => {
  render(<AsyncComponent />);

  expect(screen.getByText("Loading...")).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText("Data loaded")).toBeInTheDocument();
  });
});

// Test new ref syntax
test("ref forwarding works without forwardRef", () => {
  const ref = createRef<HTMLInputElement>();
  render(<MyInput ref={ref} />);

  expect(ref.current).toBeInstanceOf(HTMLInputElement);
});
```

## Browser Support

React 19 requires modern browser features:

- **Minimum versions**: Chrome 80+, Firefox 78+, Safari 14+, Edge 80+
- **Node.js**: 18.17.0+ for development

## Key Benefits

- **40% less boilerplate** in typical applications
- **30% faster initial load times** with server components
- **Improved developer experience** with better error messages
- **Enhanced type safety** with simplified ref handling
- **Automatic performance optimizations** with the new concurrent features

This guide provides a foundation for adopting React 19's modern patterns while maintaining type safety and performance in TypeScript applications.


## Related Concepts

### Prerequisites

- [[typescript]] - React commonly uses TypeScript for type safety
- [[node]] - React development uses Node.js tooling

### Related Topics

- [[vite]] - Vite is common build tool for React
- [[tailwind]] - Tailwind commonly used for styling React apps

### Extended By

- [[react_agent_pattern]] - Specific pattern for React-based agents