from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass(frozen=False)
class Task:
    """
    Representa una tarea individual dentro del sistema TaskFlow.

    Atributos:
        id (int): Identificador único de la tarea.
        titulo (str): Descripción breve de la tarea.
        prioridad (int): Nivel de importancia del 1 (baja) al 5 (crítica).
        estado (str): Estado actual (ej. 'Pendiente', 'En progreso', 'Completada').
        fecha (datetime): Fecha de creación o vencimiento.

    Ejemplos:
        >>> task = Task(1, "Comprar café", 5, "Pendiente", datetime.now())
        >>> print(task.titulo)
        'Comprar café'
        >>> tasks_list = []  # Manejo de lista vacía
        >>> len(tasks_list) == 0
        True
    """
    id: int
    titulo: str
    prioridad: int
    estado: str
    fecha: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validaciones básicas tras la inicialización."""
        if not (1 <= self.prioridad <= 5):
            raise ValueError("La prioridad debe estar entre 1 y 5.")
        if not self.titulo.strip():
            raise ValueError("El título no puede estar vacío.")

def procesar_tareas(tareas: list[Task]) -> None:
    """
    Ejemplo de manejo de una lista de tareas, incluyendo el caso de lista vacía.
    """
    if not tareas:
        print("ℹ️ No hay tareas registradas en TaskFlow.")
        return

    for t in tareas:
        print(f"[{t.prioridad}] {t.titulo} - {t.estado}")