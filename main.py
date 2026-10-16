
from datetime import datetime


def es_positivo(numero):
    return numero > 0


def validar_movimiento(tipo, monto):
    if es_positivo(monto):
        return True
    else:
        print(f"Error: el {tipo} debe ser mayor que cero.")
        return False


ingresos = 0.0
gastos = 0.0

# Recuperar los movimientos guardados
try:
    with open("movimientos.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()

            if not linea:
                continue

            movimiento = linea.split("|")[0]

            if movimiento.startswith("Ingreso: "):
                monto = float(movimiento.split(": ")[1])
                ingresos += monto

            elif movimiento.startswith("Gasto: "):
                gasto = float(movimiento.split(": ")[1])
                gastos += gasto

except FileNotFoundError:
    pass


# Menú principal
while True:
    print("===============================")
    print(" GESTOR DE GASTOS PERSONALES")
    print("===============================")
    print("1. Registrar ingreso")
    print("2. Registrar gasto")
    print("3. Consultar saldo")
    print("4. Ver historial de movimientos")
    print("5. Resumen mensual")
    print("6. Salir")

    opcion = input("Selecciona una opción del menú: ")

    # Registrar ingreso
    if opcion == "1":
        try:
            monto = float(input("¿Cuánto dinero recibiste? "))

            if validar_movimiento("ingreso", monto):
                with open(
                    "movimientos.txt", "a", encoding="utf-8"
                ) as archivo:
                    fecha = datetime.now().strftime("%Y-%m-%d")
                    archivo.write(
                        f"Ingreso: {monto}|Fecha: {fecha}\n"
                    )

                ingresos += monto
                print("Ingreso registrado correctamente.")

        except ValueError:
            print("Error: debes escribir un número válido.")

    # Registrar gasto
    elif opcion == "2":
        try:
            gasto = float(input("¿Cuánto dinero gastaste? "))

            if validar_movimiento("gasto", gasto):
                print("\nSelecciona una categoría:")
                print("1. Alimentación")
                print("2. Transporte")
                print("3. Servicios")
                print("4. Otros")

                categoria_opcion = input(
                    "Elige una categoría (1-4): "
                ).strip()

                categorias = {
                    "1": "Alimentación",
                    "2": "Transporte",
                    "3": "Servicios",
                    "4": "Otros"
                }

                if categoria_opcion not in categorias:
                    print("Error: categoría no válida.")
                else:
                    categoria = categorias[categoria_opcion]

                    with open(
                        "movimientos.txt", "a", encoding="utf-8"
                    ) as archivo:
                        fecha = datetime.now().strftime("%Y-%m-%d")
                        archivo.write(
                            f"Gasto: {gasto}|Categoría: {categoria}|Fecha: {fecha}\n"
                        )

                    gastos += gasto
                    print("Gasto registrado correctamente.")
                    print("Categoría:", categoria)
                    print(f"Valor: ${gasto:,.0f}")

        except ValueError:
            print("Error: debes escribir un número válido.")

    # Consultar saldo
    elif opcion == "3":
        saldo = ingresos - gastos

        print(f"Total de ingresos: ${ingresos:,.0f}")
        print(f"Total de gastos: ${gastos:,.0f}")
        print(f"Tu saldo actual es: ${saldo:,.0f}")

    # Ver historial de movimientos
    elif opcion == "4":
        try:
            with open(
                "movimientos.txt", "r", encoding="utf-8"
            ) as archivo:
                print("\n--- HISTORIAL DE MOVIMIENTOS ---")

                numero = 1

                for linea in archivo:
                    linea = linea.strip()

                    if not linea:
                        continue

                    partes = linea.split("|")
                    movimiento = partes[0]

                    if movimiento.startswith("Ingreso: "):
                        monto = float(movimiento.split(": ")[1])

                        print(
                            f"{numero}. INGRESO: +${monto:,.0f}"
                        )

                    elif movimiento.startswith("Gasto: "):
                        gasto = float(movimiento.split(": ")[1])

                        if len(partes) > 1 and partes[1].startswith(
                            "Categoría: "
                        ):
                            categoria = partes[1].replace(
                                "Categoría: ", ""
                            )
                        else:
                            categoria = (
                                "Sin categoría (registro anterior)"
                            )

                        print(
                            f"{numero}. GASTO: -${gasto:,.0f}"
                            f" | Categoría: {categoria}"
                        )

                    numero += 1

        except FileNotFoundError:
            print("Todavía no hay movimientos registrados.")

    # Resumen mensual
    elif opcion == "5":
        mes_consultado = input(
            "Escribe el mes que quieres consultar (AAAA-MM): "
        ).strip()

        try:
            fecha_mes = datetime.strptime(
                mes_consultado, "%Y-%m"
            )

            # Comprobar que el mes tenga exactamente el formato AAAA-MM
            if fecha_mes.strftime("%Y-%m") != mes_consultado:
                raise ValueError

        except ValueError:
            print(
                "Error: escribe un mes válido, por ejemplo 2026-10."
            )
            continue

        ingresos_mes = 0.0
        gastos_mes = 0.0

        try:
            with open(
                "movimientos.txt", "r", encoding="utf-8"
            ) as archivo:
                for linea in archivo:
                    linea = linea.strip()

                    if not linea:
                        continue

                    partes = linea.split("|")
                    movimiento = partes[0]
                    fecha_movimiento = None

                    for parte in partes[1:]:
                        if parte.startswith("Fecha: "):
                            fecha_movimiento = parte.replace(
                                "Fecha: ", ""
                            )
                            break

                    if fecha_movimiento is None:
                        continue

                    if not fecha_movimiento.startswith(
                        mes_consultado
                    ):
                        continue

                    if movimiento.startswith("Ingreso: "):
                        monto = float(movimiento.split(": ")[1])
                        ingresos_mes += monto

                    elif movimiento.startswith("Gasto: "):
                        gasto = float(movimiento.split(": ")[1])
                        gastos_mes += gasto

            print(f"\n--- RESUMEN DE {mes_consultado} ---")
            print(
                f"Total de ingresos: ${ingresos_mes:,.0f}"
            )
            print(
                f"Total de gastos: ${gastos_mes:,.0f}"
            )
            print(
                f"Balance mensual: "
                f"${ingresos_mes - gastos_mes:,.0f}"
            )

        except FileNotFoundError:
            print("Todavía no hay movimientos registrados.")

    # Salir
    elif opcion == "6":
        print("Gracias por utilizar el programa.")
        break

    else:
        print("Opción no válida. Intenta nuevamente.")

    print()
