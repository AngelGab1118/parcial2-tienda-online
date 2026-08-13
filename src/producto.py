class Producto:
    
    def __init__(self, id_producto, nombre, precio, categoria, stock, calificacion_promedio):
        """
        Inicializa un nuevo producto.

        """
        self.id = id_producto
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock
        self.calificacion_promedio = calificacion_promedio
    
    def __str__(self):
        """Representación en string del producto."""
        return f"Producto(id={self.id}, nombre='{self.nombre}', precio=${self.precio:.2f}, " \
               f"categoria='{self.categoria}', stock={self.stock}, calificacion={self.calificacion_promedio:.1f})"
    
    def __repr__(self):
        """Representación para depuración."""
        return self.__str__()
    
    def to_dict(self):
        """Convierte el producto a un diccionario para serialización."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'categoria': self.categoria,
            'stock': self.stock,
            'calificacion_promedio': self.calificacion_promedio
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un producto desde un diccionario."""
        return cls(
            id_producto=data['id'],
            nombre=data['nombre'],
            precio=data['precio'],
            categoria=data['categoria'],
            stock=data['stock'],
            calificacion_promedio=data['calificacion_promedio']
        )