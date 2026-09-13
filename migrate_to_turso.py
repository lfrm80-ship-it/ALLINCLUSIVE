"""
Migra los datos del promociones.db local hacia tu base de Turso.

Uso:
    1. Asegúrate de tener TURSO_URL y TURSO_TOKEN configurados como variables
       de entorno (o en .streamlit/secrets.toml) ANTES de correr este script.
    2. Corre:  python migrate_to_turso.py
    3. Al terminar, verifica en la app (apuntando a Turso) que los datos
       aparecen correctamente.

Este script es seguro de correr una sola vez sobre una base Turso vacía.
Si lo corres dos veces vas a duplicar los datos.
"""
import os
import sqlite3
import sys

import db as dbmod

TABLAS = ["propiedades", "wyndham_rewards", "promociones", "historial", "tickets"]


def main():
    if not dbmod.USANDO_TURSO:
        print("⚠️  No se detectaron TURSO_URL / TURSO_TOKEN. Configúralos antes de migrar.")
        sys.exit(1)

    if not os.path.exists("promociones.db"):
        print("No hay promociones.db local — no hay nada que migrar.")
        sys.exit(0)

    # Crea el esquema en Turso (si ya existe, no pasa nada, usa IF NOT EXISTS)
    dbmod.init_db()

    local = sqlite3.connect("promociones.db")
    local.row_factory = sqlite3.Row

    total_migrado = 0
    with dbmod.get_conn() as remoto:
        for tabla in TABLAS:
            filas = local.execute(f"SELECT * FROM {tabla}").fetchall()
            if not filas:
                print(f"· {tabla}: sin datos, se salta.")
                continue

            columnas = filas[0].keys()
            placeholders = ",".join(["?"] * len(columnas))
            cols_sql = ",".join(columnas)

            for fila in filas:
                valores = tuple(fila[c] for c in columnas)
                remoto.execute(
                    f"INSERT INTO {tabla} ({cols_sql}) VALUES ({placeholders})",
                    valores
                )
            print(f"· {tabla}: {len(filas)} filas migradas.")
            total_migrado += len(filas)

    local.close()
    print(f"\n✅ Migración completa: {total_migrado} filas en total.")


if __name__ == "__main__":
    main()
