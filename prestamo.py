# prestamo.py
from datetime import datetime

class Prestamo:
    """
    Clase que representa un préstamo en el sistema de gestión de biblioteca.
    
    Atributos:
        id_prestamo (str): Identificador único del préstamo.
        isbn_libro (str): ISBN del libro prestado.
        id_usuario (str): ID del usuario que realizó el préstamo.
        fecha_prestamo (str): Fecha en que se realizó el préstamo (formato YYYY-MM-DD).
        fecha_devolucion (str): Fecha en que se devolvió el libro (formato YYYY-MM-DD).
        activo (bool): Estado del préstamo (True si está activo, False si está finalizado).
    """
    
    def __init__(self, id_prestamo, isbn_libro, id_usuario, fecha_prestamo):
        """
        Inicializa una nueva instancia de la clase Prestamo.
        
        Args:
            id_prestamo (str): Identificador único del préstamo.
            isbn_libro (str): ISBN del libro prestado.
            id_usuario (str): ID del usuario que realizó el préstamo.
            fecha_prestamo (str): Fecha en que se realizó el préstamo.
        """
        self.id_prestamo = id_prestamo
        self.isbn_libro = isbn_libro
        self.id_usuario = id_usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = None  # Inicialmente no hay fecha de devolución
        self.activo = True  # Por defecto, el préstamo está activo
    
    def __str__(self):
        """
        Devuelve una representación en string del préstamo.
        
        Returns:
            str: Información formateada del préstamo.
        """
        estado = "Activo" if self.activo else "Finalizado"
        devolucion = f", Devolución: {self.fecha_devolucion}" if self.fecha_devolucion else ""
        return f"ID: {self.id_prestamo}, Libro: {self.isbn_libro}, Usuario: {self.id_usuario}, Préstamo: {self.fecha_prestamo}{devolucion}, Estado: {estado}"
    
    def registrar_devolucion(self, fecha_devolucion=None):
        """
        Registra la devolución del libro.
        
        Args:
            fecha_devolucion (str, optional): Fecha de devolución. Si no se proporciona, 
                                              se usa la fecha actual.
        """
        if fecha_devolucion is None:
            # Usar fecha actual si no se proporciona
            fecha_devolucion = datetime.now().strftime("%Y-%m-%d")
        
        self.fecha_devolucion = fecha_devolucion
        self.activo = False
    
    def to_dict(self):
        """
        Convierte el objeto Prestamo a un diccionario.
        
        Returns:
            dict: Diccionario con todos los atributos del préstamo.
        """
        return {
            'id_prestamo': self.id_prestamo,
            'isbn_libro': self.isbn_libro,
            'id_usuario': self.id_usuario,
            'fecha_prestamo': self.fecha_prestamo,
            'fecha_devolucion': self.fecha_devolucion,
            'activo': self.activo
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Prestamo a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del préstamo.
            
        Returns:
            Prestamo: Nueva instancia de la clase Prestamo.
        """
        prestamo = cls(
            data['id_prestamo'],
            data['isbn_libro'],
            data['id_usuario'],
            data['fecha_prestamo']
        )
        prestamo.fecha_devolucion = data['fecha_devolucion']
        prestamo.activo = data['activo']
        return prestamo
    
    def dias_retraso(self):
        """
        Calcula los días de retraso en la devolución.
        
        Returns:
            int: Número de días de retraso (0 si no hay retraso o el préstamo está activo).
        """
        if self.activo or not self.fecha_devolucion:
            return 0
        
        # Convertir fechas a objetos datetime para calcular la diferencia
        fecha_prestamo = datetime.strptime(self.fecha_prestamo, "%Y-%m-%d")
        fecha_devolucion = datetime.strptime(self.fecha_devolucion, "%Y-%m-%d")
        
        # Suponemos que el período de préstamo es de 15 días
        dias_prestamo = 15
        fecha_limite = fecha_prestamo + timedelta(days=dias_prestamo)
        
        if fecha_devolucion > fecha_limite:
            retraso = (fecha_devolucion - fecha_limite).days
            return retraso
        
        return 0


# Bloque de prueba para verificar el funcionamiento de la clase Prestamo
if __name__ == "__main__":
    print("=== Prueba de la clase Prestamo ===")
    
    # Crear un préstamo de prueba
    prestamo_prueba = Prestamo("P001", "978-0142437230", "U001", "2023-10-15")
    print(f"Préstamo creado: {prestamo_prueba}")
    
    # Registrar devolución
    prestamo_prueba.registrar_devolucion("2023-10-25")
    print(f"Después de registrar devolución: {prestamo_prueba}")
    
    # Convertir a diccionario
    dict_prestamo = prestamo_prueba.to_dict()
    print(f"Representación en diccionario: {dict_prestamo}")
    
    # Crear préstamo desde diccionario
    nuevo_prestamo = Prestamo.from_dict(dict_prestamo)
    print(f"Préstamo desde diccionario: {nuevo_prestamo}")
    
    # Probar cálculo de días de retraso
    prestamo_retraso = Prestamo("P002", "978-0061120084", "U002", "2023-10-01")
    prestamo_retraso.registrar_devolucion("2023-10-20")  # 4 días de retraso (15 días de préstamo)
    print(f"Días de retraso: {prestamo_retraso.dias_retraso()}")
    
    print("=== Prueba completada ===")