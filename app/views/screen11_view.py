"""Vista 11 - placeholder visual (mesma estrutura do ecrã 10)."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from typing import TYPE_CHECKING

from app.views.cargonautica_constants import BG_DARK, BG_PANEL, BORDER
from app.views.ui_widgets import themed_btn

if TYPE_CHECKING:
    from app.models.simulator_model import SimulatorModel


def mount_screen11(
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

    nav = tk.Frame(frame, bg=BG_DARK)
    nav.pack(fill="x", pady=(8, 0))
    themed_btn(nav, "Voltar", lambda: navigate("screen2"), secondary=True, w=100).pack(side="left", pady=2)
