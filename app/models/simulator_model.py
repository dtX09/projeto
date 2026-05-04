"""Estado do simulador de estiva (variáveis Tk e imagens PIL)."""

from __future__ import annotations

import tkinter as tk
from PIL import Image, ImageTk
from app.db.cargo_repository import (
    CargoTypeRow,
    CargoRow,
    fetch_all_cargo,
    fetch_cargo_types,
    group_cargo_by_type_id,
)
from app.db.port_repository import fetch_ports
from app.db.route_repository import PortWaypoint, RouteRow, fetch_route_waypoints, fetch_routes
from app.db.ship_repository import ShipRow, fetch_ships
from app.db.weather_repository import fetch_weather_names
from app.utils.resource_path import resolve_resource_path


class SimulatorModel:
    def __init__(self, master: tk.Misc) -> None:
        self._master = master
        self.routes_catalog, self.routes_load_error = fetch_routes()
        self.ships_catalog, self.ships_load_error = fetch_ships()
        self.ports_catalog, self.ports_load_error = fetch_ports()
        self.cargo_types_catalog, err_types = fetch_cargo_types()
        self.cargo_catalog, err_cargo = fetch_all_cargo()
        self.cargo_load_error = err_types or err_cargo
        self.cargo_by_type_id = group_cargo_by_type_id(self.cargo_catalog)
        self.weather_names, self.weather_load_error = fetch_weather_names()
        first_ship = self.ships_catalog[0].id if self.ships_catalog else 0
        self.selected_ship_id = first_ship
        self.ship_confirm_photo: ImageTk.PhotoImage | None = None
        self.route_waypoints: dict[int, tuple[PortWaypoint, ...]] = {}
        if not self.routes_load_error:
            self.route_waypoints, _ = fetch_route_waypoints()
        first_id = self.routes_catalog[0].id if self.routes_catalog else 0
        self.selected_route_id = tk.IntVar(master=master, value=first_id)
        type_ids = self.available_cargo_type_ids()
        first_tid = type_ids[0] if type_ids else 0
        self.cargo_type_id_var = tk.IntVar(master=master, value=first_tid)
        first_cargo = self._first_cargo_id_in_type(first_tid)
        self.selected_cargo_id_var = tk.IntVar(master=master, value=first_cargo or 0)
        self.porto_carga_var = tk.StringVar(master=master, value="")
        self.porto_descarga_var = tk.StringVar(master=master, value="")
        self.estado_clima_var = tk.StringVar(master=master, value="")
        self.custo_combustivel_litro_var = tk.StringVar(master=master, value="")
        self.eta_var = tk.StringVar(master=master, value="")

        self.logo_img: ImageTk.PhotoImage | None = None
        self.screen1_bg: ImageTk.PhotoImage | None = None
        self.logo_src = None
        self.liner_src = None
        self.tramp_src = None
        self.screen1_bg_src = None
        self._load_images()

    def _load_images(self) -> None:
        try:
            self.logo_src = Image.open(resolve_resource_path("imgs/ENIDH_ultra_horizontal_branco.png"))
            logo = self.logo_src.resize((320, 44), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(logo)
        except Exception:
            self.logo_img = None

        try:
            self.liner_src = Image.open(resolve_resource_path("imgs/boat2.jpg"))
        except Exception:
            self.liner_src = None

        try:
            self.tramp_src = Image.open(resolve_resource_path("imgs/boat1.jpg"))
        except Exception:
            self.tramp_src = None

        try:
            self.screen1_bg_src = Image.open(resolve_resource_path("imgs/backg.png"))
        except Exception:
            self.screen1_bg_src = None

    def get_selected_route(self) -> RouteRow | None:
        rid = self.selected_route_id.get()
        for r in self.routes_catalog:
            if r.id == rid:
                return r
        return self.routes_catalog[0] if self.routes_catalog else None

    def selected_route_summary_lines(self) -> str:
        r = self.get_selected_route()
        if not r:
            return "Nenhuma rota disponível."
        waypoints = self.waypoints_for_route(r.id)
        if waypoints:
            port_names = [wp.name.strip() for wp in waypoints if wp.name.strip()]
        else:
            port_names = [p.strip() for p in r.ports_label.split("→") if p.strip()]

        numbered_ports = "\n".join(f"{idx} - {name}" for idx, name in enumerate(port_names, start=1))
        if not numbered_ports:
            numbered_ports = "—"

        return (
            f"{r.name}\n"
            f"{numbered_ports}\n"
            f"Distancia: {r.distance_nm:.0f} nm\n"
            f"Frequência: {r.frequency_days} dias\n"
            f"Calado máximo: {r.max_draft:.2f} m\n"
            f"Profundidade do canal: {r.channel_depth:.2f} m\n"
            f"Comprimento máximo do navio: {r.max_ship_length:.2f} m"
        )

    def selected_route_one_line(self) -> str:
        r = self.get_selected_route()
        if not r:
            return "—"
        return f"{r.name} — {r.distance_nm:.0f} nm"

    def waypoints_for_route(self, route_id: int) -> tuple[PortWaypoint, ...]:
        return self.route_waypoints.get(route_id, ())

    def filtered_routes_for_selected_ports(self) -> list[RouteRow]:
        """Filtra rotas pelo porto inicial/final escolhidos no ecrã 5."""
        start_port = self.porto_carga_var.get().strip()
        end_port = self.porto_descarga_var.get().strip()

        if not start_port and not end_port:
            return list(self.routes_catalog)

        filtered: list[RouteRow] = []
        for route in self.routes_catalog:
            waypoints = self.waypoints_for_route(route.id)
            if not waypoints:
                continue

            first_name = waypoints[0].name.strip()
            last_name = waypoints[-1].name.strip()

            if start_port and first_name != start_port:
                continue
            if end_port and last_name != end_port:
                continue
            filtered.append(route)

        return filtered

    def get_selected_ship(self) -> ShipRow | None:
        for s in self.ships_catalog:
            if s.id == self.selected_ship_id:
                return s
        return self.ships_catalog[0] if self.ships_catalog else None

    def selected_ship_display_name(self) -> str:
        s = self.get_selected_ship()
        return s.name if s else "—"

    def available_cargo_type_ids(self) -> list[int]:
        """Tipos de carga (tabela cargo_type) que têm linhas em cargo"""
        have = set(self.cargo_by_type_id.keys())
        return [t.id for t in self.cargo_types_catalog if t.id in have]

    def cargo_type_display_name(self, type_id: int) -> str:
        for t in self.cargo_types_catalog:
            if t.id == type_id:
                return t.name
        return str(type_id)

    def get_cargo_type(self, type_id: int) -> CargoTypeRow | None:
        for t in self.cargo_types_catalog:
            if t.id == type_id:
                return t
        return None

    def _first_cargo_id_in_type(self, type_id: int) -> int | None:
        lst = self.cargo_by_type_id.get(type_id) or []
        return lst[0].id if lst else None

    def get_selected_cargo(self) -> CargoRow | None:
        cid = self.selected_cargo_id_var.get()
        for c in self.cargo_catalog:
            if c.id == cid:
                return c
        return self.cargo_catalog[0] if self.cargo_catalog else None

    def selected_cargo_type_label(self) -> str:
        c = self.get_selected_cargo()
        return c.cargo_type_name if c else "—"

    def selected_cargo_one_line(self) -> str:
        c = self.get_selected_cargo()
        if not c:
            return "—"
        return f"{c.cargo_name} ({self.selected_cargo_type_label()})"

    def weather_combo_values(self) -> list[str]:
        if self.weather_names:
            return list(self.weather_names)
        return ["Mar moderado", "Bonança"]

    def ensure_ship_compatible_with_cargo(self) -> None:
        """Se o navio atual não for compatível com a carga, seleciona o primeiro compatível."""
        ok = {s.id for s in self.ships_for_selected_cargo()}
        if ok and self.selected_ship_id not in ok:
            self.selected_ship_id = min(ok)

    def ships_for_selected_cargo(self) -> list[ShipRow]:
        """Navios compatíveis com a carga escolhida (contentor vs líquido), com base no tipo na BD."""
        c = self.get_selected_cargo()
        all_s = self.ships_catalog
        if not c or not all_s:
            return list(all_s)

        def is_tanker_type(name: str) -> bool:
            n = (name or "").lower()
            return any(x in n for x in ("líquid", "liquido", "tanque", "químic", "granel"))

        def is_container_type(name: str) -> bool:
            n = (name or "").lower()
            return any(x in n for x in ("contentor", "porta-content", "container"))

        if not c.need_container:
            hit = [s for s in all_s if is_tanker_type(s.ship_type_name)]
            return hit if hit else list(all_s)
        hit = [s for s in all_s if is_container_type(s.ship_type_name)]
        return hit if hit else list(all_s)
