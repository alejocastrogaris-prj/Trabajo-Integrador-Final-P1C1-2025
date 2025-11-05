#!/usr/bin/env python3
# gestion_paises.py
# TPI - Gestión de Datos de Países
# Uso: python3 gestion_paises.py

import csv
import sys

CSV_ENCODING = 'utf-8'

# ---------- Lectura y validación ----------
def leer_csv(ruta):
    """
    Lee el CSV y devuelve una lista de diccionarios válidos.
    Valida la presencia de columnas y tipos (int) para poblacion/superficie.
    """
    paises = []
    try:
        with open(ruta, newline='', encoding=CSV_ENCODING) as f:
            reader = csv.DictReader(f)
            # Validar columnas
            esperadas = {'nombre', 'poblacion', 'superficie', 'continente'}
            if not esperadas.issubset(set(reader.fieldnames or [])):
                raise ValueError(f"CSV inválido. Debe contener columnas: {esperadas}")
            for i, row in enumerate(reader, start=2):
                try:
                    nombre = row['nombre'].strip()
                    poblacion = int(row['poblacion'].replace(',', '').strip())
                    superficie = int(row['superficie'].replace(',', '').strip())
                    continente = row['continente'].strip()
                    if not nombre:
                        raise ValueError("Nombre vacío")
                    paises.append({
                        'nombre': nombre,
                        'poblacion': poblacion,
                        'superficie': superficie,
                        'continente': continente
                    })
                except Exception as e:
                    print(f"[Aviso] Línea {i}: registro ignorado por error: {e}")
    except FileNotFoundError:
        print(f"[Error] No se encontró el archivo: {ruta}")
        sys.exit(1)
    except Exception as e:
        print(f"[Error] Al leer CSV: {e}")
        sys.exit(1)
    return paises

# ---------- Búsqueda ----------
def buscar_pais(paises, termino):
    """
    Busca por nombre (coincidencia parcial, case-insensitive).
    Retorna lista de países coincidentes.
    """
    termino = termino.lower()
    return [p for p in paises if termino in p['nombre'].lower()]

# ---------- Filtros ----------
def filtrar_por_continente(paises, continente):
    return [p for p in paises if p['continente'].lower() == continente.lower()]

def filtrar_por_rango_poblacion(paises, min_p, max_p):
    return [p for p in paises if min_p <= p['poblacion'] <= max_p]

def filtrar_por_rango_superficie(paises, min_s, max_s):
    return [p for p in paises if min_s <= p['superficie'] <= max_s]

# ---------- Ordenamientos ----------
def ordenar_paises(paises, clave, descendente=False):
    """
    clave: 'nombre' | 'poblacion' | 'superficie'
    """
    if clave not in {'nombre', 'poblacion', 'superficie'}:
        raise ValueError("Clave de ordenamiento inválida")
    return sorted(paises, key=lambda x: x[clave], reverse=descendente)

# ---------- Estadísticas ----------
def estadisticas(paises):
    if not paises:
        return {}
    poblaciones = [p['poblacion'] for p in paises]
    superficies = [p['superficie'] for p in paises]
    mayor_pob = max(paises, key=lambda x: x['poblacion'])
    menor_pob = min(paises, key=lambda x: x['poblacion'])
    promedio_pob = sum(poblaciones) / len(poblaciones)
    promedio_sup = sum(superficies) / len(superficies)
    # conteo por continente
    por_continente = {}
    for p in paises:
        c = p['continente']
        por_continente[c] = por_continente.get(c, 0) + 1
    return {
        'mayor_poblacion': mayor_pob,
        'menor_poblacion': menor_pob,
        'promedio_poblacion': promedio_pob,
        'promedio_superficie': promedio_sup,
        'cantidad_por_continente': por_continente
    }

# ---------- Utilidades de impresión ----------
def imprimir_paises(paises, limite=None):
    if not paises:
        print("No hay países para mostrar.")
        return
    cab = f"{'Nombre':30} {'Poblacion':15} {'Superficie':12} {'Continente'}"
    print(cab)
    print('-' * len(cab))
    for i, p in enumerate(paises):
        if limite and i >= limite:
            print(f"... (mostrando {limite} de {len(paises)})")
            break
        print(f"{p['nombre'][:30]:30} {p['poblacion']:15,d} {p['superficie']:12,d} {p['continente']}")

def imprimir_estadisticas(stats):
    if not stats:
        print("No hay estadísticas (lista vacía).")
        return
    print("País con mayor población:", f"{stats['mayor_poblacion']['nombre']} ({stats['mayor_poblacion']['poblacion']:,})")
    print("País con menor población:", f"{stats['menor_poblacion']['nombre']} ({stats['menor_poblacion']['poblacion']:,})")
    print("Promedio población:", f"{stats['promedio_poblacion']:.2f}")
    print("Promedio superficie:", f"{stats['promedio_superficie']:.2f}")
    print("Cantidad de países por continente:")
    for c, cnt in stats['cantidad_por_continente'].items():
        print(f"  {c}: {cnt}")

# ---------- Menú y validaciones de entrada ----------
def pedir_enter_int(mensaje, minimo=None, maximo=None):
    while True:
        v = input(mensaje).strip()
        try:
            n = int(v)
            if minimo is not None and n < minimo:
                print(f"Valor mínimo {minimo}. Intente nuevamente.")
                continue
            if maximo is not None and n > maximo:
                print(f"Valor máximo {maximo}. Intente nuevamente.")
                continue
            return n
        except ValueError:
            print("Entrada inválida: ingrese un número entero.")

def menu_interactivo(paises):
    while True:
        print("\n--- Menú ---")
        print("1) Buscar país por nombre")
        print("2) Filtrar por continente")
        print("3) Filtrar por rango de población")
        print("4) Filtrar por rango de superficie")
        print("5) Ordenar países")
        print("6) Mostrar estadísticas generales")
        print("7) Mostrar todos los países (resumen)")
        print("0) Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == '1':
            termino = input("Ingrese término de búsqueda (parcial o completo): ").strip()
            res = buscar_pais(paises, termino)
            imprimir_paises(res)
        elif opcion == '2':
            cont = input("Ingrese continente (ej: América, Africa, Asia, Europa, Oceania): ").strip()
            res = filtrar_por_continente(paises, cont)
            imprimir_paises(res)
        elif opcion == '3':
            min_p = pedir_enter_int("Población mínima: ", minimo=0)
            max_p = pedir_enter_int("Población máxima: ", minimo=min_p)
            res = filtrar_por_rango_poblacion(paises, min_p, max_p)
            imprimir_paises(res)
        elif opcion == '4':
            min_s = pedir_enter_int("Superficie mínima (km²): ", minimo=0)
            max_s = pedir_enter_int("Superficie máxima (km²): ", minimo=min_s)
            res = filtrar_por_rango_superficie(paises, min_s, max_s)
            imprimir_paises(res)
        elif opcion == '5':
            print("Ordenar por: 1) nombre 2) poblacion 3) superficie")
            opt = input("Seleccione: ").strip()
            clave = {'1': 'nombre', '2': 'poblacion', '3': 'superficie'}.get(opt)
            if not clave:
                print("Opción inválida.")
                continue
            sentido = input("Ascendente (A) o Descendente (D)? [A/D]: ").strip().lower()
            descendente = (sentido == 'd')
            try:
                res = ordenar_paises(paises, clave, descendente)
                imprimir_paises(res, limite=50)
            except Exception as e:
                print("Error ordenando:", e)
        elif opcion == '6':
            stats = estadisticas(paises)
            imprimir_estadisticas(stats)
        elif opcion == '7':
            imprimir_paises(paises, limite=200)
        elif opcion == '0':
            print("Saliendo. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

# ---------- Punto de entrada ----------
def main():
    ruta = input("Ruta del CSV (por defecto 'paises.csv'): ").strip() or 'paises.csv'
    paises = leer_csv(ruta)
    if not paises:
        print("Lista de países vacía después de leer el CSV. Corrija el archivo y vuelva a intentar.")
        sys.exit(0)
    print(f"Se cargaron {len(paises)} países.")
    menu_interactivo(paises)

if __name__ == '__main__':
    main()
