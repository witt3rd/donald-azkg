# Category Theory Cheat Sheet for Computer Scientists

Category theory abstracts and generalizes mathematical structures, offering a powerful framework for computer science. It models complex systems like programming languages, type systems, and databases. This cheat sheet covers motivations, goals, basic and advanced concepts, and applications for computer scientists.

## 1. Motivations and Goals

- **Purpose**: Abstracts common patterns across mathematics (algebra, topology, logic).
- **Why Relevant?**: Provides a unified language for structures, independent of internal details.
- **Computer Science Goals**:
  - Model and design programming languages, especially functional ones.
  - Formalize type systems, concurrency, and databases.
  - Support formal verification and reasoning about computations.

## 2. Basic Concepts

| Concept | Definition | Computer Science Example |
|---------|------------|-------------------------|
| **Category** | Objects (entities) and morphisms (arrows) with composition and identity. | Types as objects, functions as morphisms. |
| **Functor** | Mapping between categories preserving structure. | Data structure transformations (e.g., `map` in Haskell). |
| **Natural Transformation** | Transforms one functor into another, respecting structure. | Converting between data representations. |
| **Limits** | Universal constructions like products, equalizers. | Cartesian products in programming. |
| **Colimits** | Dual to limits, e.g., coproducts, coequalizers. | Disjoint unions in programming. |
| **Adjunctions** | Pair of functors defining universal properties. | Free/forgetful constructions (e.g., lists to sets). |
| **Monads** | Design pattern from adjunctions for side effects. | Handling I/O, state in functional programming (Haskell). |

## 3. Advanced Topics

- **Kan Extensions**:
  - Extend functors along other functors universally.
  - **Definition**: For functors \(X: \mathbf{A} \to \mathbf{C}\), \(F: \mathbf{A} \to \mathbf{B}\), right Kan extension \(\operatorname{Ran}_F X: \mathbf{B} \to \mathbf{C}\) with natural transformation \(\epsilon: RF \to X\).
  - **Applications**: Type theory semantics, data science (extending functions over datasets), database query languages (e.g., CQL).
  - [Wikipedia: Kan Extension](https://en.wikipedia.org/wiki/Kan_extension)

- **Higher-Order Categories**:
  - Generalize categories with morphisms between morphisms (e.g., 2-categories, ∞-categories).
  - **Applications**: Semantics of higher-order functions, type constructors in programming languages, homotopy type theory.
  - [nLab: Higher Category Theory](https://ncatlab.org/nlab/show/higher+category+theory)

- **Sheaves**:
  - Assign data to open sets, respecting gluing (local to global consistency).
  - **Applications**: Distributed systems (consistent local states), type theory (dependent types).
  - [Wikipedia: Sheaf](https://en.wikipedia.org/wiki/Sheaf_(mathematics))

- **Homotopy Type Theory (HoTT)**:
  - Unifies type theory and homotopy theory, interpreting types as spaces, equality as paths.
  - **Applications**: Formal verification, proof assistants (Coq, Lean), dependent type systems.
  - [HoTT Book](https://homotopytypetheory.org/book/)

## 4. Applications in Computer Science

- **Programming Languages**:
  - Models type systems, especially in functional programming (Haskell).
  - Monads manage side effects (I/O, state, exceptions).
  - [Pierce (1991): Basic Category Theory](https://mitpress.mit.edu/9780262660716/)

- **Type Theory**:
  - Semantics for dependent types.
  - HoTT as a foundation for mathematics and programming.

- **Databases**:
  - Categories model schemas; functors represent queries.
  - Kan extensions in query languages (CQL).

- **Concurrency**:
  - Monoidal categories model concurrent processes.
  - [Applied Category Theory](https://en.wikipedia.org/wiki/Applied_category_theory)

- **Formal Verification**:
  - Category theory supports proof assistants (Coq, Lean).
  - HoTT formalizes proofs and programs.

## 5. Summary for Computer Scientists

- **Why Learn?**: Abstracts complex systems, enhances reasoning about software.
- **Key Insight**: From basic (functors, monads) to advanced (Kan extensions, HoTT), category theory unifies computer science concepts.
- **Resources**:
  - Pierce, B. C. (1991). *Basic Category Theory for Computer Scientists*.
  - Awodey, S. (2010). *Category Theory, 2nd Edition*.
  - [EECS 598 Course](https://maxsnew.com/teaching/eecs-598-w22/)