import pytest
from datetime import datetime
from taskflow.models import Task
from taskflow.logic import filter_by_status, sort_by_priority, get_stats

# --- TESTS PARA filter_by_status ---

def test_filter_empty_list():
    assert filter_by_status([], "Pendiente") == []

def test_filter_single_task_matching():
    t = Task(id=1, titulo="Tarea", prioridad=1, estado="Pendiente", fecha=datetime.now())
    assert filter_by_status([t], "Pendiente") == [t]

def test_filter_single_task_non_matching():
    t = Task(id=1, titulo="Tarea", prioridad=1, estado="Hecho", fecha=datetime.now())
    assert filter_by_status([t], "Pendiente") == []

def test_filter_case_insensitive():
    t1 = Task(id=1, titulo="A", prioridad=1, estado="pendiente", fecha=datetime.now())
    t2 = Task(id=2, titulo="B", prioridad=2, estado="Hecho", fecha=datetime.now())
    result = filter_by_status([t1, t2], "PENDIENTE")
    assert result == [t1]

# --- TESTS PARA sort_by_priority ---

def test_sort_empty_list():
    assert sort_by_priority([]) == []

def test_sort_single_task():
    t = Task(id=1, titulo="A", prioridad=2, estado="Pendiente", fecha=datetime.now())
    assert sort_by_priority([t]) == [t]

def test_sort_normal_and_reverse():
    t1 = Task(id=1, titulo="A", prioridad=1, estado="Pendiente", fecha=datetime.now())
    t2 = Task(id=2, titulo="B", prioridad=3, estado="Pendiente", fecha=datetime.now())
    t3 = Task(id=3, titulo="C", prioridad=2, estado="Pendiente", fecha=datetime.now())

    tasks = [t1, t2, t3]
    # Orden normal
    sorted_tasks = sort_by_priority(tasks)
    assert sorted_tasks == [t1, t3, t2]
    # Orden inverso
    sorted_tasks_rev = sort_by_priority(tasks, reverse=True)
    assert sorted_tasks_rev == [t2, t3, t1]

def test_sort_same_priority_stable():
    # Comprobamos estabilidad del sort
    t1 = Task(id=1, titulo="A", prioridad=2, estado="Pendiente", fecha=datetime.now())
    t2 = Task(id=2, titulo="B", prioridad=2, estado="Pendiente", fecha=datetime.now())
    sorted_tasks = sort_by_priority([t2, t1])
    # Debe mantener el orden relativo de tareas con misma prioridad
    assert sorted_tasks == [t2, t1]

# --- TESTS PARA get_stats ---

def test_get_stats_empty_list():
    stats = get_stats([])
    assert stats == {"total":0,"pendientes":0,"completadas":0,"prioridad_media":0.0}

def test_get_stats_various_tasks():
    t1 = Task(id=1, titulo="A", prioridad=1, estado="Pendiente", fecha=datetime.now())
    t2 = Task(id=2, titulo="B", prioridad=3, estado="Completada", fecha=datetime.now())
    t3 = Task(id=3, titulo="C", prioridad=5, estado="Pendiente", fecha=datetime.now())
    stats = get_stats([t1, t2, t3])
    assert stats == {"total":3,"pendientes":2,"completadas":1,"prioridad_media":3.0}

def test_get_stats_all_completed():
    t1 = Task(id=1, titulo="A", prioridad=2, estado="Completada", fecha=datetime.now())
    t2 = Task(id=2, titulo="B", prioridad=4, estado="Completada", fecha=datetime.now())
    stats = get_stats([t1, t2])
    assert stats == {"total":2,"pendientes":0,"completadas":2,"prioridad_media":3.0}