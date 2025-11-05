import funciones

print("=== MENÚ ===")
print("|1| Agregar item")
print("|2| Mostrar todos los items")
print("|3| Mostrar items filtrados")
print("|4| Modificar item")
print("|5| Eliminar item")
print("|6| Mostrar items ordenados")
print("|7| Salir\n")

opt = input("Opción: ")
print()

match opt:
    case '1':
        funciones.agregar_item()
    case '2':
        funciones.mostrar_items_totales()
    case '3':
        funciones.menu_mostrar_filtrar_items()
    case '4':
        funciones.modificar_item()
    case '5':
        funciones.eliminar_item()
    case '6':
        funciones.menu_mostrar_ordenar_items()
    case '7':
        print("Saliendo...")
    case _:
        print("Opción inválida.")