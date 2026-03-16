import pytest
from datetime import datetime
from pathlib import Path
from taskflow.storage import save_tasks, load_tasks  # Ajusta según tu paquete
from taskflow.models import Task  # Ajusta según tu paquete

def test_save_and_load_tasks(tmp_path):
    # Archivo temporal para guardar tasks
    file = tmp_path / "tasks.json"

    # Creamos 2 tasks de ejemplo
    tasks_to_save = [
        Task(id=1, titulo="Comprar leche", prioridad=2, estado="Pendiente", fecha=datetime(2026, 3, 16, 10, 0)),
        Task(id=2, titulo="Hacer ejercicio", prioridad=1, estado="Hecho", fecha=datetime(2026, 3, 16, 12, 0))
    ]

    # Guardamos tasks
    save_tasks(tasks_to_save, file)

    # Cargamos tasks
    loaded_tasks = load_tasks(file)

    # Verificamos que se cargaron correctamente
    assert loaded_tasks == tasks_to_save

def test_load_nonexistent_file(tmp_path):
    # Archivo que no existe
    file = tmp_path / "no_existe.json"

    # Cargar tasks desde archivo inexistente
    loaded_tasks = load_tasks(file)

    # Debe retornar lista vacía
    assert loaded_tasks == []