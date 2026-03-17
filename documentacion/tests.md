# tests/ - Suite de Pruebas

## Descripción General

TaskFlow incluye una suite completa de pruebas unitarias usando pytest. Las pruebas cubren los módulos principales del sistema: lógica de negocio, modelos de datos y persistencia. La suite consta de 16 tests que validan el comportamiento correcto de todas las funcionalidades críticas.

## Estructura de Tests

```
tests/
├── test_logic.py      # 11 tests - Lógica de negocio
├── test_models.py     # 3 tests - Modelos de datos
└── test_storage.py    # 2 tests - Persistencia
```

## test_logic.py - Pruebas de Lógica de Negocio

### Cobertura: `taskflow.logic`

Prueba las funciones: `filtrar_por_estatus`, `ordenar_por_prioridad`, `calcular_estadisticas`

### Tests para `filtrar_por_estatus`

#### `test_filtrar_lista_vacia()`
- **Propósito**: Verificar manejo de lista vacía
- **Entrada**: Lista vacía `[]`
- **Salida esperada**: Lista vacía `[]`
- **Caso borde**: Sin tareas que filtrar

#### `test_filtrar_tarea_unica_coincidente()`
- **Propósito**: Filtrar una tarea que coincide con el estado
- **Entrada**: Una tarea con estado "Pendiente"
- **Salida esperada**: Lista con esa tarea
- **Validación**: Coincidencia exacta

#### `test_filtrar_tarea_unica_no_coincidente()`
- **Propósito**: Filtrar una tarea que no coincide
- **Entrada**: Una tarea con estado "Hecho"
- **Filtro**: "Pendiente"
- **Salida esperada**: Lista vacía
- **Validación**: No coincidencia

#### `test_filtrar_insensible_mayusculas()`
- **Propósito**: Verificar insensibilidad a mayúsculas
- **Entrada**: Tareas con estados mixtos
- **Filtro**: "PENDIENTE" (mayúsculas)
- **Salida esperada**: Tareas con estado "pendiente"
- **Validación**: Case-insensitive funciona

### Tests para `ordenar_por_prioridad`

#### `test_ordenar_lista_vacia()`
- **Propósito**: Ordenar lista vacía
- **Entrada**: `[]`
- **Salida esperada**: `[]`
- **Validación**: No crash con lista vacía

#### `test_ordenar_tarea_unica()`
- **Propósito**: Ordenar una sola tarea
- **Entrada**: Una tarea
- **Salida esperada**: Lista con esa tarea
- **Validación**: Funciona con un elemento

#### `test_ordenar_normal_e_inverso()`
- **Propósito**: Probar orden normal y reverso
- **Entrada**: Tareas con prioridades 1, 3, 2
- **Salida normal**: [prioridad 1, 2, 3]
- **Salida reverso**: [prioridad 3, 2, 1]
- **Validación**: Ambos sentidos funcionan

#### `test_ordenar_misma_prioridad_estable()`
- **Propósito**: Verificar estabilidad del sort
- **Entrada**: Dos tareas con misma prioridad
- **Salida esperada**: Orden relativo preservado
- **Validación**: Timsort es estable

### Tests para `calcular_estadisticas`

#### `test_obtener_estadisticas_lista_vacia()`
- **Propósito**: Estadísticas de lista vacía
- **Entrada**: `[]`
- **Salida esperada**: `{"total":0,"pendientes":0,"completadas":0,"prioridad_media":0.0}`
- **Validación**: Valores por defecto correctos

#### `test_obtener_estadisticas_varias_tareas()`
- **Propósito**: Estadísticas con tareas mixtas
- **Entrada**: 2 pendientes (prioridades 1,5), 1 completada (prioridad 3)
- **Salida esperada**: `{"total":3,"pendientes":2,"completadas":1,"prioridad_media":3.0}`
- **Validación**: Cálculos aritméticos correctos

#### `test_obtener_estadisticas_todas_completadas()`
- **Propósito**: Todas las tareas completadas
- **Entrada**: 2 tareas completadas
- **Salida esperada**: `{"total":2,"pendientes":0,"completadas":2,"prioridad_media":3.0}`
- **Validación**: Manejo de casos extremos

## test_models.py - Pruebas de Modelos de Datos

### Cobertura: `taskflow.models`

Prueba la clase `Task` y su integración con storage

### `test_creacion_valida_tarea()`
- **Propósito**: Creación normal de Task
- **Entrada**: Todos los parámetros válidos
- **Validación**: Atributos asignados correctamente
- **Fecha**: Se asigna automáticamente si no se proporciona

### `test_prioridad_invalida()`
- **Propósito**: Validaciones de prioridad
- **Casos**: Prioridad 0 (muy baja) y 6 (muy alta)
- **Comportamiento esperado**: `ValueError` en ambos casos
- **Validación**: `__post_init__` funciona correctamente

### `test_task_a_dict_desde_dict()`
- **Propósito**: Round-trip Task ↔ JSON
- **Proceso**:
  1. Crear Task
  2. Guardar a JSON
  3. Cargar desde JSON
  4. Comparar objetos
- **Validación**: Serialización/deserialización preserva datos

## test_storage.py - Pruebas de Persistencia

### Cobertura: `taskflow.storage`

Prueba `guardar_tareas` y `cargar_tareas`

### `test_guardar_y_cargar_tareas(tmp_path)`
- **Propósito**: Ciclo completo de guardado/carga
- **Archivo**: Temporal (tmp_path)
- **Datos**: 2 tareas con fechas específicas
- **Validación**: Objetos idénticos después del round-trip

### `test_cargar_archivo_inexistente(tmp_path)`
- **Propósito**: Manejo de archivo inexistente
- **Archivo**: No existe
- **Comportamiento esperado**: Retorna lista vacía
- **Validación**: No lanza excepciones

## Métricas de Cobertura

- **Total de tests**: 16
- **Módulos testeados**: 3
- **Funciones testeadas**: 6
- **Clases testeadas**: 1
- **Casos borde**: Listas vacías, valores límites, errores

## Framework de Testing

- **pytest**: Framework principal
- **tmp_path**: Fixtures para archivos temporales
- **pytest.raises**: Para validar excepciones
- **Asserts directos**: Comparaciones de objetos

## Ejecución

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests específicos
pytest tests/test_logic.py
pytest tests/test_models.py -v

# Con cobertura
pytest --cov=taskflow --cov-report=html
```

## Beneficios de la Suite

- **Validación**: Confirma que todas las funcionalidades funcionan
- **Regresión**: Previene bugs en cambios futuros
- **Documentación**: Los tests sirven como ejemplos de uso
- **Refactorización**: Permite cambios seguros en el código
- **Integración**: Valida que módulos funcionan juntos