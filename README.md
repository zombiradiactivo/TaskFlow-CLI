# TaskFlow CLI 🚀
TaskFlow CLI es un gestor de tareas moderno ejecutado directamente desde la terminal. Desarrollado en Python 3.12+, el proyecto implementa una arquitectura limpia, persistencia de datos y una interfaz visual atractiva, todo bajo un flujo de trabajo de desarrollo asistido por IA.

## 🛠️ Características Principales

    Interfaz Vibrante: Uso de la librería rich para tablas y mensajes con colores y formato avanzado.

    Comandos Intuitivos: Construido con typer para una experiencia de usuario fluida en la CLI.

    Persistencia Robusta: Almacenamiento local mediante archivos JSON para no perder nunca tus tareas.

    Gestión Inteligente: Sistema de prioridades y estados de tarea (Pendiente/Completada).

    Calidad de Código: Batería de tests unitarios con pytest y uso de dataclasses para un tipado fuerte.

## 🏗️ Requisitos Técnicos

    Lenguaje: Python 3.12 o superior.

    Dependencias principales:

        typer: Para la creación de la interfaz de comandos.

        rich: Para el renderizado de tablas y estilos en consola.

        pytest: Para la ejecución de tests.

        customtkinter: Para la interfaz grafica.

        pydantic / dataclasses: Para el modelado y validación de datos.

## 🚀 Instalación y Configuración

Clona el repositorio:
````Bash
git clone https://github.com/zombiradiactivo/TaskFlow-CLI.git
cd TaskFlow-CLI
````
Crea y activa un entorno virtual(Opcional):
````Bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
````
Instala las dependencias:
````Bash
pip install -r requirements.txt
````

## 💻 Uso de la Aplicación via CLI 

A continuación, algunos comandos básicos para interactuar con TaskFlow:


Añadir una tarea(1 Prioridad baja - 5 Prioridad Alta):
````Bash
python -m taskflow.cli add "Nombre de la tarea" [1-5] 
````
Listar tareas:
````Bash
python -m taskflow.cli list
````
Completar una tarea:
````Bash
python -m taskflow.cli done [id]
````
Eliminar una tarea:
````Bash
python -m taskflow.cli delete [id]
````

## 💻 Uso de la Aplicación via GUI

Iniciar la interfaz grafica:
````Bash
python -m taskflow.gui
````

## 🧠 Metodología: Colaboración Humano-IA

Este proyecto es un caso de estudio sobre el desarrollo de software moderno. Se han aplicado los siguientes pilares:

    Generación Asistida: Uso de prompts estratégicos para el andamiaje inicial del código.

    Refactorización Iterativa: Mejora constante de la estructura del código para garantizar mantenibilidad.

    Algoritmos y Lógica: Implementación manual y asistida de sistemas de filtrado y ordenación.

    IA Responsable: Validación crítica de cada línea generada, asegurando que el código cumple con los estándares de seguridad y eficiencia.

## 🧪 Testing

Para asegurar la estabilidad del proyecto, ejecuta la suite de pruebas con el siguiente comando:
````Bash
pytest
````