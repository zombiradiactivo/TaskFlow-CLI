import customtkinter as ctk
import uuid

# Importamos la lógica de tu proyecto original
from models import Task
from storage import load_tasks, save_tasks
from logic import sort_by_priority, get_stats

# Configuración visual global de CustomTkinter
ctk.set_appearance_mode("dark")  # Modos: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

DB_PATH = "tasks.json"

class TaskFlowGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TaskFlow - Gestión Ultra Rápida")
        self.geometry("900x600")
        self.minsize(800, 500)
        
        # Estado de la aplicación
        self.tasks = load_tasks(DB_PATH)

        # Diccionario de colores para prioridades
        self.priority_colors = {
            5: "#FF4A4A", # Red (Crítica)
            4: "#FF9800", # Orange (Alta)
            3: "#FFC107", # Yellow (Media)
            2: "#4CAF50", # Green (Baja)
            1: "#00BCD4"  # Cyan (Muy baja)
        }

        self.setup_ui()
        self.refresh_ui()

    def setup_ui(self):
        """Configura la estructura principal de la interfaz."""
        # Grid layout (1 fila, 2 columnas)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1) # El panel derecho se expande

        # --- PANEL IZQUIERDO (Sidebar) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="📋 TaskFlow", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.stats_title = ctk.CTkLabel(self.sidebar_frame, text="Estadísticas:", font=ctk.CTkFont(size=14, weight="bold"))
        self.stats_title.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="w")

        self.lbl_stats = ctk.CTkLabel(self.sidebar_frame, text="", justify="left", font=ctk.CTkFont(size=13))
        self.lbl_stats.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="w")

        # --- PANEL DERECHO (Main Frame) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Área de ingreso de nueva tarea
        self.input_frame = ctk.CTkFrame(self.main_frame, height=60)
        self.input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry_title = ctk.CTkEntry(self.input_frame, placeholder_text="Escribe una nueva tarea...", font=ctk.CTkFont(size=14))
        self.entry_title.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="ew")
        
        # Bind para presionar Enter
        self.entry_title.bind("<Return>", lambda event: self.add_task())

        self.combo_priority = ctk.CTkComboBox(
            self.input_frame, 
            values=["Prio: 1 (Baja)", "Prio: 2", "Prio: 3", "Prio: 4", "Prio: 5 (Crítica)"],
            width=140
        )
        self.combo_priority.grid(row=0, column=1, padx=(0, 10), pady=15)
        self.combo_priority.set("Prio: 3") # Default

        self.btn_add = ctk.CTkButton(self.input_frame, text="➕ Añadir", command=self.add_task, width=100)
        self.btn_add.grid(row=0, column=2, padx=(0, 15), pady=15)

        # Área de lista de tareas (Scrollable)
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Tus Tareas Pendientes")
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

    def add_task(self):
        """Lógica para añadir una tarea desde la interfaz."""
        titulo = self.entry_title.get().strip()
        if not titulo:
            return # No añade nada si está vacío
        
        # Extraemos el número de prioridad del ComboBox (ej: "Prio: 3" -> 3)
        prioridad_str = self.combo_priority.get()
        prioridad = int(prioridad_str.split(" ")[1])

        nuevo_id = int(uuid.uuid4().int % 10000)
        nueva_tarea = Task(id=nuevo_id, titulo=titulo, prioridad=prioridad, estado="Pendiente")
        
        self.tasks.append(nueva_tarea)
        save_tasks(self.tasks, DB_PATH)
        
        self.entry_title.delete(0, 'end') # Limpiar input
        self.refresh_ui()

    def toggle_task_status(self, task: Task):
        """Alterna entre Pendiente y Completada."""
        task.estado = "Completada" if task.estado == "Pendiente" else "Pendiente"
        save_tasks(self.tasks, DB_PATH)
        self.refresh_ui()

    def delete_task(self, task: Task):
        """Elimina la tarea."""
        self.tasks.remove(task)
        save_tasks(self.tasks, DB_PATH)
        self.refresh_ui()

    def refresh_ui(self):
        """Limpia y vuelve a dibujar la lista de tareas y estadísticas."""
        # 1. Actualizar Estadísticas
        stats = get_stats(self.tasks)
        stats_text = (
            f"Total: {stats['total']}\n"
            f"Pendientes: {stats['pendientes']}\n"
            f"Completadas: {stats['completadas']}\n"
            f"Prioridad Media: {stats['prioridad_media']}"
        )
        self.lbl_stats.configure(text=stats_text)

        # 2. Limpiar frame de tareas
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 3. Ordenar tareas (Pendientes primero, luego completadas, ordenadas por prioridad)
        # Separamos para que las completadas vayan al final
        pendientes = [t for t in self.tasks if t.estado == "Pendiente"]
        completadas = [t for t in self.tasks if t.estado == "Completada"]
        
        pendientes = sort_by_priority(pendientes, reverse=True)
        completadas = sort_by_priority(completadas, reverse=True)
        
        todas_las_tareas = pendientes + completadas

        # 4. Dibujar tareas
        for i, task in enumerate(todas_las_tareas):
            task_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=("gray85", "gray16"))
            task_frame.grid(row=i, column=0, sticky="ew", pady=(0, 10), padx=5)
            task_frame.grid_columnconfigure(1, weight=1)

            # Checkbox de estado
            is_completed = (task.estado == "Completada")
            check_var = ctk.BooleanVar(value=is_completed)
            
            chk = ctk.CTkCheckBox(
                task_frame, 
                text="", 
                variable=check_var,
                width=24,
                command=lambda t=task: self.toggle_task_status(t)
            )
            chk.grid(row=0, column=0, padx=(15, 10), pady=15)

            # Título de la tarea
            text_color = "gray50" if is_completed else ("black", "white")
            lbl_title = ctk.CTkLabel(
                task_frame, 
                text=task.titulo, 
                font=ctk.CTkFont(size=15),
                text_color=text_color,
                anchor="w"
            )
            lbl_title.grid(row=0, column=1, sticky="ew")

            # Etiqueta de Prioridad
            color_prio = self.priority_colors.get(task.prioridad, "gray")
            lbl_prio = ctk.CTkLabel(
                task_frame, 
                text=f" P{task.prioridad} ", 
                fg_color=color_prio,
                text_color="white",
                corner_radius=6,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            lbl_prio.grid(row=0, column=2, padx=10)

            # Etiqueta de Fecha
            fecha_str = task.fecha.strftime("%d/%m %H:%M")
            lbl_fecha = ctk.CTkLabel(task_frame, text=fecha_str, font=ctk.CTkFont(size=11), text_color="gray50")
            lbl_fecha.grid(row=0, column=3, padx=(0, 15))

            # Botón de eliminar
            btn_del = ctk.CTkButton(
                task_frame, 
                text="🗑", 
                width=30, 
                fg_color="transparent", 
                hover_color="#FF4A4A",
                text_color=("black", "white"),
                command=lambda t=task: self.delete_task(t)
            )
            btn_del.grid(row=0, column=4, padx=(0, 10))

if __name__ == "__main__":
    app = TaskFlowGUI()
    app.mainloop()