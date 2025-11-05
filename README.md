# Sistema de Gestión de Ítems Jerárquico

## Descripción general
El programa implementa un sistema de gestión de datos basado en una **estructura de archivos jerárquica**.
Permite registrar, consultar, modificar, eliminar y analizar información almacenada en archivos **CSV** organizados en carpetas según distintos niveles de clasificación.

El objetivo es manejar una colección de ítems (por ejemplo, **modelos de aviones**) clasificados por **fabricante**, **familia** y **generación**, respetando la estructura de directorios definida.

Todas las operaciones se realizan desde un **menú principal** que actúa como interfaz para las funciones implementadas en el módulo `funciones.py`.

---

## Estructura del programa

### Archivos principales
- `main.py`: Contiene el menú principal y las llamadas a las funciones principales.
- `funciones.py`: Contiene todas las funciones lógicas que implementan las operaciones del sistema.

### Menú principal
El programa inicia con un menú de texto que permite acceder a todas las funciones del sistema:

```python
print("=== MENÚ ===")
print("|1| Agregar item")
print("|2| Mostrar todos los items")
print("|3| Mostrar items filtrados")
print("|4| Modificar item")
print("|5| Eliminar item")
print("|6| Mostrar items ordenados")
print("|7| Salir\n")
```

Cada opción llama a una función definida en `funciones.py`.
El menú se mantiene en ejecución hasta que el usuario elige la opción **7** para salir.

---

## Funciones principales (definidas en `funciones.py`)

### 1. `lectura_recursiva(ruta_base)`
Recorre de forma recursiva la estructura de directorios a partir de la ruta base (`datos/`).
Lee todos los archivos `.csv` encontrados y devuelve una lista de diccionarios, donde cada diccionario representa una fila de un archivo.
A cada ítem se le agregan campos derivados de su ubicación: **fabricante**, **familia**, **generación** y **origen**.

### 2. `agregar_item()`
Solicita al usuario los datos de un nuevo ítem (fabricante, familia, generación, modelo, variante y motor).
Crea automáticamente los directorios necesarios dentro de `datos/` y guarda el nuevo registro en un archivo CSV dentro de la ubicación correspondiente.
Si el archivo no existe, lo crea e incluye los encabezados.

### 3. `mostrar_items_totales()`
Muestra todos los ítems leídos recursivamente sin aplicar filtros ni ordenamientos.

### 4. `mostrar_filtrar_por_fabricante(fabricante_filtrar)`
Muestra únicamente los ítems que pertenecen al fabricante especificado.

### 5. `menu_mostrar_filtrar_items()`
Submenú que permite:
- Mostrar todos los ítems.
- Mostrar ítems filtrados por fabricante.

### 6. `modificar_item()`
Permite seleccionar un ítem existente y modificar uno de sus campos.
Actualiza el archivo CSV correspondiente, manteniendo su formato.

### 7. `eliminar_item()`
Permite seleccionar un ítem y eliminarlo. Si el archivo queda vacío, se elimina.

### 8. `mostrar_ordenar_por_fabricante()`
Muestra todos los ítems agrupados y ordenados por **fabricante**, **familia** y **modelo**.

### 9. `mostrar_ordenar_por_motor()`
Ordena y muestra los ítems agrupados por tipo de motor.

### 10. `mostrar_estadisticas()`
Calcula y muestra estadísticas simples, principalmente el total de ítems por fabricante.

### 11. `menu_mostrar_ordenar_items()`
Submenú que agrupa funciones de visualización y ordenamiento:
- Mostrar ítems ordenados por fabricante.
- Mostrar ítems ordenados por motor.
- Mostrar estadísticas de ítems.

---

## Estructura de datos y organización de archivos

La estructura de almacenamiento elegida se basa en el dominio de los **aviones comerciales**, organizada de forma jerárquica para reflejar su clasificación real.

- **Fabricante:** empresa que produce los aviones (ej. Airbus, Boeing).  
- **Familia:** grupo de modelos (ej. A320, A330, 737).  
- **Generación:** versión o evolución tecnológica (ej. CEO, NEO, NG, MAX).  

Cada carpeta de **generación** contiene un archivo `modelos.csv` con la información de los modelos correspondientes.

Ejemplo de contenido:

```csv
modelo,variante,motor
A320,200,CFM56
A320neo,200,LEAP-1A
```

En este ejemplo, ambos modelos pertenecen a la familia A320 de Airbus, pero uno corresponde a la generación **CEO** y el otro a la **NEO**.

Esta estructura permite leer, modificar y organizar los datos de manera recursiva, manteniendo una relación clara entre **fabricante**, **familia**, **generación** y **modelo**.

---

## Flujo general del programa

1. El usuario ejecuta `main.py`.
2. El menú principal muestra las opciones disponibles.
3. Según la elección, se llama a la función correspondiente de `funciones.py`.
4. Las operaciones se realizan directamente sobre los archivos CSV dentro de `datos/`.
5. Los resultados se muestran en pantalla con formato textual claro.

---

## Requisitos técnicos

- Python **3.8 o superior**
- No requiere librerías externas
- Todas las operaciones de entrada/salida usan codificación **UTF-8**