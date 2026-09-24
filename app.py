import streamlit as st
import db  # Tu módulo de base de datos

st.set_page_config(
    page_title="Gestión Comercial & Actividades - Aimbridge LATAM",
    layout="wide",
)

st.title("🏨 Aimbridge LATAM | Gestión y Operaciones Comerciales")

# Pestañas principales de navegación
pestana_registro, pestana_consulta = st.tabs(
    ["📝 Registrar Actividad / Promoción", "🔍 Consulta General"]
)

# ==========================================
# PESTAÑA 1: REGISTRO DE ACTIVIDADES
# ==========================================
with pestana_registro:
  st.header("Registro de Nuevas Actividades y Promociones")
  st.write(
      "Ingresa los detalles de la promoción o actividad comercial para"
      " almacenarla en el sistema."
  )

  with st.form("form_actividad", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
      titulo = st.text_input("Título de la Actividad o Promoción")
      propiedad = st.selectbox(
          "Propiedad / Resort",
          [
              "Wyndham Alltra Cancun",
              "Wyndham Alltra Playa del Carmen",
              "Aimbridge General",
          ],
      )
      categoria = st.selectbox(
          "Categoría",
          [
              "Promoción Comercial",
              "Tarifas y Restricciones",
              "Operación / Distribución",
              "Estrategia de Ventas",
          ],
      )

    with col2:
      fecha_actividad = st.date_input("Fecha de Aplicación / Registro")
      responsable = st.text_input(
          "Responsable", value="Luis Rodríguez"
      )  # Prellenado con tu nombre o rol

    descripcion = st.text_area("Detalles, Condiciones u Observaciones")

    # Botón de guardado
    enviar = st.form_submit_button(
        "💾 Guardar en la Base de Datos", use_container_width=True
    )

    if enviar:
      if titulo.strip():
        # Aquí llamas a tu función de base de datos (asegúrate de que db.py tenga una función compatible)
        try:
          # Ejemplo de llamada a tu DB:
          db.crear_promocion(
              titulo=titulo,
              propiedad=propiedad,
              categoria=categoria,
              fecha=str(fecha_actividad),
              responsable=responsable,
              descripcion=descripcion,
          )
          st.success(
              f"¡La actividad '{titulo}' se ha guardado y registrado"
              " correctamente!"
          )
        except Exception as e:
          # Si tu función de base de datos tiene otros parámetros, ajustala aquí según tu módulo db.py
          st.error(f"Hubo un error al guardar en la base de datos: {e}")
      else:
        st.warning("Por favor, ingresa al menos el título de la actividad.")

# ==========================================
# PESTAÑA 2: CONSULTA GENERAL Y FILTROS
# ==========================================
with pestana_consulta:
  st.header("📊 Consulta General de Actividades")
  st.write("Filtra y visualiza el historial de registros almacenados.")

  # Barra de filtros superior
  col_f1, col_f2 = st.columns(2)
  with col_f1:
    filtro_propiedad = st.selectbox(
        "Filtrar por Propiedad",
        [
            "Todas",
            "Wyndham Alltra Cancun",
            "Wyndham Alltra Playa del Carmen",
            "Aimbridge General",
        ],
    )
  with col_f2:
    busqueda_texto = st.text_input(
        "Buscar por palabra clave (Título o Descripción)"
    )

  # Botón o lógica para cargar datos desde la BD
  try:
    # Supongamos que tu módulo db tiene una función para obtener registros (ej. db.obtener_promociones())
    # Si la función no existe, puedes adaptarla al método que uses para extraer los datos de tu BD.
    registros = (
        db.obtener_promociones()
    )  # Asegúrate de usar la función de consulta de tu db.py

    if registros:
      # Si 'registros' es una lista de diccionarios o un DataFrame de Pandas, puedes filtrarlo visualmente:
      import pandas as pd

      df = pd.DataFrame(registros)

      # Aplicar filtros si existen en el DataFrame
      if filtro_propiedad != "Todas" and "propiedad" in df.columns:
        df = df[df["propiedad"] == filtro_propiedad]

      if busqueda_texto and "titulo" in df.columns:
        df = df[
            df["titulo"].str.contains(busqueda_texto, case=False, na=False)
            | df["descripcion"].str.contains(
                busqueda_texto, case=False, na=False
            )
        ]

      # Mostrar métricas rápidas
      st.metric(label="Total de registros encontrados", value=len(df))

      # Mostrar tabla interactiva
      st.dataframe(df, use_container_width=True)

      # Opción de exportación directa a CSV para reportes ejecutivos
      csv = df.to_csv(index=False).encode("utf-8")
      st.download_button(
          label="📥 Descargar Reporte en CSV",
          data=csv,
          file_name="reporte_actividades_aimbridge.csv",
          mime="text/csv",
      )
    else:
      st.info(
          "No hay registros guardados todavía en la base de datos. Utiliza la"
          " pestaña de registro para agregar el primero."
      )

  except Exception as e:
    st.info(
        "Configura la función de consulta en tu módulo `db.py` para visualizar"
        f" los datos aquí. (Detalle técnico: {e})"
    )
