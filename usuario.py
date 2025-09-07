# usuario.py
class Usuario:
    """
    Clase que representa un usuario en el sistema de gestión de biblioteca.
    
    Atributos:
        id_usuario (str): Identificador único del usuario.
        nombre (str): Nombre completo del usuario.
        contacto (str): Información de contacto del usuario (email, teléfono, etc.).
    """
    
    def __init__(self, id_usuario, nombre, contacto):
        """
        Inicializa una nueva instancia de la clase Usuario.
        
        Args:
            id_usuario (str): Identificador único del usuario.
            nombre (str): Nombre completo del usuario.
            contacto (str): Información de contacto del usuario.
        """
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.contacto = contacto
    
    def __str__(self):
        """
        Devuelve una representación en string del usuario.
        
        Returns:
            str: Información formateada del usuario.
        """
        return f"ID: {self.id_usuario}, Nombre: {self.nombre}, Contacto: {self.contacto}"
    
    def to_dict(self):
        """
        Convierte el objeto Usuario a un diccionario.
        
        Returns:
            dict: Diccionario con todos los atributos del usuario.
        """
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'contacto': self.contacto
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Usuario a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del usuario.
            
        Returns:
            Usuario: Nueva instancia de la clase Usuario.
        """
        return cls(
            data['id_usuario'],
            data['nombre'],
            data['contacto']
        )


# Bloque de prueba para verificar el funcionamiento de la clase Usuario
if __name__ == "__main__":
    print("=== Prueba de la clase Usuario ===")
    
    # Crear un usuario de prueba
    usuario_prueba = Usuario("U001", "Juan Pérez", "juan@email.com")
    print(f"Usuario creado: {usuario_prueba}")
    
    # Convertir a diccionario
    dict_usuario = usuario_prueba.to_dict()
    print(f"Representación en diccionario: {dict_usuario}")
    
    # Crear usuario desde diccionario
    nuevo_usuario = Usuario.from_dict(dict_usuario)
    print(f"Usuario desde diccionario: {nuevo_usuario}")
    
    print("=== Prueba completada ===")