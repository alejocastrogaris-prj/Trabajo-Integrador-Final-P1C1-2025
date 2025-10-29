import csv

#---------------------------------------------------------------------
# Funciones auxiliares

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

#---------------------------------------------------------------------------
# Funciones de búsqueda y filtrado

def buscar_pais(lista_de_paises, texto_buscado):
    """Busca países cuyo nombre contenga el texto indicado (parcial o completo)."""

    # Convertimos el texto ingresado a minúsculas para que la búsqueda no distinga mayúsculas
    texto_buscado = texto_buscado.lower()

    # Creamos una nueva lista con los países cuyo nombre contiene el texto buscado
    resultados = [
        pais for pais in lista_de_paises
        if texto_buscado in pais["nombre"].lower()
    ] 

    # Devolvemos la lista de coincidencias
    return resultados