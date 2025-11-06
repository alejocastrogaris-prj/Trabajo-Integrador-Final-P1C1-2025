from funciones_paises import (
    cargar_datos_csv,
    mostrar_paises_bonito,
    buscar_pais,
    filtrar_por_continente,
    filtrar_por_poblacion,
    filtrar_por_superficie,
    ordenar_paises,
    mostrar_estadisticas
)

# ----------------
# Menu principal
# -----------------

def menu():
    """Muestra las opciones del TPI solicitadas."""
    print("\n" + "="*40)
    print(" SISTEMA DE DATOS DE PAISES")
    print("="*40)
    print("1. Ver lista completa de paises")
    print("2. Buscar pais por nombre") # [cite: 99]
    print("3. Filtrar por continente") # [cite: 102]
    print("4. Filtrar por rango de poblacion") # [cite: 103]
    print("5. Filtrar por rango de superficie") # [cite: 104]
    print("6. Ordenar paises") # [cite: 105]
    print("7. Mostrar estadisticas") # [cite: 109]
    print("0. Salir")
    print("="*40)


def main():
    """Funcion principal del sistema."""
    archivo = "paises.csv"  # Nombre del archivo CSV
    paises = cargar_datos_csv(archivo) # Lista principal (diccionarios)

    if not paises:
        print("No se cargaron datos. Verifique el archivo CSV.")
        return

    while True:
        menu()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            mostrar_paises_bonito(paises, titulo="LISTA COMPLETA DE PAISES")

        elif opcion == "2":
            termino = input("Ingrese nombre o una parte del nombre del pais: ")
            resultados = buscar_pais(paises, termino) 
            mostrar_paises_bonito(resultados, titulo=f"BUSQUEDA: '{termino}'")

        elif opcion == "3":
            cont = input("Ingrese el continente: ")
            resultados = filtrar_por_continente(paises, cont) 
            mostrar_paises_bonito(resultados, titulo=f"FILTRO POR CONTINENTE: {cont}")

        elif opcion == "4":
            try:
                min_p = int(input("Poblacion minima: "))
                max_p = int(input("Poblacion maxima: "))
                # Validacion de entrada a entero
                resultados = filtrar_por_poblacion(paises, min_p, max_p)
                mostrar_paises_bonito(resultados, titulo=f"FILTRO POR POBLACION: {min_p:,} a {max_p:,}")
            except ValueError:
                print(" Error: ingrese valores enteros validos.\n")

        elif opcion == "5":
            try:
                min_s = float(input("Superficie minima (km²): "))
                max_s = float(input("Superficie maxima (km²): "))
                # Validacion de entrada a float
                resultados = filtrar_por_superficie(paises, min_s, max_s)
                mostrar_paises_bonito(resultados, titulo=f"FILTRO POR SUPERFICIE: {min_s:,.0f} a {max_s:,.0f} km²")
            except ValueError:
                print("❌ Error: ingrese valores numericos validos.\n")

        elif opcion == "6":
            print("\nOpciones de ordenamiento:")
            print("1. Nombre")
            print("2. Poblacion")
            print("3. Superficie")
            clave_op = input("Seleccione una clave: ")
            descendente = input("¿Desea ordenar de forma descendente? (s/n): ").lower() == "s"

            if clave_op == "1":
                clave = "nombre"
            elif clave_op == "2":
                clave = "poblacion"
            elif clave_op == "3":
                clave = "superficie"
            else:
                print("❌ Opcion invalida. Intente de nuevo.\n")
                continue

            resultados = ordenar_paises(paises, clave, descendente)
            mostrar_paises_bonito(resultados, titulo=f"ORDENADO por {clave.upper()} (Desc: {descendente})")

        elif opcion == "7":
            mostrar_estadisticas(paises)

        elif opcion == "0":
            print(" Saliendo del sistema.")
            break

        else:
            print(" Opcion invalida. Intente de nuevo.\n")


if __name__ == "__main__":
    main()