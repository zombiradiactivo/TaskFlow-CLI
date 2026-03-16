from datetime import datetime
from taskflow.models import Task


def test_creacion_valida_task():
    task = Task(
        id=1,
        titulo="Comprar café",
        prioridad=3,
        estado="Pendiente"
    )

    assert task.id == 1
    assert task.titulo == "Comprar café"
    assert task.prioridad == 3
    assert task.estado == "Pendiente"
    assert isinstance(task.fecha, datetime)

    print("✅ Test pasado: la tarea se creó correctamente")




import pytest
from taskflow.models import Task

def test_prioridad_invalida():
    
    # prioridad menor que el mínimo
    with pytest.raises(ValueError):
        Task(
            id=1,
            titulo="Tarea con prioridad baja",
            prioridad=0,
            estado="Pendiente"
        )

    # prioridad mayor que el máximo
    with pytest.raises(ValueError):
        Task(
            id=2,
            titulo="Tarea con prioridad alta",
            prioridad=6,
            estado="Pendiente"
        )

    print("✅ Test pasado: prioridad inválida detectada correctamente")



from taskflow.models import Task
from taskflow.storage import save_tasks,load_tasks


def test_task_a_dict_desde_dict():

    # Crear tarea original
    task_original = Task(
        id=1,
        titulo="Estudiar pytest",
        prioridad=4,
        estado="Pendiente"
    )

    # archivo temporal para el test
   
        # guardar
    save_tasks([task_original],"tasks.json")

        # cargar
    tareas_cargadas = load_tasks("tasks.json")

    task_recuperada = tareas_cargadas[0]

    assert task_original.id == task_recuperada.id
    assert task_original.titulo == task_recuperada.titulo
    assert task_original.prioridad == task_recuperada.prioridad
    assert task_original.estado == task_recuperada.estado
    assert task_original.fecha == task_recuperada.fecha

    print("✅ Test pasado: round-trip Task → JSON → Task correcto")