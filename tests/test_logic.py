import pytest
from datetime import datetime
from taskflow.models import Task
from taskflow.logic import filtrar_por_estatus, ordenar_por_prioridad, calcular_estadisticas

# --- TESTS PARA filter_by_status ---

def test_filtrar_lista_vacia():
    """Prueba que filter_by_status retorna lista vacía cuando no hay tareas."""
    assert filtrar_por_estatus([], "Pendiente") == []

def test_filtrar_tarea_unica_coincidente():
    """Prueba filtrar una sola tarea que coincide con el estado."""
    t = Task(id=1, titulo="Tarea", prioridad=1, estado="Pendiente", fecha=datetime.now())
    assert filtrar_por_estatus([t], "Pendiente") == [t]

def test_filtrar_tarea_unica_no_coincidente():
    """Prueba filtrar una sola tarea que no coincide con el estado."""
    t = Task(id=1, titulo="Tarea", prioridad=1, estado="Hecho", fecha=datetime.now())
    assert filtrar_por_estatus([t], "Pendiente") == []

## Test que da fallo intencionalmente 
def test_filtrar_tarea_unica_no_coincidente_error():
    """Prueba filtrar una sola tarea que no coincide con el estado."""
    t = Task(id=1, titulo="Tarea", prioridad=1, estado="Hecho", fecha=datetime.now())
    assert filtrar_por_estatus([t], "Rick Roll") == [t]

def test_filtrar_insensible_mayusculas():
    """Prueba que el filtro es insensible a mayúsculas y minúsculas."""
    t1 = Task(id=1, titulo="A", prioridad=1, estado="pendiente", fecha=datetime.now())
    t2 = Task(id=2, titulo="B", prioridad=2, estado="Hecho", fecha=datetime.now())
    result = filtrar_por_estatus([t1, t2], "PENDIENTE")
    assert result == [t1]

# --- TESTS PARA sort_by_priority ---

def test_ordenar_lista_vacia():
    """Prueba que sort_by_priority retorna lista vacía cuando no hay tareas."""
    assert ordenar_por_prioridad([]) == []

def test_ordenar_tarea_unica():
    """Prueba ordenar una sola tarea."""
    t = Task(id=1, titulo="A", prioridad=2, estado="Pendiente", fecha=datetime.now())
    assert ordenar_por_prioridad([t]) == [t]

def test_ordenar_normal_e_inverso():
    """Prueba ordenar en orden normal y reverso por prioridad."""
    t1 = Task(id=1, titulo="A", prioridad=1, estado="Pendiente", fecha=datetime.now())
    t2 = Task(id=2, titulo="B", prioridad=3, estado="Pendiente", fecha=datetime.now())
    t3 = Task(id=3, titulo="C", prioridad=2, estado="Pendiente", fecha=datetime.now())

    tasks = [t1, t2, t3]
    # Orden normal
    sorted_tasks = ordenar_por_prioridad(tasks)
    assert sorted_tasks == [t1, t3, t2]
    # Orden inverso
    sorted_tasks_rev = ordenar_por_prioridad(tasks, reverse=True)
    assert sorted_tasks_rev == [t2, t3, t1]

def test_ordenar_misma_prioridad_estable():
    """Prueba que el orden es estable para tareas con misma prioridad."""
    # Comprobamos estabilidad del sort
    t1 = Task(id=1, titulo="A", prioridad=2, estado="Pendiente", fecha=datetime.now())
    t2 = Task(id=2, titulo="B", prioridad=2, estado="Pendiente", fecha=datetime.now())
    sorted_tasks = ordenar_por_prioridad([t2, t1])
    # Debe mantener el orden relativo de tareas con misma prioridad
    assert sorted_tasks == [t2, t1]

# --- TESTS PARA calcular_estadisticas ---

def test_obtener_estadisticas_lista_vacia():
    """Prueba obtener estadísticas cuando no hay tareas."""
    stats = calcular_estadisticas([])
    assert stats == {"total":0,"pendientes":0,"completadas":0,"prioridad_media":0.0}

def test_obtener_estadisticas_varias_tareas():
    """Prueba obtener estadísticas con varias tareas de diferentes estados."""
    t1 = Task(id=1, titulo="A", prioridad=1, estado="Pendiente", fecha=datetime.now())
    t2 = Task(id=2, titulo="B", prioridad=3, estado="Completada", fecha=datetime.now())
    t3 = Task(id=3, titulo="C", prioridad=5, estado="Pendiente", fecha=datetime.now())
    stats = calcular_estadisticas([t1, t2, t3])
    assert stats == {"total":3,"pendientes":2,"completadas":1,"prioridad_media":3.0}

def test_obtener_estadisticas_todas_completadas():
    """Prueba obtener estadísticas cuando todas las tareas están completadas."""
    t1 = Task(id=1, titulo="A", prioridad=2, estado="Completada", fecha=datetime.now())
    t2 = Task(id=2, titulo="B", prioridad=4, estado="Completada", fecha=datetime.now())
    stats = calcular_estadisticas([t1, t2])
    assert stats == {"total":2,"pendientes":0,"completadas":2,"prioridad_media":3.0}