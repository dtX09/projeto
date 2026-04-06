"""Vista 1 — boas-vindas / escolha de perfil."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from typing import TYPE_CHECKING

from PIL import Image, ImageTk

from app.views.cargonautica_constants import BG_DARK, BG_PANEL, BORDER, TEXT_MUTED, TEXT_WHITE
from app.views.cargonautica_constants import F_BODY, F_TITLE
from app.views.ui_widgets import themed_btn

if TYPE_CHECKING:
    from app.models.simulator_model import SimulatorModel


def mount_screen1(
    parent: tk.Widget,
    model: SimulatorModel,
    navigate: Callable[[str], None],
) -> None:
    canvas = tk.Canvas(parent, highlightthickness=0, bg=BG_DARK)
    canvas.pack(fill="both", expand=True)

    bg_id = None

    def redraw_bg(event=None):
        nonlocal bg_id
        w = max(1, canvas.winfo_width())
        h = max(1, canvas.winfo_height())

        if model.screen1_bg_src:
            img = model.screen1_bg_src.resize((w, h), Image.LANCZOS)
            model.screen1_bg = ImageTk.PhotoImage(img)

            if bg_id is None:
                bg_id = canvas.create_image(0, 0, image=model.screen1_bg, anchor="nw")
            else:
                canvas.itemconfig(bg_id, image=model.screen1_bg)
                canvas.coords(bg_id, 0, 0)

            canvas.tag_lower(bg_id)

        canvas.coords("centerbox", w // 2, h // 2)

    box = tk.Frame(
        canvas,
        bg=BG_PANEL,
        padx=40,
        pady=30,
        highlightbackground=BORDER,
        highlightthickness=1,
    )
    canvas.create_window(0, 0, window=box, tags="centerbox")

    tk.Label(
        box,
        text="Bem-vindo ao simulador de planeamento de estiva!",
        bg=BG_PANEL,
        fg=TEXT_WHITE,
        font=F_TITLE,
        wraplength=360,
        justify="center",
    ).pack(pady=(0, 4))

    tk.Label(
        box,
        text="Indique o seu perfil para continuar.",
        bg=BG_PANEL,
        fg=TEXT_MUTED,
        font=F_BODY,
    ).pack(pady=(0, 20))

    themed_btn(box, "Aluno", lambda: navigate("screen3"), w=180).pack(pady=2)
    tk.Frame(box, bg=BG_PANEL, height=6).pack()
    themed_btn(box, "Docente", lambda: navigate("screen2"), w=180).pack(pady=2)

    canvas.bind("<Configure>", redraw_bg)
    redraw_bg()
