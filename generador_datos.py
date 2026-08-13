import random
import json
import os
from producto import Producto

# Listas de nombres y categorías para generar datos realistas
NOMBRES_PRODUCTOS = [
    "Smartphone Galaxy S24", "iPhone 15 Pro Max", "Laptop ThinkPad X1", "Tablet Samsung Tab S9",
    "Monitor 4K Ultra HD", "Teclado Mecánico RGB", "Mouse Inalámbrico MX", "Auriculares Bluetooth Pro",
    "Disco Duro SSD 1TB", "Memoria USB 256GB", "Camisa de Algodón Premium", "Pantalón Jeans Clásico",
    "Zapatos Deportivos Run", "Chaqueta de Cuero Negro", "Vestido Floral Primavera", "Reloj Inteligente Pro",
    "Cámara Digital 4K", "Impresora Láser Color", "Router WiFi 6", "Bocina Portátil Bluetooth",
    "Libro de Ciencia Ficción", "Novela Best Seller 2024", "Cuento Infantil Ilustrado", "Enciclopedia Temática",
    "Revista de Moda Vogue", "Cafetera Automática", "Licuadora de Alta Potencia", "Aspiradora Robot Smart",
    "Plancha de Vapor Pro", "Microondas Digital", "Refrigerador Inteligente", "Lavadora Secadora",
    "Sofá Cama 3 plazas", "Mesa de Centro Moderna", "Estantería Modular", "Lámpara LED Decorativa",
    "Set de Toallas Premium", "Juego de Sábanas 100% Algodón", "Cortinas Blackout", "Tapete Decorativo",
    "Set de Ollas Antiadherente", "Vajilla de Porcelana", "Cubiertos de Acero Inoxidable",
    "Jarras de Vidrio", "Botella de Agua Térmica", "Taza Térmica"
]

CATEGORIAS = ["Electrónica", "Ropa", "Libros", "Hogar", "Deportes", "Juguetes", "Salud", "Belleza"]

def generar_productos(cantidad=50, id_inicial=1):
    """
    Genera una lista de productos con datos aleatorios realistas.

    """
    productos = []
    nombres_usados = set()
    
    for i in range(cantidad):
        # Seleccionar nombre único y realista
        nombre_disponible = None
        intentos = 0
        while nombre_disponible is None and intentos < 100:
            nombre_base = random.choice(NOMBRES_PRODUCTOS)
            # Añadir variante para hacerlo más único (20% de probabilidad)
            if random.random() < 0.2:
                variantes = ["Pro", "Plus", "Max", "Premium", "Deluxe", "2024", "Edition"]
                nombre_base = f"{nombre_base} {random.choice(variantes)}"
            if nombre_base not in nombres_usados:
                nombre_disponible = nombre_base
                nombres_usados.add(nombre_disponible)
            intentos += 1
        
        if nombre_disponible is None:
            nombre_disponible = f"Producto Especial {i+1}"
            nombres_usados.add(nombre_disponible)
        
        # Generar datos aleatorios realistas
        precio = round(random.uniform(5.99, 1500.00), 2)
        categoria = random.choice(CATEGORIAS)
        stock = random.randint(0, 100)
        calificacion = round(random.uniform(1.0, 5.0), 1)
        
        producto = Producto(
            id_producto=id_inicial + i,
            nombre=nombre_disponible,
            precio=precio,
            categoria=categoria,
            stock=stock,
            calificacion_promedio=calificacion
        )
        productos.append(producto)
    
    return productos

def guardar_productos_json(productos, archivo_path="data/productos.json"):
    """
    Guarda la lista de productos en un archivo JSON.

    """
    os.makedirs(os.path.dirname(archivo_path), exist_ok=True)
    data = [p.to_dict() for p in productos]
    with open(archivo_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def cargar_productos_json(archivo_path="data/productos.json"):
    """
    Carga la lista de productos desde un archivo JSON.

    """
    with open(archivo_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Producto.from_dict(p) for p in data]