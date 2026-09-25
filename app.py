from datetime import date
from db import crear_promocion, obtener_promociones
import streamlit as st

st.set_page_config(
    page_title="AimbridgeApp - Promociones y Actividades", layout="wide"
)

st.title("🏨 AimbridgeApp - Gestión de Actividades y Promociones")

# 1. Formulario para registrar un nuevo ticket o actividad
with st.form("form_actividad", clear_on_submit=True):
  st.subheader("Registrar Nuevo Ticket / Actividad")

  texto = st.text_input("Título / Ticket (ej. Wyndham)")
  propiedad = st.text_input("Propiedad (ej. Dreams Playa Mujeres)")
  categoria = st.selectbox(
      "Categoría", ["Tarifas", "Operaciones", "Distribución", "Promoción"]
  )
  fecha = st.date_input("Fecha", value=date.today())
  responsable = st.text_input("Responsable (ej. Luis)")
  descripcion = st.text_area("Descripción de la actividad")

  submitted = st.form_submit_button("Guardar en la Nube")

  if submitted:
    if texto and propiedad:
      # Guardamos directamente en Supabase
      crear_promocion(
          texto=texto,
          propiedad=propiedad,
          categoria=categoria,
          fecha=str(fecha),
          responsable=responsable,
          descripcion=descripcion,
      )
      st.success("¡Registrado y guardado en Supabase con éxito!")
      st.rerun()
    else:
      st.warning("Por lo menos llena el campo de Título y Propiedad.")

st.markdown("---")
st.subheader("📋 Registros Actuales en la Nube")

# 2. Consultamos directamente desde la nube de Supabase
registros = obtener_promociones()

if registros:
  # Mostramos la tabla interactiva con los datos sincronizados
  st.dataframe(registros, use_container_width=True)
else:
  st.info("No hay registros todavía en la base de datos.")
