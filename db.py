from supabase import create_client

SUPABASE_URL = "https://zskckjfqngqftrydjjem.supabase.co"
# Aquí va tu llave (Publishable key)
SUPABASE_KEY = "sb_publishable_..."

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def obtener_promociones():
  """Consulta directamente la tabla en Supabase y trae los datos frescos."""
  try:
    response = (
        supabase.table("Actividades")
        .select("*")
        .order("fecha", desc=True)
        .execute()
    )
    return response.data
  except Exception as e:
    print(f"Error al consultar: {e}")
    return []


def crear_promocion(
    texto, propiedad, categoria, fecha, responsable, descripcion
):
  """Inserta un nuevo registro directamente en la nube."""
  data = {
      "texto": texto,
      "propiedad": propiedad,
      "categoria": categoria,
      "fecha": fecha,
      "responsable": responsable,
      "descripcion": descripcion,
  }
  supabase.table("Actividades").insert(data).execute()
