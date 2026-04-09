from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from app.db import config


@dataclass(frozen=True)
class ShipRow:
    id: int
    name: str
    imo_number: str
    ship_type_name: str
    built_year: int
    gt: float
    dwt: float
    length: float
    width: float
    height: float
    max_draft: float
    speed_knots: float
    description: str | None
    photo_url: str | None


def fetch_ships() -> Tuple[List[ShipRow], str | None]:
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
        SELECT
            s.id,
            s.name,
            s.imo_number,
            st.name AS ship_type_name,
            s.built_year,
            s.gt,
            s.dwt,
            s.length,
            s.width,
            s.height,
            s.max_draft,
            s.speed_knots,
            s.description,
            (SELECT sp.url FROM ship_photo sp WHERE sp.id_ship = s.id ORDER BY sp.id ASC LIMIT 1) AS photo_url
        FROM ship s
        INNER JOIN ship_type st ON st.id = s.id_ship_type
        ORDER BY s.name
    """

    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows: List[ShipRow] = []
        for (
            sid,
            name,
            imo,
            st_name,
            built,
            gt,
            dwt,
            lng,
            wid,
            hgt,
            draft,
            spd,
            desc,
            photo,
        ) in cur.fetchall():
            pu = str(photo).strip() if photo else None
            rows.append(
                ShipRow(
                    id=int(sid),
                    name=str(name),
                    imo_number=str(imo),
                    ship_type_name=str(st_name),
                    built_year=int(built),
                    gt=float(gt),
                    dwt=float(dwt),
                    length=float(lng),
                    width=float(wid),
                    height=float(hgt),
                    max_draft=float(draft),
                    speed_knots=float(spd),
                    description=str(desc) if desc else None,
                    photo_url=pu or None,
                )
            )
        return rows, None
    finally:
        conn.close()
