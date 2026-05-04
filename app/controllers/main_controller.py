"""Controlador: casca da janela + navegação entre vistas."""

from __future__ import annotations

import tkinter as tk

from app.models.simulator_model import SimulatorModel
from app.views.cargonautica_constants import BG_DARK, FOOTER_BG, HEADER_BG, SIDEBAR_BG, TEXT_MUTED, F_SMALL
from app.views.dashboard_view import DashboardView
from app.views.screen1_view import mount_screen1
from app.views.screen2_view import mount_screen2
from app.views.screen3_view import mount_screen3
from app.views.screen10_view import mount_screen10
from app.views.screen11_view import mount_screen11
from app.views.ui_widgets import themed_btn

_SIDEBAR_SCREENS = frozenset({"screen4", "screen5", "screen6", "screen7", "screen7b", "screen8", "screen9"})
_SIDEBAR_BACK_TARGETS = {
    "screen4": "screen3",
    "screen5": "screen4",
    "screen6": "screen5",
    "screen7": "screen6",
    "screen7b": "screen7",
    "screen8": "screen7",
    "screen9": "screen8",
}


class MainController:
    def __init__(self, root: tk.Tk, model: SimulatorModel) -> None:
        self._root = root
        self._model = model
        self._dashboard = DashboardView(model, self.go)
        self._current_screen: str | None = None
        self._screen3_back_target = "screen1"
        self._apply_global_text_scale()

        self._build_shell()
        self.go("screen1")

    def _apply_global_text_scale(self) -> None:
        """Aumenta a escala tipográfica global para 175% do valor atual."""
        current_scale = float(self._root.tk.call("tk", "scaling"))
        self._root.tk.call("tk", "scaling", current_scale * 1.45)

    def _build_shell(self) -> None:
        self._header = tk.Frame(self._root, bg=HEADER_BG, height=60)
        self._header.pack(fill="x")
        self._header.pack_propagate(False)
        self._build_header(self._header)

        self._body = tk.Frame(self._root, bg=BG_DARK)
        self._body.pack(fill="both", expand=True)

        self._content = tk.Frame(self._body, bg=BG_DARK)
        self._content.pack(side="left", fill="both", expand=True)

        # Botão "Voltar" flutuante para manter posição fixa nos ecrãs 4-9.
        self._floating_back_btn = themed_btn(self._body, "Voltar", lambda: None, secondary=True, w=100)
        self._floating_back_btn.place_forget()

        self._sidebar_frame = tk.Frame(self._body, bg=SIDEBAR_BG, width=240)
        self._sidebar_frame.pack(side="left", fill="y")
        self._sidebar_frame.pack_propagate(False)
        self._sidebar_frame.pack_forget()

        self._footer = tk.Frame(self._root, bg=FOOTER_BG, height=28)
        self._footer.pack(fill="x", side="bottom")
        self._footer.pack_propagate(False)

        tk.Label(
            self._footer,
            text="Departamento de Engenharia Marítima – 2026 @ ALL RIGHTS RESERVED",
            bg=FOOTER_BG,
            fg=TEXT_MUTED,
            font=F_SMALL,
        ).pack(expand=True)

    def _build_header(self, parent: tk.Frame) -> None:
        logo_f = tk.Frame(parent, bg=HEADER_BG)
        logo_f.pack(side="left", padx=14, pady=8)

        if self._model.logo_img:
            tk.Label(logo_f, image=self._model.logo_img, bg=HEADER_BG).pack(side="left")
        else:
            tk.Label(
                logo_f,
                text="ESCOLA SUPERIOR NÁUTICA INFANTE D. HENRIQUE",
                bg=HEADER_BG,
                fg="#e8f0f8",
                font=("Georgia", 12, "bold"),
            ).pack(side="left")

    def go(self, screen: str) -> None:
        previous_screen = self._current_screen
        if screen == "screen3":
            if previous_screen in {"screen1", "screen2"}:
                self._screen3_back_target = previous_screen

        for w in self._content.winfo_children():
            w.destroy()

        if screen in _SIDEBAR_SCREENS:
            self._sidebar_frame.pack(side="left", fill="y", before=self._content)
            active = "screen7" if screen == "screen7b" else screen
            self._dashboard.rebuild_sidebar(self._sidebar_frame, active)
            back_target = _SIDEBAR_BACK_TARGETS.get(screen)
            if back_target is not None:
                self._floating_back_btn.bind("<Button-1>", lambda _e, t=back_target: self.go(t))
                self._floating_back_btn.place(x=20, rely=1.0, y=-56)
                self._floating_back_btn.lift()
        else:
            self._sidebar_frame.pack_forget()
            self._floating_back_btn.place_forget()

        if screen == "screen1":
            mount_screen1(self._content, self._model, self.go)
        elif screen == "screen2":
            mount_screen2(self._content, self._model, self.go)
        elif screen == "screen3":
            mount_screen3(
                self._content,
                self._model,
                self.go,
                go_back=lambda: self.go(self._screen3_back_target),
            )
        elif screen == "screen10":
            mount_screen10(self._content, self._model, self.go)
        elif screen == "screen11":
            mount_screen11(self._content, self._model, self.go)
        elif screen in _SIDEBAR_SCREENS:
            self._dashboard.render(self._content, screen)

        self._current_screen = screen
