"""Vista 3 — tipo de planeamento (liner / tramp)."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from typing import TYPE_CHECKING

from PIL import Image, ImageTk

from app.views.cargonautica_constants import (
    ACCENT,
    BG_CARD,
    BG_DARK,
    BORDER,
    TEXT_MUTED,
    TEXT_WHITE,
    F_HEADING,
    F_SMALL,
)
from app.views.ui_widgets import themed_btn

if TYPE_CHECKING:
    from app.models.simulator_model import SimulatorModel


def _ship_card(
    parent: tk.Widget,
    col: int,
    title: str,
    desc: str,
    on_select: Callable[[], None] | None,
    img_src,
) -> None:
    card = tk.Frame(
        parent,
        bg=BG_CARD,
        padx=16,
        pady=16,
        highlightbackground=BORDER,
        highlightthickness=1,
    )
    card.grid(row=0, column=col, padx=14, pady=6, sticky="nsew")

    img_frame = tk.Frame(
        card,
        bg="#1a3050",
        height=420,
        highlightbackground=ACCENT,
        highlightthickness=2,
    )
    img_frame.pack(fill="x", pady=(0, 12))
    img_frame.pack_propagate(False)

    if img_src:
        lbl = tk.Label(img_frame, bg="#1a3050", bd=0, highlightthickness=0)
        lbl.pack(fill="both", expand=True)

        def update_card_image(event=None, frame=img_frame, label=lbl, src=img_src):
            w = max(1, frame.winfo_width() - 4)
            h = max(1, frame.winfo_height() - 4)

            img = src.copy()
            img.thumbnail((w, h), Image.LANCZOS)

            photo = ImageTk.PhotoImage(img)
            label.config(image=photo)
            label.image = photo

        img_frame.bind("<Configure>", update_card_image)
        update_card_image()
    else:
        tk.Label(
            img_frame,
            text="🚢",
            bg="#1a3050",
            fg=ACCENT,
            font=("Helvetica", 40),
        ).pack(expand=True)

    tk.Label(card, text=title, bg=BG_CARD, fg=TEXT_WHITE, font=F_HEADING).pack()
    tk.Label(
        card,
        text=desc,
        bg=BG_CARD,
        fg=TEXT_MUTED,
        font=F_SMALL,
        wraplength=280,
        justify="center",
    ).pack(pady=(6, 12))

    if on_select:
        themed_btn(card, "Selecionar  ➜", on_select, w=150).pack(pady=2)
    else:
        themed_btn(card, "Selecionar  ➜", lambda: None, w=150, secondary=True).pack(pady=2)


def mount_screen3(
    parent: tk.Widget,
    model: SimulatorModel,
    navigate: Callable[[str], None],
) -> None:
    f = tk.Frame(parent, bg=BG_DARK)
    f.pack(fill="both", expand=True, padx=20, pady=16)

    cards = tk.Frame(f, bg=BG_DARK)
    cards.pack(fill="both", expand=True)

    cards.columnconfigure(0, weight=1)
    cards.columnconfigure(1, weight=1)
    cards.rowconfigure(0, weight=1)

    _ship_card(
        cards,
        0,
        title="Rota definida (liner)",
        desc="A estiva é organizada com base numa rota fixa entre portos. Ideal para operações regulares de contentores e logística de linha.",
        on_select=lambda: navigate("screen4"),
        img_src=model.liner_src,
    )

    _ship_card(
        cards,
        1,
        title="Carga definida (tramp)",
        desc="O planeamento da viagem é feito com base na carga disponível. Focado em granéis, fretamento spot e rotas variáveis conforme a demanda.",
        on_select=None,
        img_src=model.tramp_src,
    )

    nav = tk.Frame(f, bg=BG_DARK)
    nav.pack(fill="x", pady=(8, 0))

    themed_btn(nav, "Voltar", lambda: navigate("screen1"), secondary=True, w=100).pack(side="left", pady=2)
