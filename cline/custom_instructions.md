### Direct Answer

**Key Points:**
- Custom instructions guide Cline's behavior; set globally via settings or per project with `.clinerules` (which can be a single file or a directory of rule files).
- Plan vs Act modes help manage tasks; Plan for strategy, Act for implementation.
- Memory bank and context mechanisms retain project details; use files like `projectbrief.md`.
- MCP tools extend functionality; integrate with external systems like GitHub.
- Combine these to control Cline effectively for coding standards and workflows.

**Setting Up Custom Instructions:**
- Open VS Code, go to Cline settings, find "Custom Instructions," and add rules like "Use Python, speak Spanish."
- For projects, create a `.clinerules` file or a `.clinerules/` directory at the project root to house specific rules, e.g., `# Ask for review after edits` within a file.

**Using Plan vs Act Modes:**
- Use Plan mode for planning without changes; Act mode for executing tasks.
- Switch modes in Cline interface; iterate as needed for complex projects.

**Managing Memory and Context:**
- Cline uses Memory Bank (files like `projectbrief.md`) for context across sessions.
- Monitor with Context Window Progress Bar; clear unnecessary context for focus.

**Leveraging MCP Tools:**
- Add MCP tools from marketplace for tasks like GitHub integration.
- Create custom MCP servers for specific needs, enhancing Cline's capabilities.

**Controlling Cline's Behavior:**
- Combine instructions, `.clinerules`, and MCP tools for tailored workflows.
- Best for enterprise: enforce standards; for personal: customize to preferences.

---

### Survey Note: Comprehensive Guide to Controlling Cline AI in VS Code

This guide provides an in-depth exploration of controlling Cline AI's behavior within Visual Studio Code (VS Code), focusing on custom instructions, Plan vs Act modes, `.clinerules`, memory bank, and MCP tools. As of May 18, 2025, Cline remains a leading open-source AI coding assistant, offering robust features for developers. This section expands on the direct answer, providing detailed insights for effective use.

#### Introduction to Cline AI for VS Code
Cline, an open-source AI coding assistant, integrates seamlessly with VS Code, offering dual Plan/Act modes, terminal execution, and the Model Context Protocol (MCP) for extensibility. It aims to enhance productivity by providing context-aware coding assistance, making it suitable for both personal projects and enterprise development. The ability to control Cline's behavior is crucial for aligning its output with specific coding standards and workflows.

#### Custom Instructions: Tailoring Cline's Behavior
Custom instructions are fundamental to shaping Cline's responses and actions. These user-defined guidelines are the primary way to influence how Cline generates code, interacts, and adheres to project standards. Cline offers two main ways to set these: globally through a dedicated field in its VS Code extension settings for user-wide preferences, and on a per-project basis using `.clinerules` files for project-specific directives. This combination provides both broad consistency and tailored control.

- **What Are Custom Instructions?**
  Custom instructions act as baseline programming, affecting all interactions. They are sets of guidelines or rules you define to tailor Cline's behavior and outputs for specific tasks or projects. Think of them as specialized "programming" for Cline. Their purpose is to:
  - **Enforce Coding Practices:** Ensure consistent code style (e.g., "Use camelCase for variables"), adherence to design patterns, and best practices for specific languages or frameworks (e.g., "Use React Query, avoid Redux").
  - **Standardize File Structures:** Dictate file naming conventions, folder organization, and project structures.
  - **Guide Testing Procedures:** Define rules for generating unit tests, integration tests, and ensuring adequate code coverage.
  - **Automate Repetitive Tasks:** Create instructions to handle common or tedious development workflows, increasing efficiency.
  - **Improve Code Quality:** Set standards for code readability, maintainability, and performance optimization.
  - **Define Workflows:** Specify steps for common operations (e.g., "Ask for review after edits").
  By providing Cline with carefully crafted instructions, you can significantly improve its accuracy, reliability, and overall effectiveness. Research suggests these instructions are key to tailoring Cline to project needs, as noted in the official documentation ([Cline FAQ](https://cline.bot/faq)).

- **Setting Custom Instructions Globally:**
  This is the primary mechanism for defining your baseline preferences for Cline across all your projects. These instructions are entered directly into a dedicated field within Cline's VS Code extension settings.
  To set globally:
  1. Open VS Code.
  2. Navigate to Cline extension settings (usually by clicking the gear icon ⚙️ next to the Cline extension and selecting "Extension Settings").
  3. Locate the "Custom Instructions" field.
  4. Enter your guidelines in Markdown format. These instructions act as persistent directives influencing every interaction with Cline.

  **Types of Global Instructions and Their Purpose:**
  You can use this field to:
  - **Enforce General Coding Styles:** Specify preferences like naming conventions (e.g., "Use camelCase for variables, PascalCase for classes"), formatting rules (e.g., "Indent with 2 spaces"), or comment styles (e.g., "Always include JSDoc comments for public functions").
  - **Define Default Behaviors:** Instruct Cline on preferred languages (e.g., "Default to Python 3.9 for new scripts"), interaction styles (e.g., "Speak in Spanish," "Provide concise answers," "Ask for clarification if a request is ambiguous"), or review processes (e.g., "Keep changes small and ask for review before applying").
  - **Integrate Broad Domain Knowledge:** Provide high-level context about technologies you frequently use or architectural patterns you prefer (e.g., "Prefer functional programming paradigms where appropriate," "When working with web components, assume usage of LitElement").
  - **Standardize Outputs:** Guide Cline on how to structure its responses or generated code snippets for consistency.
  - **Improve Accuracy:** By providing context about your common tools or libraries, Cline can generate more relevant and accurate suggestions.
  - **Set Error Handling Preferences:** Define general approaches to error handling (e.g., "For Node.js projects, use a centralized error handling middleware").

  **Example Global Instructions:**
  ```markdown
  ## My Cline Preferences
  - Default language: TypeScript
  - Indentation: 2 spaces
  - Naming: camelCase for variables/functions, PascalCase for classes/interfaces.
  - Always provide brief explanations for code suggestions.
  - For new React components, use functional components with Hooks.
  - When suggesting git commands, explain each part of the command.
  ```
  This global setting is ideal for maintaining consistent personal preferences and high-level guidelines across all your development work, as per the Cline documentation ([Cline Documentation](https://docs.cline.bot/)). For project-specific rules that might override or augment these global settings, use the `.clinerules` file described below.

- **A Note on Configuration Mechanisms:**
  It's worth noting that different AI coding assistants may offer various ways to manage custom instructions. For instance, some tools might use a `settings.json` file to reference multiple external instruction files. Cline, however, primarily relies on its dedicated "Custom Instructions" field in the VS Code extension settings for global rules and the `.clinerules` file for project-specific directives. This distinction is important for understanding how to best configure Cline for your needs.

- **Setting Project-Specific Instructions with `.clinerules`:**
  For project-specific rules, create a `.clinerules` file at the project root:
  1. Create `.clinerules` in the project directory.
  2. Add instructions starting with `#`, e.g.,
     ```
     # Use Jest tests with 85% coverage
     # Use Tailwind CSS from src/styles/theme.js
     # Do not edit docs without approval
     ```
  Cline automatically reads this file, ensuring project consistency, as highlighted in community discussions ([Reddit Post](https://www.reddit.com/r/ChatGPTCoding/comments/1hm3wcy/how_are_you_guiding_cline_in_vscode/)).

- **Best Practices for Writing Custom Instructions:**
  - Be specific: Include details like "2 spaces for indentation, use TypeScript interfaces."
  - Document technical foundation: Outline technologies, e.g., "Project uses React, Node.js, MongoDB."
  - Update as needed: Revise instructions when project requirements change.
  - Use actionable language: E.g., "Run npm run test:coverage before PRs."
  - **Leverage Structured Knowledge Systems:** Instruct Cline to utilize and maintain a structured knowledge base, like the Memory Bank system. The content within files such as `projectbrief.md`, `techContext.md`, and `systemPatterns.md` then serves as a detailed, evolving set of instructions. The custom instructions you provide to enable such a system (which might even include Mermaid diagrams to define processes) become a powerful way to guide Cline's understanding and behavior consistently.
  These practices, detailed in the Cline blog ([Cline Blog](https://cline.bot/blog/memory-bank-how-to-make-cline-an-ai-agent-that-never-forgets)), ensure effective guidance.

#### Plan vs Act Modes: Structured Development
Cline's Plan and Act modes offer a dual approach to development, emphasizing planning before implementation, as per the official guide ([Plan & Act Modes Guide](https://docs.cline.bot/exploring-clines-tools/plan-and-act-modes-a-guide-to-effective-ai-development)).

- **What Are Plan and Act Modes?**
  - **Plan Mode**: Focuses on context gathering, strategy development, and architecture discussions without code changes. It acts as a virtual solution architect, analyzing tasks and creating plans.
  - **Act Mode**: Implements the plan, making code changes and executing commands, maintaining context from planning.

- **When to Use Each Mode:**
  - **Plan Mode**: Ideal for starting new features, debugging complex issues, making architectural decisions, and analyzing requirements. It ensures clarity before action, reducing errors.
  - **Act Mode**: Best for implementing solutions, routine changes, following patterns, and executing tests. It leverages the plan for efficient execution.

- **How to Switch Between Modes:**
  Use the Cline interface to toggle modes, typically via the sidebar. The workflow involves starting in Plan Mode, developing a strategy, then switching to Act Mode for implementation. For complex projects, iterate with multiple cycles, returning to Plan Mode for unexpected complexity, as advised in community forums ([Reddit Feedback](https://www.reddit.com/r/CLine/comments/1i6zbnu/feedback_thread_how_are_you_using_plan_act_modes/)).

- **Best Practices and Tips:**
  - **Planning Phase**: Share comprehensive requirements, point to relevant files, validate the approach, and explore edge cases. Write markdown plans for reference.
  - **Implementation Phase**: Follow the plan, monitor progress, track changes, and document decisions. Switch back to Plan Mode if issues arise, as suggested in the Cline blog ([Cline Blog Post](https://cline.bot/blog/plan-smarter-code-faster-clines-plan-act-is-the-paradigm-for-agentic-coding)).

#### `.clinerules` File or Directory: Project-Specific Control
Project-level custom instructions are managed via `.clinerules`, which offers flexibility by supporting either a single configuration file or a directory containing multiple rule files. This ensures consistency across team members working on a specific project. As of May 18, 2025, Cline supports both approaches.

- **Purpose of `.clinerules`:**
  It sets project-specific guidelines, such as coding standards, testing rules, and documentation practices, overriding global settings for that project. This is crucial for maintaining consistency. Using a `.clinerules/` directory allows for a modular organization of these rules, which can be particularly beneficial for larger projects or when different aspects of the project require distinct sets of guidelines (e.g., frontend vs. backend rules, or rules for different languages used in the project). This capability was notably enhanced around Cline version 3.7.

- **How to Create and Use `.clinerules`:**
  You have two options for setting up project-specific rules:

  1.  **Single File Method:**
      *   Create a file named `.clinerules` in the project root.
      *   Add instructions directly into this file, typically starting each rule with `#`, e.g.:
          ```
          # Enforce 2-space indentation
          # Use React Query for state management
          # Run tests before commits
          ```
      *   Save the file; Cline reads it automatically. This method is straightforward for simpler projects or when all rules can be concisely managed in one place.

  2.  **Directory Method:**
      *   Create a directory named `.clinerules/` in the project root.
      *   Inside this directory, create multiple files (commonly Markdown files, e.g., `coding_standards.md`, `testing_protocols.md`, `api_guidelines.md`).
      *   Write specific sets of instructions within each of these files. Cline will read and aggregate the instructions from all files within this directory.
      *   This method allows for better organization and modularity of rules, making it easier to manage complex sets of instructions or to enable/disable specific rule sets by adding/removing files from the directory. Enhancements around Cline version 3.13 also introduced concepts like "toggleable .clinerules," likely building upon this directory support.

  Cline automatically detects and loads instructions from either the `.clinerules` file or the `.clinerules/` directory if present, as per beginner guides ([How to Use Cline](https://apidog.com/blog/how-to-use-cline/)) and recent community updates ([Cline 3.7 Release Notes](https://www.reddit.com/r/CLine/comments/1jblk9r/cline_37_release_selectable_options_clinerules/)).

- **Examples of `.clinerules` Content:**

  *   **Single `.clinerules` file:**
      ```
      # Always include Jest tests with 85% coverage.
      # Use Tailwind CSS, reference src/styles/theme.js.
      # Do not modify docs without explicit approval.
      ```

  *   **Inside a `.clinerules/` directory:**
      *   `coding_standards.md`:
          ```
          # Enforce 2-space indentation for JavaScript and TypeScript.
          # All Python code must follow PEP 8.
          # Use camelCase for variable names.
          ```
      *   `testing_rules.md`:
          ```
          # All new features must have corresponding unit tests.
          # Target 90% code coverage for critical modules.
          # Use Playwright for end-to-end tests.
          ```
      *   `documentation.md`:
          ```
          # All public APIs must be documented using JSDoc.
          # README files should be updated with any significant architectural changes.
          ```
  These examples, adapted from community posts ([Reddit Discussion](https://www.reddit.com/r/ChatGPTCoding/comments/1hm3wcy/how_are_you_guiding_cline_in_vscode/)) and the new directory structure understanding, illustrate practical use.

#### Memory Bank and Context Management: Retaining Project Context
Cline's Memory Bank and context management features ensure persistent project context, crucial for long-term development.

- **How Cline Manages Context and Memory:**
  Cline analyzes project structure, reads relevant files, and uses tools like `@file` for inclusion. The Memory Bank, a community-created feature, is a prime example of advanced context and behavior management. It's not just about passive context recall; it's an active system for guiding Cline. The custom instructions that set up the Memory Bank often include directives—sometimes even visualized with Mermaid diagrams within the instructions themselves—that teach Cline *how* to create, read, verify, update, and utilize these structured memory files (e.g., `projectbrief.md`, `techContext.md`). This process ensures Cline's behavior is continuously shaped by an evolving, project-specific knowledge base, as detailed in the Cline blog ([Memory Bank Blog](https://cline.bot/blog/memory-bank-how-to-make-cline-an-ai-agent-that-never-forgets)).

- **Tools and Features for Context Management:**
  - **@file**: Includes file content with intelligent parsing, as noted by Addy Osmani ([Why I Use Cline](https://addyo.substack.com/p/why-i-use-cline-for-ai-engineering)).
  - **Context Window Progress Bar**: Visual indicator to manage context size, preventing overflow, as explained in the Cline blog ([Context Management Blog](https://cline.bot/blog/understanding-the-new-context-window-progress-bar-in-cline)).
  - **Memory Bank**: This system utilizes a structured set of Markdown files (e.g., `projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `activeContext.md`, `progress.md`). These files do more than just store information for recall; they act as a rich, detailed, and evolving set of instructions. Cline is directed (via global or `.clinerules` custom instructions) to consult and maintain these files, which profoundly shapes its understanding of the project, its decision-making processes, and the code it generates. The instructions for managing the Memory Bank can even include Mermaid diagrams to define workflows for Cline, as per the Cline documentation ([Cline Documentation](https://docs.cline.bot/)) and the insights from the Memory Bank blog post.

- **Best Practices for Managing Context in Large Projects:**
  - Selectively include relevant files to avoid overwhelming the context window.
  - Use the Context Window Progress Bar to monitor limits.
  - Clear unnecessary context regularly to maintain focus.
  - Initialize and maintain the Memory Bank for persistent context, as advised in community forums ([Cursor Forum](https://forum.cursor.com/t/how-to-add-cline-memory-bank-feature-to-your-cursor/67868)).

#### MCP Tools: Extending Cline's Capabilities
MCP (Model Context Protocol) tools allow Cline to interact with external systems, enhancing its functionality for specific tasks.

- **What Are MCP Tools?**
  MCP tools are external tools Cline can use, such as GitHub API integration, filesystem operations, and browser monitoring, extending beyond built-in features. They are part of the MCP marketplace, as seen in the official Cline site ([MCP Marketplace](https://cline.bot/mcp-marketplace)).

- **How to Use MCP Tools in Cline:**
  1. Open Cline in VS Code.
  2. Access the MCP marketplace or use commands to add tools.
  3. Select or configure the tool, e.g., for AWS automation, as detailed in 4sysops ([AWS MCP Guide](https://4sysops.com/archives/install-mcp-server-with-vs-code-extension-cline-for-ai-driven-aws-automation/)).
  4. Use the tool in interactions, enhancing task execution.

- **Examples of Useful MCP Tools:**
  - **GitHub API Integration**: Manage repositories, issues, and pull requests.
  - **Filesystem Operations**: Read, write, and move files.
  - **Browser Monitoring**: Capture screenshots and analyze logs.
  - **Git Repository Interaction**: Handle commits, branches, and diffs.
  These are listed in the Cline MCP marketplace ([MCP Marketplace](https://cline.bot/mcp-marketplace)).

- **How to Create Custom MCP Tools:**
  Develop an MCP server conforming to the protocol, host it, and configure Cline to use it, as explained in the Cline documentation ([Cline Documentation](https://docs.cline.bot/)).

#### Controlling Cline's Behavior: Integrated Approach
To fully control Cline, combine custom instructions, `.clinerules`, Memory Bank, and MCP tools for a tailored workflow.

- **Combining Elements:**
  - Use global custom instructions for consistent preferences across all projects.
  - Use a `.clinerules` file or a `.clinerules/` directory for project-specific rules, which will override or augment global settings for that particular project.
  - Leverage Memory Bank for persistent context and detailed, evolving project knowledge across sessions.
  - Integrate MCP tools for specialized tasks, enhancing capabilities.

- **Tips for Effective Use:**
  - **Enterprise Development**: Enforce coding standards with `.clinerules`, integrate with enterprise tools via MCP, and use Memory Bank for team collaboration, as noted in the enterprise guide ([Cline Enterprise](https://cline.bot/enterprise)).
  - **Personal Projects**: Customize with global instructions, use Plan Mode for complex tasks, and add MCP tools for specific needs, as suggested in beginner guides ([How to Use Cline](https://apidog.com/blog/how-to-use-cline/)).
  - **Complex Tasks**: Start with Plan Mode for strategy, switch to Act Mode for implementation, and iterate as needed, ensuring alignment with project goals.

#### Conclusion and Resources
This guide equips you to control Cline's behavior effectively, enhancing productivity for various development scenarios. For further details, explore:
- [Cline Official Website](https://cline.bot/) for features and updates.
- [Cline GitHub Repository](https://github.com/cline/cline) for community contributions and the core project.
- [Cline Documentation](https://docs.cline.bot/) for comprehensive guides.
- [Cline Custom Instructions Library (Community)](https://github.com/nickbaumann98/cline_docs/tree/main/prompting/custom%20instructions%20library) for examples and to contribute your own instructions.
- [Reddit Community](https://www.reddit.com/r/CLine/) for user tips and discussions.

By leveraging these resources, you can master Cline for both personal and enterprise use as of May 18, 2025.

#### Key Citations
- [Cline FAQ with custom instructions details](https://cline.bot/faq)
- [Cline Documentation for comprehensive guides](https://docs.cline.bot/)
- [Cline Memory Bank implementation blog](https://cline.bot/blog/memory-bank-how-to-make-cline-an-ai-agent-that-never-forgets)
- [Cline MCP Marketplace for tool extensions](https://cline.bot/mcp-marketplace)
- [Reddit Post on guiding Cline in VSCode](https://www.reddit.com/r/ChatGPTCoding/comments/1hm3wcy/how_are_you_guiding_cline_in_vscode/)
- [Plan & Act Modes Guide for effective AI development](https://docs.cline.bot/exploring-clines-tools/plan-and-act-modes-a-guide-to-effective-ai-development)
- [Cline Blog on Plan Smarter, Code Faster](https://cline.bot/blog/plan-smarter-code-faster-clines-plan-act-is-the-paradigm-for-agentic-coding)
- [How to Use Cline for Beginners guide](https://apidog.com/blog/how-to-use-cline/)
- [Context Management Blog with progress bar details](https://cline.bot/blog/understanding-the-new-context-window-progress-bar-in-cline)
- [AWS MCP Guide for AI-driven automation](https://4sysops.com/archives/install-mcp-server-with-vs-code-extension-cline-for-ai-driven-aws-automation/)
- [Why I Use Cline for AI Engineering insights](https://addyo.substack.com/p/why-i-use-cline-for-ai-engineering)
- [Reddit Feedback on Plan & Act modes usage](https://www.reddit.com/r/CLine/comments/1i6zbnu/feedback_thread_how_are_you_using_plan_act_modes/)
- [Cline Enterprise features for teams](https://cline.bot/enterprise)
