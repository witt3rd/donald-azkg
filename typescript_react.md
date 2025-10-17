---
tags: [typescript, javascript, types, async, programming, guide]
---
# TypeScript React Developer - Modern Stack Coding Standards

## Core Technology Stack Standards

### TypeScript 5.8+ Modern Language Features

**Use built-in types directly** - `typing.List`, `typing.Dict` equivalents are deprecated:

```typescript
// ✅ Correct - Use built-in types (TypeScript 5.8+)
function processItems(items: string[]): Record<string, number> {
  return items.reduce((acc, item) => ({ ...acc, [item]: item.length }), {});
}

// ❌ Avoid - Deprecated generic aliases
import { Array as ArrayType, Record as RecordType } from "some-types-lib";
function processItems(items: ArrayType<string>): RecordType<string, number> {
  return items.reduce((acc, item) => ({ ...acc, [item]: item.length }), {});
}
```

**Enhanced conditional type inference** - TypeScript 5.8 eliminates manual type assertions:

```typescript
// ✅ TypeScript 5.8 - Automatic inference
async function fetchData<T extends "user" | "post">(
  type: T
): Promise<T extends "user" ? User : Post> {
  const response = await fetch(`/api/${type}s`);
  return response.json(); // Correctly typed without assertions
}

// ❌ Before - Required manual assertions
async function fetchData(type: "user" | "post"): Promise<User | Post> {
  const response = await fetch(`/api/${type}s`);
  return response.json() as User | Post;
}
```

**Required type annotations:**

- All function parameters and return types
- Interface properties with complex types
- Component prop interfaces
- API response and request types
- Event handler signatures

### Documentation Standards - JSDoc Style

**Use comprehensive JSDoc comments** for all public APIs:

````typescript
/**
 * Extracts and processes user data from external API.
 *
 * @param userId - Unique identifier for the user
 * @param options - Configuration options for data fetching
 * @param options.includeProfile - Whether to include profile data
 * @param options.maxRetries - Maximum number of retry attempts
 * @returns Promise resolving to processed user data
 *
 * @throws {ValidationError} When userId format is invalid
 * @throws {NetworkError} When API request fails after retries
 *
 * @example
 * ```typescript
 * const user = await fetchUserData('user-123', {
 *   includeProfile: true,
 *   maxRetries: 3
 * });
 * console.log(user.name); // Type-safe access
 * ```
 */
async function fetchUserData(
  userId: string,
  options: FetchOptions = {}
): Promise<ProcessedUserData> {
  // Implementation
}
````

**Documentation requirements:**

- Keep lines under 80 characters for editor compatibility
- Include all parameters with types and descriptions
- Document return values with specific types
- List possible exceptions with conditions
- Provide realistic, runnable examples
- Use present tense ("Extracts data" not "Extract data")

## React 19 + TypeScript Integration

### Modern Component Patterns

**Use React 19 Actions API with TypeScript:**

```typescript
interface FormState {
  success: boolean;
  message: string;
  errors?: Record<string, string>;
}

interface UserFormProps {
  onSubmit: (formData: FormData) => Promise<FormState>;
  initialData?: Partial<User>;
}

const UserForm: React.FC<UserFormProps> = ({ onSubmit, initialData }) => {
  const [state, formAction, isPending] = useActionState(onSubmit, {
    success: false,
    message: "",
  });

  return (
    <form action={formAction}>
      <input
        name="email"
        type="email"
        defaultValue={initialData?.email}
        required
      />
      <button type="submit" disabled={isPending}>
        {isPending ? "Saving..." : "Save User"}
      </button>
      {state.message && (
        <div className={state.success ? "text-green-600" : "text-red-600"}>
          {state.message}
        </div>
      )}
    </form>
  );
};
```

**Enhanced refs with TypeScript:**

```typescript
// React 19 simplified ref patterns
interface CustomInputProps {
  placeholder: string;
  onValueChange: (value: string) => void;
}

const CustomInput = ({ placeholder, onValueChange }: CustomInputProps) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const focus = () => {
    inputRef.current?.focus();
  };

  // React 19 - expose imperative API
  useImperativeHandle(ref, () => ({
    focus,
    getValue: () => inputRef.current?.value || "",
    clear: () => {
      if (inputRef.current) inputRef.current.value = "";
    },
  }));

  return (
    <input
      ref={inputRef}
      placeholder={placeholder}
      onChange={(e) => onValueChange(e.target.value)}
      className="px-3 py-2 border border-gray-300 rounded-md"
    />
  );
};
```

### Error Handling Patterns

**Comprehensive error boundaries with TypeScript:**

```typescript
interface ErrorInfo {
  componentStack: string;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

class ErrorBoundary extends React.Component<
  React.PropsWithChildren<{}>,
  ErrorBoundaryState
> {
  constructor(props: React.PropsWithChildren<{}>) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Error caught by boundary:", error, errorInfo);

    // Log to error reporting service
    reportError(error, {
      componentStack: errorInfo.componentStack,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-2">
              Something went wrong
            </h2>
            <p className="text-gray-600 mb-4">
              We're sorry, but something unexpected happened.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="btn-primary w-full"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Node.js 24 + TypeScript Integration

### Native TypeScript Support

**Direct TypeScript execution with Node.js 24:**

```typescript
// app.mts - runs directly with `node app.mts`
interface ServerConfig {
  readonly port: number;
  readonly host: string;
  readonly apiKey: string;
}

const config: ServerConfig = {
  port: parseInt(process.env.PORT || "3000"),
  host: process.env.HOST || "localhost",
  apiKey: process.env.API_KEY || "",
};

// Type-safe environment validation
function validateConfig(config: ServerConfig): void {
  if (!config.apiKey) {
    throw new Error("API_KEY environment variable is required");
  }
  if (config.port < 1 || config.port > 65535) {
    throw new Error("PORT must be between 1 and 65535");
  }
}

validateConfig(config);

// Modern fetch with proper error handling
async function startServer(): Promise<void> {
  try {
    const server = Bun.serve({
      port: config.port,
      hostname: config.host,
      fetch: handleRequest,
    });

    console.log(`Server running at http://${config.host}:${config.port}`);
  } catch (error) {
    console.error("Failed to start server:", error);
    process.exit(1);
  }
}

startServer();
```

### Permission Model Integration

**Security-first development with Node.js 24:**

```typescript
import { permission } from "node:permission";

interface SecureFileOperations {
  canRead(path: string): boolean;
  canWrite(path: string): boolean;
  safeReadFile(path: string): Promise<string | null>;
}

class SecureFileManager implements SecureFileOperations {
  canRead(path: string): boolean {
    return permission.has("fs.read", path);
  }

  canWrite(path: string): boolean {
    return permission.has("fs.write", path);
  }

  async safeReadFile(path: string): Promise<string | null> {
    if (!this.canRead(path)) {
      console.warn(`Read access denied for ${path}`);
      return null;
    }

    try {
      const { readFile } = await import("fs/promises");
      return await readFile(path, "utf-8");
    } catch (error) {
      console.error(`Failed to read file ${path}:`, error);
      return null;
    }
  }
}

// Usage with runtime permission checks
const fileManager = new SecureFileManager();
const content = await fileManager.safeReadFile("/app/config.json");
```

## Tailwind CSS 4.0 Integration

### CSS-First Configuration

**Modern Tailwind setup with TypeScript:**

```css
/* src/styles/main.css */
@import "tailwindcss";

@theme {
  /* Type-safe custom properties */
  --color-brand-primary: oklch(0.62 0.17 256.57);
  --color-brand-secondary: oklch(0.8 0.1 120);
  --font-display: "Satoshi", system-ui, sans-serif;
  --breakpoint-xs: 475px;
  --spacing-safe: env(safe-area-inset-bottom);
}

@layer base {
  html {
    scroll-behavior: smooth;
    font-family: var(--font-display);
  }

  body {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
}

@layer components {
  .btn {
    @apply inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2;
  }

  .btn-primary {
    @apply bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500;
  }

  .card {
    @apply bg-white rounded-lg shadow-sm border border-gray-200 p-6;
  }
}

@layer utilities {
  .text-shadow {
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  }

  .pb-safe {
    padding-bottom: var(--spacing-safe);
  }
}
```

**Component styling with TypeScript:**

```typescript
interface ButtonProps {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

const Button: React.FC<ButtonProps> = ({
  variant = "primary",
  size = "md",
  loading = false,
  children,
  onClick,
}) => {
  const baseClasses = "btn";
  const variantClasses = {
    primary: "btn-primary",
    secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300",
    ghost: "bg-transparent hover:bg-gray-100",
  };
  const sizeClasses = {
    sm: "px-3 py-1.5 text-xs",
    md: "px-4 py-2 text-sm",
    lg: "px-6 py-3 text-base",
  };

  const className = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`;

  return (
    <button className={className} onClick={onClick} disabled={loading}>
      {loading ? (
        <div className="flex items-center gap-2">
          <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
          Loading...
        </div>
      ) : (
        children
      )}
    </button>
  );
};
```

### Container Queries with TypeScript

```typescript
interface ResponsiveCardProps {
  data: CardData;
  adaptToContainer?: boolean;
}

const ResponsiveCard: React.FC<ResponsiveCardProps> = ({
  data,
  adaptToContainer = false,
}) => {
  const containerClass = adaptToContainer ? "@container" : "";
  const responsiveClasses = adaptToContainer
    ? "@md:grid @md:grid-cols-2 @lg:grid-cols-3"
    : "md:grid md:grid-cols-2 lg:grid-cols-3";

  return (
    <div className={containerClass}>
      <div className={`card ${responsiveClasses}`}>
        <h3 className="@lg:text-xl font-semibold">{data.title}</h3>
        <p className="text-gray-600 @md:text-sm">{data.description}</p>
      </div>
    </div>
  );
};
```

## Vite 6 Configuration Standards

### Optimized Development Setup

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { visualizer } from "rollup-plugin-visualizer";

export default defineConfig(({ mode }) => ({
  plugins: [
    react({
      jsxImportSource: "@emotion/react",
      babel: {
        plugins: ["@emotion/babel-plugin"],
      },
    }),
    tailwindcss({
      nesting: true,
      analyzer: mode === "development",
    }),
    ...(mode === "production"
      ? [
          visualizer({
            filename: "dist/stats.html",
            open: true,
            gzipSize: true,
          }),
        ]
      : []),
  ],

  build: {
    target: "esnext", // 18-25% smaller bundles
    minify: "esbuild",
    sourcemap: mode === "development",
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          ui: ["@headlessui/react", "@heroicons/react"],
        },
      },
    },
  },

  server: {
    middlewareMode: "ssr", // 40% faster HMR
    hmr: {
      overlay: true,
    },
  },

  optimizeDeps: {
    include: ["react", "react-dom", "@emotion/react"],
  },

  resolve: {
    alias: {
      "@": "/src",
      "@components": "/src/components",
      "@utils": "/src/utils",
      "@types": "/src/types",
    },
  },
}));
```

### TypeScript Configuration

```json
// tsconfig.json - Optimized for modern development
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
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"],
      "@types/*": ["src/types/*"]
    }
  },
  "include": ["src", "vite.config.ts"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

## Performance and Optimization

### Efficient React Patterns

```typescript
// Memoization strategies with TypeScript
interface UserListProps {
  users: User[];
  onUserSelect: (userId: string) => void;
  selectedUserId?: string;
}

const UserList: React.FC<UserListProps> = React.memo(
  ({ users, onUserSelect, selectedUserId }) => {
    // Stable callback reference
    const handleUserClick = useCallback(
      (userId: string) => {
        onUserSelect(userId);
      },
      [onUserSelect]
    );

    // Computed values with proper dependencies
    const sortedUsers = useMemo(() => {
      return [...users].sort((a, b) => a.name.localeCompare(b.name));
    }, [users]);

    // Expensive computations
    const userStats = useMemo(() => {
      return {
        total: users.length,
        active: users.filter((u) => u.isActive).length,
        premium: users.filter((u) => u.isPremium).length,
      };
    }, [users]);

    return (
      <div className="space-y-2">
        <div className="text-sm text-gray-600 mb-4">
          {userStats.total} users ({userStats.active} active,{" "}
          {userStats.premium} premium)
        </div>

        {sortedUsers.map((user) => (
          <UserCard
            key={user.id}
            user={user}
            isSelected={user.id === selectedUserId}
            onClick={handleUserClick}
          />
        ))}
      </div>
    );
  }
);

// Custom hooks for reusable logic
function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  const setValue = useCallback(
    (value: T) => {
      try {
        setStoredValue(value);
        window.localStorage.setItem(key, JSON.stringify(value));
      } catch (error) {
        console.error(`Error setting localStorage key "${key}":`, error);
      }
    },
    [key]
  );

  return [storedValue, setValue];
}
```

### Bundle Optimization

```typescript
// Code splitting with TypeScript
import { lazy, Suspense } from "react";

// Lazy load components
const Dashboard = lazy(() => import("@/pages/Dashboard"));
const Settings = lazy(() => import("@/pages/Settings"));
const Profile = lazy(() => import("@/pages/Profile"));

// Loading fallback component
const LoadingSpinner: React.FC = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
  </div>
);

// Route-based code splitting
const AppRouter: React.FC = () => {
  return (
    <Routes>
      <Route
        path="/dashboard"
        element={
          <Suspense fallback={<LoadingSpinner />}>
            <Dashboard />
          </Suspense>
        }
      />
      <Route
        path="/settings"
        element={
          <Suspense fallback={<LoadingSpinner />}>
            <Settings />
          </Suspense>
        }
      />
      <Route
        path="/profile"
        element={
          <Suspense fallback={<LoadingSpinner />}>
            <Profile />
          </Suspense>
        }
      />
    </Routes>
  );
};
```

## Testing Standards

### Component Testing with TypeScript

```typescript
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, test, expect, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { UserForm } from "@/components/UserForm";

// Mock implementations with proper typing
const mockOnSubmit = vi.fn<[FormData], Promise<FormState>>();

describe("UserForm", () => {
  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  test("should render form with required fields", () => {
    render(<UserForm onSubmit={mockOnSubmit} />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /save/i })).toBeInTheDocument();
  });

  test("should validate email format", async () => {
    const user = userEvent.setup();
    render(<UserForm onSubmit={mockOnSubmit} />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole("button", { name: /save/i });

    await user.type(emailInput, "invalid-email");
    await user.click(submitButton);

    expect(screen.getByText(/invalid email format/i)).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test("should submit form with valid data", async () => {
    const user = userEvent.setup();
    const mockFormState: FormState = {
      success: true,
      message: "User saved successfully",
    };

    mockOnSubmit.mockResolvedValue(mockFormState);

    render(<UserForm onSubmit={mockOnSubmit} />);

    await user.type(screen.getByLabelText(/email/i), "test@example.com");
    await user.type(screen.getByLabelText(/name/i), "John Doe");
    await user.click(screen.getByRole("button", { name: /save/i }));

    await waitFor(() => {
      expect(screen.getByText(/user saved successfully/i)).toBeInTheDocument();
    });

    expect(mockOnSubmit).toHaveBeenCalledWith(expect.any(FormData));
  });
});

// Custom testing utilities
interface RenderWithProvidersOptions {
  initialEntries?: string[];
  user?: Partial<User>;
}

function renderWithProviders(
  ui: React.ReactElement,
  options: RenderWithProvidersOptions = {}
) {
  const { initialEntries = ["/"], user = defaultUser } = options;

  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <MemoryRouter initialEntries={initialEntries}>
        <AuthProvider user={user}>
          <QueryClient>{children}</QueryClient>
        </AuthProvider>
      </MemoryRouter>
    );
  }

  return render(ui, { wrapper: Wrapper });
}
```

## Advanced React 19 Patterns

### Actions API and Async State Management

**Enhanced async transitions with startTransition:**

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

### Simplified Refs - No More forwardRef

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

### Enhanced Context API

Simplified provider syntax with performance improvements:

```typescript
const ThemeContext = createContext<"light" | "dark">("light");

// React 19 - Direct context usage
function App() {
  return (
    <ThemeContext value="dark">
      <ChildComponent />
    </ThemeContext>
  );
}

// Performance-optimized provider
const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  // Memoize to prevent unnecessary re-renders
  const value = useMemo(() => ({ theme, setTheme }), [theme]);

  return <ThemeContext value={value}>{children}</ThemeContext>;
};
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

### Custom Hooks with Actions

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

### Form Handling with Actions

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

### Web Components Integration

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

## Security Standards

### Input Validation and Sanitization

```typescript
import { z } from "zod";

// Zod schemas for type-safe validation
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(13).max(120),
  role: z.enum(["user", "admin", "moderator"]),
});

const CreateUserSchema = UserSchema.omit({ id: true });

type User = z.infer<typeof UserSchema>;
type CreateUserRequest = z.infer<typeof CreateUserSchema>;

// Validation utilities
function validateInput<T>(
  schema: z.ZodSchema<T>,
  input: unknown
): { success: true; data: T } | { success: false; errors: string[] } {
  try {
    const data = schema.parse(input);
    return { success: true, data };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        success: false,
        errors: error.errors.map((e) => `${e.path.join(".")}: ${e.message}`),
      };
    }
    return { success: false, errors: ["Validation failed"] };
  }
}

// API endpoint with validation
async function createUser(req: Request, res: Response) {
  const validation = validateInput(CreateUserSchema, req.body);

  if (!validation.success) {
    return res.status(400).json({
      error: "Validation failed",
      details: validation.errors,
    });
  }

  try {
    const user = await userService.createUser(validation.data);
    res.status(201).json(user);
  } catch (error) {
    console.error("User creation failed:", error);
    res.status(500).json({ error: "Internal server error" });
  }
}

// XSS Prevention
function sanitizeHtml(input: string): string {
  return input
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#x27;")
    .replace(/\//g, "&#x2F;");
}

// CSRF Protection
interface CSRFProtectedRequest extends Request {
  csrfToken(): string;
}

function requireCSRF(
  req: CSRFProtectedRequest,
  res: Response,
  next: NextFunction
) {
  const token = req.headers["x-csrf-token"] || req.body._csrf;
  const expectedToken = req.csrfToken();

  if (token !== expectedToken) {
    return res.status(403).json({ error: "Invalid CSRF token" });
  }

  next();
}
```

## Restrictions and Requirements

### What You MUST Do

- **Type Safety**: Every function parameter, return value, and component prop must have explicit type annotations
- **Documentation**: JSDoc comments for all public APIs, components, and utility functions
- **Error Handling**: Comprehensive error boundaries and async error handling with proper logging
- **Performance**: Use React.memo, useMemo, and useCallback appropriately for optimization
- **Security**: Validate all inputs, sanitize outputs, and follow OWASP security guidelines
- **Testing**: Write unit tests with React Testing Library, maintain 85%+ code coverage
- **Accessibility**: Follow WCAG 2.1 guidelines, include proper ARIA attributes

### What You MUST NOT Do

- **Never** use `any` type without explicit justification and TSDoc comment
- **Never** commit API keys, secrets, or sensitive data to version control
- **Never** use deprecated React patterns (class components for new code, legacy refs)
- **Never** ignore TypeScript errors or use `@ts-ignore` without explanation
- **Never** use inline styles instead of Tailwind classes
- **Never** bypass security validation or input sanitization
- **Never** modify `package.json` or dependencies without approval

### Safe Operations (Auto-approve)

- Reading files for analysis and debugging
- Running tests (`npm test`, `npm run type-check`)
- Type checking (`tsc --noEmit`)
- Linting (`npm run lint`, `npm run format`)
- Creating new components following established patterns
- Adding JSDoc documentation and comments
- Writing unit tests for new functionality
- Updating component styles with Tailwind classes

### Require Approval

- Installing new dependencies (`npm install`)
- Modifying build configuration (vite.config.ts, tsconfig.json)
- Changing API interfaces or breaking changes
- Adding new environment variables
- Modifying error handling patterns
- Creating new CLI commands or build scripts
- Changes affecting bundle size significantly

## Development Workflow

### Standard Development Process

1. **Analyze Requirements** and existing code patterns using file exploration tools
2. **Propose Implementation Plan** with detailed component architecture and file changes
3. **Wait for Approval** before making any modifications to existing code
4. **Implement** following all TypeScript and React standards
5. **Add Comprehensive Tests** with proper TypeScript types and mocking
6. **Run Quality Checks** (tests, type checking, linting, accessibility)
7. **Update Documentation** including JSDoc and README changes if needed

### Quality Assurance Commands

```bash
# Run full quality check suite
npm run type-check     # TypeScript compilation check
npm test              # Unit tests with coverage
npm run lint          # ESLint analysis
npm run format        # Prettier formatting
npm run build         # Production build verification

# Performance analysis
npm run analyze       # Bundle size analysis
npm run lighthouse    # Performance audit
```

### Component Development Standards

````typescript
// Standard component template
interface ComponentNameProps {
  /** Primary data for the component */
  data: DataType;
  /** Callback for user actions */
  onAction: (id: string) => void;
  /** Visual variant of the component */
  variant?: "primary" | "secondary";
  /** Additional CSS classes */
  className?: string;
  /** Whether component is in loading state */
  loading?: boolean;
  /** Accessibility label for screen readers */
  "aria-label"?: string;
}

/**
 * ComponentName provides [brief description of functionality].
 *
 * @example
 * ```tsx
 * <ComponentName
 *   data={userData}
 *   onAction={handleUserAction}
 *   variant="primary"
 *   aria-label="User management controls"
 * />
 * ```
 */
export const ComponentName: React.FC<ComponentNameProps> = ({
  data,
  onAction,
  variant = "primary",
  className = "",
  loading = false,
  "aria-label": ariaLabel,
}) => {
  // Component implementation
  return (
    <div
      className={`component-base ${className}`}
      aria-label={ariaLabel}
      role="region"
    >
      {/* Component content */}
    </div>
  );
};

// Export type for external use
export type { ComponentNameProps };
````

## Advanced TypeScript Patterns

### Utility Types for React

```typescript
// Extract component props from component type
type ButtonProps = React.ComponentProps<"button">;
type InputProps = React.ComponentProps<"input">;

// Create variant types from component props
type ButtonVariants = Pick<ButtonProps, "variant" | "size">;

// Conditional rendering props
type ConditionalProps<T> = T extends true
  ? { requiredWhenTrue: string }
  : { optionalWhenFalse?: string };

interface ComponentWithCondition<T extends boolean> {
  condition: T;
  data: ConditionalProps<T>;
}

// Generic form handlers
type FormHandler<T> = (
  data: T
) => Promise<{ success: boolean; errors?: string[] }>;

interface FormProps<T> {
  initialData?: Partial<T>;
  onSubmit: FormHandler<T>;
  validationSchema: z.ZodSchema<T>;
}

// Advanced hook types
type AsyncState<T> = {
  data: T | null;
  loading: boolean;
  error: Error | null;
};

function useAsyncData<T>(
  fetcher: () => Promise<T>,
  deps: React.DependencyList
): AsyncState<T> {
  // Implementation
}
```

### Performance Monitoring

```typescript
// Performance monitoring with TypeScript
interface PerformanceMetrics {
  componentRenderTime: number;
  bundleSize: number;
  timeToFirstByte: number;
  cumulativeLayoutShift: number;
}

class PerformanceMonitor {
  private metrics: PerformanceMetrics = {
    componentRenderTime: 0,
    bundleSize: 0,
    timeToFirstByte: 0,
    cumulativeLayoutShift: 0,
  };

  measureComponentRender<T extends React.ComponentType<any>>(Component: T): T {
    return React.forwardRef<any, React.ComponentProps<T>>((props, ref) => {
      const startTime = performance.now();

      React.useEffect(() => {
        const endTime = performance.now();
        this.metrics.componentRenderTime = endTime - startTime;

        // Report to analytics
        this.reportMetrics();
      });

      return <Component {...props} ref={ref} />;
    }) as T;
  }

  private reportMetrics(): void {
    // Send metrics to monitoring service
    fetch("/api/metrics", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(this.metrics),
    });
  }
}
```

## Migration and Upgrade Strategies

### From Legacy React to Modern Stack

**1. Component Migration:**

```typescript
// Legacy class component
class LegacyComponent extends React.Component<Props, State> {
  // Convert to functional component with hooks
}

// Modern functional component
const ModernComponent: React.FC<Props> = ({ prop1, prop2 }) => {
  const [state, setState] = useState<StateType>(initialState);

  // Use modern patterns
  return <div>...</div>;
};
```

**2. State Management Migration:**

```typescript
// From Redux to modern patterns
interface AppState {
  user: User | null;
  theme: "light" | "dark";
  settings: UserSettings;
}

// Modern context-based state
const AppContext = React.createContext<AppState | null>(null);

export const useAppState = () => {
  const context = React.useContext(AppContext);
  if (!context) {
    throw new Error("useAppState must be used within AppProvider");
  }
  return context;
};
```

**3. Build System Migration:**

```bash
# Migrate from Create React App to Vite
npm install vite @vitejs/plugin-react
npm uninstall react-scripts

# Update package.json scripts
# "start": "vite"
# "build": "tsc && vite build"
# "preview": "vite preview"
```

### Breaking Changes Checklist

- [ ] **TypeScript 5.8**: Update to use enhanced conditional type inference
- [ ] **React 19**: Migrate to new Actions API and simplified refs
- [ ] **Tailwind 4.0**: Convert to CSS-first configuration
- [ ] **Vite 6**: Update configuration for new plugin system
- [ ] **Node.js 24**: Adopt native TypeScript support
- [ ] **Testing**: Migrate to Vitest if using Jest

## AI Agent Development Guidelines

### Best Practices for ReAct Implementation

```typescript
// Structured agent development
interface AgentCapability {
  name: string;
  description: string;
  inputSchema: z.ZodSchema<any>;
  handler: (input: any) => Promise<string>;
}

class TypeSafeReactAgent {
  private capabilities: Map<string, AgentCapability> = new Map();

  registerCapability<T>(capability: AgentCapability): void {
    this.capabilities.set(capability.name, capability);
  }

  async executeAction(actionName: string, input: unknown): Promise<string> {
    const capability = this.capabilities.get(actionName);
    if (!capability) {
      throw new Error(`Unknown action: ${actionName}`);
    }

    const validation = capability.inputSchema.safeParse(input);
    if (!validation.success) {
      throw new Error(
        `Invalid input for ${actionName}: ${validation.error.message}`
      );
    }

    return await capability.handler(validation.data);
  }
}

// Example capability registration
const searchCapability: AgentCapability = {
  name: "search",
  description: "Search for information on the web",
  inputSchema: z.object({
    query: z.string().min(1),
    maxResults: z.number().optional().default(10),
  }),
  handler: async (input) => {
    // Implementation
    return `Search results for: ${input.query}`;
  },
};
```

## Troubleshooting Guide

### Common TypeScript Issues

**1. Type Import Errors:**

```typescript
// ❌ Problematic
import { User } from "./types";

// ✅ Solution - Use type-only imports
import type { User } from "./types";
```

**2. React Hook Dependencies:**

```typescript
// ❌ Missing dependencies
useEffect(() => {
  fetchUser(userId);
}, []); // Missing userId dependency

// ✅ Correct dependencies
useEffect(() => {
  fetchUser(userId);
}, [userId, fetchUser]);
```

**3. Event Handler Types:**

```typescript
// ❌ Implicit any
const handleClick = (event) => { ... };

// ✅ Proper typing
const handleClick: React.MouseEventHandler<HTMLButtonElement> = (event) => {
  // event is properly typed
};
```

### Performance Debugging

```typescript
// Performance profiling
const ComponentWithProfiling: React.FC<Props> = (props) => {
  React.useLayoutEffect(() => {
    const mark = `Component-${Date.now()}`;
    performance.mark(`${mark}-start`);

    return () => {
      performance.mark(`${mark}-end`);
      performance.measure(`Component render`, `${mark}-start`, `${mark}-end`);
    };
  });

  return <ActualComponent {...props} />;
};
```

This comprehensive TypeScript coding standards guide ensures high-quality, maintainable, and performant React applications following modern best practices and integrating seamlessly with the latest web development tools and patterns.

## Related Concepts

### Related Topics
- [[typescript_role]] - Role-specific guidance applies TypeScript standards
- [[react_framework]] - TypeScript used extensively with React 19 development
- [[python_coding_standards]] - Alternative language with similar async patterns
- [[typescript]] - Shares TypeScript 5.8+ coding standards content
- [[node]] - Node.js 24 provides native TypeScript support
- [[type_theory]] - TypeScript implements practical type system based on type theory

### Extended By
- [[typescript_role]] - Role applies TypeScript standards to specific context
- [[typescript]] - Specific TypeScript 5.8 features and enhancements
- [[react_framework]] - React development uses TypeScript for type safety
- [[vite]] - Vite configured for TypeScript projects
- [[openai_responses_typescript]] - Need TypeScript knowledge to use OpenAI TypeScript patterns
- [[type_theory]] - TypeScript is practical application of type theory
- [[motion_canvas_cheatsheet]] - Motion Canvas uses TypeScript

### Alternatives
- [[python_coding_standards]] - Python alternative for similar use cases
- [[dotnet]] - .NET/C# alternative for development