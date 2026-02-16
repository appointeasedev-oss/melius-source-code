import os
import subprocess
import json
import re
from rich.console import Console
from melius.models.provider import ModelProvider

console = Console()

class MeliusAgent:
    def __init__(self, workspace_dir="workspace", provider=None):
        self.workspace_dir = os.path.abspath(workspace_dir)
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
        self.provider = provider or ModelProvider()
        self.history = []
        self.system_prompt = """You are Melius, a high-performance AI coding agent.
You operate in a workspace and can execute commands, read/write files, and browse the web.
When you need to act, output a JSON block with "tool" and "parameters".

Available Tools:
1. execute_command(command: str) - Run shell commands.
2. read_file(path: str) - Read file content.
3. write_file(path: str, content: str) - Write or overwrite a file.
4. edit_file(path: str, old_text: str, new_text: str) - Replace text in a file.
5. git_op(action: str, repo_url: str = None, message: str = None) - Git operations (clone, pull, push).

Example Output:
{
    "thought": "I need to list the files in the directory.",
    "tool": "execute_command",
    "parameters": {"command": "ls -la"}
}"""

    def run_cycle(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        raw_response = self.provider.query_model(self.system_prompt, self.history)
        self.history.append({"role": "assistant", "content": raw_response})
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                action = json.loads(json_match.group())
                tool = action.get("tool")
                params = action.get("parameters", {})
                
                result = self.dispatch_tool(tool, params)
                observation = f"Observation: {result}"
                self.history.append({"role": "system", "content": observation})
                
                # Auto-continue if a tool was used to provide final answer
                return f"Executed {tool}. Result: {result}\n\n{raw_response}"
            return raw_response
        except Exception as e:
            return f"Error processing agent action: {str(e)}\nRaw Response: {raw_response}"

    def dispatch_tool(self, tool, params):
        if tool == "execute_command":
            return self.execute_command(params.get("command"))
        elif tool == "read_file":
            return self.read_file(params.get("path"))
        elif tool == "write_file":
            return self.write_file(params.get("path"), params.get("content"))
        elif tool == "edit_file":
            return self.edit_file(params.get("path"), params.get("old_text"), params.get("new_text"))
        elif tool == "git_op":
            return self.git_operation(params.get("action"), **params)
        return f"Unknown tool: {tool}"

    def execute_command(self, command):
        console.print(f"[bold blue]>[/bold blue] [dim]{command}[/dim]")
        try:
            result = subprocess.run(command, shell=True, cwd=self.workspace_dir, capture_output=True, text=True, timeout=300)
            return {"stdout": result.stdout, "stderr": result.stderr, "code": result.returncode}
        except Exception as e:
            return {"error": str(e)}

    def read_file(self, path):
        full_path = os.path.join(self.workspace_dir, path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return str(e)

    def write_file(self, path, content):
        full_path = os.path.join(self.workspace_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Wrote to {path}"
        except Exception as e:
            return str(e)

    def edit_file(self, path, old_text, new_text):
        content = self.read_file(path)
        if old_text not in content:
            return "Old text not found."
        return self.write_file(path, content.replace(old_text, new_text))

    def git_operation(self, action, **kwargs):
        if action == "clone":
            return self.execute_command(f"git clone {kwargs.get('repo_url')}")
        elif action == "pull":
            return self.execute_command("git pull")
        elif action == "push":
            self.execute_command("git add .")
            self.execute_command(f"git commit -m '{kwargs.get('message', 'Melius update')}'")
            return self.execute_command("git push")
        return "Invalid git action."
