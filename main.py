"""Ponto de entrada — arranca a janela e o controlador MVC."""

import tkinter as tk

from app.controllers.main_controller import MainController
from app.models.simulator_model import SimulatorModel
from app.window_setup import configure_window


def main() -> None:
    root = tk.Tk()
    root.minsize(720, 480)
    configure_window(root)

    model = SimulatorModel(root)
    MainController(root, model)

    root.mainloop()


if __name__ == "__main__":
    main()
