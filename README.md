# LLM Agent: A Toy Model of a Claude-like CLI Tool

This project is a deep dive into the practical application of large language models (LLMs) as autonomous agents. It’s a Python-based command-line tool that demonstrates how an LLM can be used to reason about, plan, and execute a coding task by calling a set of predefined functions. This isn't just about code generation; it's about building a system that can understand and solve a problem from start to finish.

---

### The Agentic Loop: How It Works

The core of this project is a simple but powerful "agentic loop." When you give the agent a task, it doesn't just respond with code. Instead, it:

1. **Analyzes the Task:** It reads your request (e.g., "fix my calculator app").
2. **Chooses a Tool:** It decides which of its available functions to use next. These functions, or "tools," are defined by you and can do things like read a file or execute a Python script.
3. **Executes the Tool:** The agent calls the chosen function, and the result is returned to the LLM.
4. **Repeats:** Based on the new information, the agent continues this cycle of planning, choosing, and executing until the task is complete.

This iterative process mimics how sophisticated AI systems debug and solve problems in the real world, showcasing an understanding of state management and problem-solving beyond simple one-off prompts.

---

### Capabilities

The agent is equipped with a small but powerful set of tools to interact with your codebase:

- **`get_files_info`:** Scans a directory and lists all available files.
- **`get_file_content`:** Reads and returns the content of a specific file.
- **`write_file`:** Overwrites the contents of a file.
- **`run_python_file`:** Executes a Python script and returns the output (or error).

### Example Usage

Here’s a real-world example of the agent fixing a bug in a simple calculator application. It intelligently reads the files, identifies the issue, and overwrites the code to fix it.

```bash
> uv run main.py "fix my calculator app, it's not starting correctly"
# Calling function: get_files_info
# Calling function: get_file_content
# Calling function: write_file
# Calling function: run_python_file
# Calling function: write_file
"# Calling function: run_python_file
# Final response:
# Great! The calculator app now seems to be working correctly. The output shows the expression and the result in a formatted way.
```

### Getting Started

To run this project on your local machine, you'll need the following:

- Python 3.10+
- The uv project and package manager
- Access to a Unix-like shell (e.g., zsh or bash)

### Key Takeaways

This project is more than just a cool demo; it’s a hands-on learning experience that covers several crucial concepts for modern software development:

- **Agentic AI:** Understand the fundamentals of how autonomous agents are built and how they leverage LLMs for reasoning.

- **Tool Use:** Learn how to create a well-defined set of tools that an LLM can call, a key skill for building scalable AI applications.

- **Functional Programming:** Practice writing clean, modular functions that serve as the building blocks for the agent's actions.

- **Multi-Directory Projects:** Gain experience structuring a complex Python project with multiple modules and directories.

### Project Status and Future Work

This project is a work in progress. Future improvements could include:

- Adding more sophisticated tools (e.g., a tool to execute a debugger, or one to interact with a web service).
- Implementing a more robust error handling mechanism.
- Creating a proper test suite.

This project uses Google's free Gemini API for the LLM component.
