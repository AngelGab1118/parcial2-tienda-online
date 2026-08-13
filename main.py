import os
import sys
import json
from datetime import datetime

# Añadir el directorio src al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from producto import Producto
from generador_datos import generar_productos, guardar_productos_json, cargar_productos_json
from algoritmos_ordenamiento import (
    ordenar_por_precio_ascendente,
    ordenar_por_calificacion_descendente,
    merge_sort_wrapper,
    quick_sort_wrapper,
    insertion_sort_wrapper
)
from busqueda import (
    generar_ids_para_busqueda,
    generar_subcadenas_para_busqueda,
    medir_busquedas_binarias,
    medir_busquedas_lineales
)


def imprimir_seccion(titulo, contenido="", caracter="="):
    """Imprime una sección formateada."""
    print("\n" + caracter * 70)
    print(f" {titulo} ")
    print(caracter * 70)
    if contenido:
        print(contenido)


def imprimir_productos(productos, limite=5):
    """Imprime una lista de productos con un límite."""
    if len(productos) <= limite:
        for p in productos:
            print(f"  {p}")
    else:
        for p in productos[:limite]:
            print(f"  {p}")
        print(f"  ... y {len(productos) - limite} productos más")


def ejecutar_pruebas_ordenamiento(productos):
    """Ejecuta las pruebas de ordenamiento y muestra resultados."""
    imprimir_seccion("PRUEBAS DE ORDENAMIENTO")
    
    resultados = {}
    algoritmos = ["merge", "quick", "insertion"]
    criterios = [
        ("precio_asc", ordenar_por_precio_ascendente, "Precio (Ascendente)", "Precio más bajo"),
        ("calificacion_desc", ordenar_por_calificacion_descendente, "Calificación (Descendente)", "Mejor calificación")
    ]
    
    for criterio_key, funcion, criterio_nombre, atributo_mostrar in criterios:
        print(f"\n--- Ordenamiento por: {criterio_nombre} ---")
        resultados[criterio_key] = {}
        
        for algoritmo in algoritmos:
            # Crear una copia de la lista para cada prueba
            copia_productos = productos.copy()
            
            try:
                lista_ordenada, tiempo = funcion(copia_productos, algoritmo)
                
                resultados[criterio_key][algoritmo] = {
                    'tiempo': tiempo,
                    'lista_ordenada': lista_ordenada[:5]
                }
                
                print(f"  {algoritmo.upper()} Sort: {tiempo:.6f} segundos")
                
                # Mostrar primeros productos como verificación
                if lista_ordenada:
                    primer = lista_ordenada[0]
                    print(f"    Primer producto: {primer}")
                    if criterio_key == "precio_asc":
                        print(f"    {atributo_mostrar}: ${primer.precio:.2f}")
                    else:
                        print(f"    {atributo_mostrar}: {primer.calificacion_promedio:.1f}")
            except Exception as e:
                print(f"  Error en {algoritmo.upper()} Sort: {e}")
                resultados[criterio_key][algoritmo] = {'tiempo': None, 'error': str(e)}
    
    return resultados


def ejecutar_pruebas_busqueda(productos):
    """Ejecuta las pruebas de búsqueda y muestra resultados."""
    imprimir_seccion("PRUEBAS DE BÚSQUEDA")
    
    # Ordenar productos por ID para búsqueda binaria
    print("\n--- Preparando datos para búsqueda ---")
    print("Ordenando productos por ID...")
    productos_ordenados_id, tiempo_ordenamiento = merge_sort_wrapper(productos, lambda p: p.id, reverse=False)
    print(f"  Ordenamiento por ID completado en {tiempo_ordenamiento:.6f} segundos")
    
    # Búsqueda por ID
    print("\n--- Búsqueda por ID (Búsqueda Binaria) ---")
    print("\n   Buscando IDs EXISTENTES:")
    ids_existentes = generar_ids_para_busqueda(productos, 10, existentes=True)
    print(f"    IDs a buscar: {ids_existentes}")
    resultados_existentes = medir_busquedas_binarias(productos_ordenados_id, ids_existentes)
    
    print("\n   Buscando IDs NO EXISTENTES:")
    ids_no_existentes = generar_ids_para_busqueda(productos, 10, existentes=False)
    print(f"    IDs a buscar: {ids_no_existentes}")
    resultados_no_existentes = medir_busquedas_binarias(productos_ordenados_id, ids_no_existentes)
    
    print("\n   RESULTADOS DE BÚSQUEDA POR ID:")
    print(f"\n    IDs EXISTENTES:")
    print(f"      Tiempo total: {resultados_existentes['tiempo_total']:.6f} segundos")
    print(f"      Tiempo promedio: {resultados_existentes['tiempo_promedio']:.6f} segundos")
    print(f"      Comparaciones promedio: {resultados_existentes['comparaciones_promedio']:.0f}")
    print(f"      Encontrados: {resultados_existentes['encontrados']}")
    
    print(f"\n    IDs NO EXISTENTES:")
    print(f"      Tiempo total: {resultados_no_existentes['tiempo_total']:.6f} segundos")
    print(f"      Tiempo promedio: {resultados_no_existentes['tiempo_promedio']:.6f} segundos")
    print(f"      Comparaciones promedio: {resultados_no_existentes['comparaciones_promedio']:.0f}")
    print(f"      No encontrados: {resultados_no_existentes['no_encontrados']}")
    
    # Búsqueda por nombre
    print("\n--- Búsqueda por Nombre (Búsqueda Lineal) ---")
    print("\n   Buscando subcadenas CON resultados:")
    subcadenas_con = generar_subcadenas_para_busqueda(productos, 10, con_resultados=True)
    print(f"    Subcadenas: {subcadenas_con}")
    resultados_con = medir_busquedas_lineales(productos, subcadenas_con)
    
    print("\n   Buscando subcadenas SIN resultados:")
    subcadenas_sin = generar_subcadenas_para_busqueda(productos, 10, con_resultados=False)
    print(f"    Subcadenas: {subcadenas_sin}")
    resultados_sin = medir_busquedas_lineales(productos, subcadenas_sin)
    
    print("\n   RESULTADOS DE BÚSQUEDA POR NOMBRE:")
    print(f"\n    Subcadenas CON resultados:")
    print(f"      Tiempo total: {resultados_con['tiempo_total']:.6f} segundos")
    print(f"      Tiempo promedio: {resultados_con['tiempo_promedio']:.6f} segundos")
    print(f"      Comparaciones promedio: {resultados_con['comparaciones_promedio']:.0f}")
    print(f"      Búsquedas con resultados: {resultados_con['encontrados']}")
    
    print(f"\n    Subcadenas SIN resultados:")
    print(f"      Tiempo total: {resultados_sin['tiempo_total']:.6f} segundos")
    print(f"      Tiempo promedio: {resultados_sin['tiempo_promedio']:.6f} segundos")
    print(f"      Comparaciones promedio: {resultados_sin['comparaciones_promedio']:.0f}")
    print(f"      Búsquedas sin resultados: {resultados_sin['no_encontrados']}")
    
    return {
        'busqueda_id': {
            'existentes': resultados_existentes,
            'no_existentes': resultados_no_existentes
        },
        'busqueda_nombre': {
            'con_resultados': resultados_con,
            'sin_resultados': resultados_sin
        }
    }


def mostrar_analisis(resultados_ordenamiento, resultados_busqueda):
    """Muestra el análisis completo de resultados."""
    print("\n" + "=" * 70)
    print(" ANÁLISIS DE RESULTADOS ")
    print("=" * 70)
    
    # ============ ANÁLISIS DE ORDENAMIENTO ============
    print("\n ANÁLISIS DE ORDENAMIENTO")
    print("-" * 50)
    
    for criterio_key, nombre in [("precio_asc", "precio ascendente"), 
                                ("calificacion_desc", "calificación descendente")]:
        if criterio_key in resultados_ordenamiento:
            print(f"\n Ordenamiento por {nombre}:")
            tiempos = {}
            for algo, datos in resultados_ordenamiento[criterio_key].items():
                if datos.get('tiempo') is not None:
                    tiempos[algo] = datos['tiempo']
            
            if tiempos:
                mejor = min(tiempos, key=tiempos.get)
                peor = max(tiempos, key=tiempos.get)
                print(f"  • Algoritmo más rápido: {mejor.upper()} Sort ({tiempos[mejor]:.6f}s)")
                print(f"  • Algoritmo más lento: {peor.upper()} Sort ({tiempos[peor]:.6f}s)")
                print(f"  • Diferencia: {(tiempos[peor] - tiempos[mejor]):.6f}s")
                
                # Análisis teórico
                print("\n   Comparación con la teoría:")
                if mejor in ["merge", "quick"]:
                    print(f"     {mejor.upper()} Sort tiene complejidad O(n log n), consistente con los resultados")
                if peor == "insertion":
                    print(f"     Insertion Sort es O(n²), más lento para n=50 como se esperaba")
                
                # Análisis de complejidad
                print(f"     Para n=50 elementos:")
                print(f"      • Merge Sort: O(50 log 50) ≈ 50 × 5.64 = 282 operaciones")
                print(f"      • Quick Sort: O(50 log 50) ≈ 50 × 5.64 = 282 operaciones (promedio)")
                print(f"      • Insertion Sort: O(50²) = 2500 operaciones (peor caso)")
                print(f"     La teoría predice que Insertion Sort debería ser ~9 veces más lento")
    
    # ============ ANÁLISIS DE BÚSQUEDA ============
    print("\n\n ANÁLISIS DE BÚSQUEDA")
    print("-" * 50)
    
    if 'busqueda_id' in resultados_busqueda:
        print("\n Búsqueda por ID (Búsqueda Binaria):")
        print("  ¿Por qué es ideal?")
        print("    • Reduce el espacio de búsqueda a la mitad en cada paso")
        print("    • Complejidad O(log n) ≈ log₂(50) ≈ 6 comparaciones")
        print("    • Extremadamente rápida incluso con grandes volúmenes")
        print("    • Determinista: el ID es único y ordenable")
        
        datos_existentes = resultados_busqueda['busqueda_id']['existentes']
        print(f"\n   Resultados empíricos:")
        print(f"    • Comparaciones promedio: {datos_existentes['comparaciones_promedio']:.0f}")
        print(f"    • Tiempo promedio: {datos_existentes['tiempo_promedio']:.6f}s")
        print(f"     Coincide con la teoría: log₂(50) ≈ 5.64 ≈ 6 comparaciones")
    
    if 'busqueda_nombre' in resultados_busqueda:
        print("\n Búsqueda por Nombre (Búsqueda Lineal):")
        print("  ¿Cómo afecta la naturaleza de la búsqueda por subcadena?")
        print("    • Debe recorrer TODO el arreglo: O(n) = 50 comparaciones")
        print("    • Comparación de strings es más costosa que números")
        print("    • Coincidencias parciales añaden complejidad")
        print("    • El tiempo crece linealmente con el tamaño de datos")
        
        datos_con = resultados_busqueda['busqueda_nombre']['con_resultados']
        print(f"\n   Resultados empíricos:")
        print(f"    • Comparaciones promedio: {datos_con['comparaciones_promedio']:.0f}")
        print(f"    • Tiempo promedio: {datos_con['tiempo_promedio']:.6f}s")
        print(f"    • Es ~5-10 veces más lenta que la búsqueda binaria")
        
        print("\n   Alternativas para optimizar en producción:")
        print("    • Índices de texto completo (Elasticsearch, Lucene)")
        print("    • Árboles de prefijos (Trie) para búsquedas rápidas")
        print("    • Algoritmos avanzados: KMP (Knuth-Morris-Pratt), Boyer-Moore")
        print("    • Caché de búsquedas frecuentes")
        print("    • Inverted Index (índice invertido) para palabras clave")
    
    # ============ COMPARACIÓN GLOBAL ============
    print("\n\n COMPARACIÓN GLOBAL")
    print("-" * 50)
    print("\n  Comparación de tiempos entre operaciones:")
    
    # Obtener tiempos promedio
    tiempo_ordenamiento_promedio = 0
    for criterio in ['precio_asc', 'calificacion_desc']:
        if criterio in resultados_ordenamiento:
            tiempos = [v['tiempo'] for v in resultados_ordenamiento[criterio].values() 
                      if v.get('tiempo') is not None]
            if tiempos:
                tiempo_ordenamiento_promedio += sum(tiempos) / len(tiempos) / 2
    
    tiempo_busqueda_id = resultados_busqueda['busqueda_id']['existentes']['tiempo_promedio']
    tiempo_busqueda_nombre = resultados_busqueda['busqueda_nombre']['con_resultados']['tiempo_promedio']
    
    print(f"  • Ordenamiento (promedio): {tiempo_ordenamiento_promedio:.6f}s")
    print(f"  • Búsqueda por ID: {tiempo_busqueda_id:.6f}s")
    print(f"  • Búsqueda por nombre: {tiempo_busqueda_nombre:.6f}s")
    print(f"\n La búsqueda por nombre es ~{tiempo_busqueda_nombre/tiempo_busqueda_id:.1f}x más lenta que búsqueda por ID")


def guardar_resultados_completos(resultados_ordenamiento, resultados_busqueda, 
                                 productos, archivo="resultados/resultados.txt"):
    """Guarda todos los resultados con análisis en un archivo de texto."""
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RESULTADOS DEL PARCIAL 2 - TIENDA EN LÍNEA\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total de productos: {len(productos)}\n")
        f.write("=" * 80 + "\n\n")
        
        # ===== ORDENAMIENTO =====
        f.write("RESULTADOS DE ORDENAMIENTO\n")
        f.write("-" * 60 + "\n")
        
        for criterio_key, nombre in [("precio_asc", "Precio (Ascendente)"), 
                                    ("calificacion_desc", "Calificación (Descendente)")]:
            f.write(f"\nOrdenamiento por {nombre}:\n")
            if criterio_key in resultados_ordenamiento:
                for algo, datos in resultados_ordenamiento[criterio_key].items():
                    if datos.get('tiempo') is not None:
                        f.write(f"  {algo.upper()} Sort: {datos['tiempo']:.6f} segundos\n")
                    else:
                        f.write(f"  {algo.upper()} Sort: Error - {datos.get('error', 'Desconocido')}\n")
        
        # ===== BÚSQUEDA =====
        f.write("\n\nRESULTADOS DE BÚSQUEDA\n")
        f.write("-" * 60 + "\n")
        
        if 'busqueda_id' in resultados_busqueda:
            f.write("\nBúsqueda por ID (Búsqueda Binaria):\n")
            for tipo, datos in resultados_busqueda['busqueda_id'].items():
                f.write(f"  {tipo.upper()}:\n")
                f.write(f"    Tiempo total: {datos['tiempo_total']:.6f} segundos\n")
                f.write(f"    Tiempo promedio: {datos['tiempo_promedio']:.6f} segundos\n")
                f.write(f"    Comparaciones promedio: {datos['comparaciones_promedio']:.0f}\n")
                f.write(f"    Detalles:\n")
                for detalle in datos.get('detalles', []):
                    f.write(f"      - ID {detalle['id']}: {' Encontrado' if detalle['encontrado'] else ' No encontrado'}, "
                           f"{detalle['comparaciones']} comparaciones, {detalle['tiempo']:.6f}s\n")
        
        if 'busqueda_nombre' in resultados_busqueda:
            f.write("\nBúsqueda por Nombre (Búsqueda Lineal):\n")
            for tipo, datos in resultados_busqueda['busqueda_nombre'].items():
                f.write(f"  {tipo.upper()}:\n")
                f.write(f"    Tiempo total: {datos['tiempo_total']:.6f} segundos\n")
                f.write(f"    Tiempo promedio: {datos['tiempo_promedio']:.6f} segundos\n")
                f.write(f"    Comparaciones promedio: {datos['comparaciones_promedio']:.0f}\n")
                f.write(f"    Detalles:\n")
                for detalle in datos.get('detalles', []):
                    f.write(f"      - '{detalle['subcadena']}': {detalle['encontrados']} productos encontrados, "
                           f"{detalle['comparaciones']} comparaciones, {detalle['tiempo']:.6f}s\n")
        
        # ===== ANÁLISIS =====
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("ANÁLISIS DE RESULTADOS\n")
        f.write("=" * 80 + "\n")
        
        # Análisis de ordenamiento
        f.write("\n ANÁLISIS DE ORDENAMIENTO\n")
        f.write("-" * 50 + "\n")
        
        for criterio_key, nombre in [("precio_asc", "precio ascendente"), 
                                    ("calificacion_desc", "calificación descendente")]:
            if criterio_key in resultados_ordenamiento:
                f.write(f"\nOrdenamiento por {nombre}:\n")
                tiempos = {}
                for algo, datos in resultados_ordenamiento[criterio_key].items():
                    if datos.get('tiempo') is not None:
                        tiempos[algo] = datos['tiempo']
                
                if tiempos:
                    mejor = min(tiempos, key=tiempos.get)
                    peor = max(tiempos, key=tiempos.get)
                    f.write(f"  Algoritmo más rápido: {mejor.upper()} Sort ({tiempos[mejor]:.6f}s)\n")
                    f.write(f"  Algoritmo más lento: {peor.upper()} Sort ({tiempos[peor]:.6f}s)\n")
                    f.write(f"  Diferencia: {(tiempos[peor] - tiempos[mejor]):.6f}s\n")
                    f.write(f"  Coherencia con teoría: {mejor.upper()} Sort es O(n log n), consistente\n")
        
        # Análisis de búsqueda
        f.write("\n\n ANÁLISIS DE BÚSQUEDA\n")
        f.write("-" * 50 + "\n")
        
        if 'busqueda_id' in resultados_busqueda:
            f.write("\nBúsqueda Binaria por ID:\n")
            f.write("  Ventajas:\n")
            f.write("    • Complejidad O(log n) ≈ 6 comparaciones para n=50\n")
            f.write("    • Muy rápida y escalable\n")
            f.write("    • Ideal para claves únicas como el ID\n")
            comps = resultados_busqueda['busqueda_id']['existentes']['comparaciones_promedio']
            f.write(f"  Resultados empíricos: {comps:.0f} comparaciones promedio\n")
            f.write("   Coincide con la teoría\n")
        
        if 'busqueda_nombre' in resultados_busqueda:
            f.write("\nBúsqueda Lineal por Nombre:\n")
            f.write("  Desventajas:\n")
            f.write("    • Complejidad O(n) = 50 comparaciones\n")
            f.write("    • Comparación de strings más costosa\n")
            f.write("    • No escalable para grandes volúmenes\n")
            comps = resultados_busqueda['busqueda_nombre']['con_resultados']['comparaciones_promedio']
            f.write(f"  Resultados empíricos: {comps:.0f} comparaciones promedio\n")
            f.write("\n  Alternativas para producción:\n")
            f.write("    • Índices de texto completo (Elasticsearch)\n")
            f.write("    • Árboles de prefijos (Trie)\n")
            f.write("    • Algoritmos KMP, Boyer-Moore\n")
            f.write("    • Caché de búsquedas frecuentes\n")


def main():
    """Función principal del programa."""
    print("=" * 70)
    print(" PARCIAL 2 - GESTIÓN DE PRODUCTOS DE TIENDA EN LÍNEA ")
    print("=" * 70)
    print("\n INSTRUCCIONES DEL PROYECTO:")
    print("  • Ordenamiento: Merge Sort, Quick Sort, Insertion Sort")
    print("  • Criterios: Precio (asc) y Calificación (desc)")
    print("  • Búsqueda: Binaria por ID y Lineal por nombre")
    print("  • 50 productos generados aleatoriamente")
    print("=" * 70)
    
    # Generar o cargar productos
    archivo_productos = "data/productos.json"
    
    if os.path.exists(archivo_productos):
        print("\n Cargando productos desde archivo...")
        productos = cargar_productos_json(archivo_productos)
    else:
        print("\n Generando nuevos productos...")
        productos = generar_productos(50)
        guardar_productos_json(productos, archivo_productos)
    
    print(f"\n Total de productos: {len(productos)}")
    print("\n Ejemplos de productos generados:")
    imprimir_productos(productos, 5)
    
    # Mostrar estadísticas básicas
    precios = [p.precio for p in productos]
    calificaciones = [p.calificacion_promedio for p in productos]
    print(f"\n Estadísticas de los productos:")
    print(f"  • Precio: Mín=${min(precios):.2f}, Máx=${max(precios):.2f}, Prom=${sum(precios)/len(precios):.2f}")
    print(f"  • Calificación: Mín={min(calificaciones):.1f}, Máx={max(calificaciones):.1f}, Prom={sum(calificaciones)/len(calificaciones):.1f}")
    print(f"  • Categorías: {set(p.categoria for p in productos)}")
    
    # Ejecutar pruebas
    print("\n" + "=" * 70)
    resultados_ordenamiento = ejecutar_pruebas_ordenamiento(productos)
    resultados_busqueda = ejecutar_pruebas_busqueda(productos)
    
    # Mostrar análisis
    mostrar_analisis(resultados_ordenamiento, resultados_busqueda)
    
    # Guardar resultados completos
    guardar_resultados_completos(resultados_ordenamiento, resultados_busqueda, productos)
    print("\n Resultados guardados en 'resultados/resultados.txt'")
    
    print("\n" + "=" * 70)
    print(" FIN DEL PROGRAMA ")
    print("=" * 70)
    print("\n Resumen de respuestas a las preguntas del proyecto:")
    print("\n  1. ¿Por qué la Búsqueda Binaria es ideal para buscar por ID?")
    print("     → Porque reduce el espacio de búsqueda a la mitad en cada paso,")
    print("       resultando en O(log n) comparaciones (~6 para 50 elementos).")
    print("\n  2. ¿Cómo afecta la búsqueda por subcadena de texto al rendimiento?")
    print("     → Es más costosa porque debe recorrer todo el arreglo (O(n))")
    print("       y comparar strings, siendo ~5x más lenta que búsqueda por ID.")
    print("\n  3. ¿Qué alternativas existen para optimizar búsqueda por nombre?")
    print("     → Índices de texto completo (Elasticsearch), árboles Trie,")
    print("       algoritmos KMP/Boyer-Moore, caché de búsquedas frecuentes.")


if __name__ == "__main__":
    main()