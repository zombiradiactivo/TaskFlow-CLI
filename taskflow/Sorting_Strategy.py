from abc import ABC, abstractmethod
from typing import List

from taskflow.models import Task

# Interfaz de la Estrategia
class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, tasks: List['Task']) -> List['Task']:
        pass

# Estrategia 1: Prioridad y Fecha (O(n log n))
class PriorityDateStrategy(SortingStrategy):
    def sort(self, tasks: List['Task']) -> List['Task']:
        # Complejidad Temporal: O(n log n)
        return sorted(tasks, key=lambda t: (t.prioridad, t.fecha), reverse=True)

# Estrategia 2: Solo por Fecha (Más recientes primero)
class RecentFirstStrategy(SortingStrategy):
    def sort(self, tasks: List['Task']) -> List['Task']:
        return sorted(tasks, key=lambda t: t.fecha, reverse=True)

# Estrategia 3: Alfabético por Título
class TitleAlphabeticalStrategy(SortingStrategy):
    def sort(self, tasks: List['Task']) -> List['Task']:
        return sorted(tasks, key=lambda t: t.titulo.lower())


