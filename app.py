import io
import streamlit as st
import pandas as pd
from datetime import date
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from db import (
    init_db, crear_promocion, listar_promociones,
    obtener_promocion, actualizar_campo, obtener_historial,
    crear_propiedad, listar_propiedades, actualizar_propiedad, eliminar_propiedad,
    listar_wyndham_rewards, actualizar_wyndham_rewards,
    crear_ticket, listar_tickets, obtener_ticket, actualizar_ticket
)

# ---------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS EJECUTIVOS
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Promo Dashboard | Aimbridge LATAM",
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

st.markdown("""
    <style>
    /* Ocultar elementos predeterminados de interfaz de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Bordes y fondo estilizado para contendores y tarjetas */
    div[data-testid="stExpander"] {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        background-color: #1a1c23 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Estilo para la barra lateral */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Transición y bordes redondeados en botones */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
    }
    </style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# FUNCIONES AUXILIARES DE EXPORTACIÓN (EXCEL / PDF)
# ---------------------------------------------------------------------------
def generar_excel(df: pd.DataFrame) -> io.BytesIO:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Datos")
    buffer.seek(0)
    return buffer


def generar_pdf(df: pd.DataFrame, titulo: str) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    estilos = getSampleStyleSheet()
    elementos = [Paragraph(titulo, estilos["Title"])]
    datos = [list(df.columns)] + df.astype(str).values.tolist()
    tabla = Table(datos, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2b6cb0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elementos.append(tabla)
    doc.build(elementos)
    buffer.seek(0)
    return buffer


def botones_descarga(df: pd.DataFrame, nombre_archivo: str, titulo_pdf: str, key_prefix: str):
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            "⬇️ Descargar Excel", data=generar_excel(df),
            file_name=f"{nombre_archivo}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"xlsx_{key_prefix}"
        )
    with col_b:
        st.download_button(
            "⬇️ Descargar PDF", data=generar_pdf(df, titulo_pdf),
            file_name=f"{nombre_archivo}.pdf", mime="application/pdf",
            key=f"pdf_{key_prefix}"
        )


# ---------------------------------------------------------------------------
# NAVEGACIÓN Y BARRA LATERAL
# ---------------------------------------------------------------------------
st.title("🏷️ Promo Dashboard")

st.sidebar.image("assets/aimbridge_logo.png", use_container_width=True)
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Ir a",
    ["Consultar promociones", "Agregar nueva", "Editar / Extender", "Propiedades",
     "Wyndham Rewards", "Tickets Wyndham Community"]
)

# ---------------------------------------------------------------------------
# CONSULTAR PROMOCIONES
# ---------------------------------------------------------------------------
if pagina == "Consultar promociones":
    st.subheader("Promociones registradas")

    col1, col2, col3 = st.columns(3)
    with col1:
        f_partner = st.text_input("Filtrar por Partner")
    with col2:
        f_estado = st.selectbox("Estado", ["Todas", "Activa", "Vencida", "Cancelada"])
    with col3:
        f_rate = st.text_input("Filtrar por Rate Plan")

    filas = listar_promociones({"partner": f_partner, "estado": f_estado, "rate_plan": f_rate})

    if not filas:
        st.info("No hay promociones que coincidan con el filtro.")
    else:
        df = pd.DataFrame([dict(f) for f in filas])
        df_mostrar = df[[
            "id", "nombre", "partner", "rate_plan", "bw_inicio", "bw_fin",
            "tw_inicio", "tw_fin", "descuento", "estado", "autorizo_nombre", "fecha_creacion"
        ]].rename(columns={
            "id": "ID", "nombre": "Promoción", "partner": "Partner", "rate_plan": "Rate Plan",
            "bw_inicio": "BW inicio", "bw_fin": "BW fin", "tw_inicio": "TW inicio", "tw_fin": "TW fin",
            "descuento": "% Desc.", "estado": "Estado", "autorizo_nombre": "Autorizó",
            "fecha_creacion": "Creada"
        })
        st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
        botones_descarga(df_mostrar, "promociones", "Promociones", "promos")

        st.markdown("---")
        st.caption("Selecciona un ID para ver el detalle completo (incluye imagen de autorización)")
        id_detalle = st.selectbox("Ver detalle de ID", [None] + df["id"].tolist())
        if id_detalle:
            promo = obtener_promocion(id_detalle)
            c1, c2 = st.columns([2, 1])
            with c1:
                st.write(f"**Promoción:** {promo['nombre']}")
                st.write(f"**Partner:** {promo['partner']}  |  **Rate Plan:** {promo['rate_plan']}")
                st.write(f"**BW:** {promo['bw_inicio']} → {promo['bw_fin']}")
                st.write(f"**TW:** {promo['tw_inicio']} → {promo['tw_fin']}")
                st.write(f"**% Descuento:** {promo['descuento']}")
                st.write(f"**Autorizó:** {promo['autorizo_nombre']} ({promo['autorizo_puesto']})")
                st.write(f"**Motivo:** {promo['motivo']}")
                st.write(f"**Notas:** {promo['notas'] or '-'}")
            with c2:
                if promo["autorizo_imagen"]:
                    st.image(promo["autorizo_imagen"], caption="Autorización", use_container_width=True)
                else:
                    st.caption("Sin imagen de autorización")

            with st.expander("Historial de cambios"):
                hist = obtener_historial(id_detalle)
                if hist:
                    st.dataframe(pd.DataFrame([dict(h) for h in hist]), use_container_width=True, hide_index=True)
                else:
                    st.caption("Sin cambios registrados.")

# ---------------------------------------------------------------------------
# AGREGAR NUEVA
# ---------------------------------------------------------------------------
elif pagina == "Agregar nueva":
    st.subheader("Registrar nueva promoción")

    with st.form("nueva_promo", clear_on_submit=True):
        propiedades_activas = listar_propiedades()
        opciones_propiedad = [p["nombre"] for p in propiedades_activas] or ["(agrega propiedades en la pestaña Propiedades)"]

        nombre = st.text_input("Nombre de la promoción *")
        col1, col2 = st.columns(2)
        with col1:
            partner = st.selectbox("Partner / Propiedad", opciones_propiedad)
            rate_plan = st.text_input("Rate Plan")
            descuento = st.number_input("% Descuento", min_value=0.0, max_value=100.0, step=0.5)
        with col2:
            estado = st.selectbox("Estado inicial", ["Activa", "Vencida", "Cancelada"])

        st.markdown("**Booking Window (BW)**")
        col3, col4 = st.columns(2)
        with col3:
            bw_inicio = st.date_input("BW inicio", value=date.today(), key="bwi")
        with col4:
            bw_fin = st.date_input("BW fin", value=date.today(), key="bwf")

        st.markdown("**Travel Window (TW)**")
        col5, col6 = st.columns(2)
        with col5:
            tw_inicio = st.date_input("TW inicio", value=date.today(), key="twi")
        with col6:
            tw_fin = st.date_input("TW fin", value=date.today(), key="twf")

        st.markdown("**Autorización**")
        col7, col8 = st.columns(2)
        with col7:
            autorizo_nombre = st.text_input("Nombre de quien autorizó *")
        with col8:
            autorizo_puesto = st.text_input("Puesto")
        motivo = st.text_area("Motivo de la autorización *")
        imagen = st.file_uploader("Imagen de la autorización (correo, captura, etc.)", type=["png", "jpg", "jpeg", "pdf"])
        notas = st.text_area("Notas adicionales (opcional)")

        enviado = st.form_submit_button("Guardar promoción")

        if enviado:
            if not nombre or not autorizo_nombre or not motivo:
                st.error("Completa los campos obligatorios (*).")
            else:
                img_bytes = imagen.read() if imagen else None
                img_nombre = imagen.name if imagen else None
                promo_id = crear_promocion({
                    "nombre": nombre, "partner": partner, "rate_plan": rate_plan,
                    "bw_inicio": str(bw_inicio), "bw_fin": str(bw_fin),
                    "tw_inicio": str(tw_inicio), "tw_fin": str(tw_fin),
                    "descuento": descuento, "autorizo_nombre": autorizo_nombre,
                    "autorizo_puesto": autorizo_puesto, "motivo": motivo,
                    "autorizo_imagen": img_bytes, "autorizo_imagen_nombre": img_nombre,
                    "estado": estado, "notas": notas
                })
                st.success(f"Promoción #{promo_id} guardada correctamente.")

# ---------------------------------------------------------------------------
# EDITAR / EXTENDER
# ---------------------------------------------------------------------------
elif pagina == "Editar / Extender":
    st.subheader("Editar o extender una promoción existente")

    filas = listar_promociones()
    if not filas:
        st.info("No hay promociones registradas todavía.")
    else:
        opciones = {f"#{f['id']} - {f['nombre']} ({f['partner']})": f["id"] for f in filas}
        seleccion = st.selectbox("Selecciona la promoción", list(opciones.keys()))
        promo_id = opciones[seleccion]
        promo = obtener_promocion(promo_id)

        st.info("Cada cambio que guardes aquí queda registrado en el historial con fecha, quién lo hizo y el motivo.")

        campo_legible = {
            "tw_fin": "TW fin (extender vigencia de viaje)",
            "bw_fin": "BW fin (extender ventana de reserva)",
            "descuento": "% Descuento",
            "estado": "Estado",
            "rate_plan": "Rate Plan",
            "notas": "Notas",
        }
        campo = st.selectbox("Campo a modificar", list(campo_legible.keys()), format_func=lambda x: campo_legible[x])

        valor_actual = promo[campo]
        st.write(f"Valor actual: **{valor_actual}**")

        if campo in ("tw_fin", "bw_fin"):
            nuevo_valor = st.date_input("Nueva fecha", value=date.today())
            nuevo_valor = str(nuevo_valor)
        elif campo == "descuento":
            nuevo_valor = st.number_input("Nuevo % descuento", min_value=0.0, max_value=100.0,
                                           value=float(valor_actual or 0), step=0.5)
        elif campo == "estado":
            nuevo_valor = st.selectbox("Nuevo estado", ["Activa", "Vencida", "Cancelada"])
        else:
            nuevo_valor = st.text_input("Nuevo valor", value=str(valor_actual or ""))

        quien = st.text_input("Quién autoriza este cambio *")
        motivo_cambio = st.text_area("Motivo del cambio (ej. 'se extendió por baja demanda') *")

        if st.button("Guardar cambio"):
            if not quien or not motivo_cambio:
                st.error("Indica quién autoriza y el motivo del cambio.")
            else:
                actualizar_campo(promo_id, campo, nuevo_valor, quien, motivo_cambio)
                st.success("Cambio guardado y registrado en el historial.")
                st.rerun()

        with st.expander("Ver historial completo de esta promoción"):
            hist = obtener_historial(promo_id)
            if hist:
                st.dataframe(pd.DataFrame([dict(h) for h in hist]), use_container_width=True, hide_index=True)
            else:
                st.caption("Sin cambios registrados todavía.")

# ---------------------------------------------------------------------------
# PROPIEDADES
# ---------------------------------------------------------------------------
elif pagina == "Propiedades":
    st.subheader("Propiedades que manejas (Aimbridge LATAM)")
    st.caption("Esta lista alimenta el campo Partner/Propiedad en el formulario de promociones.")

    with st.expander("➕ Agregar propiedad"):
        with st.form("nueva_propiedad", clear_on_submit=True):
            p_nombre = st.text_input("Nombre de la propiedad *")
            col1, col2 = st.columns(2)
            with col1:
                p_marca = st.text_input("Marca (ej. Wyndham Alltra, Viva)")
            with col2:
                p_ubicacion = st.text_input("Ubicación")
            p_tipo = st.selectbox("Tipo", ["All Inclusive", "Resort", "Urbano", "Otro"])
            p_notas = st.text_area("Notas (opcional)")
            if st.form_submit_button("Guardar propiedad"):
                if not p_nombre:
                    st.error("El nombre de la propiedad es obligatorio.")
                else:
                    crear_propiedad(p_nombre, p_marca, p_ubicacion, p_tipo, p_notas)
                    st.success(f"Propiedad '{p_nombre}' agregada.")
                    st.rerun()

    props = listar_propiedades()
    if not props:
        st.info("Aún no has agregado propiedades.")
    else:
        df_props = pd.DataFrame([dict(p) for p in props])
        df_props_mostrar = df_props[["id", "nombre", "marca", "ubicacion", "tipo", "notas"]].rename(columns={
            "id": "ID", "nombre": "Propiedad", "marca": "Marca",
            "ubicacion": "Ubicación", "tipo": "Tipo", "notas": "Notas"
        })
        st.dataframe(df_props_mostrar, use_container_width=True, hide_index=True)
        botones_descarga(df_props_mostrar, "propiedades", "Propiedades", "props")

        with st.expander("🗑️ Dar de baja una propiedad"):
            opciones_baja = {f"#{p['id']} - {p['nombre']}": p["id"] for p in props}
            sel_baja = st.selectbox("Selecciona propiedad", list(opciones_baja.keys()))
            if st.button("Dar de baja"):
                eliminar_propiedad(opciones_baja[sel_baja])
                st.success("Propiedad dada de baja (ya no aparecerá en el formulario de promociones).")
                st.rerun()

# ---------------------------------------------------------------------------
# WYNDHAM REWARDS
# ---------------------------------------------------------------------------
elif pagina == "Wyndham Rewards":
    st.subheader("Guía Wyndham Rewards")
    st.caption(
        "Referencia rápida de niveles y beneficios. Es editable porque el programa cambia sus "
        "condiciones periódicamente — actualiza aquí cuando veas cambios oficiales."
    )

    busqueda = st.text_input("🔍 Buscar (nivel, beneficio, requisito...)")
    registros = listar_wyndham_rewards(busqueda)

    if not registros:
        st.info("Sin resultados para esa búsqueda.")
    else:
        for r in registros:
            with st.container(border=True):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f"### {r['nivel']}")
                    st.caption(f"Requisito: {r['requisito']}")
                with col2:
                    st.write(r["beneficios"])
                    if r["notas"]:
                        st.caption(f"📝 {r['notas']}")
                    st.caption(f"Fuente: {r['fuente']} · Actualizado: {r['fecha_actualizacion']}")

            with st.expander("Editar este nivel"):
                nuevo_beneficios = st.text_area("Beneficios", value=r["beneficios"], key=f"ben_{r['id']}")
                nuevo_notas = st.text_area("Notas", value=r["notas"] or "", key=f"not_{r['id']}")
                if st.button("Guardar cambios", key=f"save_{r['id']}"):
                    actualizar_wyndham_rewards(r["id"], "beneficios", nuevo_beneficios)
                    actualizar_wyndham_rewards(r["id"], "notas", nuevo_notas)
                    st.success("Actualizado.")
                    st.rerun()

# ---------------------------------------------------------------------------
# TICKETS WYNDHAM COMMUNITY
# ---------------------------------------------------------------------------
else:
    st.subheader("Tickets — Wyndham Community")
    st.caption("Control de consultas/tickets abiertos con Wyndham Community, separado de promociones.")

    with st.expander("➕ Nuevo ticket"):
        with st.form("nuevo_ticket", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                t_numero = st.text_input("Número de ticket (Wyndham Community)")
                t_categoria = st.text_input("Categoría / Tema (ej. Conectividad, Tarifas, PMS)")
            with col2:
                t_fecha = st.date_input("Fecha de apertura", value=date.today())
                propiedades_activas = listar_propiedades()
                opciones_prop = ["(general, no aplica a una propiedad)"] + [p["nombre"] for p in propiedades_activas]
                t_propiedad = st.selectbox("Propiedad relacionada", opciones_prop)
            t_asunto = st.text_area("Asunto / Pregunta *")
            t_estado = st.selectbox("Estado", ["Abierto", "En progreso", "Cerrado"])
            t_respuesta = st.text_area("Respuesta recibida (si ya la tienes)")
            t_notas = st.text_area("Notas adicionales")
            if st.form_submit_button("Guardar ticket"):
                if not t_asunto:
                    st.error("El asunto/pregunta es obligatorio.")
                else:
                    crear_ticket({
                        "ticket_numero": t_numero, "fecha_apertura": str(t_fecha),
                        "categoria": t_categoria, "propiedad": t_propiedad,
                        "asunto": t_asunto, "estado": t_estado,
                        "respuesta": t_respuesta, "notas": t_notas
                    })
                    st.success("Ticket guardado.")
                    st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        f_estado_t = st.selectbox("Filtrar por estado", ["Todos", "Abierto", "En progreso", "Cerrado"])
    with col2:
        f_categoria_t = st.text_input("Filtrar por categoría")

    tickets = listar_tickets({"estado": f_estado_t, "categoria": f_categoria_t})

    if not tickets:
        st.info("No hay tickets registrados con ese filtro.")
    else:
        df_tickets = pd.DataFrame([dict(t) for t in tickets])
        df_tickets_mostrar = df_tickets[[
            "id", "ticket_numero", "fecha_apertura", "categoria", "propiedad", "asunto", "estado", "fecha_cierre"
        ]].rename(columns={
            "id": "ID", "ticket_numero": "N° Ticket", "fecha_apertura": "Apertura",
            "categoria": "Categoría", "propiedad": "Propiedad", "asunto": "Asunto",
            "estado": "Estado", "fecha_cierre": "Cierre"
        })
        botones_descarga(df_tickets_mostrar, "tickets_wyndham_community", "Tickets Wyndham Community", "tickets")
        st.markdown("---")
        for t in tickets:
            titulo = f"#{t['ticket_numero'] or t['id']} — {t['asunto'][:60]} · {t['estado']}"
            with st.expander(titulo):
                st.write(f"**Categoría:** {t['categoria'] or '-'}  |  **Propiedad:** {t['propiedad'] or '-'}")
                st.write(f"**Apertura:** {t['fecha_apertura']}")
                st.write(f"**Asunto:** {t['asunto']}")
                if t["respuesta"]:
                    st.write(f"**Respuesta:** {t['respuesta']}")
                if t["notas"]:
                    st.caption(f"📝 {t['notas']}")

                nuevo_estado = st.selectbox(
                    "Actualizar estado", ["Abierto", "En progreso", "Cerrado"],
                    index=["Abierto", "En progreso", "Cerrado"].index(t["estado"]),
                    key=f"estado_{t['id']}"
                )
                nueva_respuesta = st.text_area("Actualizar respuesta", value=t["respuesta"] or "", key=f"resp_{t['id']}")
                if st.button("Guardar cambios del ticket", key=f"save_ticket_{t['id']}"):
                    actualizar_ticket(t["id"], "estado", nuevo_estado)
                    actualizar_ticket(t["id"], "respuesta", nueva_respuesta)
                    if nuevo_estado == "Cerrado" and not t["fecha_cierre"]:
                        actualizar_ticket(t["id"], "fecha_cierre", date.today().isoformat())
                    st.success("Ticket actualizado.")
                    st.rerun()
