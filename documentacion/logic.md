# logic.py - Lógica de Negocio

## Descripción

El módulo `logic.py` contiene las funciones de lógica de negocio para TaskFlow. Implementa operaciones de filtrado, ordenación y cálculo de estadísticas sobre listas de tareas.

## Dependencias

- `typing`: Para type hints avanzados
- `taskflow.models`: Importa la clase Task

## Funciones

### `filtrar_por_estatus(tasks: list[Task], status: str) -> list[Task]`

Filtra tareas por estado (ej. "Pendiente", "Completada").

**Parámetros:**
- `tasks`: Lista de objetos Task
- `status`: String del estado a filtrar (case-insensitive)

**Retorna:** Lista filtrada de tareas

**Ejemplo:**
```python
pendientes = filtrar_por_estatus(tasks, "Pendiente")
```

**Características:**
- Maneja lista vacía retornando []
- Comparación case-insensitive
- Usa list comprehension para eficiencia

### `ordenar_por_prioridad(tasks: list[Task], reverse: bool = False) -> list[Task]`

Ordena tareas por nivel de prioridad usando el algoritmo Timsort de Python.

**Parámetros:**
- `tasks`: Lista de objetos Task
- `reverse`: Si True, ordena descendente (prioridad alta primero)

**Retorna:** Lista ordenada de tareas

**Algoritmo:**
- **Timsort**: Híbrido de Merge Sort + Insertion Sort
- **Complejidad**: O(n log n) peor caso, O(n) mejor caso
- **Estable**: Mantiene orden relativo de elementos con igual prioridad
- **Espacial**: O(n) adicional

**Ejemplo:**
```python
# Prioridad alta primero
tareas_ordenadas = ordenar_por_prioridad(tasks, reverse=True)
```

### `calcular_estadisticas(tasks: list[Task]) -> dict[str, Any]`

Calcula estadísticas generales de la lista de tareas.

**Retorna:** Diccionario con:
- `total`: Número total de tareas
- `pendientes`: Tareas con estado "Pendiente"
- `completadas`: Tareas con estado "Completada"
- `prioridad_media`: Promedio de prioridades (redondeado a 2 decimales)

**Ejemplo de salida:**
```python
{
    "total": 10,
    "pendientes": 7,
    "completadas": 3,
    "prioridad_media": 3.5
}
```

**Características:**
- Maneja lista vacía retornando ceros
- Usa generadores para eficiencia en sumas
- Redondea prioridad media a 2 decimales

## Casos de Uso

### En CLI (`cli.py`)
- `ordenar_por_prioridad()`: Para mostrar tareas ordenadas en tabla

### En GUI (`gui.py`)
- `ordenar_por_prioridad()`: Para ordenar tareas en la interfaz
- `calcular_estadisticas()`: Para mostrar estadísticas en sidebar

## Eficiencia

- **Filtrado**: O(n) - un solo pase por la lista
- **Ordenación**: O(n log n) - usando Timsort optimizado
- **Estadísticas**: O(n) - un solo pase calculando sumas

## Validaciones

- Todas las funciones manejan listas vacías gracefully
- Retornan tipos apropiados (listas vacías, diccionarios con valores por defecto)
- No modifican las listas originales (funciones puras)

## Testing

Las funciones incluyen docstrings con ejemplos de uso y están diseñadas para ser fácilmente testeables con casos como:
- Listas vacías
- Un solo elemento
- Múltiples elementos con diferentes prioridades/estados
- Casos edge de ordenación