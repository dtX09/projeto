"""
Dashboard do simulador: barra lateral + ecrãs 4–9 (fluxo liner).
"""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from typing import TYPE_CHECKING

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

        left = tk.Frame(body, bg=BG_PANEL)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        fields = [
            ("Porto de carga", self._model.porto_carga_var),
            ("Porto de descarga", self._model.porto_descarga_var),
            ("Prazo para entrega (ETA)", self._model.eta_var),
        ]

        for label, var in fields:
            grp = tk.Frame(left, bg=BG_PANEL)
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

        right = tk.Frame(body, bg="#050a0f", highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Mapa", bg="#050a0f", fg=TEXT_MUTED, font=F_BODY).pack(expand=True)
        self._draw_mini_map(right)

        nav_row(f, "screen4", "screen6", self._navigate)

    def _draw_mini_map(self, parent: tk.Widget) -> None:
        canvas = tk.Canvas(parent, bg="#071525", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=4, pady=4)

        def draw(e=None):
            canvas.delete("all")
            w, h = canvas.winfo_width(), canvas.winfo_height()

            if w < 2:
                return

            canvas.create_text(w // 2, h // 2, text="Visualização da rota", fill=TEXT_MUTED, font=F_SMALL)

            for i in range(0, w, 30):
                canvas.create_line(i, 0, i, h, fill="#0d2035", width=1)

            for j in range(0, h, 20):
                canvas.create_line(0, j, w, j, fill="#0d2035", width=1)

        canvas.bind("<Configure>", draw)

    def _screen_screen6(self, parent: tk.Widget) -> None:
        f = themed_panel(parent, "Opções de Rota")

        tk.Label(f, text="Selecione a rota mais adequada", bg=BG_PANEL, fg=TEXT_MUTED, font=F_BODY).pack(anchor="w")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        routes = [
            ("Rota A", "Lisboa → Roterdão\n3.200 nm / 8 dias\nFrequência: semanal"),
            ("Rota B", "Lisboa → Hamburgo\n3.900 nm / 10 dias\nFrequência: quinzenal"),
            ("Rota C", "Lisboa → Antuérpia\n2.800 nm / 7 dias\nFrequência: semanal"),
        ]

        for i, (name, info) in enumerate(routes):
            is_sel = i == self._model.selected_route.get()
            bg = BG_CARD_SEL if is_sel else BG_CARD

            card = tk.Frame(
                body,
                bg=bg,
                padx=12,
                pady=12,
                highlightbackground=ACCENT if is_sel else BORDER,
                highlightthickness=2 if is_sel else 1,
                cursor="hand2",
            )
            card.pack(side="left", fill="both", expand=True, padx=6)

            title_lbl = tk.Label(card, text=name, bg=bg, fg=TEXT_WHITE, font=F_HEADING)
            title_lbl.pack()

            info_lbl = tk.Label(card, text=info, bg=bg, fg=TEXT_MUTED, font=F_SMALL, justify="center")
            info_lbl.pack(pady=8)

            for widget in (card, title_lbl, info_lbl):
                widget.bind("<Button-1>", lambda e, idx=i: self._select_route(idx))

        nav_row(f, "screen5", "screen7", self._navigate)

    def _select_route(self, idx: int) -> None:
        self._model.selected_route.set(idx)
        self._navigate("screen6")

    def _screen_screen7(self, parent: tk.Widget) -> None:
        f = themed_panel(parent, "Navio Compatível")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        info_box = tk.Frame(body, bg=BG_CARD, padx=10, pady=10, width=160, highlightbackground=BORDER, highlightthickness=1)
        info_box.pack(side="left", fill="y", padx=(0, 12))
        info_box.pack_propagate(False)

        tk.Label(
            info_box,
            text="Info da Rota",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=F_SMALL,
            justify="left",
            wraplength=140,
        ).pack(anchor="nw")
        tk.Label(
            info_box,
            text="Rota C selecionada\nLisboa → Antuérpia\n2.800 nm\n7 dias",
            bg=BG_CARD,
            fg=TEXT_DARK,
            font=F_SMALL,
            justify="left",
        ).pack(anchor="nw", pady=6)

        ships = ["HMM Algeciras", "MSC Gülsün", "Ever Ace"]
        ship_frame = tk.Frame(body, bg=BG_PANEL)
        ship_frame.pack(side="left", fill="both", expand=True)

        for name in ships:
            col = tk.Frame(ship_frame, bg=BG_PANEL)
            col.pack(side="left", fill="both", expand=True, padx=4)

            img_box = tk.Frame(col, bg="#1a3050", height=90, highlightbackground=BORDER, highlightthickness=1)
            img_box.pack(fill="x")
            img_box.pack_propagate(False)

            tk.Label(img_box, text="🚢", bg="#1a3050", fg=ACCENT, font=("Helvetica", 28)).pack(expand=True)

            info = tk.Frame(col, bg=BG_CARD, pady=4, highlightbackground=BORDER, highlightthickness=1)
            info.pack(fill="x", pady=(4, 0))

            tk.Label(info, text=name, bg=BG_CARD, fg=TEXT_MUTED, font=F_SMALL, wraplength=110, justify="center").pack()

            themed_btn(col, "Selecionar", lambda n=name: self._select_ship(n), w=110).pack(pady=2)

        nav_row(f, "screen6", "screen8", self._navigate)

    def _select_ship(self, name: str) -> None:
        self._model.selected_ship = name
        self._navigate("screen7b")

    def _screen_screen7b(self, parent: tk.Widget) -> None:
        f = themed_panel(parent, "Navio Compatível")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        info_box = tk.Frame(body, bg=BG_CARD, padx=10, pady=10, width=160, highlightbackground=BORDER, highlightthickness=1)
        info_box.pack(side="left", fill="y", padx=(0, 12))
        info_box.pack_propagate(False)

        name = self._model.selected_ship

        tk.Label(info_box, text="Info da Rota", bg=BG_CARD, fg=TEXT_MUTED, font=F_SMALL).pack(anchor="nw")
        tk.Label(
            info_box,
            text="Rota C\nLisboa → Antuérpia\n2.800 nm / 7 dias",
            bg=BG_CARD,
            fg=TEXT_DARK,
            font=F_SMALL,
            justify="left",
        ).pack(anchor="nw", pady=6)

        right = tk.Frame(body, bg=BG_PANEL)
        right.pack(side="left", fill="both", expand=True)

        img_box = tk.Frame(right, bg="#1a3050", height=160, highlightbackground=ACCENT, highlightthickness=2)
        img_box.pack(fill="x")
        img_box.pack_propagate(False)

        tk.Label(img_box, text="🚢", bg="#1a3050", fg=ACCENT, font=("Helvetica", 50)).pack(expand=True)
        tk.Label(img_box, text=name, bg="#1a3050", fg=TEXT_WHITE, font=F_HEADING).pack(side="bottom", pady=4)

        data_box = tk.Frame(right, bg=BG_CARD, padx=14, pady=10, highlightbackground=BORDER, highlightthickness=1)
        data_box.pack(fill="x", pady=8)

        specs = [
            ("Comprimento", "399 m"),
            ("Boca", "61 m"),
            ("Capacidade", "23 964 TEU"),
            ("Calado máx.", "16.5 m"),
        ]

        for k, v in specs:
            row = tk.Frame(data_box, bg=BG_CARD)
            row.pack(fill="x", pady=1)

            tk.Label(row, text=f"{k}:", bg=BG_CARD, fg=TEXT_MUTED, font=F_SMALL, width=14, anchor="w").pack(side="left")
            tk.Label(row, text=v, bg=BG_CARD, fg=TEXT_WHITE, font=F_SMALL).pack(side="left")

        themed_btn(right, "Confirmar Navio", lambda: self._navigate("screen8"), w=160).pack(anchor="e", pady=2)
        nav_row(f, "screen7", "screen8", self._navigate)

    def _screen_screen8(self, parent: tk.Widget) -> None:
        f = themed_panel(parent, "Plano de Estiva")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        left = tk.Frame(body, bg=BG_CARD, padx=10, pady=10, highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="Resumo do Plano", bg=BG_CARD, fg=TEXT_WHITE, font=F_HEADING).pack(anchor="nw")

        route_names = ["Rota A – 3.200 nm", "Rota B – 3.900 nm", "Rota C – 2.800 nm"]
        idx = self._model.selected_route.get()
        route_text = route_names[idx] if 0 <= idx < len(route_names) else route_names[0]

        info_items = [
            ("Tipo de Rota", "Rota definida (liner)"),
            ("Carga", self._model.cargo_var.get()),
            ("Porto Carga", self._model.porto_carga_var.get() or "Lisboa"),
            ("Porto Descarga", self._model.porto_descarga_var.get() or "Antuérpia"),
            ("ETA", self._model.eta_var.get() or "20/11/2026"),
            ("Rota", route_text),
            ("Navio", self._model.selected_ship),
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
