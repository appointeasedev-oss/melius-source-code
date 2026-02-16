import requests
import json
import subprocess

class ModelProvider:
    def __init__(self, api_key=None, base_url="https://openrouter.ai/api/v1"):
        self.api_key = api_key
        self.base_url = base_url

    def query_openrouter(self, model, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(f"{self.base_url}/chat/completions", headers=headers, data=json.dumps(data))
        return response.json()

    def check_ollama(self):
        """Checks if Ollama is installed and running."""
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def install_ollama(self):
        """Install Ollama on Linux."""
        # This is a simplified version of the install command
        install_cmd = "curl -fsSL https://ollama.com/install.sh | sh"
        return subprocess.run(install_cmd, shell=True)

    def list_local_models(self):
        if self.check_ollama():
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            return result.stdout
        return "Ollama not found."
