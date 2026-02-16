# Melius

Melius is a high-performance, autonomous AI coding agent designed to operate locally with global reach. It features a sophisticated CLI, remote control via Telegram, skill-based extensibility, and multi-model support.

## Key Features

- **Autonomous Coding Agent**: Performs file operations (read, write, edit) and executes system commands within its workspace.
- **GitHub Integration**: Clone, pull, push, and manage repositories directly.
- **Remote Gateway**: Start a gateway to control the agent remotely via Telegram.
- **Skill System**: Download and manage prebuilt skills (Python/other) to extend capabilities.
- **Inbuilt Browser**: Access the web to research and improve its own performance.
- **Self-Improvement**: A dedicated `improve` command for the agent to learn and optimize itself.
- **Multi-Model Support**: Connect via OpenRouter or use local providers like Ollama.
- **Beautiful CLI**: A professional, colored command-line interface.

## Commands

- `melius gateway`: Start the remote access gateway.
- `melius connect`: Configure Telegram connectivity.
- `melius skill`: Manage and download agent skills.
- `melius browser`: Start the inbuilt browser data access.
- `melius improve`: Initiate the self-improvement protocol.
- `melius models`: Manage AI models and API keys.

## Installation

```bash
pip install melius-cli
```

## License

MIT
