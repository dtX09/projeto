from __future__ import annotations

from typing import Tuple

from app.db import config


def fetch_first_ship_photo_url() -> Tuple[str | None, str | None]:
    """
    Lê o URL da primeira linha de ship_photo.
    Devolve (url, erro_bd). Se não houver linhas, (None, None).
    """
    try:
        import mysql.connector
    except ImportError as e:
        return None, f"mysql-connector-python não instalado: {e}"

    try:
        conn = mysql.connector.connect(
            host=config.HOST,
            port=config.PORT,
            user=config.USER,
            password=config.PASSWORD,
            database=config.DATABASE,
        )
    except Exception as e:
        return None, str(e)

    try:
        cur = conn.cursor()
        cur.execute("SELECT url FROM ship_photo ORDER BY id ASC LIMIT 1")
        row = cur.fetchone()
        if not row or row[0] is None:
            return None, None
        return str(row[0]).strip() or None, None
    finally:
        conn.close()
