from __future__ import annotations

from typing import List, Tuple

from app.db import config


def fetch_weather_names() -> Tuple[List[str], str | None]:
    """Nomes da tabela weather_condition, por id."""
    try:
        import mysql.connector
    except ImportError as e:
        return [], f"mysql-connector-python não instalado: {e}"

    try:
        conn = mysql.connector.connect(
            host=config.HOST,
            port=config.PORT,
            user=config.USER,
            password=config.PASSWORD,
            database=config.DATABASE,
        )
    except Exception as e:
        return [], str(e)

    sql = "SELECT name FROM weather_condition ORDER BY id ASC"

    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = [str(r[0]) for r in cur.fetchall()]
        return rows, None
    finally:
        conn.close()
