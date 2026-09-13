import os
import sqlite3
from datetime import datetime
from contextlib import contextmanager

DB_PATH = "promociones.db"

# Credenciales de Turso: primero busca en variables de entorno, luego en
# st.secrets (Streamlit). Si no encuentra ninguna, usa SQLite local como
# respaldo (útil para pruebas rápidas sin tocar la nube).
TURSO_URL = os.environ.get("TURSO_URL")
TURSO_TOKEN = os.environ.get("TURSO_TOKEN")
if not TURSO_URL or not TURSO_TOKEN:
    try:
        import streamlit as st
        TURSO_URL = TURSO_URL or st.secrets.get("TURSO_URL")
        TURSO_TOKEN = TURSO_TOKEN or st.secrets.get("TURSO_TOKEN")
    except Exception:
        pass

USANDO_TURSO = bool(TURSO_URL and TURSO_TOKEN)


class _Row:
    """Imita sqlite3.Row: acceso por nombre de columna y compatible con dict(fila)."""
    __slots__ = ("_keys", "_values")

    def __init__(self, keys, values):
        self._keys = keys
        self._values = values

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._values[self._keys.index(key)]
        return self._values[key]

    def keys(self):
        return list(self._keys)

    def __iter__(self):
        return iter(self._values)

    def __repr__(self):
        return repr(dict(zip(self._keys, self._values)))


class _CursorWrapper:
    """Envuelve un ResultSet de libsql-client para verse como un cursor sqlite3."""

    def __init__(self, result_set):
        self._rs = result_set
        self._columns = list(result_set.columns)

    @property
    def lastrowid(self):
        return self._rs.last_insert_rowid

    def fetchall(self):
        return [_Row(self._columns, list(row.astuple())) for row in self._rs.rows]

    def fetchone(self):
        if not self._rs.rows:
            return None
        return _Row(self._columns, list(self._rs.rows[0].astuple()))


class _TursoConnWrapper:
    """Da a la conexión HTTP/WebSocket de Turso la misma interfaz que usa el
    resto del código (execute -> objeto con fetchall/fetchone/lastrowid,
    executemany, commit, close)."""

    def __init__(self, client):
        self._client = client

    def execute(self, sql, params=()):
        rs = self._client.execute(sql, list(params) if params else None)
        return _CursorWrapper(rs)

    def executemany(self, sql, seq_of_params):
        for params in seq_of_params:
            self._client.execute(sql, list(params) if params else None)

    def commit(self):
        pass  # cada execute() ya se confirma solo (autocommit vía HTTP)

    def close(self):
        self._client.close()


@contextmanager
def get_conn():
    if USANDO_TURSO:
        import libsql_client
        client = libsql_client.create_client_sync(TURSO_URL, auth_token=TURSO_TOKEN)
        conn = _TursoConnWrapper(client)
    else:
        raw = sqlite3.connect(DB_PATH)
        raw.row_factory = sqlite3.Row
        conn = raw
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS promociones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                partner TEXT,
                rate_plan TEXT,
                bw_inicio TEXT,
                bw_fin TEXT,
                tw_inicio TEXT,
                tw_fin TEXT,
                descuento REAL,
                autorizo_nombre TEXT,
                autorizo_puesto TEXT,
                motivo TEXT,
                autorizo_imagen BLOB,
                autorizo_imagen_nombre TEXT,
                estado TEXT DEFAULT 'Activa',
                fecha_creacion TEXT,
                notas TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                promocion_id INTEGER NOT NULL,
                fecha TEXT,
                tipo_cambio TEXT,
                campo TEXT,
                valor_anterior TEXT,
                valor_nuevo TEXT,
                quien TEXT,
                motivo TEXT,
                FOREIGN KEY (promocion_id) REFERENCES promociones(id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS propiedades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                marca TEXT,
                ubicacion TEXT,
                tipo TEXT,
                notas TEXT,
                activa INTEGER DEFAULT 1
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wyndham_rewards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nivel TEXT NOT NULL,
                requisito TEXT,
                beneficios TEXT,
                notas TEXT,
                fuente TEXT,
                fecha_actualizacion TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_numero TEXT,
                fecha_apertura TEXT,
                categoria TEXT,
                propiedad TEXT,
                asunto TEXT,
                estado TEXT DEFAULT 'Abierto',
                respuesta TEXT,
                fecha_cierre TEXT,
                notas TEXT
            )
        """)
        _seed_wyndham_rewards(conn)


def _seed_wyndham_rewards(conn):
    existe = conn.execute("SELECT COUNT(*) AS c FROM wyndham_rewards").fetchone()["c"]
    if existe:
        return
    datos = [
        ("Blue", "0 noches (al inscribirse)",
         "Wi-Fi gratis durante la estancia",
         "Nivel base, todos los miembros lo tienen al registrarse", "wyndhamhotels.com", ""),
        ("Gold", "5 noches calificadas por año calendario",
         "10% de puntos extra por estancia; habitación preferente sujeta a disponibilidad; late checkout bajo solicitud",
         "También se obtiene con la tarjeta Wyndham Rewards Earner (sin anualidad)", "wyndhamhotels.com / thepointsguy.com", ""),
        ("Platinum", "15 noches calificadas por año calendario",
         "15% de puntos extra por estancia; early check-in bajo solicitud; status match con Caesars Rewards",
         "Se obtiene automático con la tarjeta Earner Plus (con anualidad)", "wyndhamhotels.com / thepointsguy.com", ""),
        ("Diamond", "40 noches calificadas por año calendario",
         "20% de puntos extra por estancia; snack o bebida de bienvenida en hoteles selectos; upgrade a suite bajo disponibilidad; 10% de descuento en canjes por noches de premio",
         "Se obtiene automático con la tarjeta Earner Business (con anualidad); puede regalar 1 nivel Gold a otra persona por año", "wyndhamhotels.com / awardwallet.com", ""),
    ]
    conn.executemany("""
        INSERT INTO wyndham_rewards (nivel, requisito, beneficios, notas, fuente, fecha_actualizacion)
        VALUES (?,?,?,?,?,?)
    """, [(n, r, b, no, f, datetime.now().strftime("%Y-%m-%d")) for n, r, b, no, f, _ in datos])


def crear_promocion(data: dict) -> int:
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO promociones
            (nombre, partner, rate_plan, bw_inicio, bw_fin, tw_inicio, tw_fin,
             descuento, autorizo_nombre, autorizo_puesto, motivo,
             autorizo_imagen, autorizo_imagen_nombre, estado, fecha_creacion, notas)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            data["nombre"], data["partner"], data["rate_plan"],
            data["bw_inicio"], data["bw_fin"], data["tw_inicio"], data["tw_fin"],
            data["descuento"], data["autorizo_nombre"], data["autorizo_puesto"],
            data["motivo"], data.get("autorizo_imagen"), data.get("autorizo_imagen_nombre"),
            data.get("estado", "Activa"), datetime.now().isoformat(timespec="seconds"),
            data.get("notas", "")
        ))
        promo_id = cur.lastrowid
        conn.execute("""
            INSERT INTO historial (promocion_id, fecha, tipo_cambio, campo, valor_anterior, valor_nuevo, quien, motivo)
            VALUES (?,?,?,?,?,?,?,?)
        """, (promo_id, datetime.now().isoformat(timespec="seconds"), "Creación", "-", "-", "-",
              data["autorizo_nombre"], data["motivo"]))
        return promo_id


def listar_promociones(filtros: dict = None):
    query = "SELECT * FROM promociones WHERE 1=1"
    params = []
    if filtros:
        if filtros.get("partner"):
            query += " AND partner LIKE ?"
            params.append(f"%{filtros['partner']}%")
        if filtros.get("estado") and filtros["estado"] != "Todas":
            query += " AND estado = ?"
            params.append(filtros["estado"])
        if filtros.get("rate_plan"):
            query += " AND rate_plan LIKE ?"
            params.append(f"%{filtros['rate_plan']}%")
    query += " ORDER BY fecha_creacion DESC"
    with get_conn() as conn:
        return conn.execute(query, params).fetchall()


def obtener_promocion(promo_id: int):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM promociones WHERE id=?", (promo_id,)).fetchone()


def actualizar_campo(promo_id: int, campo: str, valor_nuevo, quien: str, motivo: str):
    promo = obtener_promocion(promo_id)
    valor_anterior = promo[campo] if promo else None
    with get_conn() as conn:
        conn.execute(f"UPDATE promociones SET {campo} = ? WHERE id = ?", (valor_nuevo, promo_id))
        conn.execute("""
            INSERT INTO historial (promocion_id, fecha, tipo_cambio, campo, valor_anterior, valor_nuevo, quien, motivo)
            VALUES (?,?,?,?,?,?,?,?)
        """, (promo_id, datetime.now().isoformat(timespec="seconds"), "Edición", campo,
              str(valor_anterior), str(valor_nuevo), quien, motivo))


def obtener_historial(promo_id: int):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM historial WHERE promocion_id=? ORDER BY fecha DESC", (promo_id,)
        ).fetchall()


# ---------------------------------------------------------------------------
# Propiedades
# ---------------------------------------------------------------------------
def crear_propiedad(nombre, marca, ubicacion, tipo, notas):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO propiedades (nombre, marca, ubicacion, tipo, notas, activa)
            VALUES (?,?,?,?,?,1)
        """, (nombre, marca, ubicacion, tipo, notas))


def listar_propiedades(solo_activas=True):
    query = "SELECT * FROM propiedades"
    if solo_activas:
        query += " WHERE activa = 1"
    query += " ORDER BY nombre"
    with get_conn() as conn:
        return conn.execute(query).fetchall()


def actualizar_propiedad(prop_id, campo, valor):
    with get_conn() as conn:
        conn.execute(f"UPDATE propiedades SET {campo} = ? WHERE id = ?", (valor, prop_id))


def eliminar_propiedad(prop_id):
    with get_conn() as conn:
        conn.execute("UPDATE propiedades SET activa = 0 WHERE id = ?", (prop_id,))


# ---------------------------------------------------------------------------
# Wyndham Rewards
# ---------------------------------------------------------------------------
def listar_wyndham_rewards(busqueda=None):
    query = "SELECT * FROM wyndham_rewards WHERE 1=1"
    params = []
    if busqueda:
        query += " AND (nivel LIKE ? OR beneficios LIKE ? OR requisito LIKE ? OR notas LIKE ?)"
        params.extend([f"%{busqueda}%"] * 4)
    query += " ORDER BY id"
    with get_conn() as conn:
        return conn.execute(query, params).fetchall()


def actualizar_wyndham_rewards(reg_id, campo, valor):
    with get_conn() as conn:
        conn.execute(f"UPDATE wyndham_rewards SET {campo} = ?, fecha_actualizacion = ? WHERE id = ?",
                     (valor, datetime.now().strftime("%Y-%m-%d"), reg_id))


# ---------------------------------------------------------------------------
# Tickets (Wyndham Community)
# ---------------------------------------------------------------------------
def crear_ticket(data: dict) -> int:
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO tickets (ticket_numero, fecha_apertura, categoria, propiedad,
                                  asunto, estado, respuesta, fecha_cierre, notas)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            data.get("ticket_numero"), data.get("fecha_apertura"), data.get("categoria"),
            data.get("propiedad"), data["asunto"], data.get("estado", "Abierto"),
            data.get("respuesta", ""), data.get("fecha_cierre"), data.get("notas", "")
        ))
        return cur.lastrowid


def listar_tickets(filtros: dict = None):
    query = "SELECT * FROM tickets WHERE 1=1"
    params = []
    if filtros:
        if filtros.get("estado") and filtros["estado"] != "Todos":
            query += " AND estado = ?"
            params.append(filtros["estado"])
        if filtros.get("categoria"):
            query += " AND categoria LIKE ?"
            params.append(f"%{filtros['categoria']}%")
        if filtros.get("propiedad"):
            query += " AND propiedad LIKE ?"
            params.append(f"%{filtros['propiedad']}%")
    query += " ORDER BY fecha_apertura DESC"
    with get_conn() as conn:
        return conn.execute(query, params).fetchall()


def obtener_ticket(ticket_id: int):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,)).fetchone()


def actualizar_ticket(ticket_id: int, campo: str, valor):
    with get_conn() as conn:
        conn.execute(f"UPDATE tickets SET {campo} = ? WHERE id = ?", (valor, ticket_id))
