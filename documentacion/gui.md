# gui.py - Interfaz Gráfica de Usuario

## Descripción

El módulo `gui.py` implementa la interfaz gráfica para TaskFlow usando CustomTkinter. Proporciona una aplicación de escritorio moderna con tema oscuro, estadísticas en tiempo real y gestión visual de tareas.

## Dependencias

- `customtkinter`: Framework moderno para interfaces Tkinter
- `uuid`: Generación de IDs únicos
- Módulos internos: `models`, `storage`, `logic`

## Clase Principal: TaskFlowGUI

### Atributos

- `tasks`: Lista de tareas cargadas desde JSON
- `priority_colors`: Diccionario de colores para prioridades (rojo a cian)
- Frames principales: sidebar, main_frame, input_frame, scrollable_frame

### Métodos Principales

#### `__init__()`

Inicializa la aplicación GUI:
- Configura apariencia (modo oscuro, tema azul)
- Carga tareas desde JSON
- Define colores de prioridad
- Configura UI y refresca pantalla

#### `setup_ui()`

Configura la estructura de la interfaz:
- **Sidebar izquierdo**: Logo, estadísticas
- **Panel derecho**: Área de input y lista scrollable
- Layout con grid system
- Componentes: entradas, combobox, botones

#### `add_task()`

Añade nueva tarea desde la interfaz:
- Obtiene título del entry
- Extrae prioridad del combobox
- Genera ID único
- Crea objeto Task y lo añade a la lista
- Guarda en JSON y refresca UI

#### `toggle_task_status(task: Task)`

Alterna estado entre Pendiente/Completada:
- Cambia el estado de la tarea
- Guarda cambios en JSON
- Refresca la interfaz

#### `delete_task(task: Task)`

Elimina una tarea:
- Remueve de la lista
- Guarda cambios en JSON
- Refresca la interfaz

#### `refresh_ui()`

Actualiza toda la interfaz:
- **Estadísticas**: Calcula y muestra totales usando `calcular_estadisticas`
- **Lista de tareas**: 
  - Limpia frame anterior
  - Ordena tareas (pendientes primero, luego completadas)
  - Dibuja cada tarea con checkbox, título, prioridad, fecha, botón eliminar

## Estructura Visual

### Sidebar
- Logo "📋 TaskFlow"
- Estadísticas: Total, Pendientes, Completadas, Prioridad Media

### Área de Input
- Entry para título de tarea
- Combobox para prioridad (1-5)
- Botón "➕ Añadir"

### Lista de Tareas
- Frame scrollable con tareas individuales
- Cada tarea: checkbox, título, etiqueta prioridad coloreada, fecha, botón eliminar
- Tareas completadas aparecen atenuadas
- Ordenadas por prioridad descendente

## Características Técnicas

- **Tema**: Modo oscuro con tema azul
- **Colores de prioridad**: Rojo (5) a cian (1)
- **Ordenación**: Pendientes primero, luego completadas, ambas por prioridad
- **IDs únicos**: `uuid.uuid4().int % 10000`
- **Persistencia**: Guardado automático en JSON tras cada acción
- **Responsive**: Layout adaptable con grid weights

## Eventos y Bindings

- **Enter en entry**: Dispara `add_task()`
- **Checkbox**: Llama `toggle_task_status()`
- **Botón eliminar**: Llama `delete_task()`
- **Botón añadir**: Llama `add_task()`

## Integración con Lógica

- Usa `ordenar_por_prioridad()` para ordenar tareas
- Usa `calcular_estadisticas()` para sidebar
- Usa `cargar_tareas()` y `guardar_tareas()` para persistencia

## Uso

```python
if __name__ == "__main__":
    app = TaskFlowGUI()
    app.mainloop()
```

Ejecutar con: `python -m taskflow.gui`