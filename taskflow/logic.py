from typing import Any
from taskflow.Sorting_Strategy import PriorityDateStrategy, SortingStrategy
from taskflow.models import Task

def filtrar_por_estatus(tasks: list[Task], status: str) -> list[Task]:
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

def ordenar_tareas(tasks: list[Task], strategy: SortingStrategy = PriorityDateStrategy()) -> list[Task]:
    """
    Ordena las tareas delegando la lógica a una estrategia específica.
    
    El patrón Strategy permite cumplir el principio Open/Closed: 
    Podemos añadir nuevos modos de ordenado creando nuevas clases 
    sin tocar esta función.
    """
    if not tasks:
        return []
    
    return strategy.sort(tasks)

def ordenar_por_prioridad(tasks: list[Task], reverse: bool = False) -> list[Task]:
    """
    Ordena las tareas por nivel de prioridad.
    
    NOTA SOBRE EL ALGORITMO:
    Python utiliza Timsort. Al realizar una sola pasada sobre la lista para
    generar las llaves de ordenamiento y luego aplicar el sort, mantenemos
    la eficiencia logarítmica lineal, ideal para conjuntos de datos grandes.
    - Complejidad Temporal: O(n log n) en el peor de los casos.
    - Complejidad Espacial: O(n).
    Es un algoritmo "estable", lo que significa que mantiene el orden 
    relativo de elementos con igual prioridad.
    """
    if not tasks:
        return []
    
    # Usamos el parámetro 'key' para acceder al atributo de la dataclass
    return sorted(tasks, key=lambda t: t.prioridad, reverse=reverse)

def ordenar_tareas_fecha_prioridad(tasks: list[Task], reverse: bool = True) -> list[Task]:
    """
    Ordena las tareas por múltiples criterios:
    1. Prioridad (de mayor a menor por defecto).
    2. Fecha (más reciente o más antigua según prioridad).
    """
    if not tasks:
        return []

    # Ordenamos usando una tupla como clave: (prioridad, fecha)
    # Si reverse=True: Prioridad 5 va primero. Si las prioridades son iguales,
    # la fecha más reciente (mayor) va primero.
    return sorted(tasks, key=lambda t: (t.prioridad, t.fecha), reverse=reverse)

def calcular_estadisticas(tasks: list[Task]) -> dict[str, Any]:
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