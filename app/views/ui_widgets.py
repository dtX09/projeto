"""Botões e painéis reutilizáveis (estilo slides)."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable

from app.views.cargonautica_constants import (
    ACCENT,
    BG_CARD,
    BG_DARK,
    BG_PANEL,
    BORDER,
    BTN_HOVER,
    BTN_PRIMARY,
    BTN_SEC_HOV,
    BTN_SECONDARY,
    TEXT_MUTED,
    TEXT_WHITE,
    F_BODY,
    F_BTN,
    F_SMALL,
    F_TITLE,
)


def themed_btn(
    parent: tk.Widget,
    text: str,
    command: Callable[[], None],
    *,
    w: int = 160,
    secondary: bool = False,
) -> tk.Label:
    bg = BTN_SECONDARY if secondary else BTN_PRIMARY
    hov = BTN_SEC_HOV if secondary else BTN_HOVER

    btn = tk.Label(
        parent,
        text=text,
        bg=bg,
        fg=TEXT_WHITE,
        font=F_BTN,
        cursor="hand2",
        width=w // 8,
        pady=6,
        relief="flat",
    )

    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>", lambda e: btn.config(bg=hov))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))

    return btn


def themed_panel(parent: tk.Widget, title: str) -> tk.Frame:
    outer = tk.Frame(parent, bg=BG_DARK, padx=14, pady=12)
    outer.pack(fill="both", expand=True)

    f = tk.Frame(outer, bg=BG_PANEL, padx=14, pady=12, highlightbackground=BORDER, highlightthickness=1)
    f.pack(fill="both", expand=True)

    tk.Label(f, text=title, bg=BG_PANEL, fg=TEXT_WHITE, font=F_TITLE).pack(anchor="w", pady=(0, 4))
    return f


def nav_row(
    parent: tk.Widget,
    back: str,
    next_: str | Callable[[], None],
    navigate: Callable[[str], None],
) -> None:
    nav = tk.Frame(parent, bg=BG_PANEL)
    nav.pack(fill="x", pady=(8, 0))

    themed_btn(nav, "Voltar", lambda: navigate(back), secondary=True, w=100).pack(side="left", pady=2)
    if isinstance(next_, str):
        next_cmd = lambda: navigate(next_)
    else:
        next_cmd = next_
    themed_btn(nav, "Próximo  ➜", next_cmd, w=130).pack(side="right", pady=2)
