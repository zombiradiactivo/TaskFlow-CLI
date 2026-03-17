# cli.py - Interfaz de Línea de Comandos

## Descripción

El módulo `cli.py` implementa la interfaz de línea de comandos para TaskFlow usando la librería Typer. Proporciona comandos intuitivos para gestionar tareas desde la terminal con una experiencia visual atractiva gracias a Rich.

## Dependencias

- `typer`: Framework para crear CLIs en Python
- `rich`: Librería para texto coloreado y tablas en terminal
- `uuid`: Generación de IDs únicos
- `datetime`: Manejo de fechas
- Módulos internos: `models`, `storage`, `logic`

## Funciones Principales

### `coger_color(prioridad: int) -> str`

Retorna un código de color de Rich basado en la prioridad de la tarea:
- 5: "bold red" (Crítica)
- 4: "orange1" (Alta)
- 3: "yellow" (Media)
- 2: "green" (Baja)
- 1: "cyan" (Muy baja)

### Comandos de Typer

#### `add(titulo: str, prioridad: int)`

Añade una nueva tarea al sistema.
- Genera un ID único usando UUID
- Valida prioridad entre 1-5
- Guarda la tarea en el archivo JSON
- Muestra confirmación coloreada

#### `list()`

Muestra todas las tareas en una tabla organizada.
- Carga tareas desde JSON
- Ordena por prioridad descendente usando `ordenar_por_prioridad`
- Muestra tabla con columnas: ID, Título, Prioridad, Estado, Fecha
- Colorea prioridades y estados
- Maneja caso de lista vacía

#### `done(task_id: int)`

Marca una tarea como completada.
- Busca tarea por ID
- Cambia estado a "Completada"
- Guarda cambios
- Muestra confirmación o error

#### `delete(task_id: int)`

Elimina una tarea permanentemente.
- Filtra la lista removiendo la tarea con el ID especificado
- Guarda la lista actualizada
- Muestra confirmación o error si no existe

#### `renombrar(task_id: int, new_title: str)`

Cambia el título de una tarea existente.
- Busca tarea por ID
- Actualiza el título
- Guarda cambios
- Muestra confirmación o error

## Estructura del Código

```python
import typer
import uuid
from rich.console import Console
from rich.table import Table
from datetime import datetime

from taskflow.models import Task
from taskflow.storage import cargar_tareas, guardar_tareas
from taskflow.logic import ordenar_por_prioridad

app = typer.Typer(help="TaskFlow CLI - Gestión de tareas ultra rápida.")
console = Console()
DB_PATH = "tasks.json"

# Funciones auxiliares y comandos...
```

## Uso

```bash
# Desde el directorio del proyecto
python -m taskflow.cli add "Nueva tarea" 3
python -m taskflow.cli list
python -m taskflow.cli done 1234
python -m taskflow.cli delete 1234
python -m taskflow.cli renombrar 1234 "Nuevo título"
```

## Características Técnicas

- **Generación de IDs**: Usa `uuid.uuid4().int % 10000` para IDs cortos pero únicos
- **Validación**: Typer valida automáticamente rangos de prioridad
- **Persistencia**: Todas las operaciones guardan inmediatamente en JSON
- **UX**: Mensajes coloreados y emojis para mejor experiencia
- **Ordenación**: Usa Timsort (O(n log n)) para ordenar tareas por prioridad

## Manejo de Errores

- Tareas no encontradas: Mensajes de error en rojo
- Lista vacía: Mensaje informativo con emoji
- Validaciones: Typer maneja automáticamente tipos y rangos