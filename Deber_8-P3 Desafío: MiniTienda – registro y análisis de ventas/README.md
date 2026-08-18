# MiniTienda – Registro y análisis de ventas

**Grupo 1:** Victor Valencia, Johan Loor, Rafael Cambera
**Curso:** Logica de Programacion — UIDE

## Descripción

Programa de consola en Python que administra un catálogo de productos, registra
ventas, calcula métricas y genera un gráfico de ingresos por producto.

- **Tuplas:** catálogo de productos (`id`, `nombre`, `categoría`).
- **Diccionarios:** precios (`PRECIOS`) y stock (`STOCK`) por id de producto.
- **Listas:** buffer de ventas de la sesión (`VENTAS_BUFFER`) e ids vendidos (`IDS_VENDIDOS`).
- **Pandas:** `DataFrame`, `groupby` y lectura/escritura de `ventas.csv`.
- **NumPy:** `mean`, `std`, `sum`, `max`, `min` sobre los totales de venta.
- **Matplotlib:** gráfico de barras de ingresos por producto (`ingresos.png`).
- **Menú:** bucle `while` con control de flujo completo (`if/elif/else`, `for`,
  `try/except/else/finally`, `break`, `continue`).

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `minitienda.py` | Programa principal (menú interactivo de consola). |
| `generar_demo.py` | Script auxiliar que registra 12 ventas de prueba sin necesidad de `input()`. |
| `MiniTienda.ipynb` | Notebook (Jupyter/Colab) con el código ejecutable y celdas de prueba. |
| `ventas.csv` | CSV generado con 12 ventas de demostración. |
| `log.txt` | Bitácora de eventos (ventas exitosas e intentos fallidos). |
| `ingresos.png` | Captura del gráfico de ingresos por producto. |
| `evidencia_MiniTienda.pdf` | Documento con evidencia de ejecución y explicación del algoritmo. |
| `README.md` | Este archivo. |

## Cómo ejecutar

```bash
python3 minitienda.py
```

El menú disponible es:

1. Ver catálogo
2. Registrar venta
3. Guardar ventas en CSV
4. Ver ventas y métricas (NumPy)
5. Graficar ingresos por producto
6. Exportar gráfico a PNG (Reto B)
7. Agregar producto nuevo (Reto A)
8. Actualizar precio/stock de un producto (Reto A)
0. Salir (guarda automáticamente antes de cerrar)

Para regenerar los datos de demostración sin usar el menú interactivo:

```bash
python3 generar_demo.py
```

## Retos implementados

- **Reto A:** opciones 7 y 8 del menú permiten agregar un producto nuevo al
  catálogo (`agregar_producto()`) y actualizar precio/stock de uno existente
  (`actualizar_precio_stock()`).
- **Reto B:** opción 6 del menú exporta el gráfico de ingresos con
  `plt.savefig("ingresos.png")`.
- **Reto C:** `calcular_descuento()` aplica automáticamente un 5% de descuento
  cuando la cantidad vendida es mayor o igual a 10 unidades.
- **Reto D:** si se intenta vender un `producto_id` que no está en el catálogo,
  además de rechazar la venta, se escribe el intento fallido en `log.txt`.

## Respuestas

**¿Qué parte la hizo Pandas? ¿Qué parte NumPy?**
Pandas construye el `DataFrame` de ventas, lee y escribe `ventas.csv`
(`pd.read_csv` / `to_csv`) y agrupa los ingresos por producto con
`groupby("producto")["total"].sum()`. NumPy se usa en `calcular_metricas()`
para convertir la columna `total` en un arreglo y calcular `sum`, `mean`,
`std`, `max` y `min`.

**¿Dónde usaste try/except y por qué?**
En `registrar_venta()` para validar que el ID y la cantidad sean números
enteros; en `leer_ventas_csv()` para controlar que `ventas.csv` no exista
todavía (`FileNotFoundError`); en `guardar_ventas_csv()` para capturar
errores al escribir el archivo; en el cálculo del precio promedio por unidad
para controlar una posible `ZeroDivisionError`; y en el menú principal,
para que un error inesperado no cierre el programa.

**¿Qué estructuras son tuplas, listas y diccionarios en el código?**
- *Tuplas:* cada producto del catálogo `(id, nombre, categoria)`.
- *Listas:* `CATALOGO` (lista de tuplas), `VENTAS_BUFFER` (lista de
  diccionarios) e `IDS_VENDIDOS` (lista/arreglo de ids vendidos).
- *Diccionarios:* `PRECIOS` (id → precio) y `STOCK` (id → stock disponible).

## Entregables

1. `MiniTienda.ipynb` — código ejecutable con celdas de prueba (Jupyter/Colab).
2. `evidencia_MiniTienda.pdf` — evidencia de ejecución (entradas/salidas),
   explicación del algoritmo y capturas de cumplimiento por requisito.
3. `README.md` — este documento.
4. `ventas.csv` con 12 ventas registradas.
5. `ingresos.png` — captura del gráfico de ingresos por producto.
