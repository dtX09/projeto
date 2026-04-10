from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from app.db import config


@dataclass(frozen=True)
class PortRow:
    id: int
    name: str


def fetch_ports() -> Tuple[List[PortRow], str | None]:
    """Lê todos os portos da tabela `port` ordenados por nome."""
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

    sql = """
        SELECT id, name
        FROM port
        ORDER BY name
    """

    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = [PortRow(id=int(pid), name=str(name)) for pid, name in cur.fetchall()]
        return rows, None
    finally:
        conn.close()
