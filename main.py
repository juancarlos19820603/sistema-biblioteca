# main.py
# Importación de módulos necesarios para el sistema
from estructuras import ListaEnlazada  # Importa la estructura de datos ListaEnlazada
from libro import Libro  # Importa la clase Libro para manejar los libros
from usuario import Usuario  # Importa la clase Usuario para manejar los usuarios
from prestamo import Prestamo  # Importa la clase Prestamo para manejar los préstamos
import os  # Módulo para funcionalidades del sistema operativo
import sys  # Módulo para interactuar con el intérprete de Python

# Definición de la clase principal del sistema de biblioteca
class SistemaBiblioteca:
    # Método constructor de la clase
    def __init__(self):
        # Inicializa una lista enlazada para almacenar los libros
        self.libros = ListaEnlazada()
        # Inicializa una lista enlazada para almacenar los usuarios
        self.usuarios = ListaEnlazada()
        # Inicializa una lista (arreglo) para almacenar los préstamos
        self.prestamos = []  # Usamos un arreglo para préstamos
        # Contador para generar IDs únicos de préstamos
        self.contador_prestamos = 1  # Contador para IDs de préstamos
        
        # Llama al método para agregar datos de ejemplo al sistema
        # Datos de ejemplo para pruebas
        self.agregar_datos_ejemplo()
    
    # Método para agregar datos de ejemplo al sistema
    def agregar_datos_ejemplo(self):
        """Agrega datos de ejemplo al sistema"""
        # Agregar algunos libros de ejemplo
        # Lista de libros predefinidos para pruebas
        libros_ejemplo = [
            Libro("978-0142437230", "1984", "George Orwell", 1949, "Ciencia Ficción"),
            Libro("978-0061120084", "To Kill a Mockingbird", "Harper Lee", 1960, "Ficción"),
            Libro("978-0544003415", "The Hobbit", "J.R.R. Tolkien", 1937, "Fantasía"),
            Libro("978-0451524935", "The Great Gatsby", "F. Scott Fitzgerald", 1925, "Ficción"),
            Libro("978-0141439518", "Pride and Prejudice", "Jane Austen", 1813, "Romance")
        ]
        
        # Itera sobre la lista de libros ejemplo y los agrega al sistema
        for libro in libros_ejemplo:
            self.libros.agregar(libro)
        
        # Agregar algunos usuarios de ejemplo
        # Lista de usuarios predefinidos para pruebas
        usuarios_ejemplo = [
            Usuario("U001", "Juan Pérez", "juan@email.com"),
            Usuario("U002", "María García", "maria@email.com"),
            Usuario("U003", "Carlos Rodríguez", "carlos@email.com"),
            Usuario("U004", "Ana López", "ana@email.com")
        ]
        
        # Itera sobre la lista de usuarios ejemplo y los agrega al sistema
        for usuario in usuarios_ejemplo:
            self.usuarios.agregar(usuario)
    
    # ===== MÉTODOS PARA LIBROS =====
    
    # Método para agregar un nuevo libro al sistema
    def agregar_libro(self, isbn, titulo, autor, año_publicacion, genero):
        """Agrega un nuevo libro al sistema"""
        # Verificar si el libro ya existe buscando por ISBN
        if self.buscar_libro_por_isbn(isbn):
            # Retorna False y mensaje de error si ya existe
            return False, "Ya existe un libro con este ISBN"
        
        # Crea una nueva instancia de Libro con los datos proporcionados
        nuevo_libro = Libro(isbn, titulo, autor, año_publicacion, genero)
        # Agrega el nuevo libro a la lista enlazada de libros
        self.libros.agregar(nuevo_libro)
        # Retorna True y mensaje de éxito
        return True, "Libro agregado exitosamente"
    
    # Método para buscar un libro por su ISBN
    def buscar_libro_por_isbn(self, isbn):
        """Busca un libro por ISBN"""
        # Utiliza el método buscar de ListaEnlazada con una función lambda
        # que compara el ISBN del libro con el ISBN buscado
        return self.libros.buscar(lambda libro: libro.isbn == isbn)
    
    # Método para buscar libros por título (búsqueda parcial)
    def buscar_libros_por_titulo(self, titulo):
        """Busca libros por título (búsqueda parcial)"""
        # List comprehension que filtra libros cuyo título contiene el texto buscado
        # (búsqueda case-insensitive)
        return [libro for libro in self.libros.listar() if titulo.lower() in libro.titulo.lower()]
    
    # Método para buscar libros por autor (búsqueda parcial)
    def buscar_libros_por_autor(self, autor):
        """Busca libros por autor (búsqueda parcial)"""
        # List comprehension que filtra libros cuyo autor contiene el texto buscado
        # (búsqueda case-insensitive)
        return [libro for libro in self.libros.listar() if autor.lower() in libro.autor.lower()]
    
    # Método para obtener todos los libros del sistema
    def listar_libros(self):
        """Devuelve todos los libros"""
        # Utiliza el método listar de ListaEnlazada para obtener todos los libros
        return self.libros.listar()
    
    # Método para obtener solo los libros disponibles
    def listar_libros_disponibles(self):
        """Devuelve solo los libros disponibles"""
        # Filtra los libros cuyo atributo disponible es True
        return [libro for libro in self.libros.listar() if libro.disponible]
    
    # Método para actualizar los datos de un libro existente
    def actualizar_libro(self, isbn, nuevos_datos):
        """Actualiza los datos de un libro"""
        # Busca el libro por ISBN
        libro = self.buscar_libro_por_isbn(isbn)
        # Si no encuentra el libro, retorna error
        if not libro:
            return False, "Libro no encontrado"
        
        # Actualizar los campos proporcionados
        # Itera sobre el diccionario de nuevos datos
        for campo, valor in nuevos_datos.items():
            # Verifica si el libro tiene el atributo (campo)
            if hasattr(libro, campo):
                # Asigna el nuevo valor al campo correspondiente
                setattr(libro, campo, valor)
        
        # Retorna éxito después de actualizar
        return True, "Libro actualizado exitosamente"
    
    # Método para eliminar un libro del sistema
    def eliminar_libro(self, isbn):
        """Elimina un libro del sistema"""
        # Verificar si el libro está prestado
        prestamos_activos = self.obtener_prestamos_activos_por_libro(isbn)
        # Si hay préstamos activos, no permite eliminar
        if prestamos_activos:
            return False, "No se puede eliminar el libro porque tiene préstamos activos"
        
        # Intenta eliminar el libro usando el método eliminar de ListaEnlazada
        if self.libros.eliminar(lambda libro: libro.isbn == isbn):
            return True, "Libro eliminado exitosamente"
        else:
            return False, "Libro no encontrado"
    
    # ===== MÉTODOS PARA USUARIOS =====
    
    # Método para agregar un nuevo usuario al sistema
    def agregar_usuario(self, id_usuario, nombre, contacto):
        """Agrega un nuevo usuario al sistema"""
        # Verificar si el usuario ya existe buscando por ID
        if self.buscar_usuario_por_id(id_usuario):
            # Retorna error si ya existe
            return False, "Ya existe un usuario con este ID"
        
        # Crea una nueva instancia de Usuario
        nuevo_usuario = Usuario(id_usuario, nombre, contacto)
        # Agrega el usuario a la lista enlazada
        self.usuarios.agregar(nuevo_usuario)
        # Retorna éxito
        return True, "Usuario agregado exitosamente"
    
    # Método para buscar un usuario por su ID
    def buscar_usuario_por_id(self, id_usuario):
        """Busca un usuario por ID"""
        # Utiliza el método buscar de ListaEnlazada con función lambda
        return self.usuarios.buscar(lambda usuario: usuario.id_usuario == id_usuario)
    
    # Método para buscar usuarios por nombre (búsqueda parcial)
    def buscar_usuarios_por_nombre(self, nombre):
        """Busca usuarios por nombre (búsqueda parcial)"""
        # Filtra usuarios cuyo nombre contiene el texto buscado (case-insensitive)
        return [usuario for usuario in self.usuarios.listar() if nombre.lower() in usuario.nombre.lower()]
    
    # Método para obtener todos los usuarios del sistema
    def listar_usuarios(self):
        """Devuelve todos los usuarios"""
        # Utiliza el método listar de ListaEnlazada
        return self.usuarios.listar()
    
    # Método para actualizar los datos de un usuario existente
    def actualizar_usuario(self, id_usuario, nuevos_datos):
        """Actualiza los datos de un usuario"""
        # Busca el usuario por ID
        usuario = self.buscar_usuario_por_id(id_usuario)
        # Si no lo encuentra, retorna error
        if not usuario:
            return False, "Usuario no encontrado"
        
        # Actualizar los campos proporcionados
        # Itera sobre el diccionario de nuevos datos
        for campo, valor in nuevos_datos.items():
            # Verifica si el usuario tiene el atributo
            if hasattr(usuario, campo):
                # Asigna el nuevo valor al campo
                setattr(usuario, campo, valor)
        
        # Retorna éxito
        return True, "Usuario actualizado exitosamente"
    
    # Método para eliminar un usuario del sistema
    def eliminar_usuario(self, id_usuario):
        """Elimina un usuario del sistema"""
        # Verificar si el usuario tiene préstamos activos
        prestamos_activos = self.obtener_prestamos_activos_por_usuario(id_usuario)
        # Si tiene préstamos activos, no permite eliminar
        if prestamos_activos:
            return False, "No se puede eliminar el usuario porque tiene préstamos activos"
        
        # Intenta eliminar el usuario
        if self.usuarios.eliminar(lambda usuario: usuario.id_usuario == id_usuario):
            return True, "Usuario eliminado exitosamente"
        else:
            return False, "Usuario no encontrado"
    
    # ===== MÉTODOS PARA PRÉSTAMOS =====
    
    # Método para registrar un nuevo préstamo
    def registrar_prestamo(self, isbn_libro, id_usuario, fecha_prestamo):
        """Registra un nuevo préstamo"""
        # Verificar si el libro existe y está disponible
        libro = self.buscar_libro_por_isbn(isbn_libro)
        if not libro:
            return False, "Libro no encontrado"
        
        # Verifica si el libro está disponible
        if not libro.disponible:
            return False, "El libro no está disponible"
        
        # Verificar si el usuario existe
        usuario = self.buscar_usuario_por_id(id_usuario)
        if not usuario:
            return False, "Usuario no encontrado"
        
        # Generar ID de préstamo con formato P001, P002, etc.
        id_prestamo = f"P{self.contador_prestamos:03d}"
        # Incrementa el contador para el próximo préstamo
        self.contador_prestamos += 1
        
        # Registrar préstamo creando una nueva instancia de Prestamo
        nuevo_prestamo = Prestamo(id_prestamo, isbn_libro, id_usuario, fecha_prestamo)
        # Agrega el préstamo a la lista de préstamos
        self.prestamos.append(nuevo_prestamo)
        
        # Actualizar disponibilidad del libro a False
        libro.disponible = False
        
        # Retorna éxito con el ID del préstamo
        return True, f"Préstamo registrado exitosamente. ID: {id_prestamo}"
    
    # Método para registrar la devolución de un préstamo
    def registrar_devolucion(self, id_prestamo, fecha_devolucion):
        """Registra la devolución de un préstamo"""
        # Buscar préstamo activo por ID
        prestamo = next((p for p in self.prestamos if p.id_prestamo == id_prestamo and p.activo), None)
        # Si no encuentra el préstamo o ya está inactivo, retorna error
        if not prestamo:
            return False, "Préstamo no encontrado o ya devuelto"
        
        # Registrar devolución actualizando fechas y estado
        prestamo.fecha_devolucion = fecha_devolucion
        prestamo.activo = False
        
        # Actualizar disponibilidad del libro a True
        libro = self.buscar_libro_por_isbn(prestamo.isbn_libro)
        if libro:
            libro.disponible = True
        
        # Retorna éxito
        return True, "Devolución registrada exitosamente"
    
    # Método para obtener todos los préstamos activos
    def obtener_prestamos_activos(self):
        """Devuelve todos los préstamos activos"""
        # Filtra los préstamos cuyo atributo activo es True
        return [p for p in self.prestamos if p.activo]
    
    # Método para obtener préstamos activos de un usuario específico
    def obtener_prestamos_activos_por_usuario(self, id_usuario):
        """Devuelve los préstamos activos de un usuario"""
        # Filtra préstamos activos que pertenecen al usuario
        return [p for p in self.prestamos if p.activo and p.id_usuario == id_usuario]
    
    # Método para obtener préstamos activos de un libro específico
    def obtener_prestamos_activos_por_libro(self, isbn_libro):
        """Devuelve los préstamos activos de un libro"""
        # Filtra préstamos activos que corresponden al libro
        return [p for p in self.prestamos if p.activo and p.isbn_libro == isbn_libro]
    
    # Método para obtener todos los préstamos (activos e inactivos)
    def listar_todos_los_prestamos(self):
        """Devuelve todos los préstamos"""
        return self.prestamos

# Función para obtener la instancia del sistema (para la interfaz gráfica)
def obtener_sistema():
    # Retorna una nueva instancia del sistema
    return SistemaBiblioteca()

# Punto de entrada principal del programa para interfaz gráfica
if __name__ == "__main__":
    try:
        # Intenta importar y ejecutar la interfaz gráfica
        from interfaz_grafica import main as gui_main
        gui_main()
    except ImportError as e:
        # Si no puede importar la interfaz gráfica, muestra mensaje de error
        print(f"Error: No se pudo cargar la interfaz gráfica: {e}")
        print("Asegúrate de tener tkinter instalado o de que el archivo interfaz_grafica.py existe")
