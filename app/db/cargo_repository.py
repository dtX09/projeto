from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

from app.db import config


def _as_bool(v: object) -> bool:
    if v is None:
        return False
    if isinstance(v, (bytes, bytearray)):
        return v != b"\x00"
    return bool(int(v))


@dataclass(frozen=True)
class CargoTypeRow:
    id: int
    code: str
    name: str
    need_container: bool


@dataclass(frozen=True)
class CargoRow:
    id: int
    id_cargo_type: int
    cargo_type_code: str
    cargo_type_name: str
    need_container: bool
    cargo_name: str
    weight: float
    volume: float
    priority: int
    imdg_class: str
    temperature_required: float | None
    quantity: float
    unit: str


def _norm_imdg(s: str) -> str:
    return (s or "").strip().upper()


def is_liquid_bulk(c: CargoRow) -> bool:
    return not c.need_container


def is_dangerous_container(c: CargoRow) -> bool:
    if not c.need_container:
        return False
    im = _norm_imdg(c.imdg_class)
    return im not in ("", "N/A", "NA", "—", "-")


def fetch_cargo_types() -> Tuple[List[CargoTypeRow], str | None]:
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
        SELECT id, code, name, need_container
        FROM cargo_type
        ORDER BY name ASC, id ASC
    """

    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows: List[CargoTypeRow] = []
        for tid, code, name, need_c in cur.fetchall():
            rows.append(
                CargoTypeRow(
                    id=int(tid),
                    code=str(code),
                    name=str(name),
                    need_container=_as_bool(need_c),
                )
            )
        return rows, None
    finally:
        conn.close()


def fetch_all_cargo() -> Tuple[List[CargoRow], str | None]:
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
            c.id,
            c.id_cargo_type,
            ct.code,
            ct.name,
            ct.need_container,
            c.cargo_name,
            c.weight,
            c.volume,
            c.priority,
            c.imdg_class,
            c.temperature_required,
            c.quantity,
            c.unit
        FROM cargo c
        INNER JOIN cargo_type ct ON ct.id = c.id_cargo_type
        ORDER BY ct.name ASC, c.id ASC
    """

    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows: List[CargoRow] = []
        for (
            cid,
            tid,
            tcode,
            tname,
            need_c,
            cname,
            w,
            vol,
            pri,
            imdg,
            temp,
            qty,
            unit,
        ) in cur.fetchall():
            rows.append(
                CargoRow(
                    id=int(cid),
                    id_cargo_type=int(tid),
                    cargo_type_code=str(tcode),
                    cargo_type_name=str(tname),
                    need_container=_as_bool(need_c),
                    cargo_name=str(cname),
                    weight=float(w),
                    volume=float(vol),
                    priority=int(pri),
                    imdg_class=str(imdg),
                    temperature_required=float(temp) if temp is not None else None,
                    quantity=float(qty),
                    unit=str(unit),
                )
            )
        return rows, None
    finally:
        conn.close()


def group_cargo_by_type_id(cargos: List[CargoRow]) -> Dict[int, List[CargoRow]]:
    acc: dict[int, list[CargoRow]] = defaultdict(list)
    for c in cargos:
        acc[c.id_cargo_type].append(c)
    return {k: v for k, v in acc.items()}
