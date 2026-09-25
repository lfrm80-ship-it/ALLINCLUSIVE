# Cambia .table("actividades") por .table("Actividades") en tus funciones:


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
  supabase.table("Actividades").insert(data).execute()  # <--- Con 'A' mayúscula


def obtener_promociones():
  response = supabase.table("Actividades").select("*").execute()  # <--- Con 'A' mayúscula
  return response.data
