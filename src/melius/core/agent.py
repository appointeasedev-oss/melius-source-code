import os
import subprocess
import json
from rich.console import Console
from melius.models.provider import ModelProvider

console = Console()

class MeliusAgent:
    def __init__(self, workspace_dir="workspace", model_provider=None):
        self.workspace_dir = os.path.abspath(workspace_dir)
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
        self.provider = model_provider or ModelProvider()
        self.history = []
        self.system_prompt = """You are Melius, a world-class AI coding agent.
You have access to a workspace and can perform file operations, run shell commands, and browse the web.
Your goal is to assist the user with coding tasks efficiently and accurately.
When you need to perform an action, specify the tool and parameters.
Available tools: read_file, write_file, edit_file, execute_command, git_operation, browse_web.
Always respond in a structured format."""

    def run_cycle(self, user_input):
        """Main agent loop: think, act, observe."""
        self.history.append({"role": "user", "content": user_input})
        
        # 1. Think (Call LLM)
        response = self.provider.query_model(self.system_prompt, self.history)
        self.history.append({"role": "assistant", "content": response})
        
        # 2. Parse and Act (Simulated for now, would use regex/JSON parsing)
        # For production, we'd use function calling if the model supports it
        return response

    def execute_command(self, command):
        """Executes a shell command within the workspace."""
        console.print(f"[bold blue]>[/bold blue] [dim]{command}[/dim]")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=self.workspace_dir, 
                capture_output=True, 
                text=True,
                timeout=300
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out after 300 seconds."}
        except Exception as e:
            return {"error": str(e)}

    def read_file(self, file_path):
        full_path = os.path.join(self.workspace_dir, file_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def write_file(self, file_path, content):
        full_path = os.path.join(self.workspace_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    def edit_file(self, file_path, old_text, new_text):
        content = self.read_file(file_path)
        if content.startswith("Error"):
            return content
        if old_text not in content:
            return f"Error: '{old_text}' not found in {file_path}"
        new_content = content.replace(old_text, new_text)
        return self.write_file(file_path, new_content)

    def git_operation(self, action, **kwargs):
        """Handles git operations like clone, pull, push."""
        if action == "clone":
            repo_url = kwargs.get("repo_url")
            return self.execute_command(f"git clone {repo_url}")
        elif action == "pull":
            return self.execute_command("git pull")
        elif action == "push":
            msg = kwargs.get("message", "Melius auto-commit")
            self.execute_command("git add .")
            self.execute_command(f'git commit -m "{msg}"')
            return self.execute_command("git push")
        return {"error": f"Unknown git action: {action}"}
