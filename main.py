import typer
import json
from tester import run_test
from lighthouse_runner import run_lighthouse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from halo import Halo
import time

app = typer.Typer(invoke_without_command=True)
console = Console()

def show_banner():
    banner = """
███████╗███████╗████████╗████████╗███████╗██████╗ ████████╗███████╗██████╗ 
██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
███████╗█████╗     ██║      ██║   █████╗  ██████╔╝   ██║   █████╗  ██████╔╝
╚════██║██╔══╝     ██║      ██║   ██╔══╝  ██╔═══╝    ██║   ██╔══╝  ██╔═══╝ 
███████║███████╗   ██║      ██║   ███████╗██║        ██║   ███████╗██║     
╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚══════╝╚═╝        ╚═╝   ╚══════╝╚═╝     
    """
    console.print(Panel(banner, style="bold green", subtitle="API & Frontend Load Tester"))

def print_summary(combined):
    console.print("\n[bold cyan] API Test Results[/bold cyan]")
    api = combined["api_test"]
    api_table = Table(show_header=True, header_style="bold magenta")
    api_table.add_column("Metric", style="dim")
    api_table.add_column("Value")
    for k, v in api.items():
        api_table.add_row(k.replace("_", " ").capitalize(), str(v))
    console.print(api_table)

    if combined["frontend_audit"]:
        console.print("\n[bold green] Frontend Lighthouse Audit[/bold green]")
        fe = combined["frontend_audit"]
        fe_table = Table(show_header=True, header_style="bold yellow")
        fe_table.add_column("Metric", style="dim")
        fe_table.add_column("Value")
        for k, v in fe.items():
            fe_table.add_row(k.upper(), str(v))
        console.print(fe_table)

@app.callback()
def main(
    url: str = typer.Option(..., help="Target URL"),
    requests: int = typer.Option(50, help="Total number of requests"),
    concurrency: int = typer.Option(10, help="Number of concurrent requests"),
    method: str = typer.Option("GET", help="HTTP method"),
    include_frontend: bool = typer.Option(False, "--frontend", help="Run Lighthouse audit"),
    output: str = typer.Option("combined_report.json", help="Output report file")
):
    show_banner()

    spinner = Halo(text='Running API Load Test...', spinner='dots')
    spinner.start()
    api_results = run_test(url, requests, concurrency, method)
    spinner.succeed("API test completed.")

    frontend_results = None
    if include_frontend:
        spinner = Halo(text='Running Lighthouse Audit...', spinner='bouncingBar')
        spinner.start()
        frontend_results = run_lighthouse(url)
        spinner.succeed(" Frontend audit completed.")

    combined = {
        "api_test": api_results,
        "frontend_audit": frontend_results
    }

    with open(output, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)

    console.print(f"\n[bold green] Combined report saved to:[/bold green] {output}")
    print_summary(combined)

if __name__ == "__main__":
    app()
