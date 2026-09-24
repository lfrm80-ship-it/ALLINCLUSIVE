import sqlite3

# Nombre fijo para tu archivo de base de datos en tu carpeta de trabajo
DB_NAME = "aimbridge_actividades.db"


def conectar():
  return sqlite3.connect(DB_NAME, check_same_thread=False)


def inicializar_bd():
  conexion = conectar()
  cursor = conexion.cursor()
  # Creamos una tabla general para guardar las actividades/promociones
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS actividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            propiedad TEXT,
            categoria TEXT,
            fecha TEXT,
            responsable TEXT,
            descripcion TEXT
        )
    """)
  conexion.commit()
  conexion.close()


def crear_promocion(
    titulo, propiedad, categoria, fecha, responsable, descripcion
):
  conexion = conectar()
  cursor = conexion.cursor()
  cursor.execute(
      """
        INSERT INTO actividades (titulo, propiedad, categoria, fecha, responsable, descripcion)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
      (titulo, propiedad, categoria, fecha, responsable, descripcion),
  )
  conexion.commit()
  conexion.close()


def obtener_promociones():
  conexion = conectar()
  cursor = conexion.cursor()
  cursor.execute("SELECT * FROM actividades ORDER BY id DESC")
  filas = cursor.fetchall()
  conexion.close()

  # Convertimos los resultados a una lista de diccionarios para que Streamlit los lea fácil
  lista_resultado = []
  for fila in filas:
    lista_resultado.append({
        "id": fila[0],
        "titulo": fila[1],
        "propiedad": fila[2],
        "categoria": fila[3],
        "fecha": fila[4],
        "responsable": fila[5],
        "descripcion": fila[6],
    })
  return lista_resultado
