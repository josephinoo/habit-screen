import typer
import json
import os
import datetime
from rich.console import Console
from rich.table import Table
from rich import box
from typing import Optional
from generate_wallpaper import main as generate_wallpaper

app = typer.Typer(help="Habit Screen CLI")
console = Console()

DATA_FILE = "habitos.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"active_habit": None, "habits": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.command()
def add(name: str, title: str = typer.Option(..., help="Display title on wallpaper"), subtitle: str = typer.Option("Last 365 Days", help="Subtitle")):
    """Add a new habit."""
    data = load_data()
    slug = name.lower().replace(" ", "-")

    if slug in data["habits"]:
        console.print(f"[bold red]Habit '{slug}' already exists![/bold red]")
        return

    data["habits"][slug] = {
        "title": title,
        "subtitle": subtitle,
        "dates": []
    }

    # If it's the first habit, make it active
    if not data.get("active_habit"):
        data["active_habit"] = slug

    save_data(data)
    console.print(f"[green]Added habit: {slug}[/green]")

@app.command()
def list():
    """List all habits."""
    data = load_data()
    active = data.get("active_habit")

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold magenta")
    table.add_column("Active", width=6, justify="center")
    table.add_column("Habit", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Count", justify="right")
    table.add_column("Last Tracked", style="dim")

    for slug, info in data.get("habits", {}).items():
        is_active = "*" if slug == active else ""
        count = len(info.get("dates", []))
        last_tracked = info.get("dates")[-1] if info.get("dates") else "-"

        table.add_row(is_active, slug, info["title"], str(count), last_tracked)

    console.print(table)

@app.command()
def switch(habit: str):
    """Switch the active wallpaper to a different habit."""
    data = load_data()
    slug = habit.lower().replace(" ", "-")

    if slug not in data["habits"]:
        console.print(f"[bold red]Habit '{slug}' not found![/bold red]")
        return

    data["active_habit"] = slug
    save_data(data)

    # Regenerate wallpaper
    info = data["habits"][slug]
    generate_wallpaper(info["title"], info["subtitle"], info["dates"])
    console.print(f"[green]Switched to {slug} and updated wallpaper.[/green]")

@app.command()
def now(habit: Optional[str] = typer.Argument(None)):
    """Track today for a habit (defaults to active habit)."""
    data = load_data()

    if habit:
        slug = habit.lower().replace(" ", "-")
    else:
        slug = data.get("active_habit")
        if not slug:
            console.print("[bold red]No active habit selected. Use 'switch' or provide a habit name.[/bold red]")
            return

    if slug not in data["habits"]:
        console.print(f"[bold red]Habit '{slug}' not found![/bold red]")
        return

    today = datetime.date.today().strftime("%Y-%m-%d")
    dates = data["habits"][slug]["dates"]

    if today not in dates:
        dates.append(today)
        dates.sort()
        save_data(data)
        console.print(f"[green]Tracked today for {slug}![/green]")
    else:
        console.print(f"[yellow]Today is already tracked for {slug}.[/yellow]")

    # Always regenerate to be sure
    info = data["habits"][slug]
    generate_wallpaper(info["title"], info["subtitle"], info["dates"])

if __name__ == "__main__":
    app()
