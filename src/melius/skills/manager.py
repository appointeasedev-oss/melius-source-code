import os
import requests
import importlib.util
import sys
from rich.console import Console
from rich.table import Table

console = Console()

class SkillManager:
    def __init__(self, skills_dir="~/.melius/skills"):
        self.skills_dir = os.path.expanduser(skills_dir)
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)
        self.ensure_default_skills()

    def ensure_default_skills(self):
        # Placeholder for default skills that could be packaged or downloaded
        pass

    def download_skill(self, skill_url, skill_name):
        """Downloads a skill file from a URL (e.g., GitHub Gist or Raw file)."""
        console.print(f"[yellow]Downloading skill '{skill_name}' from {skill_url}...[/yellow]")
        try:
            response = requests.get(skill_url, timeout=30)
            response.raise_for_status()
            file_path = os.path.join(self.skills_dir, f"{skill_name}.py")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            console.print(f"[green]Skill '{skill_name}' installed successfully.[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Failed to download skill: {e}[/red]")
            return False

    def list_skills(self):
        skills = [f[:-3] for f in os.listdir(self.skills_dir) if f.endswith('.py')]
        table = Table(title="Melius Skills")
        table.add_column("Skill Name", style="cyan")
        table.add_column("Type", style="magenta")
        for s in skills:
            table.add_row(s, "User-defined")
        console.print(table)
        return skills

    def run_skill(self, skill_name, *args, **kwargs):
        file_path = os.path.join(self.skills_dir, f"{skill_name}.py")
        if not os.path.exists(file_path):
            return f"Error: Skill '{skill_name}' not found."

        spec = importlib.util.spec_from_file_location(skill_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[skill_name] = module
        spec.loader.exec_module(module)
        
        if hasattr(module, 'execute'):
            return module.execute(*args, **kwargs)
        else:
            return f"Error: Skill '{skill_name}' does not have an 'execute' function."

    def improve_agent(self, agent):
        """Self-improvement logic: analyze history and suggest optimizations."""
        console.print("[bold magenta]Initiating Self-Improvement Protocol...[/bold magenta]")
        prompt = "Analyze your recent interactions and suggest 3 ways to improve your coding efficiency or tool usage."
        suggestions = agent.run_cycle(prompt)
        console.print(f"[green]Melius Self-Analysis:[/green]\n{suggestions}")
        
        # In a real production scenario, this could lead to updating the system prompt 
        # or downloading new skills automatically.
        return suggestions
