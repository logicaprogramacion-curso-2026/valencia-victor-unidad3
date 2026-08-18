"""
Script auxiliar SOLO para generar datos de demostracion
(no forma parte del programa de consola, sirve para poblar
ventas.csv con al menos 10 ventas y probar el resto de funciones).
"""
import random
from datetime import datetime, timedelta

import minitienda as mt

random.seed(7)

ventas_demo = [
    (1, 2), (2, 5), (3, 12), (4, 1), (5, 1),
    (6, 3), (2, 15), (1, 1), (4, 2), (3, 4),
    (6, 10), (5, 2),
]

fecha_base = datetime(2026, 8, 10, 9, 0, 0)

for i, (pid, cant) in enumerate(ventas_demo):
    producto = mt.buscar_producto(pid)
    if producto is None:
        continue
    if cant > mt.STOCK.get(pid, 0):
        cant = mt.STOCK.get(pid, 1)
    precio_unitario = mt.PRECIOS[pid]
    subtotal = precio_unitario * cant
    descuento = mt.calcular_descuento(cant, subtotal)
    total = round(subtotal - descuento, 2)
    mt.STOCK[pid] -= cant

    venta = {
        "id_venta": len(mt.VENTAS_BUFFER) + 1,
        "fecha": (fecha_base + timedelta(hours=i * 3)).strftime("%Y-%m-%d %H:%M:%S"),
        "producto_id": pid,
        "producto": producto[1],
        "cantidad": cant,
        "precio_unitario": precio_unitario,
        "descuento": descuento,
        "total": total,
    }
    mt.VENTAS_BUFFER.append(venta)
    mt.IDS_VENDIDOS.append(pid)
    mt.escribir_log(f"VENTA OK (demo): producto_id={pid}, cantidad={cant}, total={total}")

# Reto D: simular un intento fallido con producto_id inexistente
mt.escribir_log("INTENTO FALLIDO: producto_id=99 no existe en el catalogo.")
print(" Intento fallido simulado: producto_id=99 no existe en el catalogo.")

mt.guardar_ventas_csv()
mt.calcular_metricas()
mt.graficar_ingresos(guardar_png=True)

print("\nCatalogo final:")
mt.mostrar_catalogo()
