import math

def leer_float(mensaje):
    """Lee un número flotante con validación."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor <= 0:
                print("El valor debe ser mayor que 0.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Introduce un número válido.")


def calcular_palos():
    print("=== CÁLCULO DE PALOS PARA NÚCLEO ===")
    print("Unidad de medida: mm\n")

    # Entradas con validación
    w = leer_float("Tamaño de la Hoja (w): ")
    v = leer_float("Tamaño de la Ventana (v): ")
    l = leer_float("Largo de la Pierna (l): ")
    
    # Valor inicial del ruler
    r = 350
    print(f"\nEl tamaño del ruler es {r} mm")
    op = input("¿Desea Mantener (m) o Cambiar (c)? ").lower()

    if op == "c":
        r = leer_float("Nuevo valor del ruler (r): ")
    
    # Valor inicial del cs
    tmcs = 2750
    print(f"\nEl tamaño del cs es {tmcs} mm")
    op = input("¿Desea Mantener (m) o Cambiar (c)? ").lower()

    if op == "c":
        tmcs = leer_float("Nuevo valor del cs (tmcs): ")

    # Cantidades base
    cand_csjp = (w / r) * 3
    cand_csjv = (v / r) * 2

    # Redondeo hacia arriba
    cand_csjp = math.ceil(cand_csjp)
    cand_csjv = math.ceil(cand_csjv)

    print("\n=== PROCESANDO ===")

    # CASO 1
    if tmcs == l:
        size_csjv = w
        size_csjp = 0

        caven = tmcs / size_csjv
        tp_csjv = math.ceil(cand_csjv / caven)

        tp_entero_py = cand_csjp + cand_csjv

        print("\n--- RESULTADOS ---")
        print(f"Palos para ventana: {cand_csjv} (tamaño {size_csjv} mm)")
        print(f"Palos a cortar para ventana: {tp_csjv}")
        print("Palos para yugo: 0 (tamaño original)")
        print(f"Palos enteros necesarios: {tp_entero_py}")

    # CASO 2
    elif ((l - w) + r) == tmcs:
        size_csjv = w
        size_csjp = w

        caven = tmcs / size_csjv
        tp_csjv = math.ceil(cand_csjv / caven)
        tp_csjp = math.ceil(cand_csjp / caven)

        tp_entero_py = cand_csjp + cand_csjv

        print("\n--- RESULTADOS ---")
        print(f"Palos para ventana: {cand_csjv} (tamaño {size_csjv} mm)")
        print(f"Palos a cortar para ventana: {tp_csjv}")

        print(f"Palos para yugo: {cand_csjp} (tamaño {size_csjp} mm)")
        print(f"Palos a cortar para yugo: {tp_csjp}")

        print(f"Palos enteros necesarios: {tp_entero_py}")

    # CASO 3
    elif ((l - w) + r) > tmcs:
        size_csjv = w
        size_csjp = l - (tmcs + r)

        if size_csjp <= 0:
            print("\nError: el tamaño calculado para el yugo es inválido.")
            return

        caven = tmcs / size_csjv
        tp_csjv = math.ceil(cand_csjv / caven)

        caven2 = tmcs / size_csjp
        tp_csjp = math.ceil(cand_csjp / caven2)

        tp_entero_py = cand_csjp + cand_csjv

        print("\n--- RESULTADOS ---")
        print(f"Palos para ventana: {cand_csjv} (tamaño {size_csjv} mm)")
        print(f"Palos a cortar para ventana: {tp_csjv}")

        print(f"Palos para yugo: {cand_csjp} (tamaño {size_csjp} mm)")
        print(f"Palos a cortar para yugo: {tp_csjp}")

        print(f"Palos enteros necesarios: {tp_entero_py}")

    else:
        print("\nNo se cumple ninguna condición del algoritmo original.")


if __name__ == "__main__":
    calcular_palos()