"""
Dashboard do simulador: barra lateral + ecrãs 4–9 (fluxo liner).
"""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

from app.db.route_repository import RouteRow
from app.db.ship_repository import ShipRow
from app.utils.photo_loader import load_photoimage
from app.utils.world_route_map import WorldRouteMapController

from app.views.cargonautica_constants import (
    ACCENT,
    BG_CARD,
    BG_CARD_SEL,
    BG_DARK,
    BG_PANEL,
    BORDER,
    BTN_HOVER,
    BTN_PRIMARY,
    ORANGE,
    SIDEBAR_ACT,
    SIDEBAR_BG,
    TEXT_DARK,
    TEXT_MUTED,
    TEXT_WHITE,
    F_BODY,
    F_HEADING,
    F_SMALL,
    F_TITLE,
    F_SIDEBAR,
)
from app.views.ui_widgets import nav_row, themed_btn, themed_panel

if TYPE_CHECKING:
    from app.models.simulator_model import SimulatorModel

_SIDEBAR_ITEMS = [
    ("Tipo de Rota", "screen3"),
    ("Dados de carga", "screen4"),
    ("Dados Operação", "screen5"),
    ("Rotas Disponíveis", "screen6"),
    ("Dados Navios", "screen7"),
    ("Plano de Estiva", "screen8"),
]


class DashboardView:
    """Constrói a sidebar e o conteúdo dos ecrãs com painel (4–9)."""

    def __init__(self, model: SimulatorModel, navigate: Callable[[str], None]) -> None:
        self._model = model
        self._navigate = navigate

    def rebuild_sidebar(self, sidebar_frame: tk.Frame, active: str) -> None:
        for w in sidebar_frame.winfo_children():
            w.destroy()

        tk.Frame(sidebar_frame, bg=SIDEBAR_BG, height=10).pack(fill="x")

        for label, target in _SIDEBAR_ITEMS:
            is_active = target == active
            bg = SIDEBAR_ACT if is_active else SIDEBAR_BG

            row = tk.Frame(sidebar_frame, bg=bg, cursor="hand2")
            row.pack(fill="x", pady=1, padx=4)

            if is_active:
                tk.Label(row, text="▶", bg=bg, fg=TEXT_WHITE, font=("Helvetica", 8)).pack(side="left", padx=4)

            lbl = tk.Label(
                row,
                text=label,
                bg=bg,
                fg=TEXT_WHITE if is_active else TEXT_DARK,
                font=F_SIDEBAR,
                anchor="w",
                padx=10,
                pady=8,
            )
            lbl.pack(side="left", fill="x", expand=True)

            def on_enter(r=row, l=lbl, a=is_active):
                color = SIDEBAR_ACT if a else BTN_HOVER
                r.config(bg=color)
                l.config(bg=color)

            def on_leave(r=row, l=lbl, a=is_active):
                color = SIDEBAR_ACT if a else SIDEBAR_BG
                r.config(bg=color)
                l.config(bg=color)

            for widget in (row, lbl):
                widget.bind("<Button-1>", lambda e, t=target: self._navigate(t))
                widget.bind("<Enter>", lambda e, fn=on_enter: fn())
                widget.bind("<Leave>", lambda e, fn=on_leave: fn())

    def render(self, parent: tk.Widget, screen_name: str) -> None:
        fn = getattr(self, f"_screen_{screen_name}", None)
        if fn is None:
            return
        fn(parent)

    def _screen_screen4(self, parent: tk.Widget) -> None:
        f = themed_panel(parent, "Dados da Carga")
        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        left = tk.Frame(body, bg=BG_CARD, padx=12, pady=10, highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(left, text="Tipo de carga", bg=BG_CARD, fg=TEXT_WHITE, font=F_HEADING).pack(anchor="w", pady=(0, 10))

        options = [
            "Contentores (FCL)",
            "Contentores (LCL)",
            "Granéis sólidos",
            "Granéis líquidos",
            "Carga geral",
            "Ro-Ro",
        ]

        for opt in options:
            rb = tk.Radiobutton(
                left,
                text=opt,
                variable=self._model.cargo_var,
                value=opt,
                bg=BG_CARD,
                fg=TEXT_DARK,
                selectcolor=BG_CARD,
                activebackground=BG_CARD,
                font=F_BODY,
                indicatoron=True,
            )
            rb.pack(anchor="w", pady=2)

        right = tk.Frame(body, bg=BG_CARD, padx=12, pady=10, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Mais dados sobre a carga", bg=BG_CARD, fg=TEXT_MUTED, font=F_BODY).pack(expand=True)

        nav_row(f, "screen3", "screen5", self._navigate)

    def _screen_screen5(self, parent: tk.Widget) -> None:
        f = themed_panel(parent, "Configuração de Rota de Carga")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        fields_frame = tk.Frame(body, bg=BG_PANEL)
        fields_frame.pack(fill="both", expand=True)

        fields = [
            ("Porto de carga", self._model.porto_carga_var),
            ("Porto de descarga", self._model.porto_descarga_var),
            ("Prazo para entrega (ETA)", self._model.eta_var),
        ]

        for label, var in fields:
            grp = tk.Frame(fields_frame, bg=BG_PANEL)
            grp.pack(fill="x", pady=6)

            tk.Label(grp, text=label, bg=BG_PANEL, fg=TEXT_WHITE, font=F_HEADING).pack(anchor="w")

            ent = tk.Entry(
                grp,
                textvariable=var,
                bg=BG_CARD,
                fg=TEXT_WHITE,
                insertbackground=TEXT_WHITE,
                relief="flat",
                font=F_BODY,
                highlightbackground=BORDER,
                highlightthickness=1,
            )
            ent.pack(fill="x", ipady=5, pady=(4, 0))

        nav_row(f, "screen4", "screen6", self._navigate)

    def _build_scrollable_route_cards(
        self, list_parent: tk.Widget, routes: Sequence[RouteRow], map_controller: WorldRouteMapController
    ) -> None:
        """Lista vertical de cartões com scroll — suporta qualquer número de rotas."""
        scroll_wrap = tk.Frame(list_parent, bg=BG_PANEL)
        scroll_wrap.pack(fill="both", expand=True)

        canvas = tk.Canvas(scroll_wrap, bg=BG_PANEL, highlightthickness=0)
        vsb = tk.Scrollbar(scroll_wrap, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        inner = tk.Frame(canvas, bg=BG_PANEL)
        inner_win = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _stretch_inner(event) -> None:
            canvas.itemconfigure(inner_win, width=event.width)

        def _on_inner_configure(_event=None) -> None:
            canvas.configure(scrollregion=canvas.bbox("all"))
            w = inner.winfo_width()
            if w >= 40:
                wl = max(280, w - 28)
                for child in inner.winfo_children():
                    for sub in child.winfo_children():
                        if isinstance(sub, tk.Label):
                            sub.configure(wraplength=wl)

        inner.bind("<Configure>", _on_inner_configure)
        canvas.bind("<Configure>", _stretch_inner)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        wrap_init = 560

        def _wheel_windows(event) -> None:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _wheel_linux_up(_event) -> None:
            canvas.yview_scroll(-1, "units")

        def _wheel_linux_down(_event) -> None:
            canvas.yview_scroll(1, "units")

        def _bind_scroll(_event=None) -> None:
            scroll_wrap.bind_all("<MouseWheel>", _wheel_windows)
            scroll_wrap.bind_all("<Button-4>", _wheel_linux_up)
            scroll_wrap.bind_all("<Button-5>", _wheel_linux_down)

        def _unbind_scroll(_event=None) -> None:
            try:
                scroll_wrap.unbind_all("<MouseWheel>")
                scroll_wrap.unbind_all("<Button-4>")
                scroll_wrap.unbind_all("<Button-5>")
            except tk.TclError:
                pass

        scroll_wrap.bind("<Enter>", _bind_scroll)
        scroll_wrap.bind("<Leave>", _unbind_scroll)

        def _on_destroy(event) -> None:
            if event.widget is scroll_wrap:
                _unbind_scroll()

        scroll_wrap.bind("<Destroy>", _on_destroy)

        card_by_route: dict[int, tuple[tk.Frame, tk.Label, tk.Label]] = {}
        selected_id = self._model.selected_route_id.get()

        for r in routes:
            is_sel = r.id == selected_id
            bg = BG_CARD_SEL if is_sel else BG_CARD
            info = f"{r.ports_label}\n{r.distance_nm:.0f} nm\nFrequência: {r.frequency_days} dias"

            card = tk.Frame(
                inner,
                bg=bg,
                padx=14,
                pady=12,
                highlightbackground=ACCENT if is_sel else BORDER,
                highlightthickness=2 if is_sel else 1,
                cursor="hand2",
            )
            card.pack(fill="x", padx=4, pady=5)

            title_lbl = tk.Label(card, text=r.name, bg=bg, fg=TEXT_WHITE, font=F_HEADING, anchor="w", wraplength=wrap_init)
            title_lbl.pack(fill="x")

            info_lbl = tk.Label(
                card,
                text=info,
                bg=bg,
                fg=TEXT_MUTED,
                font=F_SMALL,
                justify="left",
                anchor="w",
                wraplength=wrap_init,
            )
            info_lbl.pack(fill="x", pady=(6, 0))

            rid = r.id
            card_by_route[rid] = (card, title_lbl, info_lbl)

            def on_pick(
                _event,
                route_id: int = rid,
                ctrl: WorldRouteMapController = map_controller,
            ) -> None:
                self._model.selected_route_id.set(route_id)
                for oid, (cf, tl, il) in card_by_route.items():
                    sel = oid == route_id
                    b = BG_CARD_SEL if sel else BG_CARD
                    cf.config(bg=b, highlightbackground=ACCENT if sel else BORDER, highlightthickness=2 if sel else 1)
                    tl.config(bg=b)
                    il.config(bg=b)
                wps = list(self._model.waypoints_for_route(route_id))
                ctrl.set_waypoints(wps)
                ctrl.refresh()

            for widget in (card, title_lbl, info_lbl):
                widget.bind("<Button-1>", on_pick)

        map_controller.set_waypoints(list(self._model.waypoints_for_route(selected_id)))
        map_controller.refresh()

    def _build_scrollable_ship_list(self, list_parent: tk.Widget, ships: Sequence[ShipRow]) -> None:
        """Lista vertical de navios com scroll (muitos navios)."""
        scroll_wrap = tk.Frame(list_parent, bg=BG_PANEL)
        scroll_wrap.pack(fill="both", expand=True)

        canvas = tk.Canvas(scroll_wrap, bg=BG_PANEL, highlightthickness=0)
        vsb = tk.Scrollbar(scroll_wrap, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        inner = tk.Frame(canvas, bg=BG_PANEL)
        inner_win = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _stretch_inner(event) -> None:
            canvas.itemconfigure(inner_win, width=event.width)

        def _on_inner_configure(_event=None) -> None:
            canvas.configure(scrollregion=canvas.bbox("all"))
            w = inner.winfo_width()
            if w >= 40:
                wl = max(260, w - 24)
                for child in inner.winfo_children():
                    for sub in child.winfo_children():
                        if isinstance(sub, tk.Label):
                            sub.configure(wraplength=wl)

        inner.bind("<Configure>", _on_inner_configure)
        canvas.bind("<Configure>", _stretch_inner)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        def _wheel_windows(event) -> None:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _wheel_linux_up(_event) -> None:
            canvas.yview_scroll(-1, "units")

        def _wheel_linux_down(_event) -> None:
            canvas.yview_scroll(1, "units")

        def _bind_scroll(_event=None) -> None:
            scroll_wrap.bind_all("<MouseWheel>", _wheel_windows)
            scroll_wrap.bind_all("<Button-4>", _wheel_linux_up)
            scroll_wrap.bind_all("<Button-5>", _wheel_linux_down)

        def _unbind_scroll(_event=None) -> None:
            try:
                scroll_wrap.unbind_all("<MouseWheel>")
                scroll_wrap.unbind_all("<Button-4>")
                scroll_wrap.unbind_all("<Button-5>")
            except tk.TclError:
                pass

        scroll_wrap.bind("<Enter>", _bind_scroll)
        scroll_wrap.bind("<Leave>", _unbind_scroll)

        def _on_destroy(event) -> None:
            if event.widget is scroll_wrap:
                _unbind_scroll()

        scroll_wrap.bind("<Destroy>", _on_destroy)

        sel_id = self._model.selected_ship_id

        for sh in ships:
            is_sel = sh.id == sel_id
            bg = BG_CARD_SEL if is_sel else BG_CARD
            card = tk.Frame(
                inner,
                bg=bg,
                padx=12,
                pady=10,
                highlightbackground=ACCENT if is_sel else BORDER,
                highlightthickness=2 if is_sel else 1,
            )
            card.pack(fill="x", padx=4, pady=5)

            tk.Label(card, text=sh.name, bg=bg, fg=TEXT_WHITE, font=F_HEADING, anchor="w").pack(fill="x")
            detail = (
                f"{sh.ship_type_name}\nIMO {sh.imo_number}\n"
                f"Compr. {sh.length:.1f} m × Boca {sh.width:.2f} m\n"
                f"GT {sh.gt:.0f} · DWT {sh.dwt:.0f} t · Calado máx. {sh.max_draft:.2f} m"
            )
            tk.Label(card, text=detail, bg=bg, fg=TEXT_MUTED, font=F_SMALL, justify="left", anchor="w").pack(
                fill="x", pady=(4, 0)
            )

            sid = sh.id
            themed_btn(card, "Selecionar", lambda i=sid: self._select_ship(i), w=120).pack(anchor="w", pady=(8, 0))

    def _screen_screen6(self, parent: tk.Widget) -> None:
        f = themed_panel(parent, "Opções de Rota")

        tk.Label(
            f,
            text="Selecione uma rota — mapa mundial (mundo.png) com trajeto e portos assinalados.",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=F_BODY,
            wraplength=720,
            justify="left",
        ).pack(anchor="w")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        if self._model.routes_load_error:
            tk.Label(
                body,
                text=f"Não foi possível ligar à base de dados.\n{self._model.routes_load_error}",
                bg=BG_PANEL,
                fg="#e0a030",
                font=F_SMALL,
                justify="left",
            ).pack(anchor="w", pady=8)
        elif not self._model.routes_catalog:
            tk.Label(
                body,
                text="Não existem rotas na tabela route. Execute o script de seed (scriptSeedBaseDados.sql).",
                bg=BG_PANEL,
                fg=TEXT_MUTED,
                font=F_BODY,
                justify="left",
            ).pack(anchor="w", pady=8)
        else:
            split = tk.Frame(body, bg=BG_PANEL)
            split.pack(fill="both", expand=True)

            list_col = tk.Frame(split, bg=BG_PANEL, width=340)
            list_col.pack(side="left", fill="y", padx=(0, 10))
            list_col.pack_propagate(False)

            map_col = tk.Frame(split, bg="#050a0f", highlightbackground=BORDER, highlightthickness=1)
            map_col.pack(side="left", fill="both", expand=True)

            tk.Label(
                map_col,
                text="Trajeto da rota (mapa mundial)",
                bg="#050a0f",
                fg=TEXT_MUTED,
                font=F_SMALL,
            ).pack(anchor="w", padx=10, pady=(8, 4))

            map_canvas = tk.Canvas(map_col, bg="#071525", highlightthickness=0)
            map_canvas.pack(fill="both", expand=True, padx=8, pady=(0, 8))

            map_controller = WorldRouteMapController(map_canvas)

            self._build_scrollable_route_cards(list_col, self._model.routes_catalog, map_controller)

        nav_row(f, "screen5", "screen7", self._navigate)

    def _screen_screen7(self, parent: tk.Widget) -> None:
        f = themed_panel(parent, "Navio Compatível")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        route_wrap = 200
        info_box = tk.Frame(body, bg=BG_CARD, padx=10, pady=10, width=220, highlightbackground=BORDER, highlightthickness=1)
        info_box.pack(side="left", fill="y", padx=(0, 12))
        info_box.pack_propagate(False)

        tk.Label(
            info_box,
            text="Info da Rota",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=F_SMALL,
            justify="left",
            wraplength=route_wrap,
        ).pack(anchor="nw")
        tk.Label(
            info_box,
            text=self._model.selected_route_summary_lines(),
            bg=BG_CARD,
            fg=TEXT_DARK,
            font=F_SMALL,
            justify="left",
            wraplength=route_wrap,
        ).pack(anchor="nw", pady=6)

        ships_col = tk.Frame(body, bg=BG_PANEL)
        ships_col.pack(side="left", fill="both", expand=True)

        if self._model.ships_load_error:
            tk.Label(
                ships_col,
                text=f"Não foi possível carregar navios.\n{self._model.ships_load_error}",
                bg=BG_PANEL,
                fg="#e0a030",
                font=F_SMALL,
                justify="left",
            ).pack(anchor="w")
        elif not self._model.ships_catalog:
            tk.Label(
                ships_col,
                text="Não existem navios na base de dados.",
                bg=BG_PANEL,
                fg=TEXT_MUTED,
                font=F_BODY,
            ).pack(anchor="w")
        else:
            tk.Label(
                ships_col,
                text="Navios disponíveis (base de dados) — use o scroll se a lista for longa.",
                bg=BG_PANEL,
                fg=TEXT_MUTED,
                font=F_SMALL,
            ).pack(anchor="w", pady=(0, 6))
            self._build_scrollable_ship_list(ships_col, self._model.ships_catalog)

        nav_row(f, "screen6", "screen7b", self._navigate)

    def _select_ship(self, ship_id: int) -> None:
        self._model.selected_ship_id = ship_id
        self._navigate("screen7b")

    def _screen_screen7b(self, parent: tk.Widget) -> None:
        f = themed_panel(parent, "Confirmar Navio")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        route_wrap = 200
        info_box = tk.Frame(body, bg=BG_CARD, padx=10, pady=10, width=220, highlightbackground=BORDER, highlightthickness=1)
        info_box.pack(side="left", fill="y", padx=(0, 12))
        info_box.pack_propagate(False)

        tk.Label(
            info_box,
            text="Info da Rota",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=F_SMALL,
            wraplength=route_wrap,
        ).pack(anchor="nw")
        tk.Label(
            info_box,
            text=self._model.selected_route_summary_lines(),
            bg=BG_CARD,
            fg=TEXT_DARK,
            font=F_SMALL,
            justify="left",
            wraplength=route_wrap,
        ).pack(anchor="nw", pady=6)

        right = tk.Frame(body, bg=BG_PANEL)
        right.pack(side="left", fill="both", expand=True)

        ship = self._model.get_selected_ship()
        self._model.ship_confirm_photo = None

        img_box = tk.Frame(right, bg="#1a3050", height=220, highlightbackground=ACCENT, highlightthickness=2)
        img_box.pack(fill="x")
        img_box.pack_propagate(False)

        if ship and ship.photo_url:
            try:
                self._model.ship_confirm_photo = load_photoimage(ship.photo_url, max_size=(720, 280))
                tk.Label(img_box, image=self._model.ship_confirm_photo, bg="#1a3050").pack(
                    expand=True, fill="both", padx=4, pady=4
                )
            except Exception:
                tk.Label(img_box, text="🚢", bg="#1a3050", fg=ACCENT, font=("Helvetica", 48)).pack(expand=True, pady=12)
        else:
            tk.Label(img_box, text="🚢", bg="#1a3050", fg=ACCENT, font=("Helvetica", 48)).pack(expand=True, pady=12)

        name_lbl = ship.name if ship else "—"
        tk.Label(right, text=name_lbl, bg=BG_PANEL, fg=TEXT_WHITE, font=F_HEADING).pack(anchor="w", pady=(6, 4))

        data_box = tk.Frame(right, bg=BG_CARD, padx=14, pady=10, highlightbackground=BORDER, highlightthickness=1)
        data_box.pack(fill="x", pady=8)

        if ship:
            specs = [
                ("Tipo", ship.ship_type_name),
                ("IMO", ship.imo_number),
                ("Ano", str(ship.built_year)),
                ("Comprimento", f"{ship.length:.1f} m"),
                ("Boca", f"{ship.width:.2f} m"),
                ("Altura", f"{ship.height:.2f} m"),
                ("GT", f"{ship.gt:.0f} t"),
                ("DWT", f"{ship.dwt:.0f} t"),
                ("Calado máx.", f"{ship.max_draft:.2f} m"),
                ("Velocidade", f"{ship.speed_knots:.1f} kn"),
            ]
        else:
            specs = []

        for k, v in specs:
            row = tk.Frame(data_box, bg=BG_CARD)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=f"{k}:", bg=BG_CARD, fg=TEXT_MUTED, font=F_SMALL, width=14, anchor="w").pack(side="left")
            tk.Label(row, text=v, bg=BG_CARD, fg=TEXT_WHITE, font=F_SMALL, wraplength=400, anchor="w").pack(
                side="left", fill="x"
            )

        if ship and ship.description:
            tk.Label(
                data_box,
                text=ship.description,
                bg=BG_CARD,
                fg=TEXT_DARK,
                font=F_SMALL,
                wraplength=520,
                justify="left",
            ).pack(anchor="w", pady=(8, 0))

        themed_btn(right, "Confirmar Navio", lambda: self._navigate("screen8"), w=160).pack(anchor="e", pady=2)
        nav_row(f, "screen7", "screen8", self._navigate)

    def _screen_screen8(self, parent: tk.Widget) -> None:
        f = themed_panel(parent, "Plano de Estiva")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        left = tk.Frame(body, bg=BG_CARD, padx=10, pady=10, highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="Resumo do Plano", bg=BG_CARD, fg=TEXT_WHITE, font=F_HEADING).pack(anchor="nw")

        route_text = self._model.selected_route_one_line()

        info_items = [
            ("Tipo de Rota", "Rota definida (liner)"),
            ("Carga", self._model.cargo_var.get()),
            ("Porto Carga", self._model.porto_carga_var.get() or "Lisboa"),
            ("Porto Descarga", self._model.porto_descarga_var.get() or "Antuérpia"),
            ("ETA", self._model.eta_var.get() or "20/11/2026"),
            ("Rota", route_text),
            ("Navio", self._model.selected_ship_display_name()),
        ]

        for k, v in info_items:
            r = tk.Frame(left, bg=BG_CARD)
            r.pack(fill="x", pady=2)

            tk.Label(r, text=f"{k}:", bg=BG_CARD, fg=TEXT_MUTED, font=F_SMALL, width=14, anchor="w").pack(side="left")
            tk.Label(r, text=v, bg=BG_CARD, fg=TEXT_WHITE, font=F_SMALL).pack(side="left")

        right = tk.Frame(body, bg=BG_PANEL)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right,
            text="Localização do contentor a visualizar",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=F_SMALL,
            wraplength=200,
            justify="center",
        ).pack(pady=(0, 6))

        bay_f = tk.Frame(right, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
        bay_f.pack(fill="both", expand=True)

        self._draw_bay_view(bay_f)

        themed_btn(right, "Editar Plano de Estiva", lambda: self._navigate("screen9"), w=180, secondary=True).pack(
            anchor="e", pady=(6, 0)
        )

        nav = tk.Frame(f, bg=BG_PANEL)
        nav.pack(fill="x", pady=(8, 0))

        themed_btn(nav, "Voltar", lambda: self._navigate("screen7"), secondary=True, w=100).pack(side="left", pady=2)
        themed_btn(nav, "Finalizar  ✔", lambda: self._finalizar(parent), w=140).pack(side="right", pady=2)

    def _draw_bay_view(self, parent: tk.Widget) -> None:
        canvas = tk.Canvas(parent, bg="#0d1a28", highlightthickness=0, height=160)
        canvas.pack(fill="x", padx=6, pady=6)

        def draw(e=None):
            canvas.delete("all")
            w = canvas.winfo_width()

            if w < 2:
                return

            canvas.create_text(w // 2, 10, text="Secção Transversal: Baía 10", fill=TEXT_WHITE, font=F_SMALL)

            cols, rows_n = 9, 5
            cw, ch = min(24, max(12, (w - 40) // cols)), 20
            ox = (w - cols * cw) // 2
            oy = 25

            colors = [BG_CARD] * (cols * rows_n)
            colors[13] = ORANGE
            colors[22] = "#c0c8d0"

            for r in range(rows_n):
                for c in range(cols):
                    idx = r * cols + c
                    x1, y1 = ox + c * cw, oy + r * ch
                    x2, y2 = x1 + cw - 2, y1 + ch - 2
                    canvas.create_rectangle(x1, y1, x2, y2, fill=colors[idx], outline="#1a2f45", width=1)

        canvas.bind("<Configure>", draw)

    def _finalizar(self, parent: tk.Widget) -> None:
        root = parent.winfo_toplevel()
        win = tk.Toplevel(root)
        win.title("Concluído")
        win.geometry("320x160")
        win.configure(bg=BG_DARK)
        win.grab_set()

        tk.Label(win, text="✔", bg=BG_DARK, fg="#30c070", font=("Helvetica", 36)).pack(pady=(20, 4))
        tk.Label(
            win,
            text="Plano de estiva finalizado com sucesso!",
            bg=BG_DARK,
            fg=TEXT_WHITE,
            font=F_BODY,
            wraplength=280,
        ).pack()

        themed_btn(win, "OK", win.destroy, w=80).pack(pady=12)

    def _screen_screen9(self, parent: tk.Widget) -> None:
        f = themed_panel(parent, "Plano de Estiva – Edição")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        val = tk.Frame(body, bg=BG_CARD, padx=10, pady=10, width=160, highlightbackground=BORDER, highlightthickness=1)
        val.pack(side="left", fill="y", padx=(0, 8))
        val.pack_propagate(False)

        tk.Label(val, text="Validações", bg=BG_CARD, fg=TEXT_WHITE, font=F_HEADING).pack(anchor="nw")

        validations = [
            ("✔ Estabilidade", "#30c070"),
            ("✔ Distribuição", "#30c070"),
            ("⚠ Peso por baia", "#e0a030"),
            ("✔ Segregação", "#30c070"),
        ]

        for txt, clr in validations:
            tk.Label(val, text=txt, bg=BG_CARD, fg=clr, font=F_SMALL, anchor="w").pack(fill="x", pady=3)

        mid = tk.Frame(body, bg=BG_CARD, padx=6, pady=6, highlightbackground=BORDER, highlightthickness=1)
        mid.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(mid, text="Visualização do Navio", bg=BG_CARD, fg=TEXT_MUTED, font=F_SMALL).pack()
        self._draw_ship_topview(mid)

        info = tk.Frame(body, bg=BG_PANEL, width=180)
        info.pack(side="left", fill="y")
        info.pack_propagate(False)

        cargo_box = tk.Frame(info, bg=BG_CARD, padx=10, pady=10, highlightbackground=BORDER, highlightthickness=1)
        cargo_box.pack(fill="x", pady=(0, 8))

        tk.Label(
            cargo_box,
            text="Que carga é, onde está e para onde vai",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=F_SMALL,
            wraplength=160,
            justify="left",
        ).pack(anchor="nw")

        tk.Label(
            cargo_box,
            text="MSCU1234567\n40' HC Dry\nLisboa → Antuérpia\nPeso: 28.4 t",
            bg=BG_CARD,
            fg=TEXT_DARK,
            font=F_SMALL,
            justify="left",
        ).pack(anchor="nw", pady=4)

        inf_box = tk.Frame(info, bg=BG_CARD, padx=10, pady=10, highlightbackground=BORDER, highlightthickness=1)
        inf_box.pack(fill="x")

        tk.Label(inf_box, text="Info sobre a carga", bg=BG_CARD, fg=TEXT_MUTED, font=F_SMALL).pack(anchor="nw")
        tk.Label(
            inf_box,
            text="Classe IMO: N/A\nIMDG: Não perigoso\nTemperatura: Ambiente\nVentilação: Normal",
            bg=BG_CARD,
            fg=TEXT_DARK,
            font=F_SMALL,
            justify="left",
        ).pack(anchor="nw", pady=4)

        nav = tk.Frame(f, bg=BG_PANEL)
        nav.pack(fill="x", pady=(8, 0))

        themed_btn(nav, "Voltar", lambda: self._navigate("screen8"), secondary=True, w=100).pack(side="left", pady=2)
        themed_btn(nav, "Finalizar  ✔", lambda: self._finalizar(parent), w=140).pack(side="right", pady=2)

    def _draw_ship_topview(self, parent: tk.Widget) -> None:
        canvas = tk.Canvas(parent, bg="#071525", highlightthickness=0)
        canvas.pack(fill="both", expand=True, pady=4)

        def draw(e=None):
            canvas.delete("all")
            w, h = canvas.winfo_width(), canvas.winfo_height()

            if w < 4:
                return

            bays = 10
            bw = max(18, (w - 20) // bays)
            oh = 8

            colors_row = [
                "#3060a0",
                "#3060a0",
                "#3060a0",
                BTN_PRIMARY,
                BTN_PRIMARY,
                "#c04030",
                "#c04030",
                "#3060a0",
                "#3060a0",
                "#3060a0",
            ]

            for row in range(3):
                y1 = oh + row * 18
                y2 = y1 + 15

                for b in range(bays):
                    x1 = 10 + b * bw
                    x2 = x1 + bw - 2
                    fill = colors_row[b] if row < 2 else "#1a2f45"
                    sel = b == 4 and row == 1

                    canvas.create_rectangle(
                        x1,
                        y1,
                        x2,
                        y2,
                        fill=ORANGE if sel else fill,
                        outline="#0a1828",
                    )

            ley = h - 16
            x = 10
            legend = [("General", "#3060a0"), ("Reefer", "#c04030"), ("Selected", ORANGE)]

            for label, color in legend:
                canvas.create_rectangle(x, ley, x + 10, ley + 10, fill=color, outline="")
                canvas.create_text(x + 14, ley + 5, text=label, fill=TEXT_MUTED, font=F_SMALL, anchor="w")
                x += 80

        canvas.bind("<Configure>", draw)
