Python
from db import obtener_promociones  # Importas tu función de la nube

# Cada vez que alguien entra o recarga, esto va directo a Supabase
registros = obtener_promociones()
