# TaskFlow CLI - Documentación del Proyecto

## Descripción General

TaskFlow CLI es un gestor de tareas moderno ejecutado desde la terminal, desarrollado en Python 3.12+. El proyecto implementa una arquitectura limpia con separación de responsabilidades, persistencia de datos en JSON y interfaces tanto de línea de comandos como gráfica.

## Arquitectura del Proyecto

El proyecto sigue una estructura modular con las siguientes capas:

- **models.py**: Define las estructuras de datos (dataclasses)
- **storage.py**: Maneja la persistencia de datos (JSON)
- **logic.py**: Contiene la lógica de negocio (filtrado, ordenación, estadísticas)
- **cli.py**: Interfaz de línea de comandos (Typer + Rich)
- **gui.py**: Interfaz gráfica (CustomTkinter)

## Características Principales

- Interfaz CLI vibrante con Rich para tablas coloreadas
- Interfaz GUI moderna con CustomTkinter
- Sistema de prioridades (1-5) y estados (Pendiente/Completada)
- Persistencia robusta en archivos JSON
- Tests unitarios con pytest
- Arquitectura limpia y mantenible

## Requisitos

- Python 3.12+
- Dependencias: typer, rich, customtkinter, pytest

## Instalación

```bash
git clone https://github.com/zombiradiactivo/TaskFlow-CLI.git
cd TaskFlow-CLI
pip install -r requirements.txt
```

## Uso

### CLI
```bash
# Añadir tarea
python -m taskflow.cli add "Tarea importante" 5

# Listar tareas
python -m taskflow.cli list

# Completar tarea
python -m taskflow.cli done 123

# Eliminar tarea
python -m taskflow.cli delete 123
```

### GUI
```bash
python -m taskflow.gui
```

## Tests
```bash
pytest
```

## Metodología de Desarrollo

Proyecto desarrollado con colaboración humano-IA, aplicando:
- Generación asistida de código
- Refactorización iterativa
- Validación crítica de IA
- Arquitectura limpia

## Archivos de Documentación

- [cli.md](cli.md) - Documentación del módulo CLI
- [gui.md](gui.md) - Documentación del módulo GUI
- [logic.md](logic.md) - Documentación del módulo de lógica
- [models.md](models.md) - Documentación del módulo de modelos
- [storage.md](storage.md) - Documentación del módulo de almacenamiento