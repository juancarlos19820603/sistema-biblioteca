# estructuras.py
class Nodo:
    """
    Clase que representa un nodo en una lista enlazada.
    
    Atributos:
        dato: El dato almacenado en el nodo.
        siguiente: Referencia al siguiente nodo en la lista.
    """
    
    def __init__(self, dato):
        """
        Inicializa un nuevo nodo con el dato proporcionado.
        
        Args:
            dato: El dato a almacenar en el nodo.
        """
        self.dato = dato  # Almacena el dato en el nodo
        self.siguiente = None  # Inicialmente no hay siguiente nodo


class ListaEnlazada:
    """
    Clase que representa una lista enlazada simple.
    
    Atributos:
        cabeza: Referencia al primer nodo de la lista.
        tamanio: Número de elementos en la lista.
    """
    
    def __init__(self):
        """Inicializa una lista enlazada vacía."""
        self.cabeza = None  # La lista comienza vacía
        self.tamanio = 0    # Tamaño inicial es cero
    
    def esta_vacia(self):
        """
        Verifica si la lista está vacía.
        
        Returns:
            bool: True si la lista está vacía, False en caso contrario.
        """
        return self.cabeza is None
    
    def agregar(self, dato):
        """
        Agrega un nuevo elemento al final de la lista.
        
        Args:
            dato: El dato a agregar a la lista.
        """
        # Crear un nuevo nodo con el dato
        nuevo_nodo = Nodo(dato)
        
        # Si la lista está vacía, el nuevo nodo se convierte en la cabeza
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            # Recorrer hasta el último nodo
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            # Enlazar el último nodo con el nuevo nodo
            actual.siguiente = nuevo_nodo
        
        # Incrementar el tamaño de la lista
        self.tamanio += 1
    
    def eliminar(self, criterio):
        """
        Elimina el primer elemento que cumpla con el criterio especificado.
        
        Args:
            criterio: Función que toma un dato y devuelve True si cumple el criterio de eliminación.
            
        Returns:
            bool: True si se eliminó un elemento, False en caso contrario.
        """
        # Si la lista está vacía, no hay nada que eliminar
        if self.esta_vacia():
            return False
        
        # Si el primer nodo cumple el criterio
        if criterio(self.cabeza.dato):
            self.cabeza = self.cabeza.siguiente  # La cabeza ahora es el siguiente nodo
            self.tamanio -= 1  # Decrementar el tamaño
            return True
        
        # Buscar el nodo a eliminar
        actual = self.cabeza
        while actual.siguiente is not None:
            # Si el siguiente nodo cumple el criterio
            if criterio(actual.siguiente.dato):
                # Saltar el nodo a eliminar
                actual.siguiente = actual.siguiente.siguiente
                self.tamanio -= 1  # Decrementar el tamaño
                return True
            actual = actual.siguiente
        
        # No se encontró ningún elemento que cumpla el criterio
        return False
    
    def buscar(self, criterio):
        """
        Busca el primer elemento que cumpla con el criterio especificado.
        
        Args:
            criterio: Función que toma un dato y devuelve True si cumple el criterio de búsqueda.
            
        Returns:
            El dato encontrado o None si no se encuentra.
        """
        # Recorrer todos los nodos
        actual = self.cabeza
        while actual is not None:
            # Si el dato cumple el criterio, devolverlo
            if criterio(actual.dato):
                return actual.dato
            actual = actual.siguiente
        
        # No se encontró ningún elemento que cumpla el criterio
        return None
    
    def listar(self):
        """
        Devuelve todos los elementos de la lista en forma de lista Python.
        
        Returns:
            list: Una lista con todos los datos almacenados en la lista enlazada.
        """
        elementos = []  # Lista para almacenar los elementos
        actual = self.cabeza
        
        # Recorrer todos los nodos y agregar sus datos a la lista
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        
        return elementos
    
    def actualizar(self, criterio, nuevos_datos):
        """
        Actualiza el primer elemento que cumpla con el criterio especificado.
        
        Args:
            criterio: Función que toma un dato y devuelve True si cumple el criterio de actualización.
            nuevos_datos: Diccionario con los campos a actualizar y sus nuevos valores.
            
        Returns:
            bool: True si se actualizó un elemento, False en caso contrario.
        """
        # Buscar el elemento a actualizar
        elemento = self.buscar(criterio)
        
        # Si se encontró el elemento, actualizar sus campos
        if elemento:
            for clave, valor in nuevos_datos.items():
                # Verificar que el elemento tenga el atributo antes de actualizarlo
                if hasattr(elemento, clave):
                    setattr(elemento, clave, valor)
            return True
        
        # No se encontró ningún elemento que cumpla el criterio
        return False
    
    def __str__(self):
        """
        Representación en string de la lista enlazada.
        
        Returns:
            str: Una representación legible de la lista.
        """
        elementos = []
        actual = self.cabeza
        
        # Recorrer todos los nodos y agregar sus datos a la lista
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        
        return " -> ".join(elementos) if elementos else "Lista vacía"


# Bloque de prueba para verificar el funcionamiento de las estructuras
if __name__ == "__main__":
    print("=== Prueba de las estructuras de datos ===")
    
    # Prueba de la ListaEnlazada
    lista = ListaEnlazada()
    print(f"Lista inicial: {lista}")
    print(f"¿Está vacía? {lista.esta_vacia()}")
    
    # Agregar elementos
    lista.agregar("Libro 1")
    lista.agregar("Libro 2")
    lista.agregar("Libro 3")
    print(f"Lista después de agregar elementos: {lista}")
    print(f"Tamaño de la lista: {lista.tamanio}")
    
    # Buscar elemento
    resultado = lista.buscar(lambda x: x == "Libro 2")
    print(f"Búsqueda de 'Libro 2': {resultado}")
    
    # Eliminar elemento
    eliminado = lista.eliminar(lambda x: x == "Libro 2")
    print(f"¿Se eliminó 'Libro 2'? {eliminado}")
    print(f"Lista después de eliminar: {lista}")
    print(f"Tamaño de la lista: {lista.tamanio}")
    
    # Listar todos los elementos
    todos = lista.listar()
    print(f"Todos los elementos: {todos}")
    
    print("=== Prueba completada ===")