from supabase import Client, create_client

# Tu URL de Supabase de tu proyecto AimbridgeApp
SUPABASE_URL = "https://zskckjfqngqftrydjjem.supabase.co"

# Pega aquí exactamente la llave larga que guardaste en tu Excel (empieza con sb_publish__)
SUPABASE_KEY = "pega_aqui_tu_llave_completa"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def crear_promocion(
    titulo, propiedad, categoria, fecha, responsable, descripcion
):
  data = {
      "titulo": titulo,
      "propiedad": propiedad,
      "categoria": categoria,
      "fecha": fecha,
      "responsable": responsable,
      "descripcion": descripcion,
  }
  supabase.table("actividades").insert(data).execute()


def obtener_promociones():
  response = supabase.table("actividades").select("*").execute()
  return response.data
