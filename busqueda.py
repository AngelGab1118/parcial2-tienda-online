import time
import random
from typing import List, Optional, Tuple
from producto import Producto

def busqueda_binaria_por_id(productos: List[Producto], id_buscar: int) -> Tuple[Optional[Producto], int]:
    """
    Realiza búsqueda binaria de un producto por su ID.

    """
    izquierda = 0
    derecha = len(productos) - 1
    comparaciones = 0
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        comparaciones += 1
        
        if productos[medio].id == id_buscar:
            return productos[medio], comparaciones
        elif productos[medio].id < id_buscar:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    
    return None, comparaciones

def busqueda_lineal_por_subcadena(productos: List[Producto], subcadena: str) -> Tuple[List[Producto], int]:
    """
    Realiza búsqueda lineal de productos cuyo nombre contiene una subcadena.

    """
    resultados = []
    comparaciones = 0
    subcadena_lower = subcadena.lower()
    
    for producto in productos:
        comparaciones += 1
        if subcadena_lower in producto.nombre.lower():
            resultados.append(producto)
    
    return resultados, comparaciones

def generar_ids_para_busqueda(productos: List[Producto], cantidad: int, existentes: bool) -> List[int]:
    """
    Genera IDs para realizar búsquedas.

    """
    ids_existentes = [p.id for p in productos]
    ids_resultado = []
    
    if existentes:
        # Seleccionar IDs aleatorios de los existentes
        ids_resultado = random.sample(ids_existentes, min(cantidad, len(ids_existentes)))
    else:
        # Generar IDs que no existen
        max_id = max(ids_existentes) + 100
        generados = set()
        intentos = 0
        while len(generados) < cantidad and intentos < 10000:
            id_candidato = random.randint(max_id + 1, max_id + 1000)
            if id_candidato not in ids_existentes and id_candidato not in generados:
                generados.add(id_candidato)
            intentos += 1
        ids_resultado = list(generados)
    
    return ids_resultado

def generar_subcadenas_para_busqueda(productos: List[Producto], cantidad: int, con_resultados: bool) -> List[str]:
    """
    Genera subcadenas realistas para búsqueda por nombre.
    
    """
    subcadenas = []
    
    if con_resultados:
        # Extraer subcadenas significativas de los nombres existentes
        for _ in range(cantidad):
            producto = random.choice(productos)
            nombre = producto.nombre
            # Tomar una subcadena de al menos 3 caracteres
            if len(nombre) >= 5:
                # Intentar tomar una palabra completa o parte de ella
                palabras = nombre.split()
                if len(palabras) >= 2:
                    # Tomar una palabra completa aleatoria
                    palabra = random.choice(palabras)
                    if len(palabra) >= 3:
                        subcadenas.append(palabra.lower())
                    else:
                        # Tomar parte de una palabra
                        inicio = random.randint(0, len(nombre) - 3)
                        fin = random.randint(inicio + 3, len(nombre))
                        subcadenas.append(nombre[inicio:fin].lower())
                else:
                    # Tomar parte del nombre
                    inicio = random.randint(0, len(nombre) - 3)
                    fin = random.randint(inicio + 3, len(nombre))
                    subcadenas.append(nombre[inicio:fin].lower())
            else:
                subcadenas.append(nombre.lower())
    else:
        # Generar subcadenas que NO estén en los nombres
        palabras_no_existentes = [
            "xyz", "qwerty", "zzz", "abcxyz", "patata", "tralala",
            "supercalifragilistico", "electrodomestico", "automovil",
            "computadora", "telefono", "cocina", "jardin", "piscina",
            "montaña", "oceano", "desierto", "selva", "volcan"
        ]
        for _ in range(cantidad):
            palabra = random.choice(palabras_no_existentes)
            # Asegurar que realmente no exista en ningún nombre
            existe = any(palabra.lower() in p.nombre.lower() for p in productos)
            if existe:
                palabra = f"{palabra}{random.randint(100, 999)}"
            subcadenas.append(palabra)
    
    # Asegurar que todas las subcadenas tengan al menos 3 caracteres
    subcadenas = [s for s in subcadenas if len(s) >= 3]
    
    # Si alguna quedó vacía, añadir una palabra común
    while len(subcadenas) < cantidad:
        subcadenas.append("pro")
    
    return subcadenas[:cantidad]

def medir_busquedas_binarias(productos: List[Producto], ids_buscar: List[int]) -> dict:
    """
    Mide el rendimiento de búsquedas binarias.

    """
    tiempos = []
    comparaciones = []
    resultados = []
    detalles = []
    
    for id_buscar in ids_buscar:
        inicio = time.time()
        producto, comps = busqueda_binaria_por_id(productos, id_buscar)
        fin = time.time()
        
        tiempos.append(fin - inicio)
        comparaciones.append(comps)
        resultados.append(producto is not None)
        detalles.append({
            'id': id_buscar,
            'encontrado': producto is not None,
            'comparaciones': comps,
            'tiempo': fin - inicio
        })
    
    return {
        'tiempo_total': sum(tiempos),
        'tiempo_promedio': sum(tiempos) / len(tiempos),
        'comparaciones_totales': sum(comparaciones),
        'comparaciones_promedio': sum(comparaciones) / len(comparaciones),
        'encontrados': sum(resultados),
        'no_encontrados': len(resultados) - sum(resultados),
        'detalles': detalles
    }

def medir_busquedas_lineales(productos: List[Producto], subcadenas: List[str]) -> dict:
    """
    Mide el rendimiento de búsquedas lineales por subcadena.

    """
    tiempos = []
    comparaciones = []
    resultados = []
    detalles = []
    
    for subcadena in subcadenas:
        inicio = time.time()
        encontrados, comps = busqueda_lineal_por_subcadena(productos, subcadena)
        fin = time.time()
        
        tiempos.append(fin - inicio)
        comparaciones.append(comps)
        resultados.append(len(encontrados) > 0)
        detalles.append({
            'subcadena': subcadena,
            'encontrados': len(encontrados),
            'tiene_resultados': len(encontrados) > 0,
            'comparaciones': comps,
            'tiempo': fin - inicio
        })
    
    return {
        'tiempo_total': sum(tiempos),
        'tiempo_promedio': sum(tiempos) / len(tiempos),
        'comparaciones_totales': sum(comparaciones),
        'comparaciones_promedio': sum(comparaciones) / len(comparaciones),
        'encontrados': sum(resultados),
        'no_encontrados': len(resultados) - sum(resultados),
        'detalles': detalles
    }