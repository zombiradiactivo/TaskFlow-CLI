from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Console
from rich.columns import Columns
from rich.table import Table
from rich.panel import Panel
from typing import Optional
import typer
import uuid


# Importamos nuestras capas previas
from taskflow.Sorting_Strategy import PriorityDateStrategy, RecentFirstStrategy, SortingStrategy, TitleAlphabeticalStrategy
from taskflow.logic import calcular_estadisticas
from taskflow.storage import TaskRepository
from taskflow.models import Task

app = typer.Typer(help="TaskFlow CLI - Gestión de tareas ultra rápida.")
console = Console()
DB_PATH = "tasks.json"
taskrepository = TaskRepository(DB_PATH)

def coger_color(prioridad: int) -> str:
    """Retorna un color de Rich según la prioridad."""
    colors = {5: "bold red", 4: "orange1", 3: "yellow", 2: "green", 1: "cyan"}
    return colors.get(prioridad, "white")

@app.command()
def add(titulo: str, prioridad: int = typer.Argument(..., min=1, max=5)):
    """Añade una nueva tarea con un ID único."""
    tasks = taskrepository.cargar_tareas(DB_PATH)
    
    # Generamos ID usando la parte inicial de un uuid4 para brevedad
    nuevo_id = int(uuid.uuid4().int % 10000)
    nueva_tarea = Task(id=nuevo_id, titulo=titulo, prioridad=prioridad, estado="Pendiente")
    
    tasks.append(nueva_tarea)
    taskrepository.guardar_tareas(tasks, DB_PATH)
    
    console.print(f"[bold green]✔[/bold green] Tarea '[italic]{titulo}[/italic]' añadida con ID [bold]{nuevo_id}[/bold]")

@app.command()
def list(type: Optional[str] = None):
    """Muestra todas las tareas en una tabla organizada por prioridad."""
    tasks = taskrepository.cargar_tareas(DB_PATH)
    
    if not tasks:
        console.print("[yellow]No hay tareas pendientes. ¡Tómate un café! ☕[/yellow]")
        raise typer.Exit()

    # 1. Definimos las estrategias disponibles
    strategies: dict[str, SortingStrategy] = {
        "fecha": RecentFirstStrategy(),
        "prioridad": PriorityDateStrategy(),
        "abc": TitleAlphabeticalStrategy()
    }

    # 2. Manejamos el caso None explícitamente
    # Si 'type' es None o no está en el diccionario, usamos PriorityDateStrategy    
    # Por si el usuario escribe algo que no existe:
    strategy = strategies.get(type, PriorityDateStrategy()) if type else PriorityDateStrategy()
    tasks_ordenadas = strategy.sort(tasks)

    table = Table(title="📋 TaskFlow - Lista de Tareas")
    table.add_column("ID", justify="right", style="dim")
    table.add_column("Título", style="white")
    table.add_column("Prioridad", justify="center")
    table.add_column("Estado", justify="center")
    table.add_column("Fecha", justify="right", style="blue")

    for t in tasks_ordenadas:
        color = coger_color(t.prioridad)
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
    tasks = taskrepository.cargar_tareas(DB_PATH)
    encontrada = False
    
    for t in tasks:
        if t.id == task_id:
            t.estado = "Completada"
            encontrada = True
            break
    
    if encontrada:
        taskrepository.guardar_tareas(tasks, DB_PATH)
        console.print(f"[bold green]Done![/bold green] Tarea {task_id} actualizada.")
    else:
        console.print(f"[bold red]Error:[/bold red] No se encontró la tarea {task_id}")

@app.command()
def delete(task_id: int):
    """Elimina una tarea permanentemente."""
    tasks = taskrepository.cargar_tareas(DB_PATH)
    original_count = len(tasks)
    
    # Filtramos la lista eliminando el ID coincidente
    tasks = [t for t in tasks if t.id != task_id]
    
    if len(tasks) < original_count:
        taskrepository.guardar_tareas(tasks, DB_PATH)
        console.print(f"[bold red]🗑 Eliminada:[/bold red] La tarea {task_id} ha sido borrada.")
    else:
        console.print(f"[bold red]Error:[/bold red] La tarea {task_id} no existe.")

# Reto Comando stats visual
@app.command()
def stats():
    """Muestra estadísticas visuales de las tareas y progreso de completado."""
    repo = TaskRepository(DB_PATH)
    tasks = repo.cargar_tareas(DB_PATH)
    
    stats = calcular_estadisticas(tasks)
    
    if stats["total"] == 0:
        console.print("[yellow]No hay datos suficientes para generar estadísticas. 📊[/yellow]")
        return

    # 1. Creación de la barra de progreso visual
    progress_bar = Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    
    # Añadimos la tarea a la barra (completadas vs total)
    task_id = progress_bar.add_task("Progreso General", total=stats["total"])
    progress_bar.update(task_id, completed=stats["completadas"])

    # 2. Organización de métricas en paneles (Cards)
    # Calculamos cuántas tareas hay por cada nivel de prioridad para el detalle
    prioridades = {i: sum(1 for t in tasks if t.prioridad == i) for i in range(1, 6)}
    
    detalle_prioridad = "\n".join([f"Prioridad {p}: {count}" for p, count in prioridades.items() if count > 0])

    panel_main = Panel(
        f"[bold]Total:[/bold] {stats['total']}\n"
        f"[green]Completadas:[/green] {stats['completadas']}\n"
        f"[yellow]Pendientes:[/yellow] {stats['pendientes']}",
        title="📊 Resumen",
        expand=True
    )

    panel_extra = Panel(
        f"[bold]Prioridad Media:[/bold] {stats['prioridad_media']} ⭐\n\n"
        f"[dim]{detalle_prioridad}[/dim]",
        title="📈 Detalles",
        expand=True
    )

    # 3. Renderizado final
    console.print(Panel(progress_bar, title="🚀 Rendimiento", border_style="blue"))
    console.print(Columns([panel_main, panel_extra]))

@app.command()
def renombrar(task_id: int, new_title: str):
    """Modifica el nombre de una tarea existente."""
    tasks = taskrepository.cargar_tareas(DB_PATH)
    encontrada = False
    
    for t in tasks:
        if t.id == task_id:
            t.titulo = new_title 
            encontrada = True
            break
    
    if encontrada:
        taskrepository.guardar_tareas(tasks, DB_PATH)
        console.print(f"[bold green]Renombrada![/bold green] Tarea {task_id} ahora se llama '[italic]{new_title}[/italic]'.")
    else:
        console.print(f"[bold red]Error:[/bold red] No se encontró la tarea {task_id}")

if __name__ == "__main__":
    app()