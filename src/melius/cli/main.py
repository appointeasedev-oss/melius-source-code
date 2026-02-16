import click
import os
import json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from melius.gateway.telegram_handler import MeliusGateway
from melius.models.provider import ModelProvider
from melius.skills.manager import SkillManager
from melius.core.agent import MeliusAgent

console = Console()

def print_banner():
    banner = Text("MELIUS", style="bold cyan")
    banner.append("\nAI Coding Agent & Remote Gateway", style="italic magenta")
    console.print(Panel(banner, border_style="blue", expand=False))

@click.group()
def main():
    """Melius: Your Autonomous AI Coding Agent."""
    pass

@main.command()
def gateway():
    """Start the remote access gateway."""
    print_banner()
    config_path = os.path.expanduser("~/.melius/telegram_config.json")
    if not os.path.exists(config_path):
        console.print("[red]Telegram not configured. Run 'melius connect' first.[/red]")
        return
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    gateway = MeliusGateway(config['token'], config.get('allowed_user_id'))
    gateway.run()

@main.command()
@click.option('--token', help='Telegram Bot Token')
@click.option('--user-id', type=int, help='Your Telegram User ID for security')
def connect(token, user_id):
    """Configure Telegram connectivity."""
    print_banner()
    if not token:
        token = click.prompt("Please enter your Telegram Bot Token", hide_input=True)
    if not user_id:
        user_id = click.prompt("Please enter your Telegram User ID (for security)", type=int)
    
    config_path = os.path.expanduser("~/.melius/telegram_config.json")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump({"token": token, "allowed_user_id": user_id}, f, indent=4)
    
    console.print("[bold green]Success![/bold green] Melius is now linked to your Telegram bot.")

@main.command()
@click.argument('action', type=click.Choice(['list', 'install', 'run']))
@click.argument('skill_name', required=False)
@click.option('--url', help='URL to download skill from')
def skill(action, skill_name, url):
    """Manage and download agent skills."""
    print_banner()
    manager = SkillManager()
    if action == 'list':
        manager.list_skills()
    elif action == 'install':
        if not skill_name or not url:
            console.print("[red]Usage: melius skill install <name> --url <url>[/red]")
            return
        manager.download_skill(url, skill_name)
    elif action == 'run':
        if not skill_name:
            console.print("[red]Usage: melius skill run <name>[/red]")
            return
        result = manager.run_skill(skill_name)
        console.print(f"Result: {result}")

@main.command()
@click.argument('url')
def browser(url):
    """Start the inbuilt browser data access."""
    print_banner()
    console.print(f"[blue]Launching Melius Browser for: {url}[/blue]")
    # In production, this would trigger the Playwright engine
    from melius.browser.engine import MeliusBrowser
    import asyncio
    
    async def run_browser():
        b = MeliusBrowser()
        title = await b.navigate(url)
        console.print(f"Page Title: [bold]{title}[/bold]")
        await b.close()
    
    asyncio.run(run_browser())

@main.command()
def improve():
    """Initiate the self-improvement protocol."""
    print_banner()
    agent = MeliusAgent()
    manager = SkillManager()
    manager.improve_agent(agent)

@main.command()
@click.argument('action', type=click.Choice(['list', 'set-provider', 'add-key', 'ollama-install']))
@click.argument('value', required=False)
def models(action, value):
    """Manage AI models and API keys."""
    print_banner()
    provider = ModelProvider()
    if action == 'list':
        console.print(f"Active Provider: [bold green]{provider.config['active_provider']}[/bold green]")
        console.print(f"Default Model: [cyan]{provider.config['default_model']}[/cyan]")
        if provider.config['active_provider'] == 'ollama':
            console.print("Local Ollama Models:")
            console.print(provider.list_ollama_models())
    elif action == 'set-provider':
        if value in ['openrouter', 'ollama']:
            provider.config['active_provider'] = value
            provider.save_config()
            console.print(f"Provider set to {value}")
        else:
            console.print("[red]Invalid provider. Choose 'openrouter' or 'ollama'.[/red]")
    elif action == 'add-key':
        key = value or click.prompt("Enter OpenRouter API Key", hide_input=True)
        provider.config['openrouter_keys'].append(key)
        provider.save_config()
        console.print("[green]API Key added.[/green]")
    elif action == 'ollama-install':
        provider.install_ollama()

if __name__ == "__main__":
    main()
