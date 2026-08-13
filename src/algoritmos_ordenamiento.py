import time
from typing import List, Callable, Any
from producto import Producto

def medir_tiempo(func):
    """
    Decorador para medir el tiempo de ejecución de una función.
    """
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        return resultado, fin - inicio
    return wrapper

def merge_sort(arr: List[Any], key_func: Callable[[Any], Any], reverse: bool = False) -> List[Any]:
    """
    Implementación del algoritmo Merge Sort.

    """
    if len(arr) <= 1:
        return arr.copy()
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key_func, reverse)
    right = merge_sort(arr[mid:], key_func, reverse)
    
    return _merge(left, right, key_func, reverse)

def _merge(left: List[Any], right: List[Any], key_func: Callable[[Any], Any], reverse: bool) -> List[Any]:
    """Función auxiliar para fusionar dos listas ordenadas."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        left_key = key_func(left[i])
        right_key = key_func(right[j])
        
        if reverse:
            condition = left_key >= right_key
        else:
            condition = left_key <= right_key
        
        if condition:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

@medir_tiempo
def merge_sort_wrapper(arr: List[Producto], key_func: Callable[[Producto], Any], reverse: bool = False) -> List[Producto]:
    """Wrapper para medir el tiempo de Merge Sort."""
    return merge_sort(arr, key_func, reverse)

def quick_sort(arr: List[Any], key_func: Callable[[Any], Any], reverse: bool = False) -> List[Any]:
    """
    Implementación del algoritmo Quick Sort con pivote mediana de tres.

    """
    if len(arr) <= 1:
        return arr.copy()
    
    # Mejorar la selección del pivote con mediana de tres
    if len(arr) >= 3:
        first = key_func(arr[0])
        mid = key_func(arr[len(arr)//2])
        last = key_func(arr[-1])
        # Elegir la mediana como pivote
        if (first <= mid <= last) or (last <= mid <= first):
            pivot_idx = len(arr)//2
        elif (mid <= first <= last) or (last <= first <= mid):
            pivot_idx = 0
        else:
            pivot_idx = -1
        # Intercambiar pivote con el primer elemento
        arr[0], arr[pivot_idx] = arr[pivot_idx], arr[0]
    
    pivot_key = key_func(arr[0])
    left = []
    right = []
    equal = [arr[0]]
    
    for item in arr[1:]:
        item_key = key_func(item)
        if reverse:
            if item_key > pivot_key:
                left.append(item)
            elif item_key < pivot_key:
                right.append(item)
            else:
                equal.append(item)
        else:
            if item_key < pivot_key:
                left.append(item)
            elif item_key > pivot_key:
                right.append(item)
            else:
                equal.append(item)
    
    left_sorted = quick_sort(left, key_func, reverse)
    right_sorted = quick_sort(right, key_func, reverse)
    
    return left_sorted + equal + right_sorted

@medir_tiempo
def quick_sort_wrapper(arr: List[Producto], key_func: Callable[[Producto], Any], reverse: bool = False) -> List[Producto]:
    """Wrapper para medir el tiempo de Quick Sort."""
    return quick_sort(arr, key_func, reverse)

def insertion_sort(arr: List[Any], key_func: Callable[[Any], Any], reverse: bool = False) -> List[Any]:
    """
    Implementación del algoritmo Insertion Sort.

    """
    result = arr.copy()
    n = len(result)
    
    for i in range(1, n):
        key_item = result[i]
        key_value = key_func(key_item)
        j = i - 1
        
        while j >= 0:
            current_key = key_func(result[j])
            if reverse:
                condition = current_key < key_value
            else:
                condition = current_key > key_value
            
            if condition:
                result[j + 1] = result[j]
                j -= 1
            else:
                break
        
        result[j + 1] = key_item
    
    return result

@medir_tiempo
def insertion_sort_wrapper(arr: List[Producto], key_func: Callable[[Producto], Any], reverse: bool = False) -> List[Producto]:
    """Wrapper para medir el tiempo de Insertion Sort."""
    return insertion_sort(arr, key_func, reverse)

def ordenar_por_precio_ascendente(productos: List[Producto], algoritmo: str = "merge") -> tuple:
    """
    Ordena productos por precio ascendente (más barato primero).

    """
    key_func = lambda p: p.precio
    
    if algoritmo == "merge":
        return merge_sort_wrapper(productos, key_func, reverse=False)
    elif algoritmo == "quick":
        return quick_sort_wrapper(productos, key_func, reverse=False)
    elif algoritmo == "insertion":
        return insertion_sort_wrapper(productos, key_func, reverse=False)
    else:
        raise ValueError(f"Algoritmo '{algoritmo}' no reconocido")

def ordenar_por_calificacion_descendente(productos: List[Producto], algoritmo: str = "merge") -> tuple:
    """
    Ordena productos por calificación promedio descendente (mejor calificado primero).
    
    """
    key_func = lambda p: p.calificacion_promedio
    
    if algoritmo == "merge":
        return merge_sort_wrapper(productos, key_func, reverse=True)
    elif algoritmo == "quick":
        return quick_sort_wrapper(productos, key_func, reverse=True)
    elif algoritmo == "insertion":
        return insertion_sort_wrapper(productos, key_func, reverse=True)
    else:
        raise ValueError(f"Algoritmo '{algoritmo}' no reconocido")