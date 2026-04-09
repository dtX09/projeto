from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from typing import Dict, List, Tuple

from app.db import config


@dataclass(frozen=True)
class RouteRow:
    id: int
    name: str
    distance_nm: float
    frequency_days: int
    ports_label: str


@dataclass(frozen=True)
class PortWaypoint:
    port_order: int
    name: str
    latitude: float
    longitude: float


def fetch_routes() -> Tuple[List[RouteRow], str | None]:
    """
    Lê rotas da BD com a cadeia de portos (route_port + port).
    Devolve (lista, erro). Se erro não for None, a lista pode estar vazia.
    """
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
            r.id,
            r.name,
            r.distance_nm,
            r.frequency_days,
            GROUP_CONCAT(p.name ORDER BY rp.port_order SEPARATOR ' → ') AS ports
        FROM route r
        LEFT JOIN route_port rp ON rp.id_route = r.id
        LEFT JOIN port p ON p.id = rp.id_port
        GROUP BY r.id, r.name, r.distance_nm, r.frequency_days
        ORDER BY r.id
    """

    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows: List[RouteRow] = []
        for rid, name, dist, freq, ports in cur.fetchall():
            pl = (ports or "").strip() or "(sem portos definidos)"
            rows.append(
                RouteRow(
                    id=int(rid),
                    name=str(name),
                    distance_nm=float(dist),
                    frequency_days=int(freq),
                    ports_label=pl,
                )
            )
        return rows, None
    finally:
        conn.close()


def fetch_route_waypoints() -> Tuple[Dict[int, Tuple[PortWaypoint, ...]], str | None]:
    """
    Portos por rota, ordenados por port_order, com coordenadas para desenhar o mapa.
    """
    try:
        import mysql.connector
    except ImportError as e:
        return {}, f"mysql-connector-python não instalado: {e}"

    try:
        conn = mysql.connector.connect(
            host=config.HOST,
            port=config.PORT,
            user=config.USER,
            password=config.PASSWORD,
            database=config.DATABASE,
        )
    except Exception as e:
        return {}, str(e)

    sql = """
        SELECT rp.id_route, rp.port_order, p.name, p.latitude, p.longitude
        FROM route_port rp
        INNER JOIN port p ON p.id = rp.id_port
        ORDER BY rp.id_route, rp.port_order
    """

    try:
        cur = conn.cursor()
        cur.execute(sql)
        acc: dict[int, list[PortWaypoint]] = defaultdict(list)
        for rid, port_order, name, lat, lon in cur.fetchall():
            acc[int(rid)].append(
                PortWaypoint(
                    port_order=int(port_order),
                    name=str(name),
                    latitude=float(lat),
                    longitude=float(lon),
                )
            )
        return {k: tuple(v) for k, v in acc.items()}, None
    finally:
        conn.close()
