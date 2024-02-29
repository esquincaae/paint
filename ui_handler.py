import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from drawing_tools import draw_line, draw_polyline, draw_rectangle, draw_circle, erase_area

class UIHandler:
    def __init__(self, window, canvas_width, canvas_height):
        self.window = window
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        # Definiendo el canvas principal
        self.canvas = tk.Canvas(window, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        # Inicializando la imagen de OpenCV como lienzo blanco
        self.image = self.initialize_image(canvas_width, canvas_height)
        # Creando la ventana de herramientas antes de configurar los botones
        self.tools_window = tk.Toplevel(window)
        self.tools_window.title("Herramientas")
        self.tools_window.geometry("600x100")  # Configuración para una ventana apaisada
        # Configurando los botones de herramientas después de definir tools_window
        self.setup_tool_buttons()
        # Atributo para la herramienta actual
        self.current_tool = None

    def initialize_image(self, width, height):
        """Inicializa una imagen en blanco."""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        image.fill(255)
        return image

    def setup_tool_buttons(self):
        # Botones para seleccionar herramientas, colocados de forma horizontal.
        line_button = tk.Button(self.tools_window, text="Línea", command=lambda: self.select_tool('line'))
        line_button.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        polyline_button = tk.Button(self.tools_window, text="Polilínea", command=lambda: self.select_tool('polyline'))
        polyline_button.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        rectangle_button = tk.Button(self.tools_window, text="Rectángulo", command=lambda: self.select_tool('rectangle'))
        rectangle_button.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        circle_button = tk.Button(self.tools_window, text="Círculo", command=lambda: self.select_tool('circle'))
        circle_button.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        erase_button = tk.Button(self.tools_window, text="Borrar", command=lambda: self.select_tool('erase'))
        erase_button.pack(side=tk.LEFT, fill=tk.Y, expand=True)

    def on_button_press(self, event):
        """Delega a la función correspondiente según la herramienta activa."""
        if self.current_tool == 'line':
            self.on_button_press_line(event)
        # Agrega condiciones similares para otras herramientas.

    def on_button_release(self, event):
        """Delega a la función correspondiente según la herramienta activa."""
        if self.current_tool == 'line':
            self.on_button_release_line(event)
        # Agrega condiciones similares para otras herramientas.

    def on_button_press_line(self, event):
        """Acciones específicas al presionar el botón para dibujar una línea."""
        self.start_point = (event.x, event.y)

    def on_button_release_line(self, event):
        """Acciones específicas al liberar el botón después de dibujar una línea."""
        self.end_point = (event.x, event.y)
        draw_line(self.image, self.start_point, self.end_point)
        self.update_canvas()

    def draw_polyline(self, event):
        """Dibuja segmentos conectando el último punto con el actual."""
        current_point = (event.x, event.y)
        if self.last_point:
            draw_polyline(self.image, self.last_point, current_point)
            self.update_canvas()
        self.last_point = current_point

    def erase_area_event(self, event):
        """Borra un área alrededor del punto donde se encuentra el cursor."""
        eraser_size = 20  # Define el tamaño del borrador.
        top_left = (event.x - eraser_size, event.y - eraser_size)
        bottom_right = (event.x + eraser_size, event.y + eraser_size)
        erase_area(self.image, top_left, bottom_right)
        self.update_canvas()

    def update_canvas(self):
        """Actualiza el lienzo de Tkinter con la imagen de OpenCV."""
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.image))
        # Crea una nueva imagen en el lienzo o actualiza la existente.
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def select_tool(self, tool):
        """Selecciona la herramienta y actualiza los enlaces de eventos."""
        # Primero, desvincula todos los eventos para evitar conflictos.
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        # Reinicia los puntos de inicio y final para asegurar que no se arrastren datos de eventos anteriores.
        self.start_point = None
        self.end_point = None
        self.current_tool = tool
        if tool == 'line':
            self.canvas.bind("<ButtonPress-1>", self.on_button_press_line)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release_line)
        elif tool == 'polyline':
            self.canvas.bind("<ButtonPress-1>", self.on_button_press_polyline)
            self.canvas.bind("<B1-Motion>", self.draw_polyline)
        elif tool == 'rectangle':
            self.canvas.bind("<ButtonPress-1>", self.on_button_press_rectangle)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release_rectangle)
        elif tool == 'circle':
            self.canvas.bind("<ButtonPress-1>", self.on_button_press_circle)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release_circle)
        elif tool == 'erase':
            self.canvas.bind("<B1-Motion>", self.erase_area_event)

    def on_button_press_polyline(self, event):
        """Establece el punto de inicio para la polilínea."""
        if not self.start_point:
            self.start_point = (event.x, event.y)
        self.last_point = self.start_point

    def on_button_release_polyline(self, event):
        """No es necesario definir acciones al soltar el botón para polilíneas."""
        pass

    def on_button_press_rectangle(self, event):
        self.start_point = (event.x, event.y)

    def on_button_release_rectangle(self, event):
        self.end_point = (event.x, event.y)
        draw_rectangle(self.image, self.start_point, self.end_point)
        self.update_canvas()

    def on_button_press_circle(self, event):
        self.start_point = (event.x, event.y)

    def on_button_release_circle(self, event):
        radius = int(((self.start_point[0] - event.x)**2 + (self.start_point[1] - event.y)**2) ** 0.5)
        draw_circle(self.image, self.start_point, radius)
        self.update_canvas()
    
    def on_tools_window_close(self):
        # Función para manejar el cierre de la ventana de herramientas.
        self.window.destroy()