import csv

# ===============================
# Funciones auxiliares
# ===============================

def cargar_datos_csv(archivo):
    """Carga los datos de paises desde un archivo CSV y los valida."""
    paises = []
    try:
        with open(archivo, newline="", encoding="utf-8") as archivo_cargado:
            lector = csv.DictReader(archivo_cargado)
            for fila in lector:
                try:
                    nombre = fila["nombre"].strip()
                    continente = fila["continente"].strip()
                    
                    # Limpiar separadores de miles (punto o coma) antes de convertir a numero
                    poblacion_str = fila["poblacion"].strip().replace('.', '').replace(',', '')
                    superficie_str = fila["superficie"].strip().replace('.', '').replace(',', '')
                    
                    poblacion = int(poblacion_str)
                    superficie = float(superficie_str)

                    paises.append({
                        "nombre": nombre,
                        "continente": continente,
                        "poblacion": poblacion,
                        "superficie": superficie
                    })
                except (ValueError, KeyError) as e:
                    print(f"Error en formato/clave de fila: {fila} | Detalle: {e}")
    except FileNotFoundError:
        print(f"Error: el archivo '{archivo}' no fue encontrado.")
    return paises


# ===============================
# Funciones de busqueda y filtrado
# ===============================

def buscar_pais(paises, termino):
    """Busca paises cuyo nombre contenga el termino dado."""
    termino = termino.lower()
    return [p for p in paises if termino in p["nombre"].lower()]


def filtrar_por_continente(paises, continente):
    """Filtra paises por continente."""
    return [p for p in paises if p["continente"].lower() == continente.lower()]


def filtrar_por_poblacion(paises, min_pob, max_pob):
    """Filtra paises dentro de un rango de poblacion."""
    return [p for p in paises if min_pob <= p["poblacion"] <= max_pob]


def filtrar_por_superficie(paises, min_sup, max_sup):
    """Filtra paises dentro de un rango de superficie."""
    return [p for p in paises if min_sup <= p["superficie"] <= max_sup]


# ------------------
# Funciones de ordenamiento
# --------------------

def ordenar_paises(paises, clave, descendente=False):
    """Ordena los paises segun la clave elegida (nombre, poblacion o superficie)."""
    return sorted(paises, key=lambda x: x[clave], reverse=descendente)


# --------------
# Funciones estadisticas
# -----------------

def mostrar_estadisticas(paises):
    """Calcula y muestra estadisticas basicas sobre el conjunto de paises."""
    if not paises:
        print("No hay datos para calcular estadisticas.")
        return

    # Calculo de promedios
    pob_total = sum(p["poblacion"] for p in paises)
    promedio_pob = pob_total / len(paises)
    promedio_sup = sum(p["superficie"] for p in paises) / len(paises)

    # Maximo y minimo
    pais_mayor_pob = max(paises, key=lambda x: x["poblacion"])
    pais_menor_pob = min(paises, key=lambda x: x["poblacion"])
    
    # Conteo por continente
    conteo_continentes = {}
    for p in paises:
        cont = p["continente"]
        conteo_continentes[cont] = conteo_continentes.get(cont, 0) + 1

    print("\n ESTADISTICAS:")
    print(f"- Pais con mayor poblacion: {pais_mayor_pob['nombre']} ({pais_mayor_pob['poblacion']:,.0f} hab.)")
    print(f"- Pais con menor poblacion: {pais_menor_pob['nombre']} ({pais_menor_pob['poblacion']:,.0f} hab.)")
    print(f"- Promedio de poblacion: {promedio_pob:,.0f}")
    print(f"- Promedio de superficie: {promedio_sup:,.2f} km²")
    print("- Cantidad de paises por continente:")
    for cont, cant in conteo_continentes.items():
        print(f"   {cont}: {cant} paises")
    print()


# ===============================
# Funcion para mostrar paises en tabla
# ===============================

def mostrar_paises_bonito(lista, titulo="RESULTADOS"):
    """Muestra los paises en formato tabular y alineado."""
    if not lista:
        print(f"No se encontraron resultados para: {titulo}\n")
        return

    # Calculo de anchos dinamicos para la tabla
    max_nombre = max(len(p["nombre"]) for p in lista) if lista else 25
    max_cont = max(len(p["continente"]) for p in lista) if lista else 15
    largo_nombre = max(25, max_nombre + 2)
    largo_cont = max(15, max_cont + 2)
    ancho_total = largo_nombre + largo_cont + 12 + 15 + 6

    print(f"\n {titulo.upper()} (Total: {len(lista)} paises) ")
    print("=" * ancho_total)
    print(f"{'NOMBRE':<{largo_nombre}} | {'CONTINENTE':<{largo_cont}} | {'POBLACION':>12} | {'SUPERFICIE (km²)':>15}")
    print("-" * ancho_total)

    for p in lista:
        nombre = p["nombre"]
        cont = p["continente"]
        
        # Formateo de numeros
        pob = f"{p['poblacion']:,.0f}".replace(",", "_TEMP_").replace(".", ",").replace("_TEMP_", ".")
        sup = f"{p['superficie']:,.2f}".replace(",", "_TEMP_").replace(".", ",").replace("_TEMP_", ".")

        print(f"{nombre:<{largo_nombre}} | {cont:<{largo_cont}} | {pob:>12} | {sup:>15}")

    print("=" * ancho_total + "\n")