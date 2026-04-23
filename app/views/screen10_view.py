"""Vista 10 - critérios de avaliação (sem sidebar)."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from typing import TYPE_CHECKING

from app.views.cargonautica_constants import BG_CARD, BG_DARK, BG_PANEL, BORDER, TEXT_MUTED, TEXT_WHITE
from app.views.ui_widgets import themed_btn

if TYPE_CHECKING:
    from app.models.simulator_model import SimulatorModel


def mount_screen10(
    parent: tk.Widget,
    model: SimulatorModel,
    navigate: Callable[[str], None],
) -> None:
    del model  # Mantem assinatura consistente com os outros ecras.

    frame = tk.Frame(parent, bg=BG_DARK)
    frame.pack(fill="both", expand=True, padx=20, pady=16)

    center = tk.Frame(frame, bg=BG_DARK)
    center.pack(fill="both", expand=True)

    panel = tk.Frame(
        center,
        bg=BG_PANEL,
        padx=28,
        pady=24,
        highlightbackground=BORDER,
        highlightthickness=1,
    )
    panel.pack(expand=True, fill="both", padx=20, pady=12)

    tk.Label(
        panel,
        text="Criterios de avaliacao",
        bg=BG_PANEL,
        fg=TEXT_WHITE,
        font=("Georgia", 15, "bold"),
    ).pack(pady=(0, 8))

    tk.Label(
        panel,
        text="Descreva os criterios usados para avaliar o plano de estiva.",
        bg=BG_PANEL,
        fg=TEXT_MUTED,
        font=("Helvetica", 9),
    ).pack(pady=(0, 10))

    input_wrap = tk.Frame(panel, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
    input_wrap.pack(expand=True, fill="both", padx=14, pady=(6, 0))

    criteria_input = tk.Text(
        input_wrap,
        bg=BG_CARD,
        fg=TEXT_WHITE,
        insertbackground=TEXT_WHITE,
        relief="flat",
        bd=0,
        wrap="word",
        font=("Helvetica", 10),
    )
    criteria_input.pack(fill="both", expand=True, padx=10, pady=10)
    criteria_input.focus_set()

    nav = tk.Frame(frame, bg=BG_DARK)
    nav.pack(fill="x", pady=(8, 0))
    themed_btn(nav, "Voltar", lambda: navigate("screen2"), secondary=True, w=100).pack(side="left", pady=2)
