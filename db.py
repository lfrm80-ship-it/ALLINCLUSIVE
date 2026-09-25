def crear_promocion(
    texto, propiedad, categoria, fecha, responsable, descripcion
):
  data = {
      "texto": texto,  # <--- Cambiamos "titulo" por "texto"
      "propiedad": propiedad,
      "categoria": categoria,
      "fecha": fecha,
      "responsable": responsable,
      "descripcion": descripcion,
  }
  supabase.table("Actividades").insert(data).execute()
