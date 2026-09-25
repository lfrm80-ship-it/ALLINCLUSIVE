from datetime import date
from db import crear_promocion, obtener_promociones
import streamlit as st

st.set_page_config(
    page_title="AimbridgeApp - Tiempo Real", layout="wide"
)

st.title("🏨 AimbridgeApp - Panel Colaborativo en Vivo")

# Formulario para registrar un nuevo ticket
with st.form("form_ticket", clear_on_submit=True):
  st.subheader("Registrar Nuevo Ticket / Actividad")

  col1, col2 = st.columns(2)
  with col1:
    texto = st.text_input("Título / Ticket")
    propiedad = st.text_input("Propiedad (ej. Wyndham / Dreams)")
    categoria = st.selectbox(
        "Categoría", ["Tarifas", "Operaciones", "Distribución", "Promoción"]
    )
  with col2:
    fecha = st.date_input("Fecha", value=date.today())
    responsable = st.text_input("Responsable")
    descripcion = st.text_area("Descripción de la actividad")

  submitted = st.form_submit_button("Guardar en Supabase")

  if submitted:
    if texto and propiedad:
      crear_promocion(
          texto, propiedad, categoria, str(fecha), responsable, descripcion
      )
      st.success("¡Guardado en la nube con éxito!")
      st.rerun()
    else:
      st.warning("Completa al menos el título y la propiedad.")

st.markdown("---")


# Fragmento inteligente que consulta la nube automáticamente cada 3 segundos
@st.fragment(run_every="3s")
def render_tabla_en_vivo():
  st.subheader("📋 Registros en Tiempo Real (Sincronizados)")

  # Llamada directa a Supabase
  registros = obtener_promociones()

  if registros:
    st.dataframe(registros, use_container_width=True)
  else:
    st.info("No hay registros todavía en la base de datos.")


# Ejecutamos el fragmento en la app principal
render_tabla_en_vivo()
