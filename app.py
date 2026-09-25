# En tu archivo app.py, cuando quieras mostrar las actividades registradas:
from db import obtener_promociones

# Traemos los datos directamente desde la nube de Supabase
registros = obtener_promociones()

# Si 'registros' trae datos, los muestras en tu tabla o dataframe de Streamlit:
if registros:
  st.dataframe(registros)
else:
  st.info("No hay actividades registradas todavía.")
