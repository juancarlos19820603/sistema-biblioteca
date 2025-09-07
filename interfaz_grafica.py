# interfaz_grafica.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import font as tkfont
from PIL import Image, ImageTk
import sys
import os

# Importar el sistema de biblioteca desde main.py
from main import obtener_sistema

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca - SAPIENS")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f5f5f5')
        
        # Inicializar el sistema de biblioteca
        self.sistema = obtener_sistema()
        
        # Configurar fuentes
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.subtitle_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=10)
        self.text_font = tkfont.Font(family="Helvetica", size=10)
        
        # Crear el notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear las pestañas
        self.crear_pestana_inicio()
        self.crear_pestana_libros()
        self.crear_pestana_usuarios()
        self.crear_pestana_prestamos()
        self.crear_pestana_reportes()
        
    def crear_pestana_inicio(self):
        # Pestaña de inicio
        self.inicio_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inicio_frame, text="Inicio")
        
        # Título principal
        title_label = tk.Label(self.inicio_frame, text="Sistema de Gestión de Biblioteca", 
                              font=self.title_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=30)
        
        # Subtítulo
        subtitle_label = tk.Label(self.inicio_frame, text="Bienvenido al sistema SAPIENS", 
                                 font=self.subtitle_font, bg='#f5f5f5', fg='#7f8c8d')
        subtitle_label.pack(pady=10)
        
        # Frame para estadísticas
        stats_frame = tk.LabelFrame(self.inicio_frame, text="Estadísticas", font=self.subtitle_font,
                                   bg='#f5f5f5', fg='#2c3e50')
        stats_frame.pack(pady=20, padx=20, fill='x')
        
        # Obtener estadísticas
        total_libros = len(self.sistema.listar_libros())
        libros_disponibles = len(self.sistema.listar_libros_disponibles())
        total_usuarios = len(self.sistema.listar_usuarios())
        prestamos_activos = len(self.sistema.obtener_prestamos_activos())
        
        # Mostrar estadísticas
        stats_text = f"""
        Total de libros: {total_libros}
        Libros disponibles: {libros_disponibles}
        Total de usuarios: {total_usuarios}
        Préstamos activos: {prestamos_activos}
        """
        stats_label = tk.Label(stats_frame, text=stats_text, font=self.text_font, 
                              bg='#f5f5f5', justify='left')
        stats_label.pack(pady=10, padx=10)
        
        # Frame para acciones rápidas
        actions_frame = tk.LabelFrame(self.inicio_frame, text="Acciones Rápidas", 
                                     font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        actions_frame.pack(pady=20, padx=20, fill='x')
        
        # Botones de acciones rápidas
        quick_buttons = [
            ("Agregar Libro", self.agregar_libro),
            ("Registrar Usuario", self.agregar_usuario),
            ("Registrar Préstamo", self.registrar_prestamo),
            ("Ver Libros Disponibles", self.mostrar_libros_disponibles)
        ]
        
        for text, command in quick_buttons:
            btn = tk.Button(actions_frame, text=text, command=command, 
                          font=self.button_font, bg='#3498db', fg='white',
                          width=20, height=2, relief='flat')
            btn.pack(side='left', padx=10, pady=10)
    
    def crear_pestana_libros(self):
        # Pestaña de gestión de libros
        self.libros_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.libros_frame, text="Gestión de Libros")
        
        # Frame para búsqueda
        search_frame = tk.Frame(self.libros_frame, bg='#f5f5f5')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Buscar libro:", bg='#f5f5f5').pack(side='left', padx=5)
        self.libro_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.libro_search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        search_type = ttk.Combobox(search_frame, values=["ISBN", "Título", "Autor"], width=10)
        search_type.set("Título")
        search_type.pack(side='left', padx=5)
        
        search_btn = tk.Button(search_frame, text="Buscar", command=lambda: self.buscar_libros(
            self.libro_search_var.get(), search_type.get()), bg='#3498db', fg='white')
        search_btn.pack(side='left', padx=5)
        
        # Frame para lista de libros
        list_frame = tk.Frame(self.libros_frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para mostrar libros
        columns = ('ISBN', 'Título', 'Autor', 'Año', 'Género', 'Estado')
        self.libros_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Configurar columnas
        for col in columns:
            self.libros_tree.heading(col, text=col)
            self.libros_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.libros_tree.yview)
        self.libros_tree.configure(yscroll=scrollbar.set)
        
        self.libros_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para botones de acción
        action_frame = tk.Frame(self.libros_frame, bg='#f5f5f5')
        action_frame.pack(fill='x', padx=10, pady=10)
        
        # Botones de acción
        action_buttons = [
            ("Agregar Libro", self.agregar_libro),
            ("Editar Libro", self.editar_libro),
            ("Eliminar Libro", self.eliminar_libro),
            ("Actualizar Lista", self.actualizar_lista_libros)
        ]
        
        for text, command in action_buttons:
            btn = tk.Button(action_frame, text=text, command=command, 
                          font=self.button_font, bg='#3498db', fg='white',
                          width=15, height=1, relief='flat')
            btn.pack(side='left', padx=5, pady=5)
        
        # Cargar libros iniciales
        self.actualizar_lista_libros()
    
    def actualizar_lista_libros(self):
        # Limpiar treeview
        for item in self.libros_tree.get_children():
            self.libros_tree.delete(item)
        
        # Obtener y mostrar libros
        libros = self.sistema.listar_libros()
        for libro in libros:
            estado = "Disponible" if libro.disponible else "Prestado"
            self.libros_tree.insert('', 'end', values=(
                libro.isbn, libro.titulo, libro.autor, libro.año_publicacion, 
                libro.genero, estado
            ))
    
    def buscar_libros(self, criterio, tipo):
        # Limpiar treeview
        for item in self.libros_tree.get_children():
            self.libros_tree.delete(item)
        
        # Buscar según el tipo
        if tipo == "ISBN":
            libro = self.sistema.buscar_libro_por_isbn(criterio)
            if libro:
                estado = "Disponible" if libro.disponible else "Prestado"
                self.libros_tree.insert('', 'end', values=(
                    libro.isbn, libro.titulo, libro.autor, libro.año_publicacion, 
                    libro.genero, estado
                ))
        elif tipo == "Título":
            libros = self.sistema.buscar_libros_por_titulo(criterio)
            for libro in libros:
                estado = "Disponible" if libro.disponible else "Prestado"
                self.libros_tree.insert('', 'end', values=(
                    libro.isbn, libro.titulo, libro.autor, libro.año_publicacion, 
                    libro.genero, estado
                ))
        elif tipo == "Autor":
            libros = self.sistema.buscar_libros_por_autor(criterio)
            for libro in libros:
                estado = "Disponible" if libro.disponible else "Prestado"
                self.libros_tree.insert('', 'end', values=(
                    libro.isbn, libro.titulo, libro.autor, libro.año_publicacion, 
                    libro.genero, estado
                ))
    
    def agregar_libro(self):
        # Crear ventana para agregar libro
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Libro")
        add_window.geometry("500x400")
        add_window.configure(bg='#f5f5f5')
        add_window.grab_set()  # Hacer la ventana modal
        
        # Frame principal
        main_frame = tk.Frame(add_window, bg='#f5f5f5')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="Agregar Nuevo Libro", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Formulario
        form_frame = tk.Frame(main_frame, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        # Campos del formulario
        fields = [
            ("ISBN:", "isbn"),
            ("Título:", "titulo"),
            ("Autor:", "autor"),
            ("Año de publicación:", "año"),
            ("Género:", "genero")
        ]
        
        self.entries = {}
        for i, (label, field) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label, bg='#f5f5f5', anchor='e', width=15)
            lbl.grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field] = entry
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(pady=20)
        
        def guardar_libro():
            # Recoger datos del formulario
            datos = {field: self.entries[field].get() for field in self.entries}
            
            # Validar campos obligatorios
            if not all([datos['isbn'], datos['titulo'], datos['autor']]):
                messagebox.showerror("Error", "ISBN, Título y Autor son campos obligatorios")
                return
            
            # Validar que el año sea numérico si se proporciona
            try:
                año = int(datos['año']) if datos['año'] else 0
            except ValueError:
                messagebox.showerror("Error", "El año debe ser un número válido")
                return
            
            # Agregar libro
            exito, mensaje = self.sistema.agregar_libro(
                datos['isbn'], datos['titulo'], datos['autor'], año, datos['genero']
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                add_window.destroy()
                self.actualizar_lista_libros()
            else:
                messagebox.showerror("Error", mensaje)
        
        tk.Button(button_frame, text="Guardar", command=guardar_libro,
                 bg='#27ae60', fg='white', font=self.button_font).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancelar", command=add_window.destroy,
                 bg='#e74c3c', fg='white', font=self.button_font).pack(side='left', padx=10)
    
    def editar_libro(self):
        # Obtener libro seleccionado
        selected_item = self.libros_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un libro para editar")
            return
        
        # Obtener ISBN del libro seleccionado
        isbn = self.libros_tree.item(selected_item[0])['values'][0]
        
        # Buscar libro en el sistema
        libro = self.sistema.buscar_libro_por_isbn(isbn)
        if not libro:
            messagebox.showerror("Error", "No se encontró el libro seleccionado")
            return
        
        # Crear ventana para editar libro
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Libro")
        edit_window.geometry("500x400")
        edit_window.configure(bg='#f5f5f5')
        edit_window.grab_set()  # Hacer la ventana modal
        
        # Frame principal
        main_frame = tk.Frame(edit_window, bg='#f5f5f5')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="Editar Libro", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Formulario
        form_frame = tk.Frame(main_frame, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        # Campos del formulario con valores actuales
        fields = [
            ("ISBN:", "isbn", libro.isbn, False),  # ISBN no editable
            ("Título:", "titulo", libro.titulo, True),
            ("Autor:", "autor", libro.autor, True),
            ("Año de publicación:", "año", libro.año_publicacion, True),
            ("Género:", "genero", libro.genero, True)
        ]
        
        self.edit_entries = {}
        for i, (label, field, value, editable) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label, bg='#f5f5f5', anchor='e', width=15)
            lbl.grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.insert(0, str(value))
            if not editable:
                entry.config(state='readonly')
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.edit_entries[field] = entry
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(pady=20)
        
        def actualizar_libro():
            # Recoger datos del formulario
            nuevos_datos = {}
            for field in self.edit_entries:
                if field != 'isbn':  # No actualizar ISBN
                    nuevos_datos[field] = self.edit_entries[field].get()
            
            # Validar que el año sea numérico si se proporciona
            try:
                if 'año' in nuevos_datos:
                    nuevos_datos['año'] = int(nuevos_datos['año'])
            except ValueError:
                messagebox.showerror("Error", "El año debe ser un número válido")
                return
            
            # Actualizar libro
            exito, mensaje = self.sistema.actualizar_libro(isbn, nuevos_datos)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                edit_window.destroy()
                self.actualizar_lista_libros()
            else:
                messagebox.showerror("Error", mensaje)
        
        tk.Button(button_frame, text="Actualizar", command=actualizar_libro,
                 bg='#27ae60', fg='white', font=self.button_font).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancelar", command=edit_window.destroy,
                 bg='#e74c3c', fg='white', font=self.button_font).pack(side='left', padx=10)
    
    def eliminar_libro(self):
        # Obtener libro seleccionado
        selected_item = self.libros_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un libro para eliminar")
            return
        
        # Obtener ISBN del libro seleccionado
        isbn = self.libros_tree.item(selected_item[0])['values'][0]
        titulo = self.libros_tree.item(selected_item[0])['values'][1]
        
        # Confirmar eliminación
        confirmar = messagebox.askyesno(
            "Confirmar eliminación", 
            f"¿Está seguro de que desea eliminar el libro '{titulo}' (ISBN: {isbn})?"
        )
        
        if confirmar:
            # Eliminar libro
            exito, mensaje = self.sistema.eliminar_libro(isbn)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_lista_libros()
            else:
                messagebox.showerror("Error", mensaje)
    
    def crear_pestana_usuarios(self):
        # Pestaña de gestión de usuarios
        self.usuarios_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.usuarios_frame, text="Gestión de Usuarios")
        
        # Frame para búsqueda
        search_frame = tk.Frame(self.usuarios_frame, bg='#f5f5f5')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Buscar usuario:", bg='#f5f5f5').pack(side='left', padx=5)
        self.usuario_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.usuario_search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        search_type = ttk.Combobox(search_frame, values=["ID", "Nombre"], width=10)
        search_type.set("Nombre")
        search_type.pack(side='left', padx=5)
        
        search_btn = tk.Button(search_frame, text="Buscar", command=lambda: self.buscar_usuarios(
            self.usuario_search_var.get(), search_type.get()), bg='#3498db', fg='white')
        search_btn.pack(side='left', padx=5)
        
        # Frame para lista de usuarios
        list_frame = tk.Frame(self.usuarios_frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para mostrar usuarios
        columns = ('ID', 'Nombre', 'Contacto')
        self.usuarios_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Configurar columnas
        for col in columns:
            self.usuarios_tree.heading(col, text=col)
            self.usuarios_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.usuarios_tree.yview)
        self.usuarios_tree.configure(yscroll=scrollbar.set)
        
        self.usuarios_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para botones de acción
        action_frame = tk.Frame(self.usuarios_frame, bg='#f5f5f5')
        action_frame.pack(fill='x', padx=10, pady=10)
        
        # Botones de acción
        action_buttons = [
            ("Agregar Usuario", self.agregar_usuario),
            ("Editar Usuario", self.editar_usuario),
            ("Eliminar Usuario", self.eliminar_usuario),
            ("Actualizar Lista", self.actualizar_lista_usuarios)
        ]
        
        for text, command in action_buttons:
            btn = tk.Button(action_frame, text=text, command=command, 
                          font=self.button_font, bg='#3498db', fg='white',
                          width=15, height=1, relief='flat')
            btn.pack(side='left', padx=5, pady=5)
        
        # Cargar usuarios iniciales
        self.actualizar_lista_usuarios()
    
    def actualizar_lista_usuarios(self):
        # Limpiar treeview
        for item in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(item)
        
        # Obtener y mostrar usuarios
        usuarios = self.sistema.listar_usuarios()
        for usuario in usuarios:
            self.usuarios_tree.insert('', 'end', values=(
                usuario.id_usuario, usuario.nombre, usuario.contacto
            ))
    
    def buscar_usuarios(self, criterio, tipo):
        # Limpiar treeview
        for item in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(item)
        
        # Buscar según el tipo
        if tipo == "ID":
            usuario = self.sistema.buscar_usuario_por_id(criterio)
            if usuario:
                self.usuarios_tree.insert('', 'end', values=(
                    usuario.id_usuario, usuario.nombre, usuario.contacto
                ))
        elif tipo == "Nombre":
            usuarios = self.sistema.buscar_usuarios_por_nombre(criterio)
            for usuario in usuarios:
                self.usuarios_tree.insert('', 'end', values=(
                    usuario.id_usuario, usuario.nombre, usuario.contacto
                ))
    
    def agregar_usuario(self):
        # Crear ventana para agregar usuario
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Usuario")
        add_window.geometry("500x300")
        add_window.configure(bg='#f5f5f5')
        add_window.grab_set()  # Hacer la ventana modal
        
        # Frame principal
        main_frame = tk.Frame(add_window, bg='#f5f5f5')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="Agregar Nuevo Usuario", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Formulario
        form_frame = tk.Frame(main_frame, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        # Campos del formulario
        fields = [
            ("ID de usuario:", "id_usuario"),
            ("Nombre:", "nombre"),
            ("Contacto:", "contacto")
        ]
        
        self.user_entries = {}
        for i, (label, field) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label, bg='#f5f5f5', anchor='e', width=15)
            lbl.grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.user_entries[field] = entry
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(pady=20)
        
        def guardar_usuario():
            # Recoger datos del formulario
            datos = {field: self.user_entries[field].get() for field in self.user_entries}
            
            # Validar campos obligatorios
            if not all([datos['id_usuario'], datos['nombre']]):
                messagebox.showerror("Error", "ID y Nombre son campos obligatorios")
                return
            
            # Agregar usuario
            exito, mensaje = self.sistema.agregar_usuario(
                datos['id_usuario'], datos['nombre'], datos['contacto']
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                add_window.destroy()
                self.actualizar_lista_usuarios()
            else:
                messagebox.showerror("Error", mensaje)
        
        tk.Button(button_frame, text="Guardar", command=guardar_usuario,
                 bg='#27ae60', fg='white', font=self.button_font).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancelar", command=add_window.destroy,
                 bg='#e74c3c', fg='white', font=self.button_font).pack(side='left', padx=10)
    
    def editar_usuario(self):
        # Obtener usuario seleccionado
        selected_item = self.usuarios_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario para editar")
            return
        
        # Obtener ID del usuario seleccionado
        id_usuario = self.usuarios_tree.item(selected_item[0])['values'][0]
        
        # Buscar usuario en el sistema
        usuario = self.sistema.buscar_usuario_por_id(id_usuario)
        if not usuario:
            messagebox.showerror("Error", "No se encontró el usuario seleccionado")
            return
        
        # Crear ventana para editar usuario
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Usuario")
        edit_window.geometry("500x300")
        edit_window.configure(bg='#f5f5f5')
        edit_window.grab_set()  # Hacer la ventana modal
        
        # Frame principal
        main_frame = tk.Frame(edit_window, bg='#f5f5f5')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="Editar Usuario", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Formulario
        form_frame = tk.Frame(main_frame, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        # Campos del formulario con valores actuales
        fields = [
            ("ID de usuario:", "id_usuario", usuario.id_usuario, False),  # ID no editable
            ("Nombre:", "nombre", usuario.nombre, True),
            ("Contacto:", "contacto", usuario.contacto, True)
        ]
        
        self.edit_user_entries = {}
        for i, (label, field, value, editable) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label, bg='#f5f5f5', anchor='e', width=15)
            lbl.grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.insert(0, str(value))
            if not editable:
                entry.config(state='readonly')
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.edit_user_entries[field] = entry
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(pady=20)
        
        def actualizar_usuario():
            # Recoger datos del formulario
            nuevos_datos = {}
            for field in self.edit_user_entries:
                if field != 'id_usuario':  # No actualizar ID
                    nuevos_datos[field] = self.edit_user_entries[field].get()
            
            # Actualizar usuario
            exito, mensaje = self.sistema.actualizar_usuario(id_usuario, nuevos_datos)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                edit_window.destroy()
                self.actualizar_lista_usuarios()
            else:
                messagebox.showerror("Error", mensaje)
        
        tk.Button(button_frame, text="Actualizar", command=actualizar_usuario,
                 bg='#27ae60', fg='white', font=self.button_font).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancelar", command=edit_window.destroy,
                 bg='#e74c3c', fg='white', font=self.button_font).pack(side='left', padx=10)
    
    def eliminar_usuario(self):
        # Obtener usuario seleccionado
        selected_item = self.usuarios_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario para eliminar")
            return
        
        # Obtener ID del usuario seleccionado
        id_usuario = self.usuarios_tree.item(selected_item[0])['values'][0]
        nombre = self.usuarios_tree.item(selected_item[0])['values'][1]
        
        # Confirmar eliminación
        confirmar = messagebox.askyesno(
            "Confirmar eliminación", 
            f"¿Está seguro de que desea eliminar al usuario '{nombre}' (ID: {id_usuario})?"
        )
        
        if confirmar:
            # Eliminar usuario
            exito, mensaje = self.sistema.eliminar_usuario(id_usuario)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_lista_usuarios()
            else:
                messagebox.showerror("Error", mensaje)
    
    def crear_pestana_prestamos(self):
        # Pestaña de gestión de préstamos
        self.prestamos_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.prestamos_frame, text="Gestión de Préstamos")
        
        # Frame para operaciones de préstamos
        operations_frame = tk.LabelFrame(self.prestamos_frame, text="Operaciones de Préstamos", 
                                       font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        operations_frame.pack(fill='x', padx=10, pady=10)
        
        # Botones de operaciones
        operation_buttons = [
            ("Registrar Préstamo", self.registrar_prestamo),
            ("Registrar Devolución", self.registrar_devolucion),
            ("Actualizar Lista", self.actualizar_lista_prestamos)
        ]
        
        for text, command in operation_buttons:
            btn = tk.Button(operations_frame, text=text, command=command, 
                          font=self.button_font, bg='#3498db', fg='white',
                          width=15, height=2, relief='flat')
            btn.pack(side='left', padx=10, pady=10)
        
        # Frame para lista de préstamos
        list_frame = tk.Frame(self.prestamos_frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para mostrar préstamos
        columns = ('ID Préstamo', 'ISBN Libro', 'ID Usuario', 'Fecha Préstamo', 'Fecha Devolución', 'Estado')
        self.prestamos_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Configurar columnas
        column_widths = [100, 120, 100, 120, 120, 100]
        for i, col in enumerate(columns):
            self.prestamos_tree.heading(col, text=col)
            self.prestamos_tree.column(col, width=column_widths[i])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.prestamos_tree.yview)
        self.prestamos_tree.configure(yscroll=scrollbar.set)
        
        self.prestamos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar préstamos iniciales
        self.actualizar_lista_prestamos()
    
    def actualizar_lista_prestamos(self):
        # Limpiar treeview
        for item in self.prestamos_tree.get_children():
            self.prestamos_tree.delete(item)
        
        # Obtener y mostrar préstamos
        prestamos = self.sistema.listar_todos_los_prestamos()
        for prestamo in prestamos:
            estado = "Activo" if prestamo.activo else "Finalizado"
            self.prestamos_tree.insert('', 'end', values=(
                prestamo.id_prestamo, prestamo.isbn_libro, prestamo.id_usuario,
                prestamo.fecha_prestamo, prestamo.fecha_devolucion or "No devuelto", estado
            ))
    
    def registrar_prestamo(self):
        # Crear ventana para registrar préstamo
        prestamo_window = tk.Toplevel(self.root)
        prestamo_window.title("Registrar Préstamo")
        prestamo_window.geometry("500x300")
        prestamo_window.configure(bg='#f5f5f5')
        prestamo_window.grab_set()  # Hacer la ventana modal
        
        # Frame principal
        main_frame = tk.Frame(prestamo_window, bg='#f5f5f5')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="Registrar Nuevo Préstamo", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Formulario
        form_frame = tk.Frame(main_frame, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        # Campos del formulario
        fields = [
            ("ISBN del libro:", "isbn_libro"),
            ("ID del usuario:", "id_usuario"),
            ("Fecha de préstamo (YYYY-MM-DD):", "fecha_prestamo")
        ]
        
        self.prestamo_entries = {}
        for i, (label, field) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label, bg='#f5f5f5', anchor='e', width=25)
            lbl.grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.prestamo_entries[field] = entry
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(pady=20)
        
        def guardar_prestamo():
            # Recoger datos del formulario
            datos = {field: self.prestamo_entries[field].get() for field in self.prestamo_entries}
            
            # Validar campos obligatorios
            if not all(datos.values()):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            # Registrar préstamo
            exito, mensaje = self.sistema.registrar_prestamo(
                datos['isbn_libro'], datos['id_usuario'], datos['fecha_prestamo']
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                prestamo_window.destroy()
                self.actualizar_lista_prestamos()
                self.actualizar_lista_libros()  # Actualizar estado de libros
            else:
                messagebox.showerror("Error", mensaje)
        
        tk.Button(button_frame, text="Registrar", command=guardar_prestamo,
                 bg='#27ae60', fg='white', font=self.button_font).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancelar", command=prestamo_window.destroy,
                 bg='#e74c3c', fg='white', font=self.button_font).pack(side='left', padx=10)
    
    def registrar_devolucion(self):
        # Obtener préstamo seleccionado
        selected_item = self.prestamos_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un préstamo para registrar devolución")
            return
        
        # Obtener ID del préstamo seleccionado
        id_prestamo = self.prestamos_tree.item(selected_item[0])['values'][0]
        estado = self.prestamos_tree.item(selected_item[0])['values'][5]
        
        # Verificar que el préstamo esté activo
        if estado != "Activo":
            messagebox.showwarning("Advertencia", "Solo se pueden registrar devoluciones de préstamos activos")
            return
        
        # Pedir fecha de devolución
        fecha_devolucion = simpledialog.askstring(
            "Registrar Devolución", 
            f"Ingrese la fecha de devolución (YYYY-MM-DD) para el préstamo {id_prestamo}:"
        )
        
        if fecha_devolucion:
            # Registrar devolución
            exito, mensaje = self.sistema.registrar_devolucion(id_prestamo, fecha_devolucion)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_lista_prestamos()
                self.actualizar_lista_libros()  # Actualizar estado de libros
            else:
                messagebox.showerror("Error", mensaje)
    
    def crear_pestana_reportes(self):
        # Pestaña de reportes
        self.reportes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reportes_frame, text="Reportes")
        
        # Frame para reportes
        reports_frame = tk.Frame(self.reportes_frame, bg='#f5f5f5')
        reports_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(reports_frame, text="Reportes del Sistema", 
                              font=self.subtitle_font, bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Frame para botones de reportes
        buttons_frame = tk.Frame(reports_frame, bg='#f5f5f5')
        buttons_frame.pack(pady=20)
        
        # Botones de reportes
        report_buttons = [
            ("Libros Disponibles", self.mostrar_libros_disponibles),
            ("Préstamos Activos", self.mostrar_prestamos_activos),
            ("Todos los Libros", self.mostrar_todos_libros),
            ("Todos los Usuarios", self.mostrar_todos_usuarios)
        ]
        
        for i, (text, command) in enumerate(report_buttons):
            btn = tk.Button(buttons_frame, text=text, command=command, 
                          font=self.button_font, bg='#3498db', fg='white',
                          width=20, height=2, relief='flat')
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
    
    def mostrar_libros_disponibles(self):
        # Crear ventana para mostrar libros disponibles
        disp_window = tk.Toplevel(self.root)
        disp_window.title("Libros Disponibles")
        disp_window.geometry("800x400")
        
        # Frame principal
        main_frame = tk.Frame(disp_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, text="Libros Disponibles", 
                              font=self.subtitle_font)
        title_label.pack(pady=10)
        
        # Treeview para mostrar libros disponibles
        columns = ('ISBN', 'Título', 'Autor', 'Año', 'Género')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Obtener y mostrar libros disponibles
        libros = self.sistema.listar_libros_disponibles()
        for libro in libros:
            tree.insert('', 'end', values=(
                libro.isbn, libro.titulo, libro.autor, 
                libro.año_publicacion, libro.genero
            ))
    
    def mostrar_prestamos_activos(self):
        # Crear ventana para mostrar préstamos activos
        activos_window = tk.Toplevel(self.root)
        activos_window.title("Préstamos Activos")
        activos_window.geometry("900x400")
        
        # Frame principal
        main_frame = tk.Frame(activos_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, text="Préstamos Activos", 
                              font=self.subtitle_font)
        title_label.pack(pady=10)
        
        # Treeview para mostrar préstamos activos
        columns = ('ID Préstamo', 'ISBN Libro', 'ID Usuario', 'Fecha Préstamo')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        # Configurar columnas
        column_widths = [100, 120, 100, 120]
        for i, col in enumerate(columns):
            tree.heading(col, text=col)
            tree.column(col, width=column_widths[i])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Obtener y mostrar préstamos activos
        prestamos = self.sistema.obtener_prestamos_activos()
        for prestamo in prestamos:
            tree.insert('', 'end', values=(
                prestamo.id_prestamo, prestamo.isbn_libro, 
                prestamo.id_usuario, prestamo.fecha_prestamo
            ))
    
    def mostrar_todos_libros(self):
        # Similar a mostrar_libros_disponibles pero con todos los libros
        # Crear ventana para mostrar todos los libros
        all_window = tk.Toplevel(self.root)
        all_window.title("Todos los Libros")
        all_window.geometry("800x400")
        
        # Frame principal
        main_frame = tk.Frame(all_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, text="Todos los Libros", 
                              font=self.subtitle_font)
        title_label.pack(pady=10)
        
        # Treeview para mostrar todos los libros
        columns = ('ISBN', 'Título', 'Autor', 'Año', 'Género', 'Estado')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Obtener y mostrar todos los libros
        libros = self.sistema.listar_libros()
        for libro in libros:
            estado = "Disponible" if libro.disponible else "Prestado"
            tree.insert('', 'end', values=(
                libro.isbn, libro.titulo, libro.autor, 
                libro.año_publicacion, libro.genero, estado
            ))
    
    def mostrar_todos_usuarios(self):
        # Crear ventana para mostrar todos los usuarios
        users_window = tk.Toplevel(self.root)
        users_window.title("Todos los Usuarios")
        users_window.geometry("700x400")
        
        # Frame principal
        main_frame = tk.Frame(users_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, text="Todos los Usuarios", 
                              font=self.subtitle_font)
        title_label.pack(pady=10)
        
        # Treeview para mostrar todos los usuarios
        columns = ('ID', 'Nombre', 'Contacto')
        tree = tttk.Treeview(main_frame, columns=columns, show='headings')
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Obtener y mostrar todos los usuarios
        usuarios = self.sistema.listar_usuarios()
        for usuario in usuarios:
            tree.insert('', 'end', values=(
                usuario.id_usuario, usuario.nombre, usuario.contacto
            ))

def main():
    # Crear ventana principal
    root = tk.Tk()
    app = BibliotecaApp(root)
    
    # Centrar ventana en la pantalla
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == "__main__":
    main()