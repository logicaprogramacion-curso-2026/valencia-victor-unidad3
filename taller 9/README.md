# 📚 Sistema de Preguntas y Respuestas - Proyecto Taller 9

## 👥 Integrantes del Grupo
- Rafael Cambera

## 📅 Fechas
- Inicio: 27/07/2026
- Entrega: 27/07/2026

## 📝 Descripción del Proyecto
Aplicación en Python que gestiona un banco de 50 preguntas de selección múltiple
sobre programación en Python. Permite cargar preguntas desde archivos TXT, CSV y
JSON, almacenarlas de forma persistente en una base de datos SQLite, exportarlas
de vuelta a los tres formatos, y ejecutar un simulador de evaluación que selecciona
preguntas al azar, valida respuestas, calcula el puntaje y genera reportes en
TXT, CSV y JSON.

## 🛠️ Tecnologías Utilizadas
- Python 3.8+
- SQLite3 (módulo estándar `sqlite3`)
- Git

## 📁 Estructura del Proyecto
```
taller9-banco_preguntas/
├── preguntas.txt
├── preguntas.csv
├── preguntas.json
├── src/
│   ├── __init__.py
│   ├── entidad.py
│   ├── dao.py
│   ├── gestor.py
│   ├── simulador.py
│   └── main.py
├── database/
│   └── preguntas.db
├── resultados/
│   ├── respuestas_usuario.txt
│   ├── estadisticas.csv
│   └── reporte.json
├── tests/
│   ├── __init__.py
│   ├── test_entidad.py
│   └── test_dao.py
├── requirements.txt
└── README.md
```

---

## 📊 Evidencias de Ejecución por Iteración

### Iteración 1: Configuración Inicial
- ✅ Estructura de carpetas creada (`src/`, `database/`, `resultados/`, `tests/`)
- ✅ Clase `Pregunta` implementada en `entidad.py` con `__init__`, `__str__`, `to_dict`

### Iteración 2: Creación de Archivos de Preguntas
- ✅ preguntas.txt (50 preguntas)
- ✅ preguntas.csv (50 preguntas)
- ✅ preguntas.json (50 preguntas)

Muestra (pregunta 1, igual en los tres formatos):
```
ID: 1 | Tema: Operadores Aritméticos | Dificultad: Fácil
¿Cuál es la salida de print(5 // 2)?
A) 2.5  B) 2  C) 3  D) 2.0
Respuesta correcta: B
```

### Iteración 3: DAO y Base de Datos
- ✅ Tabla `preguntas` creada en `database/preguntas.db`
- ✅ Conexión exitosa vía `sqlite3`
- ✅ Métodos CRUD implementados: `crear_tabla`, `insertar`, `insertar_muchas`,
  `obtener_todas`, `obtener_por_id`, `obtener_por_tema`, `obtener_por_dificultad`,
  `actualizar`, `eliminar`, `contar_preguntas`, `estadisticas_por_tema`,
  `estadisticas_por_dificultad`

### Iteración 4: Carga de Datos desde Archivos
Resultado real de ejecución:
```
TXT: 50 preguntas cargadas
CSV: 50 preguntas cargadas
JSON: 50 preguntas cargadas
```

### Iteración 5: Guardado en Base de Datos y Exportación
```
Guardadas en BD: 50
Conteo DAO: 50
Por tema: {'Listas': 9, 'Strings': 7, 'Funciones Built-in': 7, 'Operadores Aritméticos': 6,
'Tipos de Datos': 4, 'Conversión de Tipos': 3, 'Bucles': 2, ... (19 temas en total)}
Por dificultad: {'Fácil': 31, 'Media': 19}
Exportado OK -> resultados_exportados.txt / .csv / .json
```

### Iteración 6: Simulador de Evaluación
- ✅ Selección aleatoria de preguntas (`random.sample`)
- ✅ Presentación interactiva por consola
- ✅ Validación de respuestas (`Pregunta.es_correcta`)
- ✅ Cálculo de puntaje

Ejemplo de ejecución (simulación de 10 preguntas):
```
Pregunta 1/10 - [Strings | Fácil] ¿Qué operador se usa para concatenar strings?
...
Puntaje: 3 / 10
```

### Iteración 7: Generación de Reportes
- ✅ `resultados/respuestas_usuario.txt` generado
- ✅ `resultados/estadisticas.csv` generado
- ✅ `resultados/reporte.json` generado

Cada reporte incluye: fecha y hora, preguntas mostradas, respuesta del usuario,
respuesta correcta, puntaje total, y estadísticas agrupadas por tema y por
dificultad.

### Iteración 8: Integración Final y Pruebas
- ✅ Pruebas unitarias en `tests/test_entidad.py` y `tests/test_dao.py`
- ✅ Menú completo en `main.py` (cargar, ver preguntas, estadísticas, simular,
  exportar, ver reportes, salir)
- ✅ Manejo de errores con `try/except` en el menú principal
- ✅ Flujo completo verificado: TXT/CSV/JSON → BD → Simulación → Reportes

---

## ▶️ Cómo ejecutar
```bash
python3 src/main.py
```

## 🧪 Pruebas Realizadas
```bash
python3 -m unittest discover tests
```
Se probó la creación de objetos `Pregunta`, su conversión a diccionario, y las
operaciones CRUD del DAO (crear tabla, insertar, consultar, actualizar, eliminar,
contar y estadísticas), todo contra una base de datos SQLite temporal.

## 📊 Estadísticas Finales
- Total preguntas: 50
- Temas cubiertos: 19
- Dificultades: Fácil (31), Media (19)
- Formatos soportados: TXT, CSV, JSON (carga y exportación en ambos sentidos)

## 🎯 Conclusiones
El proyecto integra manejo de archivos, persistencia con SQLite y una capa de
simulación interactiva en una arquitectura simple por capas (entidad, DAO,
gestor, simulador), lo que facilita el mantenimiento y la extensión del banco
de preguntas.

## 🔮 Mejoras Futuras
- Interfaz gráfica (Tkinter o web) en lugar de menú por consola
- Autenticación de usuarios y control de intentos
- Historial de simulaciones por usuario con ranking
