# Rust Import Conventions: Confirming and Refining Best Practices

Based on extensive research into Rust's official style guide, community practices, and expert opinions, I can **confirm** most of your proposed best practices while offering important refinements that will help the next generation of Rust developers write more idiomatic code.

## Confirmed Best Practices

### **1. Import Specific Items When Using Few Things**

**Confirmed**: Your example is excellent and aligns with official Rust conventions[1][2]:

```rust
use regex::Regex;
use reqwest::get as http_get;  // Rename for clarity
use std::path::{Path, PathBuf};
```

This practice enhances code readability by making dependencies explicit and avoiding namespace pollution[3].

### **2. Import Module When Using Multiple Items**

**Confirmed**: This is a widely accepted pattern[1][2]:

```rust
use tokio::fs::{self, File};   // Can use fs::* and File directly
```

The `self` keyword brings the module itself into scope alongside specific items, which is particularly useful for maintaining clarity about where functions originate.

### **3. Avoid Full Crate Paths When Possible**

**Confirmed**: Your criticism of `use reqwest;` followed by `reqwest::get()` is valid[4]. Explicit imports reduce verbosity and improve maintainability.

## Important Refinements and Additional Best Practices

### **Functions vs. Types Import Conventions**

A crucial distinction your examples don't address is the **different conventions for functions vs. types**[1][5][6]:

**For Functions**: Import the parent module, not the function itself:

```rust
use std::collections::HashMap;  // ✅ Good
use std::io;                   // ✅ Good

// Usage
let map = HashMap::new();
io::stdin().read_line(&mut buffer)?;
```

**For Types/Structs/Enums**: Import the item directly:

```rust
use std::collections::HashMap;  // ✅ Good
use std::path::PathBuf;        // ✅ Good
```

This convention helps readers immediately understand whether they're looking at a function call or type construction[1][6].

### **Import Ordering and Grouping**

The official Rust Style Guide specifies a three-section approach[1][2]:

1. **Standard library imports**
2. **External crate imports**
3. **Internal/local imports**

Each section should be separated by blank lines and sorted alphabetically within groups[1][2].

```rust
// Standard library
use std::collections::HashMap;
use std::io::{self, Read, Write};

// External crates
use regex::Regex;
use reqwest::Client;

// Internal modules
use crate::config::Config;
use crate::utils::helpers;
```

### **Avoiding Glob Imports**

**Critical refinement**: Glob imports (`use module::*`) should be avoided in most cases[3][7][8]:

```rust
// ❌ Avoid
use some_crate::*;

// ✅ Prefer
use some_crate::{Item1, Item2, Item3};
```

**Exceptions** where glob imports are acceptable[3][9]:

- Prelude modules explicitly designed for glob imports
- Unit test modules: `use super::*;`
- Very limited local scope with discipline

### **Handling Name Conflicts**

Use the `as` keyword for renaming when conflicts occur[10][11]:

```rust
use std::fmt::Result;
use std::io::Result as IoResult;  // Avoid conflict

// Or bring in the module to maintain clarity
use std::io;
// Then use: io::Result
```

### **Trait Imports**

Traits must be in scope to use their methods[6]. Import traits explicitly when needed:

```rust
use std::io::Read;  // Required to use .read_to_string()

let mut file = File::open("file.txt")?;
let mut contents = String::new();
file.read_to_string(&mut contents)?;  // Works because Read is in scope
```

## Advanced Considerations

### **Re-exports and Public APIs**

For library authors, use `pub use` to create clean, flat APIs[12][13]:

```rust
// In lib.rs
pub use crate::internal::module::PublicType;
pub use crate::complex::nested::ImportantTrait;

// Users can then do:
use your_crate::{PublicType, ImportantTrait};
```

### **Conditional Compilation**

Be mindful of feature flags and conditional compilation when organizing imports[14]:

```rust
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};
```

## Refined Guidelines for Next-Generation Rust Developers

1. **Be explicit and intentional** with imports - favor clarity over brevity
2. **Follow the function vs. type convention** consistently
3. **Group imports into three sections** with proper spacing
4. **Avoid glob imports** except for well-established preludes and test modules
5. **Use descriptive renames** when conflicts arise
6. **Import traits explicitly** when you need their methods
7. **Consider your API's user experience** when designing public re-exports
8. **Use tools like `rust-analyzer`** to help manage imports automatically
9. **Follow rustfmt conventions** for consistent team practices
10. **Document your import strategy** in team guidelines when deviating from defaults

Your initial principles are sound and align well with Rust community standards. These refinements will help developers write more idiomatic, maintainable Rust code that integrates seamlessly with the broader ecosystem.

[1] <https://github.com/rust-lang-nursery/fmt-rfcs/issues/24>
[2] <https://doc.rust-lang.org/beta/style-guide/items.html>
[3] <https://corrode.dev/blog/dont-use-preludes-and-globs/>
[4] <https://stackoverflow.com/questions/29013617/is-it-considered-bad-style-to-declare-multiple-use-statements-in-rust>
[5] <https://web.mit.edu/rust-lang_v1.25/arch/amd64_ubuntu1404/share/doc/rust/html/book/first-edition/crates-and-modules.html>
[6] <https://github.com/pretzelhammer/rust-blog/blob/master/posts/tour-of-rusts-standard-library-traits.md>
[7] <https://internals.rust-lang.org/t/hiding-in-use-re-export/12631>
[8] <https://www.reddit.com/r/rust/comments/i9uvek/against_glob_imports/>
[9] <https://web.mit.edu/rust-lang_v1.25/arch/amd64_ubuntu1404/share/doc/rust/html/std/prelude/index.html>
[10] <https://doc.rust-lang.org/rust-by-example/mod/use.html>
[11] <https://doc.rust-lang.org/reference/items/use-declarations.html>
[12] <https://www.reddit.com/r/rust/comments/alsph9/rusts_modules_and_project_organization_best/>
[13] <https://github.com/rust-lang/api-guidelines/discussions/176>
[14] <https://www.reddit.com/r/rust/comments/yi1cuy/looking_for_a_good_rustfmttoml_example_file/>
[15] <https://tarquin-the-brave.github.io/blog/posts/rust_use_statements/>
[16] <https://stackoverflow.com/questions/66915951/rust-use-vs-mod>
[17] <https://users.rust-lang.org/t/best-way-to-organize-structure-modules-in-project/114883>
[18] <https://www.reddit.com/r/rust/comments/wwbxhw/how_do_you_organize_imports_reexports_structs/>
[19] <https://www.reddit.com/r/rust/comments/fyvmdh/using_use_usefully/>
[20] <https://www.youtube.com/watch?v=C0_b9r1Wcpo>
[21] <https://rust-lang.github.io/api-guidelines/naming.html>
[22] <https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html>
[23] <https://users.rust-lang.org/t/proper-file-structure-and-imports/92811>
[24] <https://rustwiki.org/en/reference/items/use-declarations.html>
[25] <https://dmitryfrank.com/articles/rust_module_system_encourages_bad_practices>
[26] <https://users.rust-lang.org/t/rust-file-organization-imports-etc/103713>
[27] <https://stackoverflow.com/questions/79182928/what-exactly-is-the-scope-of-the-use-statement-in-rust-and-why>
[28] <https://highassurance.rs/chp3/modules.html>
[29] <https://rust-lang.github.io/api-guidelines/checklist.html>
[30] <https://dev.to/ajtech0001/rusts-module-system-explained-a-complete-guide-to-organizing-your-code-3i8i>
[31] <https://www.shuttle.dev/blog/2022/07/28/patterns-with-rust-types>
[32] <https://internals.rust-lang.org/t/safe-library-imports/9320>
[33] <https://google.github.io/comprehensive-rust/std-types/std.html>
[34] <https://rust-lang.github.io/api-guidelines/about.html>
[35] <https://doc.rust-lang.org/std/>
[36] <https://www.reddit.com/r/rust/comments/kmw6xc/code_style_question_grouping_of_use_statements/>
[37] <https://doc.rust-lang.org/std/prelude/index.html>
[38] <https://dev.to/xphoniex/adding-our-own-custom-statement-to-rust-language-30lc>
[39] <https://stdrs.dev>
[40] <https://www.reddit.com/r/rust/comments/np41l2/designing_rust_bindings_for_rest_apis/>
[41] <https://github.com/rust-dev-tools/fmt-rfcs/issues/57>
[42] <https://doc.rust-lang.org/core/>
[43] <https://github.com/rust-lang/api-guidelines>
[44] <https://rust-lang.github.io/rfcs/1560-name-resolution.html>
[45] <https://github.com/rust-lang/rust/issues/31337>
[46] <https://internals.rust-lang.org/t/custom-prelude-imports/14147>
[47] <https://stackoverflow.com/questions/69683758/should-shadowing-be-avoided-in-with-package-names-and-variables>
[48] <https://effective-rust.com/wildcard.html>
[49] <https://www.reddit.com/r/rust/comments/a7pcp2/is_using_a_crateprelude_good_practice/>
[50] <https://discuss.kotlinlang.org/t/rust-style-variable-shadowing/16338?page=2>
[51] <https://stackoverflow.com/questions/77691905/resolving-conflicts-w-r-t-ambiguous-names-during-imports-in-rust>
[52] <https://mlops.systems/posts/2024-09-16-what-is-the-rust-prelude.html>
[53] <https://www.reddit.com/r/rust/comments/xx6ibp/what_is_the_logic_behind_shadowing/>
[54] <https://users.rust-lang.org/t/to-use-prelude-or-to-not-to-use-prelude-that-is-the-question/110855>
[55] <https://stackoverflow.com/questions/50946308/what-is-the-best-practice-for-wildcard-prelude-imports-in-rust>
[56] <https://github.com/rust-lang/rust/issues/98467>
[57] <https://internals.rust-lang.org/t/module-local-preludes/14143>
[58] <https://stackoverflow.com/questions/70468643/is-it-possible-to-use-rustfmt-to-format-just-the-imports>
[59] <https://doc.rust-lang.org/edition-guide/rust-2024/rustfmt-version-sorting.html>
[60] <https://pingcap.github.io/style-guide/rust/>
[61] <https://github.com/rust-lang/rustfmt>
[62] <https://doc.rust-lang.org/edition-guide/rust-2024/rustfmt-raw-identifier-sorting.html>
[63] <https://www.jetbrains.com/help/rust/rustfmt.html>
[64] <https://github.com/enso-org/enso/blob/develop/docs/style-guide/rust.md>
[65] <https://rustwiki.org/en/style-guide/>
[66] <https://crates.io/crates/rust-style-guide/0.1.1>
[67] <https://rust-lang.github.io/rustfmt/>
[68] <https://doc.rust-lang.org/style-guide/items.html>
[69] <https://rust-lang.github.io/rustfmt/?version=v1.7.0&search=import>
[70] <https://develop.sentry.dev/engineering-practices/rust/>
[71] <https://github.com/rust-lang/rustfmt/issues/5269>
[72] <https://doc.rust-lang.org/nightly/style-guide/>
