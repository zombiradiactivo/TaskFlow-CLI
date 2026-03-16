from typing import Any
from taskflow.models import Task

def filter_by_status(tasks: list[Task], status: str) -> list[Task]:
    """
    Filtra las tareas según su estado.
    
    Ejemplo:
        >>> tasks = [Task(1, "A", 1, "Pendiente"), Task(2, "B", 1, "Hecho")]
        >>> filter_by_status(tasks, "Hecho")
        [Task(id=2, titulo='B', prioridad=1, estado='Hecho', ...)]
    """
    if not tasks:
        return []
    
    return [t for t in tasks if t.estado.lower() == status.lower()]

def sort_by_priority(tasks: list[Task], reverse: bool = False) -> list[Task]:
    """
    Ordena las tareas por nivel de prioridad.
    
    NOTA SOBRE EL ALGORITMO:
    Python usa internamente Timsort, un algoritmo híbrido derivado de 
    Merge Sort e Insertion Sort. 
    - Complejidad Temporal: O(n log n) en el peor de los casos.
    - Complejidad Espacial: O(n).
    Es un algoritmo "estable", lo que significa que mantiene el orden 
    relativo de elementos con igual prioridad.
    """
    if not tasks:
        return []
    
    # Usamos el parámetro 'key' para acceder al atributo de la dataclass
    return sorted(tasks, key=lambda t: t.prioridad, reverse=reverse)

def get_stats(tasks: list[Task]) -> dict[str, Any]:
    """
    Calcula estadísticas generales de la lista de tareas.
    
    Ejemplo de salida:
        {'total': 10, 'pendientes': 7, 'completadas': 3, 'prioridad_media': 3.5}
    """
    if not tasks:
        return {
            "total": 0,
            "pendientes": 0,
            "completadas": 0,
            "prioridad_media": 0.0
        }

    total = len(tasks)
    pendientes = sum(1 for t in tasks if t.estado.lower() == "pendiente")
    completadas = sum(1 for t in tasks if t.estado.lower() == "completada")
    # Calculamos la media usando una expresión generadora para eficiencia
    prioridad_media = sum(t.prioridad for t in tasks) / total

    return {
        "total": total,
        "pendientes": pendientes,
        "completadas": completadas,
        "prioridad_media": round(prioridad_media, 2)
    }