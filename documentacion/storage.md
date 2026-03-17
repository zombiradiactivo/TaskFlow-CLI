# storage.py - Persistencia de Datos

## Descripción

El módulo `storage.py` maneja la persistencia de datos para TaskFlow. Implementa funciones para guardar y cargar listas de tareas en formato JSON, con manejo robusto de errores y serialización de fechas.

## Dependencias

- `json`: Para serialización/deserialización JSON
- `pathlib.Path`: Para manejo de rutas de archivos
- `dataclasses.asdict`: Para convertir dataclasses a diccionarios
- `datetime`: Para manejo de fechas
- `taskflow.models`: Importa la clase Task

## Funciones Principales

### `guardar_tareas(tasks: list[Task], path: str | Path) -> None`

Guarda una lista de objetos Task en un archivo JSON.

**Parámetros:**
- `tasks`: Lista de instancias de Task
- `path`: Ruta del archivo (string o Path object)

**Proceso:**
1. Convierte cada Task a diccionario usando `asdict()`
2. Serializa fechas a formato ISO string
3. Escribe JSON con indentación y encoding UTF-8

**Características:**
- **Encoding**: UTF-8 para soporte de caracteres especiales
- **Formato**: JSON pretty-printed (indent=2)
- **Fechas**: Convertidas a ISO format para serialización
- **Unicode**: `ensure_ascii=False` para caracteres no-ASCII

### `cargar_tareas(path: str | Path) -> list[Task]`

Carga tareas desde un archivo JSON con manejo robusto de errores.

**Parámetros:**
- `path`: Ruta del archivo JSON

**Retorna:** Lista de objetos Task reconstruidos

**Comportamiento:**
- **Archivo inexistente**: Retorna lista vacía (no lanza excepción)
- **JSON corrupto**: Retorna lista vacía (manejo graceful de errores)
- **Fechas**: Reconstruye objetos datetime desde strings ISO

**Manejo de Errores:**
- `FileNotFoundError`: Lista vacía
- `json.JSONDecodeError`: Lista vacía
- `KeyError`: Lista vacía (campos faltantes)
- `TypeError`: Lista vacía (tipos incorrectos)

## Formato JSON

### Estructura de Guardado

```json
[
  {
    "id": 1,
    "titulo": "Comprar café",
    "prioridad": 3,
    "estado": "Pendiente",
    "fecha": "2024-03-17T10:30:00"
  },
  {
    "id": 2,
    "titulo": "Llamar cliente",
    "prioridad": 5,
    "estado": "Completada",
    "fecha": "2024-03-17T09:15:30.123456"
  }
]
```

### Reconstrucción

1. Carga JSON como lista de diccionarios
2. Convierte string de fecha a `datetime` usando `fromisoformat()`
3. Crea instancias de Task con `Task(**item)`

## Integración con el Sistema

### Uso en CLI y GUI

- **Carga inicial**: `tasks = cargar_tareas(DB_PATH)`
- **Guardado**: `guardar_tareas(tasks, DB_PATH)` tras cada modificación
- **Archivo por defecto**: `"tasks.json"` en el directorio actual

### Operaciones Atómicas

Todas las operaciones de modificación siguen el patrón:
1. Cargar tareas existentes
2. Modificar lista en memoria
3. Guardar lista completa

Esto asegura consistencia de datos aún si el programa se interrumpe.

## Características Técnicas

- **Robusto**: Manejo de errores previene corrupción de datos
- **UTF-8**: Soporte completo para caracteres internacionales
- **Fechas**: Preservación exacta de timestamps con microsegundos
- **Path flexible**: Acepta tanto strings como objetos Path
- **No bloqueante**: Operaciones de archivo son síncronas pero rápidas

## Casos de Uso

### Inicialización
```python
tasks = cargar_tareas("tasks.json")  # Lista vacía si no existe
```

### Guardado
```python
guardar_tareas(tasks, "tasks.json")  # Sobreescribe completamente
```

### Recuperación de Errores
```python
# Si tasks.json está corrupto, retorna []
# El programa puede continuar normalmente
tasks = cargar_tareas("tasks.json")
```

## Ventajas del Diseño

- **Resistente a fallos**: Nunca pierde datos por archivos corruptos
- **Simple**: API de dos funciones principales
- **Portable**: JSON estándar, legible por humanos
- **Escalable**: Maneja listas grandes eficientemente
- **Type-safe**: Trabaja con objetos Task tipados

## Testing

Funciones diseñadas para testing con:
- Archivos inexistentes
- JSON malformado
- Fechas inválidas
- Caracteres Unicode
- Listas vacías y grandes