import customtkinter as ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GestorTareas:
    def __init__(self):
        self.tareas = []
        self.tareas_mostradas = []
        self.busqueda_actual = ""
        self.filtro_actual = "todas"

        self.cargar_tareas()
        self.crear_ui()
        self.entrada.focus()
        self.actualizar_lista()

    def crear_ui(self):
        self.ventana = ctk.CTk()
        self.ventana.title("Gestor de tareas")
        self.ventana.geometry("650x600")
        self.ventana.configure(bg="#0e0e49")
        self.ventana.bind("<Return>", self.agregar_tarea)

        self.titulo = ctk.CTkLabel(
            self.ventana,
            text="Gestor de tareas 🧠",
            font=("Segoe UI", 16),
            text_color="white"
        ) 

        self.entrada = ctk.CTkEntry(
            self.ventana,
            font=("Segoe UI", 12),
            width= 5,
            justify="center"
        )

        self.frame_tareas = ctk.CTkFrame(self.ventana)

        self.contador = ctk.CTkLabel(
            self.ventana,
            text="Total: 0",
            font=("Segoe UI", 12),
            text_color="white"
        ) 

        self.buscar = ctk.CTkEntry(
            self.ventana,
            font=("Segoe UI", 12),
            width=30,
            justify="center"
        )
        self.buscar.bind("<KeyRelease>", self.texto_busqueda)

        self.agregar = ctk.CTkButton(
            self.ventana,
            text="Agregar tarea",
            command=self.agregar_tarea,
            text_color="white",
            font=("Segoe UI", 10),
        )

        self.titulo.pack(pady=5)
        self.entrada.pack(pady= (15, 5), padx=20, fill="x")
        self.frame_tareas.pack(pady=15, padx=20, fill="both", expand=True)
        self.contador.pack(pady=5)
        self.buscar.pack(pady=(5, 10), padx=20, fill="x")
        self.agregar.pack(padx=10, pady=5)

    def actualizar_lista(self):
        for widget in self.frame_tareas.winfo_children():
            widget.destroy()
        self.tareas_mostradas.clear()

        tareas_a_mostrar = self.tareas
        completadas = sum(1 for t in self.tareas if t["completada"])
        pendientes = len(self.tareas) - completadas

        if self.filtro_actual == "pendientes":
            tareas_a_mostrar = [t for t in self.tareas if not t["completada"]]

        elif self.filtro_actual == "completadas":
            tareas_a_mostrar = [t for t in self.tareas if t["completada"]]


        if self.busqueda_actual:
            tareas_a_mostrar = [t for t in tareas_a_mostrar if self.busqueda_actual in t["titulo"].lower()]

        for tarea in tareas_a_mostrar:
            self.tareas_mostradas.append(tarea)

            texto = f"✔{tarea["titulo"]}" if tarea["completada"] else f"{tarea["titulo"]}"

            item = ctk.CTkFrame(self.frame_tareas, corner_radius=10)
            item.pack(fill="x", pady=6, padx=15)

            label = ctk.CTkLabel(item, text=texto, anchor="w")
            label.pack(side="left", padx=10, pady=5) 

            botones_frame = ctk.CTkFrame(item, fg_color="transparent")
            botones_frame.pack(side="right", padx=10)

            btn_completar = ctk.CTkButton(
                botones_frame,
                text="✔",
                width=30,
                command=lambda t=tarea: self.toggle_tarea(t)
            )
            btn_completar.pack(side="left", padx=2)

            btn_eliminar = ctk.CTkButton(
                botones_frame,
                text="🗑",
                width=30,
                fg_color="#a81818",
                hover_color="#8f1414",
                command=lambda t=tarea: self.eliminar_tarea_directa(t)
            )
            btn_eliminar.pack(side="left", padx=2)

            if tarea["completada"]:
                label.configure(text_color="#ffffff")
                item.configure(fg_color="#2f4f2f")
                btn_completar.configure(text="↺")
            else:
                item.configure(fg_color="#1a1a3d")

            item.bind("<Button-1>", lambda e, t=tarea: self.toggle_tarea(t))
            item.bind("<Enter>", lambda e, w=item: w.configure(fg_color="#2a2a5a"))

            item.bind( 
                "<Leave>",
                lambda e, w=item, t=tarea:
                w.configure(fg_color="#2f4f2f" if t["completada"] else "#1a1a3d")
            )

            item.configure(fg_color="#1a1a3d")
            item.configure(cursor="hand2")
            item.pack_propagate(False)
            item.configure(height=40)

            label.bind("<Button-1>", lambda e, t=tarea: self.toggle_tarea(t))
            label.configure(cursor="hand2")

        if not tareas_a_mostrar:
            ctk.CTkLabel(
                self.frame_tareas,
                text="No hay tareas...",
                text_color="gray"
            ).pack(pady=20)

        self.contador.configure(text=f"Total: {len(self.tareas)} | ✔: {completadas} | Pendientes: {pendientes}")

    def toggle_tarea(self, tarea):
        tarea["completada"] = not tarea["completada"]
        self.actualizar_lista()
        self.guardar()

    def eliminar_tarea_directa(self, tarea):
        self.tareas.remove(tarea)
        self.actualizar_lista()
        self.guardar()

    def cargar_tareas(self):
        try:
            with open("tareas.txt", "r") as archivo:
                for linea in archivo:
                    titulo, estado = linea.strip().split("|")
                    tarea = {
                        "titulo": titulo,
                        "completada": estado == "True"
                    }
                    self.tareas.append(tarea)
        except FileNotFoundError:
            pass

    def agregar_tarea(self, event=None): 
        titulo = self.entrada.get().strip()
        if not titulo:
            return
        tarea = {
            "titulo": titulo,
            "completada": False
        }
        self.tareas.append(tarea)
        self.actualizar_lista()
        self.entrada.delete(0, ctk.END)
        self.entrada.focus()
        self.guardar()

    def eliminar_tarea(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            return
    
        indice = seleccion[0]

        tarea = self.tareas_mostradas[indice]
        self.tareas.remove(tarea)
        self.guardar()
        self.actualizar_lista()

    def completar_tarea(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            return
    
        indice = seleccion[0]

        tarea = self.tareas_mostradas[indice]
        tarea["completada"] = not tarea["completada"]

        self.actualizar_lista()
        self.guardar()

    def texto_busqueda(self, event=None):
        self.busqueda_actual = self.buscar.get().strip().lower()

        self.actualizar_lista()

    def guardar(self):
        with open("tareas.txt", "w") as archivo:
            for tarea in self.tareas:
                linea = f'{tarea["titulo"]}|{tarea["completada"]}'
                archivo.write(linea + "\n")

app = GestorTareas()
app.ventana.mainloop()