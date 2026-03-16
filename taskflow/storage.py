import json
from pathlib import Path
from dataclasses import asdict
from datetime import datetime
from models import Task

def save_tasks(tasks: list[Task], path: str | Path) -> None:
    """
    Guarda una lista de objetos Task en un archivo JSON.
    
    Args:
        tasks: Lista de instancias de Task.
        path: Ruta del archivo (string o Path object).
    """
    # Convertimos los objetos dataclass a diccionarios
    # La fecha se convierte a string ISO para que sea serializable
    data = []
    for task in tasks:
        task_dict = asdict(task)
        task_dict['fecha'] = task.fecha.isoformat()
        data.append(task_dict)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_tasks(path: str | Path) -> list[Task]:
    """
    Carga tareas desde un archivo JSON. Si el archivo no existe,
    retorna una lista vacía en lugar de lanzar una excepción.
    
    Args:
        path: Ruta del archivo JSON.
        
    Returns:
        list[Task]: Lista de objetos Task reconstruidos.
    """
    archivo = Path(path)
    
    if not archivo.exists():
        return []

    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        tasks = []
        for item in data:
            # Reconvertimos el string de fecha a objeto datetime
            item['fecha'] = datetime.fromisoformat(item['fecha'])
            tasks.append(Task(**item))
        return tasks
        
    except (json.JSONDecodeError, KeyError, TypeError):
        # Si el JSON está corrupto o mal formado, retornamos lista vacía
        return []

# Ejemplo de uso:
# tareas = [Task(1, "Lavar coche", 3, "Pendiente")]
# save_tasks(tareas, "tareas.json")
# nuevas_tareas = load_tasks("tareas.json")