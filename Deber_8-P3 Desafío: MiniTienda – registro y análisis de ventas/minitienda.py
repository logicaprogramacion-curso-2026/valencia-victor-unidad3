"""
MiniTienda - Registro y análisis de ventas
Grupo 1 - Valencia, Loor, Cambera
Logica de Programacion - UIDE

Programa de consola que:
 1. Mantiene un catalogo (tuplas), precios/stock (diccionarios)
 2. Registra ventas (listas + pandas DataFrame)
 3. Guarda/lee datos desde un CSV (archivos)
 4. Calcula metricas con NumPy
 5. Grafica ingresos por producto con Matplotlib
 6. Tiene un menu con bucle while y control de flujo completo
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend sin pantalla, apto para consola/servidor
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# 1) CATALOGO (tuplas) + PRECIOS / STOCK (diccionarios)
# ----------------------------------------------------------------------
# Cada producto del catalogo es una TUPLA (id, nombre, categoria).
# El catalogo en si es una lista para poder agregar productos nuevos
# (Reto A), pero cada registro individual sigue siendo una tupla.
CATALOGO = [
    (1, "Laptop", "Electronica"),
    (2, "Mouse", "Electronica"),
    (3, "Teclado", "Electronica"),
    (4, "Monitor", "Electronica"),
    (5, "Silla Gamer", "Muebles"),
    (6, "Audifonos", "Electronica"),
]

# Diccionarios: precio y stock por id de producto
PRECIOS = {
    1: 850.00,
    2: 15.50,
    3: 25.00,
    4: 199.99,
    5: 120.00,
    6: 45.00,
}

STOCK = {
    1: 10,
    2: 50,
    3: 40,
    4: 15,
    5: 8,
    6: 25,
}

# ----------------------------------------------------------------------
# 2) LISTAS: buffer de ventas de la sesion + arreglo de IDs vendidos
# ----------------------------------------------------------------------
VENTAS_BUFFER = []   # lista de diccionarios -> luego se convierte en DataFrame
IDS_VENDIDOS = []    # lista/arreglo con los ids de producto vendidos

# ----------------------------------------------------------------------
# Rutas de archivos
# ----------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "ventas.csv")
LOG_PATH = os.path.join(BASE_DIR, "log.txt")
PNG_PATH = os.path.join(BASE_DIR, "ingresos.png")

COLUMNAS_CSV = ["id_venta", "fecha", "producto_id", "producto", "cantidad",
                "precio_unitario", "descuento", "total"]


# ----------------------------------------------------------------------
# FUNCIONES DE APOYO (todo modular)
# ----------------------------------------------------------------------
def escribir_log(mensaje):
    """Escribe una linea con marca de tiempo en log.txt (archivo)."""
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}\n")


def buscar_producto(producto_id):
    """Busca un producto en el catalogo (tuplas). Retorna la tupla o None."""
    for producto in CATALOGO:
        if producto[0] == producto_id:
            return producto
    return None


def mostrar_catalogo():
    print("\n--- CATALOGO DE PRODUCTOS ---")
    print(f"{'ID':<4}{'Nombre':<15}{'Categoria':<15}{'Precio':<10}{'Stock':<6}")
    for producto in CATALOGO:
        pid, nombre, categoria = producto
        precio = PRECIOS.get(pid, 0)
        stock = STOCK.get(pid, 0)
        print(f"{pid:<4}{nombre:<15}{categoria:<15}${precio:<9.2f}{stock:<6}")


def calcular_descuento(cantidad, subtotal):
    """Reto C: si unidades >= 10 se aplica 5% de descuento."""
    if cantidad >= 10:
        return round(subtotal * 0.05, 2)
    return 0.0


def registrar_venta():
    """
    Registra una venta nueva.
    Usa try/except/else/finally para validar entradas del usuario,
    controla producto inexistente (Reto D: se registra en log.txt)
    y controla stock insuficiente.
    """
    mostrar_catalogo()
    try:
        producto_id = int(input("\nIngrese el ID del producto a vender: "))
        cantidad = int(input("Ingrese la cantidad: "))
    except ValueError:
        print(" Entrada invalida: debe ingresar numeros enteros.")
        escribir_log("ERROR: entrada no numerica al registrar venta.")
        return
    except Exception as e:
        print(f" Error inesperado: {e}")
        return
    else:
        producto = buscar_producto(producto_id)

        # Reto D: producto_id que no existe en el catalogo -> log.txt
        if producto is None:
            print(" El producto no existe en el catalogo.")
            escribir_log(f"INTENTO FALLIDO: producto_id={producto_id} no existe en el catalogo.")
            return

        if cantidad <= 0:
            print(" La cantidad debe ser mayor a 0.")
            escribir_log(f"INTENTO FALLIDO: cantidad invalida ({cantidad}) para producto_id={producto_id}.")
            return

        if cantidad > STOCK.get(producto_id, 0):
            print(f" Stock insuficiente. Stock disponible: {STOCK.get(producto_id, 0)}")
            escribir_log(f"INTENTO FALLIDO: stock insuficiente para producto_id={producto_id}, "
                         f"solicitado={cantidad}, disponible={STOCK.get(producto_id, 0)}.")
            return

        try:
            precio_unitario = PRECIOS[producto_id]
            subtotal = precio_unitario * cantidad
            # division por cero controlada (ejemplo: precio promedio por unidad)
            precio_promedio_unidad = subtotal / cantidad if cantidad != 0 else 0
        except ZeroDivisionError:
            print(" Division por cero controlada, se usa 0 como valor por defecto.")
            precio_promedio_unidad = 0
        finally:
            pass  # el bloque finally siempre corre, aqui no se requiere limpieza extra

        descuento = calcular_descuento(cantidad, subtotal)
        total = round(subtotal - descuento, 2)

        # actualizar stock (diccionario)
        STOCK[producto_id] -= cantidad

        venta = {
            "id_venta": len(VENTAS_BUFFER) + 1,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "producto_id": producto_id,
            "producto": producto[1],
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "descuento": descuento,
            "total": total,
        }

        VENTAS_BUFFER.append(venta)     # lista de diccionarios
        IDS_VENDIDOS.append(producto_id)  # lista/arreglo de ids

        print(f" Venta registrada: {cantidad}x {producto[1]} -> Total: ${total:.2f}"
              f"{' (con descuento 5%)' if descuento > 0 else ''}")
        escribir_log(f"VENTA OK: producto_id={producto_id}, cantidad={cantidad}, total={total}")


def guardar_ventas_csv():
    """
    Guarda las ventas del buffer en ventas.csv usando pandas.
    Si el archivo ya existe, agrega (append) las ventas nuevas.
    """
    if not VENTAS_BUFFER:
        print(" No hay ventas nuevas para guardar.")
        return

    df_nuevo = pd.DataFrame(VENTAS_BUFFER, columns=COLUMNAS_CSV)

    try:
        if os.path.exists(CSV_PATH):
            df_existente = pd.read_csv(CSV_PATH)
            # re-numerar id_venta para que sea consecutivo
            df_nuevo["id_venta"] = range(len(df_existente) + 1,
                                          len(df_existente) + 1 + len(df_nuevo))
            df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
        else:
            df_final = df_nuevo

        df_final.to_csv(CSV_PATH, index=False)
        print(f" {len(df_nuevo)} venta(s) guardadas en {CSV_PATH}")
        escribir_log(f"CSV actualizado con {len(df_nuevo)} venta(s) nuevas.")
        VENTAS_BUFFER.clear()
    except Exception as e:
        print(f" Error al guardar el CSV: {e}")
        escribir_log(f"ERROR al guardar CSV: {e}")


def leer_ventas_csv():
    """
    Lee ventas.csv y las muestra. Controla el caso de archivo inexistente.
    """
    try:
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        print(" El archivo ventas.csv no existe todavia. Registre ventas primero.")
        escribir_log("ERROR: intento de leer ventas.csv pero no existe.")
        return None
    else:
        print(f"\n--- VENTAS REGISTRADAS ({len(df)}) ---")
        print(df.to_string(index=False))
        return df
    finally:
        pass


def calcular_metricas():
    """
    Calcula metricas con NumPy: mean, std, sum sobre el arreglo de totales.
    """
    df = leer_ventas_csv()
    if df is None or df.empty:
        print(" No hay datos para calcular metricas.")
        return

    totales = np.array(df["total"])  # arreglo NumPy
    print("\n--- METRICAS (NumPy) ---")
    print(f"Suma total de ingresos : ${np.sum(totales):.2f}")
    print(f"Promedio por venta      : ${np.mean(totales):.2f}")
    print(f"Desviacion estandar     : ${np.std(totales):.2f}")
    print(f"Venta maxima            : ${np.max(totales):.2f}")
    print(f"Venta minima            : ${np.min(totales):.2f}")


def graficar_ingresos(guardar_png=False):
    """
    Agrupa ingresos por producto con pandas (groupby) y grafica con
    matplotlib. Reto B: opcion para exportar a PNG con plt.savefig().
    """
    df = leer_ventas_csv()
    if df is None or df.empty:
        print(" No hay datos para graficar.")
        return

    ingresos_por_producto = df.groupby("producto")["total"].sum().sort_values(ascending=False)

    plt.figure(figsize=(9, 5))
    ingresos_por_producto.plot(kind="bar", color="#4C72B0")
    plt.title("Ingresos por producto - MiniTienda")
    plt.xlabel("Producto")
    plt.ylabel("Ingresos ($)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    if guardar_png:
        plt.savefig(PNG_PATH)
        print(f" Grafico exportado como {PNG_PATH}")
        escribir_log("Grafico de ingresos exportado a PNG.")
    else:
        plt.savefig(PNG_PATH)  # tambien se guarda para poder visualizarlo
        print(" Grafico generado (ver ingresos.png).")

    plt.close()


def agregar_producto():
    """Reto A: agrega un producto nuevo al catalogo y sus precios/stock."""
    try:
        nuevo_id = max(p[0] for p in CATALOGO) + 1
        nombre = input("Nombre del nuevo producto: ").strip()
        categoria = input("Categoria: ").strip()
        precio = float(input("Precio: "))
        stock_inicial = int(input("Stock inicial: "))
    except ValueError:
        print(" Datos invalidos, no se agrego el producto.")
        escribir_log("ERROR: datos invalidos al agregar producto nuevo.")
        return

    CATALOGO.append((nuevo_id, nombre, categoria))  # tupla nueva en la lista
    PRECIOS[nuevo_id] = precio
    STOCK[nuevo_id] = stock_inicial
    print(f" Producto '{nombre}' agregado con ID {nuevo_id}.")
    escribir_log(f"Producto nuevo agregado: id={nuevo_id}, nombre={nombre}, "
                 f"precio={precio}, stock={stock_inicial}")


def actualizar_precio_stock():
    """Permite actualizar precio y/o stock de un producto existente (Reto A)."""
    mostrar_catalogo()
    try:
        producto_id = int(input("\nID del producto a actualizar: "))
    except ValueError:
        print(" ID invalido.")
        return

    producto = buscar_producto(producto_id)
    if producto is None:
        print(" Producto no encontrado.")
        escribir_log(f"INTENTO FALLIDO: actualizar producto inexistente id={producto_id}.")
        return

    try:
        nuevo_precio = input(f"Nuevo precio (enter para mantener {PRECIOS[producto_id]}): ").strip()
        if nuevo_precio:
            PRECIOS[producto_id] = float(nuevo_precio)

        nuevo_stock = input(f"Nuevo stock (enter para mantener {STOCK[producto_id]}): ").strip()
        if nuevo_stock:
            STOCK[producto_id] = int(nuevo_stock)

        print(" Producto actualizado correctamente.")
        escribir_log(f"Producto actualizado: id={producto_id}, "
                      f"precio={PRECIOS[producto_id]}, stock={STOCK[producto_id]}")
    except ValueError:
        print(" Valor invalido, no se actualizo el producto.")
        escribir_log(f"ERROR: valor invalido al actualizar producto id={producto_id}.")


# ----------------------------------------------------------------------
# MENU PRINCIPAL (bucle while + control de flujo completo)
# ----------------------------------------------------------------------
def mostrar_menu():
    print("\n===== MINITIENDA - MENU PRINCIPAL =====")
    print("1) Ver catalogo")
    print("2) Registrar venta")
    print("3) Guardar ventas en CSV")
    print("4) Ver ventas y metricas (NumPy)")
    print("5) Graficar ingresos por producto")
    print("6) Exportar grafico a PNG")
    print("7) Agregar producto nuevo (Reto A)")
    print("8) Actualizar precio/stock de un producto")
    print("0) Salir")


def main():
    intentos_invalidos = 0
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()

        try:
            if opcion == "0":
                print("Guardando datos antes de salir...")
                guardar_ventas_csv()
                print("Hasta luego!")
                break
            elif opcion == "1":
                mostrar_catalogo()
            elif opcion == "2":
                registrar_venta()
            elif opcion == "3":
                guardar_ventas_csv()
            elif opcion == "4":
                calcular_metricas()
            elif opcion == "5":
                graficar_ingresos(guardar_png=False)
            elif opcion == "6":
                graficar_ingresos(guardar_png=True)
            elif opcion == "7":
                agregar_producto()
            elif opcion == "8":
                actualizar_precio_stock()
            else:
                intentos_invalidos += 1
                print(" Opcion invalida, intente de nuevo.")
                if intentos_invalidos >= 3:
                    print(" Demasiados intentos invalidos consecutivos, "
                          "revise las opciones del menu.")
                    intentos_invalidos = 0
                continue
        except KeyboardInterrupt:
            print("\nInterrumpido por el usuario. Guardando y saliendo...")
            guardar_ventas_csv()
            break
        except Exception as e:
            print(f" Error inesperado en el menu: {e}")
            escribir_log(f"ERROR inesperado en el menu: {e}")
            continue
        else:
            intentos_invalidos = 0
        finally:
            pass


if __name__ == "__main__":
    main()
