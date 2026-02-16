import os
import subprocess
from rich.console import Console

console = Console()

class MeliusAgent:
    def __init__(self, workspace_dir="workspace"):
        self.workspace_dir = os.path.abspath(workspace_dir)
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
        
    def execute_command(self, command):
        """Executes a shell command within the workspace."""
        console.print(f"[dim]Executing: {command}[/dim]")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=self.workspace_dir, 
                capture_output=True, 
                text=True
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {"error": str(e)}

    def read_file(self, file_path):
        full_path = os.path.join(self.workspace_dir, file_path)
        try:
            with open(full_path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def write_file(self, file_path, content):
        full_path = os.path.join(self.workspace_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            with open(full_path, 'w') as f:
                f.write(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    def edit_file(self, file_path, old_text, new_text):
        content = self.read_file(file_path)
        if "Error" in content:
            return content
        new_content = content.replace(old_text, new_text)
        return self.write_file(file_path, new_content)

    def git_clone(self, repo_url):
        return self.execute_command(f"git clone {repo_url}")
