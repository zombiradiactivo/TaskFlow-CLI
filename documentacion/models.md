# models.py - Modelos de Datos

## Descripción

El módulo `models.py` define las estructuras de datos principales de TaskFlow usando dataclasses de Python. Implementa la clase Task con validaciones y documentación completa.

## Dependencias

- `dataclasses`: Para definición de clases de datos
- `datetime`: Para manejo de fechas
- `typing`: Para type hints (Optional)

## Clase Task

### Definición

```python
@dataclass(frozen=False)
class Task:
    id: int
    titulo: str
    prioridad: int
    estado: str
    fecha: datetime = field(default_factory=datetime.now)
```

### Atributos

- **id** (`int`): Identificador único de la tarea
- **titulo** (`str`): Descripción breve de la tarea
- **prioridad** (`int`): Nivel de importancia del 1 (baja) al 5 (crítica)
- **estado** (`str`): Estado actual ("Pendiente", "Completada", etc.)
- **fecha** (`datetime`): Fecha de creación (por defecto ahora)

### Validaciones

#### `__post_init__()`

Método ejecutado después de la inicialización que valida:
- **Prioridad**: Debe estar entre 1 y 5 inclusive
- **Título**: No puede estar vacío o contener solo espacios

**Lanza:** `ValueError` si las validaciones fallan

### Características Técnicas

- **Mutable**: `frozen=False` permite modificar atributos después de creación
- **Fecha automática**: Campo `fecha` se inicializa con `datetime.now()` si no se proporciona
- **Type hints**: Todos los atributos tienen tipos explícitos
- **Documentación**: Docstring completa con ejemplos de uso

## Función Auxiliar

### `procesar_tareas(tareas: list[Task]) -> None`

Función de ejemplo que demuestra manejo de listas de tareas:
- Maneja caso de lista vacía
- Itera sobre tareas imprimiendo información formateada
- Útil para debugging y ejemplos

**Salida de ejemplo:**
```
ℹ️ No hay tareas registradas en TaskFlow.
```
O para tareas existentes:
```
[3] Comprar café - Pendiente
[5] Llamar al cliente - Completada
```

## Uso en el Sistema

### Creación de Tareas

```python
from taskflow.models import Task
from datetime import datetime

# Tarea con fecha automática
tarea1 = Task(id=1, titulo="Comprar café", prioridad=3, estado="Pendiente")

# Tarea con fecha específica
tarea2 = Task(
    id=2, 
    titulo="Reunión importante", 
    prioridad=5, 
    estado="Pendiente",
    fecha=datetime(2024, 3, 17, 10, 30)
)
```

### Validaciones Automáticas

```python
# Esto lanza ValueError
tarea_invalida = Task(id=3, titulo="", prioridad=6, estado="Pendiente")
```

### Integración con Otros Módulos

- **storage.py**: Usa `asdict()` para serialización JSON
- **logic.py**: Opera sobre listas de Task
- **cli.py/gui.py**: Crean y modifican instancias de Task

## Ventajas de Dataclasses

- **Automático**: Genera `__init__`, `__repr__`, `__eq__`, etc.
- **Inmutable por defecto**: Pero configurable con `frozen=False`
- **Type-safe**: Integración con mypy y otros tools
- **Serializable**: Fácil conversión a dict/JSON
- **Comparaciones**: Ordenación natural por atributos

## Casos de Uso

- **Almacenamiento**: Serialización a JSON en storage.py
- **Ordenación**: Comparación por prioridad en logic.py
- **Filtrado**: Búsqueda por estado en logic.py
- **UI**: Display en tablas (CLI) y listas (GUI)

## Testing

La clase incluye ejemplos en docstrings para testing:
- Creación básica
- Validaciones de error
- Manejo de listas vacías