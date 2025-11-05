import os
import csv
import utilidades
from collections import Counter

def lectura_recursiva(ruta_base):
    lista_items = []

    for elemento in os.listdir(ruta_base):
        ruta_completa = os.path.join(ruta_base, elemento)

        if os.path.isdir(ruta_completa):
            # Si es carpeta, hacer llamada recursiva
            lista_items.extend(lectura_recursiva(ruta_completa))

        elif elemento.endswith(".csv"):
            # Si es .csv, leer
            with open(ruta_completa, newline='', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    partes = ruta_completa.split(os.sep)
                    if len(partes) >= 5:  # datos / fabricante / familia / generación / modelos.csv
                        fila["fabricante"] = partes[-4]
                        fila["familia"] = partes[-3]
                        fila["generacion"] = partes[-2]
                        
                    fila["origen"] = ruta_completa

                    lista_items.append(fila) # Añadir items del .csv a lista global de items

    return lista_items

def agregar_item():
    fabricante = utilidades.normalizar_texto(input("Fabricante: "))
    familia = utilidades.normalizar_texto(input("Familia: "))
    generacion = utilidades.normalizar_texto(input("Generacion: "))

    ruta_directorio = os.path.join("datos", fabricante, familia, generacion)
    os.makedirs(ruta_directorio, exist_ok=True) # Crear elementos de la ruta que no existan y dejar/usar los que si existan

    ruta_csv = os.path.join(ruta_directorio, "modelos.csv")

    print("\n==========\n")
    modelo = input("Modelo: ")
    variante = input("Variante: ")
    motor = input("Motor: ")

    if not modelo or not variante or not motor:
        print("\nInválido - todos los campos son obligatorios.")
        return
    
    archivo_nuevo = not os.path.exists(ruta_csv) # Bool para ver si existe o no el archivo csv

    with open(ruta_csv, 'a', newline='', encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["modelo", "variante", "motor"])

        if archivo_nuevo:
            escritor.writeheader() # Si es archivo nuevo, escribir cabecera

        escritor.writerow({
            "modelo": modelo,
            "variante": variante,
            "motor": motor
        })

    print("\nAñadido con éxito.\n")

def mostrar_items_totales():
    total_items = lectura_recursiva("datos")

    if not total_items:
        print("No hay items para mostrar.\n")
        return
    
    for i in total_items:
        print(i)

def mostrar_filtrar_por_fabricante(fabricante_filtrar):
    total_items = lectura_recursiva("datos")

    total_items.sort(key=lambda x: (x.get("fabricante", ""), x.get("familia", ""), x.get("modelo", "")))
    items = [i for i in total_items if i.get("fabricante", "").lower() == fabricante_filtrar]

    fabricante_actual = None
    familia_actual = None

    print("=== LISTADO DE ÍTEMS ===\n")

    for item in items:
        fab = item.get("fabricante", "Desconocido")
        gen = item.get("generacion", "-")
        fam = item.get("familia", "-")

        modelo = item.get("modelo", "-")
        variante = item.get("variante", "-")
        motor = item.get("motor", "-")

        if fab != fabricante_actual:
            print(f"--- Fabricante: {fab} ---")
            fabricante_actual = fab
            familia_actual = None
            generacion_actual = None

        if fam != familia_actual:
            print(f"\n   > Familia: {fam}")
            familia_actual = fam
            generacion_actual = None

        if gen != generacion_actual:
            print(f"   > Generación: {gen}")
            generacion_actual = gen

        print(f"      - Modelo: {modelo}, Variante: {variante}, Motor: {motor}")

    print("\n=== FIN DE LISTADO ===\n")

def menu_mostrar_filtrar_items():
    print(f"  |1| Mostrar items totales ordenados")
    print(f"  |2| Mostrar items filtrados por fabricante\n")

    opt = input("Opción: ")

    match opt:
        case '1':
            print()
            mostrar_items_totales()
        case '2':
            print()
            fabricante_filtrar = input("Fabricante a filtrar: ")
            print()
            mostrar_filtrar_por_fabricante(fabricante_filtrar)
        case _:
            print("\nOpción inválida.\n")

def modificar_item():
    # Leer todos los ítems existentes
    total_items = lectura_recursiva("datos")

    if not total_items:
        print("No hay ítems registrados.")
        return

    # Mostrar un listado para ayudar al usuario a elegir
    print("\n=== ÍTEMS DISPONIBLES ===\n")
    for i, item in enumerate(total_items, start=1):
        print(f"|{i}| {item.get("fabricante", '')} | {item.get("familia", '')} | {item.get("modelo", '')} | {item.get("variante", '')} | {item.get("motor", '')}")

    # Pedir al usuario el número del ítem a modificar
    try:
        indice = int(input("\nNúmero del ítem a modificar: ")) - 1
        if indice < 0 or indice >= len(total_items):
            print("Número inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    item = total_items[indice]

    print("\nÍtem seleccionado:")
    for k, v in item.items():
        print(f"  {k}: {v}")

    # Pedir el campo a modificar
    campo = input("\nCampo a modificar (modelo, variante, motor): ").strip().lower()
    if campo not in ["modelo", "variante", "motor"]:
        print("Campo no válido.")
        return

    nuevo_valor = input(f"Nuevo valor para '{campo}': ").strip()

    # Actualizar el valor en memoria
    item[campo] = nuevo_valor

    # Determinar el archivo CSV correspondiente
    fabricante = item.get("fabricante", "")
    familia = item.get("familia", "")
    generacion = item.get("generacion", "")
    archivo_csv = os.path.join("datos", fabricante, familia, generacion, f"{familia.lower()}.csv")

    if not os.path.exists(archivo_csv):
        print("No se encontró el archivo CSV original. No se guardaron los cambios.")
        return

    # Leer todos los registros del CSV y modificar el que corresponde
    registros = []
    with open(archivo_csv, newline='', encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila.get("modelo") == item.get("modelo"):
                fila[campo] = nuevo_valor
            registros.append(fila)

    # Reescribir el CSV con los cambios
    with open(archivo_csv, 'w', newline='', encoding="utf-8") as archivo:
        campos = registros[0].keys()
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)

    print("\nÍtem modificado con éxito.\n")

def eliminar_item():
    # Leer todos los ítems existentes
    total_items = lectura_recursiva("datos")

    if not total_items:
        print("No hay ítems registrados.")
        return

    # Mostrar el listado de ítems disponibles
    print("\n=== ÍTEMS DISPONIBLES ===\n")
    for i, item in enumerate(total_items, start=1):
        print(f"|{i}| {item.get("fabricante", '')} | {item.get("familia", '')} | {item.get("modelo", '')} | {item.get("variante", '')} | {item.get("motor", '')}")

    # Pedir el número del ítem a eliminar
    try:
        indice = int(input("\nNúmero del ítem a eliminar: ")) - 1
        if indice < 0 or indice >= len(total_items):
            print("Número inválido.")
            return
    except ValueError:
        print("Inválido - la entrada debe ser un número.")
        return

    item = total_items[indice]

    print("\nÍtem seleccionado:")
    for k, v in item.items():
        print(f"  {k}: {v}")

    # Confirmar eliminación
    confirmar = input("\n¿Confirma la eliminación? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Operación cancelada.")
        return

    # Determinar el archivo CSV correspondiente
    fabricante = item.get("fabricante", "")
    familia = item.get("familia", "")
    generacion = item.get("generacion", "")
    archivo_csv = os.path.join("datos", fabricante, familia, generacion, f"{familia.lower()}.csv")

    if not os.path.exists(archivo_csv):
        print("No se encontró el archivo CSV original. No se realizaron cambios.")
        return

    # Leer todas las filas y conservar solo las que no coinciden con el ítem
    registros = []
    with open(archivo_csv, 'r', newline='', encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila.get("modelo") != item.get("modelo"):
                registros.append(fila)

    # Reescribir el archivo CSV sin el ítem eliminado
    if registros:
        with open(archivo_csv, 'w', newline='', encoding="utf-8") as archivo:
            campos = registros[0].keys()
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(registros)
    else:
        os.remove(archivo_csv)
        print("El archivo quedó vacío y fue eliminado.")

    print("\nÍtem eliminado con éxito.\n")

def mostrar_ordenar_por_fabricante():

    total_items = lectura_recursiva("datos")

    if not total_items:
        print("No hay ítems registrados.")
        return

    # Ordenar por fabricante, familia, generación y modelo
    total_items.sort(key=lambda x: (x.get("fabricante", ""), x.get("familia", ""), x.get("generacion", ""), x.get("modelo", "")))

    fabricante_actual = None

    print("=== ÍTEMS ORDENADOS POR FABRICANTE ===\n")

    for item in total_items:
        fab = item.get("fabricante", "-")
        fam = item.get("familia", "-")
        gen = item.get("generacion", "-")
        modelo = item.get("modelo", "-")
        variante = item.get("variante", "-")
        motor = item.get("motor", "-")

        if fab != fabricante_actual:
            print(f"\n--- Fabricante: {fab} ---")
            fabricante_actual = fab

        print(f"   {fam} ({gen}) - {modelo} | Variante: {variante} | Motor: {motor}")

    print("\n=== FIN DE LISTADO ===\n")

def mostrar_ordenar_por_motor():
    # Leer todos los ítems existentes
    total_items = lectura_recursiva("datos")

    if not total_items:
        print("No hay ítems registrados.")
        return

    # Ordenar por motor
    total_items.sort(key=lambda x: x.get("motor", ""))

    print("=== ÍTEMS ORDENADOS POR MOTOR ===\n")

    motor_actual = None
    for item in total_items:
        motor = item.get("motor", "—")
        fabricante = item.get("fabricante", "—")
        familia = item.get("familia", "—")
        generacion = item.get("generacion", "-")
        modelo = item.get("modelo", "—")

        if motor != motor_actual:
            print(f"\n--- Motor: {motor} ---")
            motor_actual = motor

        print(f"   {fabricante} | {familia} | {generacion} | {modelo}")

    print("\n=== FIN DE LISTADO ===\n")

def mostrar_estadisticas():
    total_items = lectura_recursiva("datos")

    if not total_items:
        print("No hay ítems registrados.")
        return

    # Contar ítems por fabricante
    conteo = Counter(item.get("fabricante", "") for item in total_items)

    print("\n=== CANTIDAD DE ÍTEMS POR FABRICANTE ===\n")
    for fabricante, cantidad in conteo.items():
        print(f"{fabricante}: {cantidad}")

    print(f"\nTotal general: {len(total_items)} ítems\n")

def menu_mostrar_ordenar_items():
    print(f"  |1| Mostrar items totales ordenados por fabricante")
    print(f"  |2| Mostrar items totales ordenados por motor")
    print(f"  |3| Mostrar estadísticas\n")

    opt = input("Opción: ")

    match opt:
        case '1':
            print()
            mostrar_ordenar_por_fabricante()
        case '2':
            print()
            mostrar_ordenar_por_motor()
        case '3':
            print()
            mostrar_estadisticas()
        case _:
            print("\nOpción inválida.\n")