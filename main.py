import tkinter as tk


def main() -> None:
    root = tk.Tk()
    root.title("Minha App Desktop")

    # tamanho inicial da janela
    root.geometry("800x600")

    def go_to_second_page() -> None:
        # limpar a "primeira página"
        for widget in root.winfo_children():
            widget.destroy()

        # configurar segunda página
        root.configure(bg="white")
        label = tk.Label(
            root,
            text="Segunda página",
            bg="white",
            fg="#007BFF",
            font=("Segoe UI", 24, "bold"),
        )
        label.pack(pady=40)

        back_button = tk.Button(
            root,
            text="Voltar",
            bg="#007BFF",
            fg="white",
            padx=20,
            pady=10,
            borderwidth=0,
            highlightthickness=0,
            command=show_first_page,
        )
        back_button.pack(pady=20)

    def show_first_page() -> None:
        # limpar tudo e voltar à primeira página
        for widget in root.winfo_children():
            widget.destroy()

        root.configure(bg="#007BFF")

        button = tk.Button(
            root,
            text="Começar",
            bg="white",
            fg="#007BFF",
            padx=20,
            pady=10,
            borderwidth=0,
            highlightthickness=0,
            command=go_to_second_page,
        )
        button.pack(pady=40)

    # mostrar primeira página ao iniciar
    show_first_page()

    root.mainloop()


if __name__ == "__main__":
    main()

