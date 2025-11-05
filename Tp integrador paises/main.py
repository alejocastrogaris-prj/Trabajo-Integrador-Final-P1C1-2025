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
# Menú principal
# -----------------

def menu():
    print("""
==========================
SISTEMA DE DATOS DE PAÍSES
==========================
1. Ver lista completa de países
2. Buscar país por nombre
3. Filtrar por continente
4. Filtrar por rango de población
5. Filtrar por rango de superficie
6. Ordenar países
7. Mostrar estadísticas
8. Salir
""")


def main():
    archivo = "paises.csv"  # Nombre del archivo CSV
    paises = cargar_datos_csv(archivo)

    if not paises:
        print("No se cargaron datos. Verifique el archivo CSV.")
        return

    while True:
        menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            mostrar_paises_bonito(paises)

        elif opcion == "2":
            termino = input("Ingrese nombre o una parte del nombre del país: ")
            resultados = buscar_pais(paises, termino)
            mostrar_paises_bonito(resultados)

        elif opcion == "3":
            cont = input("Ingrese el continente: ")
            resultados = filtrar_por_continente(paises, cont)
            mostrar_paises_bonito(resultados)

        elif opcion == "4":
            try:
                min_p = int(input("Población mínima: "))
                max_p = int(input("Población máxima: "))
                resultados = filtrar_por_poblacion(paises, min_p, max_p)
                mostrar_paises_bonito(resultados)
            except ValueError:
                print("Error: ingrese valores válidos.\n")

        elif opcion == "5":
            try:
                min_s = float(input("Superficie mínima: "))
                max_s = float(input("Superficie máxima: "))
                resultados = filtrar_por_superficie(paises, min_s, max_s)
                mostrar_paises_bonito(resultados)
            except ValueError:
                print("Error: ingrese valores válidos.\n")

        elif opcion == "6":
            print("\nOpciones de ordenamiento:")
            print("1. Nombre")
            print("2. Población")
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
                print("Opción inválida.\n")
                continue

            resultados = ordenar_paises(paises, clave, descendente)
            mostrar_paises_bonito(resultados)

        elif opcion == "7":
            mostrar_estadisticas(paises)

        elif opcion == "8":
            print("Saliendo del sistema.")
            break

        else:
            print("Opción inválida. Intente de nuevo.\n")


if __name__ == "__main__":
    main()
