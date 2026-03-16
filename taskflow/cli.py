import typer
import uuid
from rich.console import Console
from rich.table import Table
from datetime import datetime

# Importamos nuestras capas previas
from taskflow.models import Task
from taskflow.storage import load_tasks, save_tasks
from taskflow.logic import sort_by_priority

app = typer.Typer(help="TaskFlow CLI - Gestión de tareas ultra rápida.")
console = Console()
DB_PATH = "tasks.json"

def get_color(prioridad: int) -> str:
    """Retorna un color de Rich según la prioridad."""
    colors = {5: "bold red", 4: "orange1", 3: "yellow", 2: "green", 1: "cyan"}
    return colors.get(prioridad, "white")

@app.command()
def add(titulo: str, prioridad: int = typer.Argument(..., min=1, max=5)):
    """Añade una nueva tarea con un ID único."""
    tasks = load_tasks(DB_PATH)
    
    # Generamos ID usando la parte inicial de un uuid4 para brevedad
    nuevo_id = int(uuid.uuid4().int % 10000)
    nueva_tarea = Task(id=nuevo_id, titulo=titulo, prioridad=prioridad, estado="Pendiente")
    
    tasks.append(nueva_tarea)
    save_tasks(tasks, DB_PATH)
    
    console.print(f"[bold green]✔[/bold green] Tarea '[italic]{titulo}[/italic]' añadida con ID [bold]{nuevo_id}[/bold]")

@app.command()
def list():
    """Muestra todas las tareas en una tabla organizada por prioridad."""
    tasks = load_tasks(DB_PATH)
    
    if not tasks:
        console.print("[yellow]No hay tareas pendientes. ¡Tómate un café! ☕[/yellow]")
        raise typer.Exit()

    # Ordenamos antes de mostrar (O(n log n) gracias a Timsort)
    tasks_ordenadas = sort_by_priority(tasks, reverse=True)
    
    table = Table(title="📋 TaskFlow - Lista de Tareas")
    table.add_column("ID", justify="right", style="dim")
    table.add_column("Título", style="white")
    table.add_column("Prioridad", justify="center")
    table.add_column("Estado", justify="center")
    table.add_column("Fecha", justify="right", style="blue")

    for t in tasks_ordenadas:
        color = get_color(t.prioridad)
        table.add_row(
            str(t.id),
            t.titulo,
            f"[{color}]{t.prioridad}[/{color}]",
            "✅ Completada" if t.estado == "Completada" else "⏳ Pendiente",
            t.fecha.strftime("%Y-%m-%d %H:%M")
        )

    console.print(table)

@app.command()
def done(task_id: int):
    """Marca una tarea como completada."""
    tasks = load_tasks(DB_PATH)
    encontrada = False
    
    for t in tasks:
        if t.id == task_id:
            t.estado = "Completada"
            encontrada = True
            break
    
    if encontrada:
        save_tasks(tasks, DB_PATH)
        console.print(f"[bold green]Done![/bold green] Tarea {task_id} actualizada.")
    else:
        console.print(f"[bold red]Error:[/bold red] No se encontró la tarea {task_id}")

@app.command()
def delete(task_id: int):
    """Elimina una tarea permanentemente."""
    tasks = load_tasks(DB_PATH)
    original_count = len(tasks)
    
    # Filtramos la lista eliminando el ID coincidente
    tasks = [t for t in tasks if t.id != task_id]
    
    if len(tasks) < original_count:
        save_tasks(tasks, DB_PATH)
        console.print(f"[bold red]🗑 Eliminada:[/bold red] La tarea {task_id} ha sido borrada.")
    else:
        console.print(f"[bold red]Error:[/bold red] La tarea {task_id} no existe.")

@app.command()
def rename(task_id: int, new_title: str):
    """Modifica el nombre de una tarea existente."""
    tasks = load_tasks(DB_PATH)
    encontrada = False
    
    for t in tasks:
        if t.id == task_id:
            t.titulo = nuevo_titulo  # Error intencional: nuevo_titulo no definido
            encontrada = True
            break
    
    if encontrada:
        save_tasks(tasks, DB_PATH)
        console.print(f"[bold green]Renombrada![/bold green] Tarea {task_id} ahora se llama '[italic]{new_title}[/italic]'.")
    else:
        console.print(f"[bold red]Error:[/bold red] No se encontró la tarea {task_id}")

if __name__ == "__main__":
    app()