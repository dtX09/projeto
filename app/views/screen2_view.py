"""Vista 2 — opções docente."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from typing import TYPE_CHECKING

from PIL import Image, ImageTk

from app.db.ship_photo_repository import fetch_first_ship_photo_url
from app.utils.photo_loader import open_pil_image
from app.views.cargonautica_constants import BG_DARK, BG_PANEL, BORDER, TEXT_MUTED, TEXT_WHITE
from app.views.ui_widgets import themed_btn

if TYPE_CHECKING:
    from app.models.simulator_model import SimulatorModel


def mount_screen2(
    parent: tk.Widget,
    model: SimulatorModel,
    navigate: Callable[[str], None],
) -> None:
    url, db_err = fetch_first_ship_photo_url()
    bg_src = None
    load_err: str | None = None
    if url and not db_err:
        try:
            bg_src = open_pil_image(url)
        except Exception as e:
            load_err = str(e)

    f = tk.Frame(parent, bg=BG_DARK)
    f.pack(fill="both", expand=True, padx=20, pady=16)

    canvas = tk.Canvas(f, highlightthickness=0, bg=BG_DARK)
    canvas.pack(fill="both", expand=True)

    bg_id = None
    photo_ref: list[ImageTk.PhotoImage | None] = [None]

    def redraw_bg(event=None):
        nonlocal bg_id
        w = max(1, canvas.winfo_width())
        h = max(1, canvas.winfo_height())

        if bg_src:
            img = bg_src.resize((w, h), Image.LANCZOS)
            photo_ref[0] = ImageTk.PhotoImage(img)

            if bg_id is None:
                bg_id = canvas.create_image(0, 0, image=photo_ref[0], anchor="nw")
            else:
                canvas.itemconfig(bg_id, image=photo_ref[0])
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
        text="Escolha uma opção para prosseguir",
        bg=BG_PANEL,
        fg=TEXT_WHITE,
        font=("Georgia", 15, "bold"),
    ).pack(pady=(0, 8))

    if db_err:
        tk.Label(
            box,
            text=f"BD: {db_err}",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=("Helvetica", 8),
            wraplength=320,
            justify="center",
        ).pack(pady=(0, 6))
    elif load_err:
        tk.Label(
            box,
            text=f"Imagem: {load_err}",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=("Helvetica", 8),
            wraplength=320,
            justify="center",
        ).pack(pady=(0, 6))
    elif not url and not db_err:
        tk.Label(
            box,
            text="Sem fotografia em ship_photo (tabela vazia).",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=("Helvetica", 8),
            wraplength=320,
            justify="center",
        ).pack(pady=(0, 6))

    btn_frame = tk.Frame(box, bg=BG_PANEL)
    btn_frame.pack(pady=(12, 0))

    themed_btn(btn_frame, "Retomar plano de estiva", lambda: navigate("screen3"), w=220).pack(pady=2)
    tk.Frame(btn_frame, bg=BG_PANEL, height=8).pack()
    themed_btn(btn_frame, "Criar novo plano de estiva", lambda: navigate("screen3"), w=220).pack(pady=2)

    nav = tk.Frame(f, bg=BG_DARK)
    nav.pack(fill="x", pady=(8, 0))

    themed_btn(nav, "Voltar", lambda: navigate("screen1"), secondary=True, w=100).pack(side="left", pady=2)

    canvas.bind("<Configure>", redraw_bg)
    redraw_bg()
