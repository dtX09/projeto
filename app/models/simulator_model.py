"""Estado do simulador de estiva (variáveis Tk e imagens PIL)."""

from __future__ import annotations

import tkinter as tk
from PIL import Image, ImageTk


class SimulatorModel:
    def __init__(self, master: tk.Misc) -> None:
        self._master = master
        self.selected_ship = "HMM Algeciras"
        self.selected_route = tk.IntVar(master=master, value=2)
        self.cargo_var = tk.StringVar(master=master, value="Contentores (FCL)")
        self.porto_carga_var = tk.StringVar(master=master, value="")
        self.porto_descarga_var = tk.StringVar(master=master, value="")
        self.eta_var = tk.StringVar(master=master, value="20/11/2026")

        self.logo_img: ImageTk.PhotoImage | None = None
        self.screen1_bg: ImageTk.PhotoImage | None = None
        self.logo_src = None
        self.liner_src = None
        self.tramp_src = None
        self.screen1_bg_src = None
        self._load_images()

    def _load_images(self) -> None:
        try:
            self.logo_src = Image.open("imgs/ENIDH_ultra_horizontal_branco.png")
            logo = self.logo_src.resize((320, 44), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(logo)
        except Exception:
            self.logo_img = None

        try:
            self.liner_src = Image.open("imgs/boat2.jpg")
        except Exception:
            self.liner_src = None

        try:
            self.tramp_src = Image.open("imgs/boat1.jpg")
        except Exception:
            self.tramp_src = None

        try:
            self.screen1_bg_src = Image.open("imgs/backg.png")
        except Exception:
            self.screen1_bg_src = None
