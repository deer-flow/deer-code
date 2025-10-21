# 🦌 deer-code

A minimalist yet powerful AI coding agent that helps developers learn and build intelligent coding assistants. Built with Python and featuring a VSCode-like TUI interface, deer-code demonstrates how to create AI agents that can reason, plan, and act on code.

**Brought to you by** [🦌 The DeerFlow Team](https://github.com/bytedance/deer-flow).

*Inspired by Anthropic's Claude Code.*

## 🚀 Quick Start

DeerCode is written in Python and designed to be easy to set up and use. Follow these steps to get started:

### Prerequisites

- [Python](https://www.python.org/downloads/) 3.12 or higher
- [uv](https://docs.astral.sh/uv/) (recommended for dependency management)
- [langgraph-cli](https://docs.langchain.com/langsmith/cli) (for development and debugging)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bytedance/deer-flow.git
   cd deer-flow
   ```

2. **Install dependencies:**
   ```bash
   make install
   ```

### Configuration

1. **Copy the configuration template:**
   ```bash
   cp config.example.yaml config.yaml
   ```

2. **Edit `config.yaml` with your settings:**

```yaml
models:
  chat_model:
    model: 'gpt-5-2025-08-07'
    base_url: 'https://api.openai.com/v1'
    api_key: $OPENAI_API_KEY
    temperature: 0
    max_tokens: 8192
    extra_body:
      reasoning_effort: minimal # `minimal`, `low`, `medium` or `high`
  # Alternatively, uncomment the following section to use Doubao's model:
  #
  # chat_model:
  #   model: 'doubao-seed-1-6-250615'
  #   base_url: 'https://ark.cn-beijing.volces.com/api/v3'
  #   api_key: $ARK_API_KEY
  #   temperature: 0
  #   max_tokens: 8192
  #   extra_body:
  #     thinking:
  #       type: disabled # `disabled` or `auto`
tools:
  mcp_servers:
    context7:
      transport: 'streamable_http'
      url: 'https://mcp.context7.com/mcp'
    # your_mcp_server:
    #   ...
```

### Running the Application

**Start deer-code:**
```bash
uv run -m deer_code.main "/path/to/your/developing/project"
```

**Development mode (with LangGraph CLI):**
```bash
make dev
```

## 🌟 Features

- [x] **Beginner-friendly**: Simple project structure designed for learning
- [x] **VSCode-like CUI**: Intuitive terminal interface
- [x] **OpenAI Compatible**: Works with any OpenAI-compatible API
- [x] **ReAct Framework**: Reasoning, planning, and acting capabilities
- [x] **Multi-turn Conversations**: Maintains context across interactions
- [x] **Task Planning**: Built-in todo system for project management
- [x] **Code Generation**: AI-powered code creation and editing
- [x] **Code Search**: Intelligent code location and search
- [x] **Bash Execution**: Bash command execution
- [x] **MCP Integration**: Bring your own MCP tools to enhance the agent's capabilities
- [ ] **Working Memory**: Persistent memory across sessions (coming soon)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is open source and available under the [MIT License](./LICENSE).

## 🙏 Acknowledgments

- Inspired by [Anthropic's Claude Code](https://github.com/anthropics/claude-code)
- Built with [Textual](https://github.com/Textualize/textual) for the TUI interface
- Powered by [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
