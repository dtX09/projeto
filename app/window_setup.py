"""Configuração inicial da janela (DPI, escala, maximizar)."""

from __future__ import annotations

import ctypes
import tkinter as tk

from app.views.cargonautica_constants import BG_DARK


def configure_window(root: tk.Tk) -> None:
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    try:
        root.tk.call("tk", "scaling", 1.2)
    except Exception:
        pass
    root.title("CargoNautica")
    root.configure(bg=BG_DARK)
    root.after(0, lambda: _maximize_window(root))


def _maximize_window(root: tk.Tk) -> None:
    try:
        root.state("zoomed")
    except Exception:
        try:
            root.attributes("-zoomed", True)
        except Exception:
            root.geometry("1200x800")
