"""
HoneyClaw CLI Application.
Built with Click & Rich. Adheres to GrooveXlabs OLED-Black aesthetic.
"""

import json
import os
import sys
from typing import Optional
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from honeyclaw import __version__
from honeyclaw.config import HoneypotConfig, load_config
from honeyclaw.core.canary import CanaryEngine
from honeyclaw.server import DecoyMcpServer

console = Console()


def print_banner():
    banner = f"""[bold yellow] ██╗  ██╗ ██████╗ ███╗   ██╗███████╗██╗   ██╗ ██████╗██╗      █████╗ ██╗    ██╗[/bold yellow]
[bold yellow] ██║  ██║██╔═══██╗████╗  ██║██╔════╝╚██╗ ██╔╝██╔════╝██║     ██╔══██╗██║    ██║[/bold yellow]
[bold yellow] ███████║██║   ██║██╔██╗ ██║█████╗   ╚████╔╝ ██║     ██║     ███████║██║ █╗ ██║[/bold yellow]
[bold yellow] ██╔══██║██║   ██║██║╚██╗██║██╔══╝    ╚██╔╝  ██║     ██║     ██╔══██║██║███╗██║[/bold yellow]
[bold yellow] ██║  ██║╚██████╔╝██║ ╚████║███████╗   ██║   ╚██████╗███████╗██║  ██║╚███╔███╔╝[/bold yellow]
[bold yellow] ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚═════╝╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝ [/bold yellow]
[dim cyan]  Autonomous AI Honeypot & Agent Canary Engine (v{__version__})[/dim cyan]
[dim red]  GrooveXlabs Sovereign Defense Ecosystem[/dim red]
"""
    console.print(banner)


@click.group()
@click.version_option(version=__version__)
def main():
    """HoneyClaw: Autonomous AI Honeypot & Agent Canary Engine."""
    pass


@main.command(name="status")
@click.option("--config", "-c", "config_path", help="Path to honeyclaw.yaml config file.")
def status_cmd(config_path: Optional[str]):
    """Display active honeypot status and decoy suite health."""
    print_banner()
    cfg = load_config(config_path)

    table = Table(title="[bold green]HoneyClaw Honeypot Status[/bold green]", border_style="dim white")
    table.add_column("Component", style="cyan")
    table.add_column("Status / Details", style="bold white")

    table.add_row("Server Name", cfg.server_name)
    table.add_row("Vault Decoy Tool", "✅ Active (Synthetic AWS/GitHub/OpenAI tokens)" if cfg.enable_vault_decoy else "❌ Disabled")
    table.add_row("Database Decoy Tool", "✅ Active (Synthetic customer PII & canary emails)" if cfg.enable_database_decoy else "❌ Disabled")
    table.add_row("Shell Decoy Tool", "✅ Active (Simulated sandbox Linux shell)" if cfg.enable_shell_decoy else "❌ Disabled")
    table.add_row("Filesystem Decoy Tool", "✅ Active (Synthetic .env & secrets)" if cfg.enable_filesystem_decoy else "❌ Disabled")
    table.add_row("Event Log File", f"[underline]{cfg.event_log_path}[/underline]")

    # Event count check
    event_count = 0
    if os.path.exists(cfg.event_log_path):
        with open(cfg.event_log_path, "r", encoding="utf-8") as f:
            event_count = sum(1 for line in f if line.strip())
    table.add_row("Trapped Interactions", f"[bold yellow]{event_count}[/bold yellow] events recorded")

    console.print(table)


@main.command(name="serve")
@click.option("--config", "-c", "config_path", help="Path to honeyclaw.yaml config file.")
def serve_cmd(config_path: Optional[str]):
    """Launch the Decoy MCP Server over stdio."""
    cfg = load_config(config_path)
    server = DecoyMcpServer(cfg)
    server.run_stdio()


@main.command(name="generate-canary")
@click.option("--type", "-t", "canary_type", type=click.Choice(["aws", "github", "openai"]), default="aws", help="Type of canary to generate.")
@click.option("--label", "-l", default="manual-canary", help="Identifying label for tracking.")
def generate_canary_cmd(canary_type: str, label: str):
    """Generate a realistic synthetic canary credential."""
    engine = CanaryEngine()

    if canary_type == "aws":
        data = engine.generate_aws_canary(label=label)
        console.print(Panel(
            f"[bold cyan]Type:[/bold cyan] AWS Access Key Pair\n"
            f"[bold cyan]Label:[/bold cyan] {label}\n"
            f"[bold green]AWS_ACCESS_KEY_ID:[/bold green] [bold white]{data['access_key_id']}[/bold white]\n"
            f"[bold green]AWS_SECRET_ACCESS_KEY:[/bold green] [bold white]{data['secret_access_key']}[/bold white]",
            title="Generated HoneyClaw Canary",
            border_style="yellow",
        ))
    elif canary_type == "github":
        data = engine.generate_github_pat_canary(label=label)
        console.print(Panel(
            f"[bold cyan]Type:[/bold cyan] GitHub Personal Access Token\n"
            f"[bold cyan]Label:[/bold cyan] {label}\n"
            f"[bold green]TOKEN:[/bold green] [bold white]{data['token']}[/bold white]",
            title="Generated HoneyClaw Canary",
            border_style="yellow",
        ))
    elif canary_type == "openai":
        data = engine.generate_openai_canary(label=label)
        console.print(Panel(
            f"[bold cyan]Type:[/bold cyan] OpenAI API Key\n"
            f"[bold cyan]Label:[/bold cyan] {label}\n"
            f"[bold green]API_KEY:[/bold green] [bold white]{data['token']}[/bold white]",
            title="Generated HoneyClaw Canary",
            border_style="yellow",
        ))


@main.command(name="verify-canary")
@click.option("--key", "-k", required=True, help="Canary token/key to verify.")
@click.option("--label", "-l", default="manual-canary", help="Expected label.")
def verify_canary_cmd(key: str, label: str):
    """Verify if an intercepted token was generated by HoneyClaw."""
    engine = CanaryEngine()
    is_valid, msg = engine.verify_aws_canary(key, label=label)

    if is_valid:
        console.print(Panel(
            f"[bold green]✔ AUTHENTIC HONEYCLAW CANARY[/bold green]\n"
            f"[bold]Details:[/bold] {msg}\n"
            f"[bold yellow]Alert: This token was exfiltrated from your HoneyClaw environment![/bold yellow]",
            title="Canary Verification Success",
            border_style="green",
        ))
    else:
        console.print(Panel(
            f"[bold red]✖ NOT A VERIFIED HONEYCLAW CANARY[/bold red]\n"
            f"[dim]The provided key does not match the HMAC signature for this honeypot.[/dim]",
            title="Canary Verification Result",
            border_style="red",
        ))
        sys.exit(1)


@main.command(name="events")
@click.option("--log", "-l", "log_path", default="honeyclaw_events.jsonl", help="Path to events file.")
@click.option("--limit", "-n", default=10, help="Number of recent events to display.")
def events_cmd(log_path: str, limit: int):
    """View recent trapped agent interactions and behavioral profiles."""
    if not os.path.exists(log_path):
        console.print(f"[dim]No event log found at {log_path}. Honeypot has not recorded any triggers yet.[/dim]")
        return

    events = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    events.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue

    recent = events[-limit:]
    table = Table(title=f"[bold yellow]Recent HoneyClaw Events (Last {len(recent)})[/bold yellow]", border_style="dim white")
    table.add_column("Timestamp", style="cyan")
    table.add_column("Tool Trapped", style="bold white")
    table.add_column("Attacker Archetype", style="magenta")
    table.add_column("Threat Level", style="bold red")

    for ev in reversed(recent):
        profile = ev.get("profile", {})
        table.add_row(
            ev.get("timestamp", "N/A"),
            ev.get("tool_name", "N/A"),
            profile.get("archetype", "UNKNOWN"),
            profile.get("threat_level", "LOW"),
        )

    console.print(table)


@main.command(name="init")
def init_cmd():
    """Create default honeyclaw.yaml configuration template."""
    content = """# HoneyClaw Honeypot Configuration
version: "1.0.0"
server_name: "internal-infra-agent-mcp"
server_version: "1.0.0"

# Decoy Suites
enable_vault_decoy: true
enable_database_decoy: true
enable_shell_decoy: true
enable_filesystem_decoy: true

# Forensic Telemetry
event_log_path: "honeyclaw_events.jsonl"
webhook_url: null
"""
    with open("honeyclaw.yaml", "w", encoding="utf-8") as f:
        f.write(content)
    console.print("[bold green]Created honeyclaw.yaml with sovereign honeypot defaults.[/bold green]")


if __name__ == "__main__":
    main()
