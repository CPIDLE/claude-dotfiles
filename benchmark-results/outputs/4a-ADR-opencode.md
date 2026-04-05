# ADR 005: Migration of Task Execution Engine from Opencode CLI to LangGraph and Direct Gemini API

## Status
Accepted

## Context
Our current task delegation architecture relies on a "Spec-to-Executor" pattern. Claude Code generates technical specifications which are then piped into the `opencode` CLI. While `opencode` leverages Gemini models to perform file operations and shell commands, it operates as a black-box execution layer with several architectural bottlenecks:

1.  **Linear Execution Flow**: The current pipeline is strictly sequential. If a command fails or an edge case is encountered, the system cannot autonomously branch into a recovery or diagnostic path without returning control to the top-level agent.
2.  **Lack of State Persistence**: Each `opencode` invocation is essentially stateless. Contextual memory between separate sessions is limited to what is passed in the prompt, leading to redundant analysis and lost "working memory" during complex, multi-step refactors.
3.  **No Conditional Routing**: There is no native mechanism to route tasks based on complexity or type (e.g., routing a documentation task to a cheaper model and a kernel-level bug fix to a more capable one).
4.  **Limited Observability**: Internal decision-making within the CLI is difficult to instrument or intercept for validation purposes.

## Decision
We will migrate the execution engine from the `opencode` CLI wrapper to a custom orchestration layer built on **LangGraph** using direct **Gemini API** integrations.

### Technical Implementation Details
1.  **Graph Topology**: We will implement a StateGraph with the following specialized nodes:
    *   `classify`: Analyzes the spec to determine required tools, risk level, and branching path.
    *   `execute`: Performs the core file/shell operations using Gemini Function Calling.
    *   `validate`: A dedicated node that runs linters, tests, and static analysis to verify the work of the `execute` node.
    *   `report`: Summarizes the outcome and updates the project state.
2.  **Persistence Layer**: Use `langgraph.checkpoint.sqlite.SqliteSaver` to persist the graph state. This allows for "human-in-the-loop" interruptions, session resumes, and historical "time-travel" debugging of agent actions.
3.  **Control Flow**: Implement conditional edges to handle retries. If the `validate` node identifies a regression, the graph will route back to `execute` with the error logs as feedback, rather than failing the entire task.
4.  **Direct API Integration**: Bypass the CLI wrapper to use the Vertex AI or Google AI SDK directly, enabling finer control over system instructions, safety settings, and token usage tracking.

## Consequences

### Positive
*   **Cyclic Error Recovery**: The system can now self-correct. If a test fails, the graph can automatically trigger a fix loop up to a defined recursion limit.
*   **Long-running Sessions**: Complex tasks can be paused and resumed across different CLI sessions because the state is persisted in SQLite.
*   **Granular Validation**: We can enforce strict "gatekeeper" nodes that must pass (e.g., `npm test`) before any code is committed or reported as finished.
*   **Parallelism**: LangGraph supports parallel node execution, allowing for simultaneous linting and testing across different modules.

### Negative
*   **Increased Complexity**: Replacing a single CLI call with a Graph-based orchestrator increases the codebase size and requires developers to understand LangGraph concepts (edges, nodes, state).
*   **Infrastructure Requirements**: We now need to manage a local SQLite database file for state persistence.
*   **Hand-off Overhead**: The initial setup of tool-calling and system prompts that were previously "baked into" `opencode` must now be explicitly maintained in our custom implementation.

## Alternatives Considered
*   **Continuing with Opencode CLI**: Rejected due to the inability to implement custom retry logic and the lack of visibility into the agent's internal state.
*   **AutoGen**: Considered for its multi-agent capabilities, but rejected in favor of LangGraph's more deterministic control flow and superior state management (checkpointers).
*   **CrewAI**: Rejected as it is too high-level for our needs; we require the low-level graph control that LangGraph provides for precise CLI task delegation.