from supabase import create_client

SUPABASE_URL = "https://zskckjfqngqftrydjjem.supabase.co"
SUPABASE_KEY = "sb_publishable_..."  # Tu llave pública real

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def obtener_promociones():
  """Consulta directamente la tabla en Supabase y trae todos los registros."""
  try:
    response = supabase.table("Actividades").select("*").execute()
    return response.data
  except Exception as e:
    print(f"Error al consultar Supabase: {e}")
    return []


def crear_promocion(
    texto, propiedad, categoria, fecha, responsable, descripcion
):
  """Inserta el registro directamente en la nube y valida que se guarde."""
  data = {
      "texto": texto,
      "propiedad": propiedad,
      "categoria": categoria,
      "fecha": fecha,
      "responsable": responsable,
      "descripcion": descripcion,
  }
  try:
    resultado = supabase.table("Actividades").insert(data).execute()
    return True
  except Exception as e:
    print(f"Error al insertar en Supabase: {e}")
    return False
