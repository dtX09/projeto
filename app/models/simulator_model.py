"""Estado do simulador de estiva (variáveis Tk e imagens PIL)."""

from __future__ import annotations

import tkinter as tk
from PIL import Image, ImageTk

from app.db.route_repository import PortWaypoint, RouteRow, fetch_route_waypoints, fetch_routes
from app.db.ship_repository import ShipRow, fetch_ships


class SimulatorModel:
    def __init__(self, master: tk.Misc) -> None:
        self._master = master
        self.routes_catalog, self.routes_load_error = fetch_routes()
        self.ships_catalog, self.ships_load_error = fetch_ships()
        first_ship = self.ships_catalog[0].id if self.ships_catalog else 0
        self.selected_ship_id = first_ship
        self.ship_confirm_photo: ImageTk.PhotoImage | None = None
        self.route_waypoints: dict[int, tuple[PortWaypoint, ...]] = {}
        if not self.routes_load_error:
            self.route_waypoints, _ = fetch_route_waypoints()
        first_id = self.routes_catalog[0].id if self.routes_catalog else 0
        self.selected_route_id = tk.IntVar(master=master, value=first_id)
        self.cargo_var = tk.StringVar(master=master, value="Contentores (FCL)")
        self.porto_carga_var = tk.StringVar(master=master, value="")
        self.porto_descarga_var = tk.StringVar(master=master, value="")
        self.eta_var = tk.StringVar(master=master, value="20/11/2026")

        self.logo_img: ImageTk.PhotoImage | None = None
        self.screen1_bg: ImageTk.PhotoImage | None = None
        self.logo_src = None
        self.liner_src = None
        self.tramp_src = None
        self.screen1_bg_src = None
        self._load_images()

    def _load_images(self) -> None:
        try:
            self.logo_src = Image.open("imgs/ENIDH_ultra_horizontal_branco.png")
            logo = self.logo_src.resize((320, 44), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(logo)
        except Exception:
            self.logo_img = None

        try:
            self.liner_src = Image.open("imgs/boat2.jpg")
        except Exception:
            self.liner_src = None

        try:
            self.tramp_src = Image.open("imgs/boat1.jpg")
        except Exception:
            self.tramp_src = None

        try:
            self.screen1_bg_src = Image.open("imgs/backg.png")
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
        return f"{r.name}\n{r.ports_label}\n{r.distance_nm:.0f} nm\nFrequência: {r.frequency_days} dias"

    def selected_route_one_line(self) -> str:
        r = self.get_selected_route()
        if not r:
            return "—"
        return f"{r.name} — {r.distance_nm:.0f} nm"

    def waypoints_for_route(self, route_id: int) -> tuple[PortWaypoint, ...]:
        return self.route_waypoints.get(route_id, ())

    def get_selected_ship(self) -> ShipRow | None:
        for s in self.ships_catalog:
            if s.id == self.selected_ship_id:
                return s
        return self.ships_catalog[0] if self.ships_catalog else None

    def selected_ship_display_name(self) -> str:
        s = self.get_selected_ship()
        return s.name if s else "—"
