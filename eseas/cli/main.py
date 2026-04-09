#!/usr/bin/env python
"""
eseas CLI - Command line interface for eseas seasonal adjustment tool
"""

import sys
import argparse
from pathlib import Path
import yaml
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


DEFAULT_CONFIG = {
    "demetra_folder": None,  # Will be set from first run
    "java_folder": None,  # Will use auto-download
    "local_folder": "./eseas_output",
    "auto_download": True,
    "auto_approve": False,
    "csvlayout": "vtable",
    "workspace_mode": True,
    "result_file_names": ["sa", "s", "cal"],
    "verbose": False,
    "test": False,
    "replace_general_params": False,
    "replace_original_files": False,
    "file_name_explanation": True,
}


def get_config_path() -> Path:
    """Get the path to the config file in current directory"""
    return Path.cwd() / "eseas_config.yaml"


def create_default_config(workspace_path: Optional[str] = None) -> dict:
    """Create default configuration with optional workspace path"""
    config = DEFAULT_CONFIG.copy()
    if workspace_path:
        config["demetra_folder"] = str(Path(workspace_path).absolute())
    return config


def load_config(config_path: Path) -> dict:
    """Load configuration from YAML file"""
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            if config is None:
                return {}
            return config
    except FileNotFoundError:
        return {}
    except yaml.YAMLError as e:
        console.print(f"[red]Error parsing config file: {e}[/red]")
        sys.exit(1)


def save_config(config: dict, config_path: Path):
    """Save configuration to YAML file"""
    try:
        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        console.print(f"[green]✓[/green] Configuration saved to {config_path}")
    except Exception as e:
        console.print(f"[red]Error saving config: {e}[/red]")
        sys.exit(1)


def show_config(config: dict):
    """Display current configuration in a nice table"""
    table = Table(title="Current Configuration")
    table.add_column("Parameter", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    for key, value in config.items():
        if isinstance(value, list):
            value_str = ", ".join(str(v) for v in value)
        else:
            value_str = str(value) if value is not None else "[dim]not set[/dim]"
        table.add_row(key, value_str)

    console.print(table)


def cmd_run(args):
    """Run seasonal adjustment"""
    from eseas import Options, Seasonal

    # Determine config file location
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            console.print(f"[red]Config file not found: {config_path}[/red]")
            sys.exit(1)
    else:
        config_path = get_config_path()

    # Load existing config or create new one
    if config_path.exists():
        console.print(f"[cyan]Loading configuration from {config_path}[/cyan]")
        config = load_config(config_path)
    else:
        # First run - create config
        workspace_path = args.workspace or args.demetra_folder
        if not workspace_path:
            console.print(
                "[yellow]No workspace path provided and no config file found.[/yellow]"
            )
            console.print("[cyan]Usage:[/cyan] eseas run <workspace_path>")
            console.print("[cyan]Or:[/cyan]     eseas run --workspace <path>")
            sys.exit(1)

        console.print("[cyan]First run detected! Creating configuration file...[/cyan]")
        config = create_default_config(workspace_path)
        save_config(config, config_path)
        console.print()
        console.print(
            Panel.fit(
                f"""[green]Configuration created![/green]

Edit [cyan]{config_path}[/cyan] to customize settings.
Next time, simply run: [yellow]eseas run[/yellow]""",
                title="Setup Complete",
                border_style="green",
            )
        )
        console.print()

    # Override config with command line arguments
    if args.workspace:
        config["demetra_folder"] = str(Path(args.workspace).absolute())
    if args.output:
        config["local_folder"] = str(Path(args.output).absolute())
    if args.verbose is not None:
        config["verbose"] = args.verbose
    if args.test is not None:
        config["test"] = args.test
    if args.csvlayout:
        config["csvlayout"] = args.csvlayout

    # Validate required fields
    if not config.get("demetra_folder"):
        console.print(
            "[red]Error: demetra_folder not set in config or command line[/red]"
        )
        sys.exit(1)

    # Create Options and run
    try:
        console.print("[cyan]Starting seasonal adjustment...[/cyan]")
        options = Options(
            demetra_folder=config["demetra_folder"],
            java_folder=config.get("java_folder"),
            local_folder=config["local_folder"],
            auto_download=config.get("auto_download", True),
            auto_approve=config.get("auto_approve", False),
            csvlayout=config.get("csvlayout", "vtable"),
            workspace_mode=config.get("workspace_mode", True),
            result_file_names=tuple(
                config.get("result_file_names", ["sa", "s", "cal"])
            ),
            verbose=config.get("verbose", False),
            test=config.get("test", False),
            replace_general_params=config.get("replace_general_params", False),
            replace_original_files=config.get("replace_original_files", False),
            file_name_explanation=config.get("file_name_explanation", True),
        )

        m = Seasonal(options)
        m.run()

        console.print()
        console.print(
            Panel.fit(
                "[green]✓ Seasonal adjustment completed successfully![/green]",
                border_style="green",
            )
        )

    except Exception as e:
        console.print(f"\n[red]Error during execution: {e}[/red]")
        console.print("\n[yellow]Check logs at:[/yellow] .eseas/.logs/failed_runs.log")
        sys.exit(1)


def cmd_config(args):
    """Manage configuration"""
    config_path = Path(args.config) if args.config else get_config_path()

    if args.action == "show":
        # Show current configuration
        if not config_path.exists():
            console.print(
                f"[yellow]No configuration file found at {config_path}[/yellow]"
            )
            console.print("[cyan]Run 'eseas run <workspace>' to create one.[/cyan]")
            return

        config = load_config(config_path)
        show_config(config)

    elif args.action == "set":
        # Set a configuration value
        if not args.key or not args.value:
            console.print("[red]Error: Both --key and --value are required[/red]")
            sys.exit(1)

        # Load existing or create new
        if config_path.exists():
            config = load_config(config_path)
        else:
            config = create_default_config()

        # Parse value (handle booleans and lists)
        value = args.value
        if value.lower() in ("true", "yes", "on"):
            value = True
        elif value.lower() in ("false", "no", "off"):
            value = False
        elif "," in value:
            value = [v.strip() for v in value.split(",")]

        config[args.key] = value
        save_config(config, config_path)
        console.print(f"[green]✓[/green] Set {args.key} = {value}")

    elif args.action == "init":
        # Create new config with defaults
        if config_path.exists() and not args.force:
            console.print(f"[yellow]Config file already exists: {config_path}[/yellow]")
            console.print("[cyan]Use --force to overwrite[/cyan]")
            return

        workspace = args.workspace if args.workspace else None
        config = create_default_config(workspace)
        save_config(config, config_path)
        console.print()
        show_config(config)


def cmd_validate(args):
    """Validate workspace and configuration"""

    workspace_path = Path(args.workspace)

    console.print(f"[cyan]Validating workspace:[/cyan] {workspace_path}")
    console.print()

    # Check if path exists
    if not workspace_path.exists():
        console.print(f"[red]✗ Path does not exist: {workspace_path}[/red]")
        sys.exit(1)
    console.print("[green]✓[/green] Path exists")

    # Check if it's a directory
    if not workspace_path.is_dir():
        console.print("[red]✗ Path is not a directory[/red]")
        sys.exit(1)
    console.print("[green]✓[/green] Path is a directory")

    # Check for XML files
    xml_files = list(workspace_path.rglob("*.xml"))
    if not xml_files:
        console.print("[yellow]⚠[/yellow] No XML files found")
    else:
        console.print(f"[green]✓[/green] Found {len(xml_files)} XML file(s)")
        for xml_file in xml_files[:5]:  # Show first 5
            console.print(f"  - {xml_file.name}")
        if len(xml_files) > 5:
            console.print(f"  ... and {len(xml_files) - 5} more")

    console.print()
    console.print("[green]Validation complete![/green]")


def cmd_doctor(args):
    """Check system requirements"""
    import platform
    import subprocess

    console.print("[cyan]System Diagnostics[/cyan]")
    console.print()

    # Python version
    python_version = platform.python_version()
    console.print(f"[green]✓[/green] Python: {python_version}")

    # Platform
    system = platform.system()
    console.print(f"[green]✓[/green] OS: {system}")

    # Java check
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            check=False,
            encoding='utf-8'
             
        )
        if result.returncode == 0:
            # Java version is in stderr
            java_version = result.stderr.split("\n")[0]
            console.print(f"[green]✓[/green] Java: {java_version}")
        else:
            console.print("[yellow]⚠[/yellow] Java not found in PATH")
            console.print("  [dim]Tip: Set auto_download=true in config[/dim]")
    except FileNotFoundError:
        console.print("[yellow]⚠[/yellow] Java not found")
        console.print("  [dim]Tip: Set auto_download=true in config[/dim]")

    # Config file check
    config_path = get_config_path()
    if config_path.exists():
        console.print(f"[green]✓[/green] Config: {config_path}")
    else:
        console.print("[yellow]⚠[/yellow] No config file found")
        console.print("  [dim]Run 'eseas run <workspace>' to create one[/dim]")

    # Logs directory
    logs_dir = Path.cwd() / ".eseas" / ".logs"
    if logs_dir.exists():
        log_files = list(logs_dir.glob("*.log"))
        console.print(f"[green]✓[/green] Logs directory: {len(log_files)} log file(s)")
    else:
        console.print("[yellow]⚠[/yellow] No logs directory yet")

    console.print()
    console.print("[green]Diagnostics complete![/green]")


def cmd_logs(args):
    """Show logs"""
    logs_dir = Path.cwd() / ".eseas" / ".logs"

    if not logs_dir.exists():
        console.print("[yellow]No logs directory found[/yellow]")
        console.print("[dim]Logs will be created after first run[/dim]")
        return

    if args.type == "success":
        log_file = logs_dir / "last_good_run.log"
    elif args.type == "error":
        log_file = logs_dir / "failed_runs.log"
    elif args.type == "emergency":
        log_file = logs_dir / "emergency.log"
    else:
        # Show all logs
        console.print(f"[cyan]Logs directory:[/cyan] {logs_dir}")
        console.print()
        for log_file in logs_dir.glob("*.log"):
            size = log_file.stat().st_size
            console.print(f"  {log_file.name} ({size:,} bytes)")
        return

    if not log_file.exists():
        console.print(f"[yellow]Log file not found: {log_file.name}[/yellow]")
        return

    # Show last N lines
    lines = args.lines or 50
    content = log_file.read_text()
    log_lines = content.split("\n")
    last_lines = log_lines[-lines:]

    console.print(f"[cyan]Last {lines} lines from {log_file.name}:[/cyan]")
    console.print()
    for line in last_lines:
        if line.strip():
            console.print(line)


def main():
    """Main CLI entry point"""
    # Get version
    try:
        from eseas import __version__
    except ImportError:
        import importlib.metadata

        __version__ = importlib.metadata.version("eseas")

    parser = argparse.ArgumentParser(
        description="eseas - Seasonal adjustment tool CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show version
  eseas --version

  # First run - creates eseas_config.yaml
  eseas run /path/to/workspace

  # Subsequent runs - uses eseas_config.yaml
  eseas run

  # Use custom config file
  eseas run --config myproject.yaml

  # Override settings
  eseas run --verbose --test

  # Show current configuration
  eseas config show

  # Validate workspace
  eseas validate /path/to/workspace

  # Check system requirements
  eseas doctor

  # View logs
  eseas logs --type error
        """,
    )

    parser.add_argument(
        "--version", "-V", action="version", version=f"eseas {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run seasonal adjustment")
    run_parser.add_argument("workspace", nargs="?", help="Path to Demetra workspace")
    run_parser.add_argument(
        "--config", "-c", help="Path to config file (default: eseas_config.yaml)"
    )
    run_parser.add_argument(
        "--demetra-folder", help="Path to Demetra workspace (alternative to positional)"
    )
    run_parser.add_argument("--output", "-o", help="Output directory")
    run_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )
    run_parser.add_argument(
        "--test", "-t", action="store_true", help="Test mode (limit files)"
    )
    run_parser.add_argument(
        "--csvlayout", choices=["vtable", "list"], help="CSV layout format"
    )
    run_parser.set_defaults(func=cmd_run)

    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument(
        "action", choices=["show", "set", "init"], help="Config action"
    )
    config_parser.add_argument("--key", help="Configuration key to set")
    config_parser.add_argument("--value", help="Configuration value to set")
    config_parser.add_argument("--workspace", help="Workspace path for init")
    config_parser.add_argument("--config", "-c", help="Config file path")
    config_parser.add_argument(
        "--force", action="store_true", help="Force overwrite for init"
    )
    config_parser.set_defaults(func=cmd_config)

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate workspace")
    validate_parser.add_argument("workspace", help="Path to workspace to validate")
    validate_parser.set_defaults(func=cmd_validate)

    # Doctor command
    doctor_parser = subparsers.add_parser("doctor", help="Check system requirements")
    doctor_parser.set_defaults(func=cmd_doctor)

    # Logs command
    logs_parser = subparsers.add_parser("logs", help="View logs")
    logs_parser.add_argument(
        "--type",
        "-t",
        choices=["success", "error", "emergency"],
        help="Log type to view",
    )
    logs_parser.add_argument(
        "--lines", "-n", type=int, help="Number of lines to show (default: 50)"
    )
    logs_parser.set_defaults(func=cmd_logs)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Execute command
    args.func(args)


if __name__ == "__main__":
    main()
