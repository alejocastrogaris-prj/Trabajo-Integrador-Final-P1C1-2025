import csv

# ===============================
# Funciones auxiliares
# ===============================

def cargar_datos_csv(nombre_archivo):
    """Carga los datos de países desde un archivo CSV y los valida."""
    paises = []
    try:
        with open(nombre_archivo, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                try:
                    nombre = fila["nombre"].strip()
                    continente = fila["continente"].strip()
                    poblacion = int(fila["poblacion"])
                    superficie = float(fila["superficie"])

                    paises.append({
                        "nombre": nombre,
                        "continente": continente,
                        "poblacion": poblacion,
                        "superficie": superficie
                    })
                except (ValueError, KeyError):
                    print(f"Error en formato de fila: {fila}")
    except FileNotFoundError:
        print("Error: el archivo no fue encontrado.")
    return paises


# ===============================
# Funciones de búsqueda y filtrado
# ===============================

def buscar_pais(paises, termino):
    """Busca países cuyo nombre contenga el término dado."""
    termino = termino.lower()
    return [p for p in paises if termino in p["nombre"].lower()]


def filtrar_por_continente(paises, continente):
    """Filtra países por continente."""
    return [p for p in paises if p["continente"].lower() == continente.lower()]


def filtrar_por_poblacion(paises, min_pob, max_pob):
    """Filtra países dentro de un rango de población."""
    return [p for p in paises if min_pob <= p["poblacion"] <= max_pob]


def filtrar_por_superficie(paises, min_sup, max_sup):
    """Filtra países dentro de un rango de superficie."""
    return [p for p in paises if min_sup <= p["superficie"] <= max_sup]


# ------------------
# Funciones de ordenamiento
# --------------------

def ordenar_paises(paises, clave, descendente=False):
    """Ordena los países según la clave elegida (nombre, población o superficie)."""
    return sorted(paises, key=lambda x: x[clave], reverse=descendente)


# --------------
# Funciones estadísticas
# -----------------

def mostrar_estadisticas(paises):
    """Calcula y muestra estadísticas básicas sobre el conjunto de países."""
    if not paises:
        print("No hay datos para calcular estadísticas.")
        return

    pais_mayor_pob = max(paises, key=lambda x: x["poblacion"])
    pais_menor_pob = min(paises, key=lambda x: x["poblacion"])
    promedio_pob = sum(p["poblacion"] for p in paises) / len(paises)
    promedio_sup = sum(p["superficie"] for p in paises) / len(paises)

    # Conteo por continente
    conteo_continentes = {}
    for p in paises:
        cont = p["continente"]
        conteo_continentes[cont] = conteo_continentes.get(cont, 0) + 1

    print("\n📊 ESTADÍSTICAS:")
    print(f"- País con mayor población: {pais_mayor_pob['nombre']} ({pais_mayor_pob['poblacion']:,} hab.)")
    print(f"- País con menor población: {pais_menor_pob['nombre']} ({pais_menor_pob['poblacion']:,} hab.)")
    print(f"- Promedio de población: {promedio_pob:,.0f}")
    print(f"- Promedio de superficie: {promedio_sup:,.2f} km²")
    print("- Cantidad de países por continente:")
    for cont, cant in conteo_continentes.items():
        print(f"   {cont}: {cant} países")
    print()


# ===============================
# Función para mostrar países en tabla
# ===============================

def mostrar_paises_bonito(lista):
    """Muestra los países en formato tabular y alineado."""
    if not lista:
        print("No se encontraron resultados.\n")
        return

    # Encabezado
    print("\n" + "="*75)
    print(f"{'NOMBRE':25} | {'CONTINENTE':15} | {'POBLACIÓN':>12} | {'SUPERFICIE (km²)':>15}")
    print("-"*75)

    # Filas
    for p in lista:
        nombre = p["nombre"]
        cont = p["continente"]
        pob = f"{p['poblacion']:,}".replace(",", ".")
        sup = f"{p['superficie']:,}".replace(",", ".")
        print(f"{nombre:25} | {cont:15} | {pob:>12} | {sup:>15}")

    print("="*75 + "\n")
