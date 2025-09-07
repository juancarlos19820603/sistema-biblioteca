# libro.py
class Libro:
    """
    Clase que representa un libro en el sistema de gestión de biblioteca.
    
    Atributos:
        isbn (str): Número único de identificación del libro.
        titulo (str): Título del libro.
        autor (str): Autor del libro.
        año_publicacion (int): Año de publicación del libro.
        genero (str): Género literario del libro.
        disponible (bool): Estado de disponibilidad del libro (True si está disponible, False si está prestado).
    """
    
    def __init__(self, isbn, titulo, autor, año_publicacion, genero):
        """
        Inicializa una nueva instancia de la clase Libro.
        
        Args:
            isbn (str): Número único de identificación del libro.
            titulo (str): Título del libro.
            autor (str): Autor del libro.
            año_publicacion (int): Año de publicación del libro.
            genero (str): Género literario del libro.
        """
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.año_publicacion = año_publicacion
        self.genero = genero
        self.disponible = True  # Por defecto, el libro está disponible
    
    def __str__(self):
        """
        Devuelve una representación en string del libro.
        
        Returns:
            str: Información formateada del libro incluyendo su estado de disponibilidad.
        """
        estado = "Disponible" if self.disponible else "Prestado"
        return f"ISBN: {self.isbn}, Título: {self.titulo}, Autor: {self.autor}, Año: {self.año_publicacion}, Género: {self.genero}, Estado: {estado}"
    
    def cambiar_estado(self):
        """
        Cambia el estado de disponibilidad del libro.
        
        Si está disponible, lo marca como prestado y viceversa.
        """
        self.disponible = not self.disponible
    
    def to_dict(self):
        """
        Convierte el objeto Libro a un diccionario.
        
        Returns:
            dict: Diccionario con todos los atributos del libro.
        """
        return {
            'isbn': self.isbn,
            'titulo': self.titulo,
            'autor': self.autor,
            'año_publicacion': self.año_publicacion,
            'genero': self.genero,
            'disponible': self.disponible
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Libro a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del libro.
            
        Returns:
            Libro: Nueva instancia de la clase Libro.
        """
        libro = cls(
            data['isbn'],
            data['titulo'],
            data['autor'],
            data['año_publicacion'],
            data['genero']
        )
        libro.disponible = data['disponible']
        return libro


# Bloque de prueba para verificar el funcionamiento de la clase Libro
if __name__ == "__main__":
    print("=== Prueba de la clase Libro ===")
    
    # Crear un libro de prueba
    libro_prueba = Libro("978-0142437230", "1984", "George Orwell", 1949, "Ciencia Ficción")
    print(f"Libro creado: {libro_prueba}")
    
    # Cambiar estado del libro
    libro_prueba.cambiar_estado()
    print(f"Después de cambiar estado: {libro_prueba}")
    
    # Convertir a diccionario
    dict_libro = libro_prueba.to_dict()
    print(f"Representación en diccionario: {dict_libro}")
    
    # Crear libro desde diccionario
    nuevo_libro = Libro.from_dict(dict_libro)
    print(f"Libro desde diccionario: {nuevo_libro}")
    
    print("=== Prueba completada ===")