import requests
import json
import subprocess
import os
from rich.console import Console

console = Console()

class ModelProvider:
    def __init__(self, config_path="~/.melius/config.json"):
        self.config_path = os.path.expanduser(config_path)
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "active_provider": "openrouter",
                "openrouter_keys": [],
                "default_model": "anthropic/claude-3.5-sonnet",
                "ollama_model": "llama3"
            }
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            self.save_config()

    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def query_model(self, system_prompt, history):
        if self.config["active_provider"] == "openrouter":
            return self.query_openrouter(system_prompt, history)
        elif self.config["active_provider"] == "ollama":
            return self.query_ollama(system_prompt, history)
        return "Error: No active provider configured."

    def query_openrouter(self, system_prompt, history):
        if not self.config["openrouter_keys"]:
            return "Error: No OpenRouter API keys found. Use 'melius models add-key' to add one."
        
        # Simple round-robin or first-available key strategy
        api_key = self.config["openrouter_keys"][0]
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://melius.ai", # Optional
            "X-Title": "Melius CLI"
        }
        
        messages = [{"role": "system", "content": system_prompt}] + history
        
        data = {
            "model": self.config["default_model"],
            "messages": messages
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(data),
                timeout=60
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error querying OpenRouter: {str(e)}"

    def query_ollama(self, system_prompt, history):
        messages = [{"role": "system", "content": system_prompt}] + history
        data = {
            "model": self.config["ollama_model"],
            "messages": messages,
            "stream": False
        }
        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json=data,
                timeout=120
            )
            response.raise_for_status()
            return response.json()['message']['content']
        except Exception as e:
            return f"Error querying Ollama: {str(e)}. Is Ollama running?"

    def install_ollama(self):
        """Install Ollama automatically."""
        console.print("[yellow]Installing Ollama...[/yellow]")
        try:
            subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
            console.print("[green]Ollama installed successfully![/green]")
            return True
        except Exception as e:
            console.print(f"[red]Failed to install Ollama: {e}[/red]")
            return False

    def list_ollama_models(self):
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            return result.stdout
        except:
            return "Ollama not found."
