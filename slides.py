import tkinter as tk
from PIL import Image, ImageTk
import ctypes

# fix dpi no windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# ── colors ─────────────────────────────────────────────
BG_DARK       = "#1a2332"
BG_PANEL      = "#243447"
BG_CARD       = "#2d3f55"
BG_CARD_SEL   = "#4a5f80"
SIDEBAR_BG    = "#162030"
SIDEBAR_ACT   = "#2a7db8"
BTN_PRIMARY   = "#2a7db8"
BTN_HOVER     = "#3a9dd8"
BTN_SECONDARY = "#3a4f6a"
BTN_SEC_HOV   = "#4a6080"
ACCENT        = "#5ab0e8"
TEXT_WHITE    = "#e8f0f8"
TEXT_MUTED    = "#8a9bb0"
TEXT_DARK     = "#c0cdd8"
HEADER_BG     = "#0f1927"
FOOTER_BG     = "#0f1927"
BORDER        = "#3a5070"
ORANGE        = "#e07030"


class App(tk.Tk):
    # sidebar items
    SIDEBAR_ITEMS = [
        ("Tipo de Rota", "screen3"),
        ("Dados de carga", "screen4"),
        ("Dados Operação", "screen5"),
        ("Rotas Disponíveis", "screen6"),
        ("Dados Navios", "screen7"),
        ("Plano de Estiva", "screen8"),
    ]

    # screens com sidebar
    SIDEBAR_SCREENS = {"screen4", "screen5", "screen6", "screen7", "screen7b", "screen8", "screen9"}

    def __init__(self):
        super().__init__()
        self.title("CargoNautica")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # escala base
        try:
            self.tk.call("tk", "scaling", 1.2)
        except Exception:
            pass

        # state
        self.selected_ship = "HMM Algeciras"
        self.selected_route = tk.IntVar(value=2)
        self.cargo_var = tk.StringVar(value="Contentores (FCL)")

        # values da rota
        self.porto_carga_var = tk.StringVar(value="")
        self.porto_descarga_var = tk.StringVar(value="")
        self.eta_var = tk.StringVar(value="20/11/2026")

        self.logo_img = None
        self.screen1_bg = None

        self.logo_src = None
        self.liner_src = None
        self.tramp_src = None
        self.screen1_bg_src = None

        self.after(0, self._maximize_window)

        self._define_fonts()
        self._load_images()
        self._build_shell()
        self.show_screen("screen1")

    # maximizar janela
    def _maximize_window(self):
        try:
            self.state("zoomed")
        except Exception:
            try:
                self.attributes("-zoomed", True)
            except Exception:
                self.geometry("1200x800")

    # fontes
    def _define_fonts(self):
        self.f_title = ("Georgia", 14, "bold")
        self.f_heading = ("Georgia", 11, "bold")
        self.f_body = ("Helvetica", 9)
        self.f_small = ("Helvetica", 8)
        self.f_btn = ("Helvetica", 9, "bold")
        self.f_sidebar = ("Helvetica", 8, "bold")

    # carregar imagens
    def _load_images(self):
        try:
            self.logo_src = Image.open("ENIDH_ultra_horizontal_branco.png")
            logo = self.logo_src.resize((320, 44), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(logo)
        except Exception:
            self.logo_img = None

        try:
            self.liner_src = Image.open("cargo-ship-sailing-through-ocean.jpg")
        except Exception:
            self.liner_src = None

        try:
            self.tramp_src = Image.open("ai-generated-boat-picture.jpg")
        except Exception:
            self.tramp_src = None

        try:
            self.screen1_bg_src = Image.open("Gasc.png")
        except Exception:
            self.screen1_bg_src = None

    # shell principal
    def _build_shell(self):
        # header
        self.header = tk.Frame(self, bg=HEADER_BG, height=60)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        self._build_header(self.header)

        # body
        self.body = tk.Frame(self, bg=BG_DARK)
        self.body.pack(fill="both", expand=True)

        self.content = tk.Frame(self.body, bg=BG_DARK)
        self.content.pack(side="left", fill="both", expand=True)

        self.sidebar_frame = tk.Frame(self.body, bg=SIDEBAR_BG, width=155)
        self.sidebar_frame.pack(side="right", fill="y")
        self.sidebar_frame.pack_propagate(False)
        self.sidebar_frame.pack_forget()

        # footer
        self.footer = tk.Frame(self, bg=FOOTER_BG, height=28)
        self.footer.pack(fill="x", side="bottom")
        self.footer.pack_propagate(False)

        tk.Label(
            self.footer,
            text="Departamento de Engenharia Marítima – 2026 @ ALL RIGHTS RESERVED",
            bg=FOOTER_BG,
            fg=TEXT_MUTED,
            font=self.f_small
        ).pack(expand=True)

    # header
    def _build_header(self, parent):
        logo_f = tk.Frame(parent, bg=HEADER_BG)
        logo_f.pack(side="left", padx=14, pady=8)

        if self.logo_img:
            tk.Label(logo_f, image=self.logo_img, bg=HEADER_BG).pack(side="left")
        else:
            tk.Label(
                logo_f,
                text="ESCOLA SUPERIOR NÁUTICA INFANTE D. HENRIQUE",
                bg=HEADER_BG,
                fg=TEXT_WHITE,
                font=("Georgia", 12, "bold")
            ).pack(side="left")

    # sidebar
    def _build_sidebar(self, active):
        for w in self.sidebar_frame.winfo_children():
            w.destroy()

        tk.Frame(self.sidebar_frame, bg=SIDEBAR_BG, height=10).pack(fill="x")

        for label, target in self.SIDEBAR_ITEMS:
            is_active = target == active
            bg = SIDEBAR_ACT if is_active else SIDEBAR_BG

            row = tk.Frame(self.sidebar_frame, bg=bg, cursor="hand2")
            row.pack(fill="x", pady=1, padx=4)

            if is_active:
                tk.Label(row, text="▶", bg=bg, fg=TEXT_WHITE, font=("Helvetica", 8)).pack(side="left", padx=4)

            lbl = tk.Label(
                row,
                text=label,
                bg=bg,
                fg=TEXT_WHITE if is_active else TEXT_DARK,
                font=self.f_sidebar,
                anchor="w",
                padx=10,
                pady=8
            )
            lbl.pack(side="left", fill="x", expand=True)

            def on_enter(r=row, l=lbl, a=is_active):
                color = SIDEBAR_ACT if a else BTN_HOVER
                r.config(bg=color)
                l.config(bg=color)

            def on_leave(r=row, l=lbl, a=is_active):
                color = SIDEBAR_ACT if a else SIDEBAR_BG
                r.config(bg=color)
                l.config(bg=color)

            for widget in (row, lbl):
                widget.bind("<Button-1>", lambda e, t=target: self.show_screen(t))
                widget.bind("<Enter>", lambda e, fn=on_enter: fn())
                widget.bind("<Leave>", lambda e, fn=on_leave: fn())

    # router
    def show_screen(self, name):
        for w in self.content.winfo_children():
            w.destroy()

        if name in self.SIDEBAR_SCREENS:
            self.sidebar_frame.pack(side="right", fill="y")
            active = "screen7" if name == "screen7b" else name
            self._build_sidebar(active)
        else:
            self.sidebar_frame.pack_forget()

        getattr(self, f"_show_{name}")(self.content)

    # resize normal
    def _resize_image(self, pil_img, max_w, max_h):
        if pil_img is None:
            return None

        img = pil_img.copy()
        img.thumbnail((max_w, max_h), Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    # ────────────────────────────────────────────────────
    # TELA 1 - boas vindas / perfil
    # ────────────────────────────────────────────────────
    def _show_screen1(self, parent):
        canvas = tk.Canvas(parent, highlightthickness=0, bg=BG_DARK)
        canvas.pack(fill="both", expand=True)

        bg_id = None

        def redraw_bg(event=None):
            nonlocal bg_id
            w = max(1, canvas.winfo_width())
            h = max(1, canvas.winfo_height())

            if self.screen1_bg_src:
                img = self.screen1_bg_src.resize((w, h), Image.LANCZOS)
                self.screen1_bg = ImageTk.PhotoImage(img)

                if bg_id is None:
                    bg_id = canvas.create_image(0, 0, image=self.screen1_bg, anchor="nw")
                else:
                    canvas.itemconfig(bg_id, image=self.screen1_bg)
                    canvas.coords(bg_id, 0, 0)

                canvas.tag_lower(bg_id)

            canvas.coords("centerbox", w // 2, h // 2)

        box = tk.Frame(
            canvas,
            bg=BG_PANEL,
            padx=40,
            pady=30,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        canvas.create_window(0, 0, window=box, tags="centerbox")

        tk.Label(
            box,
            text="Bem-vindo ao simulador de planeamento de estiva!",
            bg=BG_PANEL,
            fg=TEXT_WHITE,
            font=self.f_title,
            wraplength=360,
            justify="center"
        ).pack(pady=(0, 4))

        tk.Label(
            box,
            text="Indique o seu perfil para continuar.",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=self.f_body
        ).pack(pady=(0, 20))

        self._btn(box, "Aluno", lambda: self.show_screen("screen3"), w=180).pack(pady=2)
        tk.Frame(box, bg=BG_PANEL, height=6).pack()
        self._btn(box, "Docente", lambda: self.show_screen("screen2"), w=180).pack(pady=2)

        canvas.bind("<Configure>", redraw_bg)
        redraw_bg()

    # ────────────────────────────────────────────────────
    # TELA 2 - opções docente
    # ────────────────────────────────────────────────────
    def _show_screen2(self, parent):
        f = tk.Frame(parent, bg=BG_DARK)
        f.pack(fill="both", expand=True, padx=20, pady=16)

        tk.Label(
            f,
            text="Escolha uma opção para prosseguir",
            bg=BG_DARK,
            fg=TEXT_WHITE,
            font=("Georgia", 15, "bold")
        ).pack(pady=(50, 30))

        btn_frame = tk.Frame(f, bg=BG_DARK)
        btn_frame.pack()

        self._btn(btn_frame, "Retomar plano de estiva", lambda: self.show_screen("screen3"), w=220).pack(pady=2)
        tk.Frame(btn_frame, bg=BG_DARK, height=8).pack()
        self._btn(btn_frame, "Criar novo plano de estiva", lambda: self.show_screen("screen3"), w=220).pack(pady=2)

        nav = tk.Frame(f, bg=BG_DARK)
        nav.pack(fill="x", side="bottom", pady=(8, 0))

        self._btn(nav, "Voltar", lambda: self.show_screen("screen1"), w=100, secondary=True).pack(side="left", pady=2)

    # ────────────────────────────────────────────────────
    # TELA 3 - tipo de planeamento
    # ────────────────────────────────────────────────────
    def _show_screen3(self, parent):
        f = tk.Frame(parent, bg=BG_DARK)
        f.pack(fill="both", expand=True, padx=20, pady=16)

        cards = tk.Frame(f, bg=BG_DARK)
        cards.pack(fill="both", expand=True)

        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)
        cards.rowconfigure(0, weight=1)

        self._ship_card(
            cards,
            0,
            title="Rota definida (liner)",
            desc="A estiva é organizada com base numa rota fixa entre portos. Ideal para operações regulares de contentores e logística de linha.",
            on_select=lambda: self.show_screen("screen4"),
            img_src=self.liner_src
        )

        self._ship_card(
            cards,
            1,
            title="Carga definida (tramp)",
            desc="O planeamento da viagem é feito com base na carga disponível. Focado em granéis, fretamento spot e rotas variáveis conforme a demanda.",
            on_select=None,
            img_src=self.tramp_src
        )

        nav = tk.Frame(f, bg=BG_DARK)
        nav.pack(fill="x", pady=(8, 0))

        self._btn(
            nav,
            "Voltar",
            lambda: self.show_screen("screen1"),
            secondary=True,
            w=100
        ).pack(side="left", pady=2)

    # card da tela 3
    def _ship_card(self, parent, col, title, desc, on_select, img_src=None):
        card = tk.Frame(
            parent,
            bg=BG_CARD,
            padx=16,
            pady=16,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.grid(row=0, column=col, padx=14, pady=6, sticky="nsew")

        img_frame = tk.Frame(
            card,
            bg="#1a3050",
            height=420,
            highlightbackground=ACCENT,
            highlightthickness=2
        )
        img_frame.pack(fill="x", pady=(0, 12))
        img_frame.pack_propagate(False)

        if img_src:
            lbl = tk.Label(img_frame, bg="#1a3050", bd=0, highlightthickness=0)
            lbl.pack(fill="both", expand=True)

            def update_card_image(event=None, frame=img_frame, label=lbl, src=img_src):
                w = max(1, frame.winfo_width() - 4)
                h = max(1, frame.winfo_height() - 4)

                img = src.copy()
                img.thumbnail((w, h), Image.LANCZOS)

                photo = ImageTk.PhotoImage(img)
                label.config(image=photo)
                label.image = photo

            img_frame.bind("<Configure>", update_card_image)
            update_card_image()
        else:
            tk.Label(
                img_frame,
                text="🚢",
                bg="#1a3050",
                fg=ACCENT,
                font=("Helvetica", 40)
            ).pack(expand=True)

        tk.Label(card, text=title, bg=BG_CARD, fg=TEXT_WHITE, font=self.f_heading).pack()
        tk.Label(card, text=desc, bg=BG_CARD, fg=TEXT_MUTED, font=self.f_small, wraplength=280, justify="center").pack(pady=(6, 12))

        if on_select:
            self._btn(card, "Selecionar  ➜", on_select, w=150).pack(pady=2)
        else:
            self._btn(card, "Selecionar  ➜", lambda: None, w=150, secondary=True).pack(pady=2)

    # ────────────────────────────────────────────────────
    # TELA 4 - dados da carga
    # ────────────────────────────────────────────────────
    def _show_screen4(self, parent):
        f = self._panel(parent, "Dados da Carga")
        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        left = tk.Frame(body, bg=BG_CARD, padx=12, pady=10, highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(left, text="Tipo de carga", bg=BG_CARD, fg=TEXT_WHITE, font=self.f_heading).pack(anchor="w", pady=(0, 10))

        options = [
            "Contentores (FCL)",
            "Contentores (LCL)",
            "Granéis sólidos",
            "Granéis líquidos",
            "Carga geral",
            "Ro-Ro"
        ]

        for opt in options:
            rb = tk.Radiobutton(
                left,
                text=opt,
                variable=self.cargo_var,
                value=opt,
                bg=BG_CARD,
                fg=TEXT_DARK,
                selectcolor=BG_CARD,
                activebackground=BG_CARD,
                font=self.f_body,
                indicatoron=True
            )
            rb.pack(anchor="w", pady=2)

        right = tk.Frame(body, bg=BG_CARD, padx=12, pady=10, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Mais dados sobre a carga", bg=BG_CARD, fg=TEXT_MUTED, font=self.f_body).pack(expand=True)

        self._nav_row(f, back="screen3", next_="screen5")

    # ────────────────────────────────────────────────────
    # TELA 5 - configuração da rota
    # ────────────────────────────────────────────────────
    def _show_screen5(self, parent):
        f = self._panel(parent, "Configuração de Rota de Carga")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        left = tk.Frame(body, bg=BG_PANEL)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        fields = [
            ("Porto de carga", self.porto_carga_var),
            ("Porto de descarga", self.porto_descarga_var),
            ("Prazo para entrega (ETA)", self.eta_var),
        ]

        for label, var in fields:
            grp = tk.Frame(left, bg=BG_PANEL)
            grp.pack(fill="x", pady=6)

            tk.Label(grp, text=label, bg=BG_PANEL, fg=TEXT_WHITE, font=self.f_heading).pack(anchor="w")

            ent = tk.Entry(
                grp,
                textvariable=var,
                bg=BG_CARD,
                fg=TEXT_WHITE,
                insertbackground=TEXT_WHITE,
                relief="flat",
                font=self.f_body,
                highlightbackground=BORDER,
                highlightthickness=1
            )
            ent.pack(fill="x", ipady=5, pady=(4, 0))

        right = tk.Frame(body, bg="#050a0f", highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Mapa", bg="#050a0f", fg=TEXT_MUTED, font=self.f_body).pack(expand=True)
        self._draw_mini_map(right)

        self._nav_row(f, back="screen4", next_="screen6")

    # mini mapa
    def _draw_mini_map(self, parent):
        canvas = tk.Canvas(parent, bg="#071525", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=4, pady=4)

        def draw(e=None):
            canvas.delete("all")
            w, h = canvas.winfo_width(), canvas.winfo_height()

            if w < 2:
                return

            canvas.create_text(w // 2, h // 2, text="Visualização da rota", fill=TEXT_MUTED, font=self.f_small)

            for i in range(0, w, 30):
                canvas.create_line(i, 0, i, h, fill="#0d2035", width=1)

            for j in range(0, h, 20):
                canvas.create_line(0, j, w, j, fill="#0d2035", width=1)

        canvas.bind("<Configure>", draw)

    # ────────────────────────────────────────────────────
    # TELA 6 - opções de rota
    # ────────────────────────────────────────────────────
    def _show_screen6(self, parent):
        f = self._panel(parent, "Opções de Rota")

        tk.Label(f, text="Selecione a rota mais adequada", bg=BG_PANEL, fg=TEXT_MUTED, font=self.f_body).pack(anchor="w")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        routes = [
            ("Rota A", "Lisboa → Roterdão\n3.200 nm / 8 dias\nFrequência: semanal"),
            ("Rota B", "Lisboa → Hamburgo\n3.900 nm / 10 dias\nFrequência: quinzenal"),
            ("Rota C", "Lisboa → Antuérpia\n2.800 nm / 7 dias\nFrequência: semanal"),
        ]

        for i, (name, info) in enumerate(routes):
            is_sel = i == self.selected_route.get()
            bg = BG_CARD_SEL if is_sel else BG_CARD

            card = tk.Frame(
                body,
                bg=bg,
                padx=12,
                pady=12,
                highlightbackground=ACCENT if is_sel else BORDER,
                highlightthickness=2 if is_sel else 1,
                cursor="hand2"
            )
            card.pack(side="left", fill="both", expand=True, padx=6)

            title_lbl = tk.Label(card, text=name, bg=bg, fg=TEXT_WHITE, font=self.f_heading)
            title_lbl.pack()

            info_lbl = tk.Label(card, text=info, bg=bg, fg=TEXT_MUTED, font=self.f_small, justify="center")
            info_lbl.pack(pady=8)

            for widget in (card, title_lbl, info_lbl):
                widget.bind("<Button-1>", lambda e, idx=i: self._select_route(idx))

        self._nav_row(f, back="screen5", next_="screen7")

    # selecionar rota
    def _select_route(self, idx):
        self.selected_route.set(idx)
        self.show_screen("screen6")

    # ────────────────────────────────────────────────────
    # TELA 7 - lista de navios
    # ────────────────────────────────────────────────────
    def _show_screen7(self, parent):
        f = self._panel(parent, "Navio Compatível")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        info_box = tk.Frame(body, bg=BG_CARD, padx=10, pady=10, width=160, highlightbackground=BORDER, highlightthickness=1)
        info_box.pack(side="left", fill="y", padx=(0, 12))
        info_box.pack_propagate(False)

        tk.Label(info_box, text="Info da Rota", bg=BG_CARD, fg=TEXT_MUTED, font=self.f_small, justify="left", wraplength=140).pack(anchor="nw")
        tk.Label(info_box, text="Rota C selecionada\nLisboa → Antuérpia\n2.800 nm\n7 dias", bg=BG_CARD, fg=TEXT_DARK, font=self.f_small, justify="left").pack(anchor="nw", pady=6)

        ships = ["HMM Algeciras", "MSC Gülsün", "Ever Ace"]
        ship_frame = tk.Frame(body, bg=BG_PANEL)
        ship_frame.pack(side="left", fill="both", expand=True)

        for name in ships:
            col = tk.Frame(ship_frame, bg=BG_PANEL)
            col.pack(side="left", fill="both", expand=True, padx=4)

            img_box = tk.Frame(col, bg="#1a3050", height=90, highlightbackground=BORDER, highlightthickness=1)
            img_box.pack(fill="x")
            img_box.pack_propagate(False)

            tk.Label(img_box, text="🚢", bg="#1a3050", fg=ACCENT, font=("Helvetica", 28)).pack(expand=True)

            info = tk.Frame(col, bg=BG_CARD, pady=4, highlightbackground=BORDER, highlightthickness=1)
            info.pack(fill="x", pady=(4, 0))

            tk.Label(info, text=name, bg=BG_CARD, fg=TEXT_MUTED, font=self.f_small, wraplength=110, justify="center").pack()

            self._btn(col, "Selecionar", lambda n=name: self._select_ship(n), w=110).pack(pady=2)

        self._nav_row(f, back="screen6", next_="screen8")

    # selecionar navio
    def _select_ship(self, name):
        self.selected_ship = name
        self.show_screen("screen7b")

    # ────────────────────────────────────────────────────
    # TELA 7B - detalhe do navio
    # ────────────────────────────────────────────────────
    def _show_screen7b(self, parent):
        self.sidebar_frame.pack(side="right", fill="y")
        self._build_sidebar("screen7")

        f = self._panel(parent, "Navio Compatível")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        info_box = tk.Frame(body, bg=BG_CARD, padx=10, pady=10, width=160, highlightbackground=BORDER, highlightthickness=1)
        info_box.pack(side="left", fill="y", padx=(0, 12))
        info_box.pack_propagate(False)

        name = self.selected_ship

        tk.Label(info_box, text="Info da Rota", bg=BG_CARD, fg=TEXT_MUTED, font=self.f_small).pack(anchor="nw")
        tk.Label(info_box, text="Rota C\nLisboa → Antuérpia\n2.800 nm / 7 dias", bg=BG_CARD, fg=TEXT_DARK, font=self.f_small, justify="left").pack(anchor="nw", pady=6)

        right = tk.Frame(body, bg=BG_PANEL)
        right.pack(side="left", fill="both", expand=True)

        img_box = tk.Frame(right, bg="#1a3050", height=160, highlightbackground=ACCENT, highlightthickness=2)
        img_box.pack(fill="x")
        img_box.pack_propagate(False)

        tk.Label(img_box, text="🚢", bg="#1a3050", fg=ACCENT, font=("Helvetica", 50)).pack(expand=True)
        tk.Label(img_box, text=name, bg="#1a3050", fg=TEXT_WHITE, font=self.f_heading).pack(side="bottom", pady=4)

        data_box = tk.Frame(right, bg=BG_CARD, padx=14, pady=10, highlightbackground=BORDER, highlightthickness=1)
        data_box.pack(fill="x", pady=8)

        specs = [
            ("Comprimento", "399 m"),
            ("Boca", "61 m"),
            ("Capacidade", "23 964 TEU"),
            ("Calado máx.", "16.5 m")
        ]

        for k, v in specs:
            row = tk.Frame(data_box, bg=BG_CARD)
            row.pack(fill="x", pady=1)

            tk.Label(row, text=f"{k}:", bg=BG_CARD, fg=TEXT_MUTED, font=self.f_small, width=14, anchor="w").pack(side="left")
            tk.Label(row, text=v, bg=BG_CARD, fg=TEXT_WHITE, font=self.f_small).pack(side="left")

        self._btn(right, "Confirmar Navio", lambda: self.show_screen("screen8"), w=160).pack(anchor="e", pady=2)
        self._nav_row(f, back="screen7", next_="screen8")

    # ────────────────────────────────────────────────────
    # TELA 8 - resumo do plano
    # ────────────────────────────────────────────────────
    def _show_screen8(self, parent):
        f = self._panel(parent, "Plano de Estiva")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        left = tk.Frame(body, bg=BG_CARD, padx=10, pady=10, highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="Resumo do Plano", bg=BG_CARD, fg=TEXT_WHITE, font=self.f_heading).pack(anchor="nw")

        route_names = ["Rota A – 3.200 nm", "Rota B – 3.900 nm", "Rota C – 2.800 nm"]
        idx = self.selected_route.get()
        route_text = route_names[idx] if 0 <= idx < len(route_names) else route_names[0]

        info_items = [
            ("Tipo de Rota", "Rota definida (liner)"),
            ("Carga", self.cargo_var.get()),
            ("Porto Carga", self.porto_carga_var.get() or "Lisboa"),
            ("Porto Descarga", self.porto_descarga_var.get() or "Antuérpia"),
            ("ETA", self.eta_var.get() or "20/11/2026"),
            ("Rota", route_text),
            ("Navio", self.selected_ship),
        ]

        for k, v in info_items:
            r = tk.Frame(left, bg=BG_CARD)
            r.pack(fill="x", pady=2)

            tk.Label(r, text=f"{k}:", bg=BG_CARD, fg=TEXT_MUTED, font=self.f_small, width=14, anchor="w").pack(side="left")
            tk.Label(r, text=v, bg=BG_CARD, fg=TEXT_WHITE, font=self.f_small).pack(side="left")

        right = tk.Frame(body, bg=BG_PANEL)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right,
            text="Localização do contentor a visualizar",
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            font=self.f_small,
            wraplength=200,
            justify="center"
        ).pack(pady=(0, 6))

        bay_f = tk.Frame(right, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
        bay_f.pack(fill="both", expand=True)

        self._draw_bay_view(bay_f)

        self._btn(right, "Editar Plano de Estiva", lambda: self.show_screen("screen9"), w=180, secondary=True).pack(anchor="e", pady=(6, 0))

        nav = tk.Frame(f, bg=BG_PANEL)
        nav.pack(fill="x", pady=(8, 0))

        self._btn(nav, "Voltar", lambda: self.show_screen("screen7"), secondary=True, w=100).pack(side="left", pady=2)
        self._btn(nav, "Finalizar  ✔", self._finalizar, w=140).pack(side="right", pady=2)

    # desenho da baía
    def _draw_bay_view(self, parent):
        canvas = tk.Canvas(parent, bg="#0d1a28", highlightthickness=0, height=160)
        canvas.pack(fill="x", padx=6, pady=6)

        def draw(e=None):
            canvas.delete("all")
            w = canvas.winfo_width()

            if w < 2:
                return

            canvas.create_text(w // 2, 10, text="Secção Transversal: Baía 10", fill=TEXT_WHITE, font=self.f_small)

            cols, rows_n = 9, 5
            cw, ch = min(24, max(12, (w - 40) // cols)), 20
            ox = (w - cols * cw) // 2
            oy = 25

            colors = [BG_CARD] * (cols * rows_n)
            colors[13] = ORANGE
            colors[22] = "#c0c8d0"

            for r in range(rows_n):
                for c in range(cols):
                    idx = r * cols + c
                    x1, y1 = ox + c * cw, oy + r * ch
                    x2, y2 = x1 + cw - 2, y1 + ch - 2
                    canvas.create_rectangle(x1, y1, x2, y2, fill=colors[idx], outline="#1a2f45", width=1)

        canvas.bind("<Configure>", draw)

    # popup finalizar
    def _finalizar(self):
        win = tk.Toplevel(self)
        win.title("Concluído")
        win.geometry("320x160")
        win.configure(bg=BG_DARK)
        win.grab_set()

        tk.Label(win, text="✔", bg=BG_DARK, fg="#30c070", font=("Helvetica", 36)).pack(pady=(20, 4))
        tk.Label(
            win,
            text="Plano de estiva finalizado com sucesso!",
            bg=BG_DARK,
            fg=TEXT_WHITE,
            font=self.f_body,
            wraplength=280
        ).pack()

        self._btn(win, "OK", win.destroy, w=80).pack(pady=12)

    # ────────────────────────────────────────────────────
    # TELA 9 - edição do plano
    # ────────────────────────────────────────────────────
    def _show_screen9(self, parent):
        f = self._panel(parent, "Plano de Estiva – Edição")

        body = tk.Frame(f, bg=BG_PANEL)
        body.pack(fill="both", expand=True, pady=10)

        val = tk.Frame(body, bg=BG_CARD, padx=10, pady=10, width=160, highlightbackground=BORDER, highlightthickness=1)
        val.pack(side="left", fill="y", padx=(0, 8))
        val.pack_propagate(False)

        tk.Label(val, text="Validações", bg=BG_CARD, fg=TEXT_WHITE, font=self.f_heading).pack(anchor="nw")

        validations = [
            ("✔ Estabilidade", "#30c070"),
            ("✔ Distribuição", "#30c070"),
            ("⚠ Peso por baia", "#e0a030"),
            ("✔ Segregação", "#30c070")
        ]

        for txt, clr in validations:
            tk.Label(val, text=txt, bg=BG_CARD, fg=clr, font=self.f_small, anchor="w").pack(fill="x", pady=3)

        mid = tk.Frame(body, bg=BG_CARD, padx=6, pady=6, highlightbackground=BORDER, highlightthickness=1)
        mid.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(mid, text="Visualização do Navio", bg=BG_CARD, fg=TEXT_MUTED, font=self.f_small).pack()
        self._draw_ship_topview(mid)

        info = tk.Frame(body, bg=BG_PANEL, width=180)
        info.pack(side="left", fill="y")
        info.pack_propagate(False)

        cargo_box = tk.Frame(info, bg=BG_CARD, padx=10, pady=10, highlightbackground=BORDER, highlightthickness=1)
        cargo_box.pack(fill="x", pady=(0, 8))

        tk.Label(
            cargo_box,
            text="Que carga é, onde está e para onde vai",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=self.f_small,
            wraplength=160,
            justify="left"
        ).pack(anchor="nw")

        tk.Label(
            cargo_box,
            text="MSCU1234567\n40' HC Dry\nLisboa → Antuérpia\nPeso: 28.4 t",
            bg=BG_CARD,
            fg=TEXT_DARK,
            font=self.f_small,
            justify="left"
        ).pack(anchor="nw", pady=4)

        inf_box = tk.Frame(info, bg=BG_CARD, padx=10, pady=10, highlightbackground=BORDER, highlightthickness=1)
        inf_box.pack(fill="x")

        tk.Label(inf_box, text="Info sobre a carga", bg=BG_CARD, fg=TEXT_MUTED, font=self.f_small).pack(anchor="nw")
        tk.Label(
            inf_box,
            text="Classe IMO: N/A\nIMDG: Não perigoso\nTemperatura: Ambiente\nVentilação: Normal",
            bg=BG_CARD,
            fg=TEXT_DARK,
            font=self.f_small,
            justify="left"
        ).pack(anchor="nw", pady=4)

        nav = tk.Frame(f, bg=BG_PANEL)
        nav.pack(fill="x", pady=(8, 0))

        self._btn(nav, "Voltar", lambda: self.show_screen("screen8"), secondary=True, w=100).pack(side="left", pady=2)
        self._btn(nav, "Finalizar  ✔", self._finalizar, w=140).pack(side="right", pady=2)

    # topo do navio
    def _draw_ship_topview(self, parent):
        canvas = tk.Canvas(parent, bg="#071525", highlightthickness=0)
        canvas.pack(fill="both", expand=True, pady=4)

        def draw(e=None):
            canvas.delete("all")
            w, h = canvas.winfo_width(), canvas.winfo_height()

            if w < 4:
                return

            bays = 10
            bw = max(18, (w - 20) // bays)
            oh = 8

            colors_row = [
                "#3060a0", "#3060a0", "#3060a0", BTN_PRIMARY, BTN_PRIMARY,
                "#c04030", "#c04030", "#3060a0", "#3060a0", "#3060a0"
            ]

            for row in range(3):
                y1 = oh + row * 18
                y2 = y1 + 15

                for b in range(bays):
                    x1 = 10 + b * bw
                    x2 = x1 + bw - 2
                    fill = colors_row[b] if row < 2 else "#1a2f45"
                    sel = b == 4 and row == 1

                    canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=ORANGE if sel else fill,
                        outline="#0a1828"
                    )

            ley = h - 16
            x = 10
            legend = [("General", "#3060a0"), ("Reefer", "#c04030"), ("Selected", ORANGE)]

            for label, color in legend:
                canvas.create_rectangle(x, ley, x + 10, ley + 10, fill=color, outline="")
                canvas.create_text(x + 14, ley + 5, text=label, fill=TEXT_MUTED, font=self.f_small, anchor="w")
                x += 80

        canvas.bind("<Configure>", draw)

    # panel comum
    def _panel(self, parent, title):
        outer = tk.Frame(parent, bg=BG_DARK, padx=14, pady=12)
        outer.pack(fill="both", expand=True)

        f = tk.Frame(outer, bg=BG_PANEL, padx=14, pady=12, highlightbackground=BORDER, highlightthickness=1)
        f.pack(fill="both", expand=True)

        tk.Label(f, text=title, bg=BG_PANEL, fg=TEXT_WHITE, font=self.f_title).pack(anchor="w", pady=(0, 4))
        return f

    # linha de navegação
    def _nav_row(self, parent, back, next_):
        nav = tk.Frame(parent, bg=BG_PANEL)
        nav.pack(fill="x", pady=(8, 0))

        self._btn(nav, "Voltar", lambda: self.show_screen(back), secondary=True, w=100).pack(side="left", pady=2)
        self._btn(nav, "Próximo  ➜", lambda: self.show_screen(next_), w=130).pack(side="right", pady=2)

    # botão custom
    def _btn(self, parent, text, command, w=160, secondary=False):
        bg = BTN_SECONDARY if secondary else BTN_PRIMARY
        hov = BTN_SEC_HOV if secondary else BTN_HOVER

        btn = tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=TEXT_WHITE,
            font=self.f_btn,
            cursor="hand2",
            width=w // 8,
            pady=6,
            relief="flat"
        )

        btn.bind("<Button-1>", lambda e: command())
        btn.bind("<Enter>", lambda e: btn.config(bg=hov))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))

        return btn


if __name__ == "__main__":
    app = App()
    app.mainloop()
