# Melius: The Global AI Coding Agent

Melius is a production-ready, autonomous AI coding agent that lives in your terminal and can be controlled from anywhere via Telegram. It supports both high-end cloud models via OpenRouter and private local models via Ollama.

## 🌍 Global Installation

Melius is designed to be installed easily on any system (Linux, macOS, Windows).

### 1. Install via Pip
```bash
pip install melius-cli
```

### 2. Setup AI Models
Choose between cloud-based intelligence or local privacy:

- **Cloud (OpenRouter):**
  ```bash
  melius models add-key <YOUR_OPENROUTER_API_KEY>
  melius models set-provider openrouter
  ```

- **Local (Ollama):**
  ```bash
  melius models ollama-install
  melius models set-provider ollama
  ```

### 3. Link Telegram (Remote Control)
To control Melius from your phone:
1. Message [@BotFather](https://t.me/botfather) on Telegram to create a bot and get a **Token**.
2. Get your **User ID** from [@userinfobot](https://t.me/userinfobot).
3. Connect Melius:
   ```bash
   melius connect --token <BOT_TOKEN> --user-id <YOUR_ID>
   ```

---

## 🚀 Usage

### Start the Remote Gateway
Run this on your computer/server to enable remote control:
```bash
melius gateway
```
*Now you can send coding instructions to your Telegram bot from anywhere in the world!*

### Key Commands
| Command | Description |
| :--- | :--- |
| `melius gateway` | Start the remote control listener. |
| `melius connect` | Link your Telegram bot. |
| `melius skill list` | View installed agent capabilities. |
| `melius improve` | Run the self-optimization protocol. |
| `melius models list` | See active AI providers and models. |

---

## 🛠 Features

- **Full Workspace Control**: Read, write, and edit files; run shell commands; manage Git repos.
- **Skill Extensibility**: Download new "skills" (Python plugins) to give Melius new powers.
- **Auto-Improvement**: Melius analyzes its own logs to become a better coder over time.
- **Secure Access**: Only you (via your Telegram User ID) can control your agent.

## 📦 Automated Publishing (For Developers)

To publish Melius globally:
1. Update the version in `pyproject.toml`.
2. Push a tag: `git tag v0.1.0 && git push origin v0.1.0`.
3. The GitHub Action will automatically build and upload Melius to PyPI.

---
*Developed by AppointEase Dev - Empowering global developers with autonomous AI.*
