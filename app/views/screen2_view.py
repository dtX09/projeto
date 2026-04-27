"""Vista 2 — opções docente."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from typing import TYPE_CHECKING

from app.views.cargonautica_constants import BG_DARK, BG_PANEL, BORDER, TEXT_MUTED, TEXT_WHITE
from app.views.ui_widgets import themed_btn

if TYPE_CHECKING:
    from app.models.simulator_model import SimulatorModel


def mount_screen2(
    parent: tk.Widget,
    model: SimulatorModel,
    navigate: Callable[[str], None],
) -> None:
    f = tk.Frame(parent, bg=BG_DARK)
    f.pack(fill="both", expand=True, padx=20, pady=16)

    center = tk.Frame(f, bg=BG_DARK)
    center.pack(fill="both", expand=True)

    box = tk.Frame(
        center,
        bg=BG_PANEL,
        padx=40,
        pady=30,
        highlightbackground=BORDER,
        highlightthickness=1,
    )
    box.pack(expand=True)

    tk.Label(
        box,
        text="Escolha uma opção para prosseguir",
        bg=BG_PANEL,
        fg=TEXT_WHITE,
        font=("Georgia", 15, "bold"),
    ).pack(pady=(0, 8))

    tk.Label(
        box,
        text="",
        bg=BG_PANEL,
        fg=TEXT_MUTED,
        font=("Helvetica", 8),
    ).pack(pady=(0, 6))

    btn_frame = tk.Frame(box, bg=BG_PANEL)
    btn_frame.pack(pady=(12, 0))

    themed_btn(btn_frame, "Retomar plano de estiva", lambda: navigate("screen3"), w=220).pack(pady=2)
    tk.Frame(btn_frame, bg=BG_PANEL, height=8).pack()
    themed_btn(btn_frame, "Criar novo plano de estiva", lambda: navigate("screen10"), w=220).pack(pady=2)

    nav = tk.Frame(f, bg=BG_DARK)
    nav.pack(fill="x", pady=(8, 0))

    themed_btn(nav, "Voltar", lambda: navigate("screen1"), secondary=True, w=100).pack(side="left", pady=2)
