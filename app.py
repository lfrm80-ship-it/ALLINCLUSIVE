from datetime import date
from db import crear_promocion, obtener_promociones
import streamlit as st

st.set_page_config(
    page_title="AimbridgeApp - Supabase Real-Time", layout="wide"
)

st.title("🏨 AimbridgeApp - Gestión Conectada a Supabase")

# Formulario de registro
with st.form("form_actividad", clear_on_submit=True):
  st.subheader("Registrar Nuevo Ticket / Actividad")

  col1, col2 = st.columns(2)
  with col1:
    texto = st.text_input("Título / Ticket")
    propiedad = st.text_input("Propiedad (ej. Wyndham)")
    categoria = st.selectbox(
        "Categoría", ["Tarifas", "Operaciones", "Distribución", "Promoción"]
    )
  with col2:
    fecha = st.date_input("Fecha", value=date.today())
    responsable = st.text_input("Responsable")
    descripcion = st.text_area("Descripción")

  submitted = st.form_submit_button("Guardar en Supabase")

  if submitted:
    if texto and propiedad:
      # Llamamos a la función que inserta en la nube
      exito = crear_promocion(
          texto, propiedad, categoria, str(fecha), responsable, descripcion
      )
      if exito:
        st.success("¡Guardado exitosamente en la base de datos de Supabase!")
        st.rerun()
      else:
        st.error(
            "Hubo un error al guardar en la nube. Revisa la consola o las"
            " políticas de Supabase."
        )
    else:
      st.warning("Llena al menos el Título y la Propiedad.")

st.markdown("---")
st.subheader("📋 Registros Oficiales desde la Nube")

# CONSULTA DIRECTA: Aquí le pedimos los datos a Supabase cada vez que carga
registros = obtener_promociones()

if registros:
  st.dataframe(registros, use_container_width=True)
else:
  st.info(
      "No hay registros en Supabase o la tabla está vacía actualmente."
  )
