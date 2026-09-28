import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import math

# ============================================================
# MATERIAL SELECTION STUDIO
# Neon Gradient UI + Ashby-style Material Selection
#
# Python 3.x
# Standard library only — no external packages
#
# Density is stored/displayed in g/cm³
# ============================================================

APP_TITLE = "Material Selection Studio"

# ============================================================
# COLOR PALETTE (Neon / Gradient-inspired)
# ============================================================

C = {
    "bg": "#050814",
    "panel": "#070C1F",
    "card": "#0B1024",
    "card2": "#101735",
    "border": "#1F2A4A",

    "text": "#F9FAFF",
    "muted": "#9CA3C7",

    "purple": "#8B5CF6",
    "purple2": "#7C3AED",
    "pink": "#EC4899",

    "cyan": "#22D3EE",
    "cyan_glow": "#38BDF8",
    "blue_glow": "#3B82F6",

    "green": "#10B981",
    "orange": "#F59E0B",
    "red": "#EF4444",

    "grid": "#263149",
}

# ============================================================
# MATERIAL DATABASE
# ============================================================

MATERIAL_DATA = [
    # ---------------- METALS ----------------
    ["Aluminum 6061-T6", "Metal",
     2.70, 68.9, 276, 310, 167, 2.60, 0.33],
    ["Aluminum 7075-T6", "Metal",
     2.81, 71.7, 503, 572, 130, 4.00, 0.33],
    ["Mild Steel", "Metal",
     7.85, 200, 250, 400, 51.9, 1.20, 0.29],
    ["Stainless Steel 304", "Metal",
     8.00, 193, 215, 505, 16.2, 3.50, 0.29],
    ["Stainless Steel 316", "Metal",
     8.00, 193, 205, 515, 16.2, 4.50, 0.30],
    ["Titanium Grade 5", "Metal",
     4.43, 114, 830, 900, 6.7, 18.00, 0.34],
    ["Copper", "Metal",
     8.96, 117, 70, 220, 398, 9.00, 0.34],
    ["Brass", "Metal",
     8.50, 100, 200, 550, 120, 7.00, 0.34],
    ["Cast Iron", "Metal",
     7.20, 130, 250, 180, 50, 1.50, 0.27],
    ["Magnesium AZ31B", "Metal",
     1.77, 45, 200, 260, 96, 5.00, 0.35],

    # ---------------- POLYMERS ----------------
    ["ABS", "Polymer",
     1.04, 2.30, 40, 45, 0.20, 2.20, 0.35],
    ["Nylon 6", "Polymer",
     1.14, 2.80, 55, 75, 0.25, 3.00, 0.39],
    ["Polycarbonate", "Polymer",
     1.20, 2.35, 65, 70, 0.20, 3.20, 0.37],
    ["PEEK", "Polymer",
     1.32, 3.60, 95, 100, 0.25, 75.00, 0.38],
    ["HDPE", "Polymer",
     0.95, 1.00, 25, 30, 0.45, 1.80, 0.46],
    ["LDPE", "Polymer",
     0.92, 0.25, 8, 12, 0.33, 1.70, 0.46],
    ["PP", "Polymer",
     0.91, 1.50, 30, 35, 0.13, 1.60, 0.42],
    ["PVC Rigid", "Polymer",
     1.40, 3.00, 45, 50, 0.16, 1.80, 0.40],
    ["PTFE", "Polymer",
     2.20, 0.50, 10, 25, 0.25, 12.00, 0.46],
    ["PEI", "Polymer",
     1.27, 3.30, 105, 110, 0.22, 55.00, 0.37],

    # ---------------- COMPOSITES ----------------
    ["Carbon Fiber/Epoxy", "Composite",
     1.55, 70, 600, 800, 5.5, 35.00, 0.30],
    ["Glass Fiber/Polyester", "Composite",
     1.80, 25, 250, 350, 0.80, 8.00, 0.27],
    ["Glass Fiber/Epoxy", "Composite",
     1.90, 30, 400, 600, 1.00, 10.00, 0.28],
    ["Aramid/Epoxy", "Composite",
     1.35, 40, 350, 700, 0.80, 30.00, 0.34],
    ["GFRP Pultruded", "Composite",
     1.90, 35, 300, 500, 0.90, 7.00, 0.28],
    ["CFRP", "Composite",
     1.60, 80, 700, 1000, 5.0, 45.00, 0.30],

    # ---------------- WOODS ----------------
    ["Oak", "Wood",
     0.70, 11, 40, 80, 0.16, 3.50, 0.35],
    ["Pine", "Wood",
     0.50, 9, 30, 60, 0.12, 2.50, 0.37],
    ["Balsa", "Wood",
     0.16, 3.5, 10, 20, 0.06, 8.00, 0.25],
    ["Birch", "Wood",
     0.67, 13, 45, 100, 0.16, 4.00, 0.36],

    # ---------------- CERAMICS ----------------
    ["Concrete", "Ceramic",
     2.40, 25, 3, 4, 1.70, 0.12, 0.20],
    ["Alumina", "Ceramic",
     3.90, 370, 300, 300, 30, 4.00, 0.22],
    ["Silicon Carbide", "Ceramic",
     3.10, 410, 300, 300, 120, 12.00, 0.17],
    ["Glass", "Ceramic",
     2.50, 70, 50, 35, 1.00, 0.80, 0.22],

    # ---------------- OTHER POLYMERS / ELASTOMERS ----------------
    ["Epoxy Resin", "Polymer",
     1.15, 3.0, 70, 75, 0.20, 6.00, 0.38],
    ["Silicone Rubber", "Elastomer",
     1.10, 0.01, 5, 8, 0.20, 4.00, 0.49],
    ["Natural Rubber", "Elastomer",
     0.93, 0.01, 20, 25, 0.14, 2.50, 0.49],
    ["Neoprene", "Elastomer",
     1.23, 0.01, 15, 25, 0.20, 3.50, 0.49],

    # ---------------- NATURAL MATERIALS ----------------
    ["Cork", "Natural",
     0.24, 0.03, 2, 7, 0.08, 4.00, 0.30],
    ["Bamboo", "Natural",
     0.65, 12, 40, 140, 0.20, 5.00, 0.35],
]

# ============================================================
# PROPERTY INFORMATION
# ============================================================

PROPERTY_INFO = {
    "density": ("Density", "g/cm³", "lower"),
    "modulus": ("Young's Modulus", "GPa", "higher"),
    "yield": ("Yield Strength", "MPa", "higher"),
    "tensile": ("Tensile Strength", "MPa", "higher"),
    "thermal": ("Thermal Conductivity", "W/m·K", "higher"),
    "cost": ("Relative Cost", "$/kg", "lower"),
    "poisson": ("Poisson Ratio", "", "target"),
}

PROPERTY_INDEX = {
    "density": 2,
    "modulus": 3,
    "yield": 4,
    "tensile": 5,
    "thermal": 6,
    "cost": 7,
    "poisson": 8,
}

# ============================================================
# FAMILY COLORS
# ============================================================

FAMILY_COLORS = {
    "Metal": "#38BDF8",
    "Polymer": "#A78BFA",
    "Composite": "#EC4899",
    "Wood": "#F59E0B",
    "Ceramic": "#10B981",
    "Elastomer": "#FB7185",
    "Natural": "#84CC16",
}

# ============================================================
# COLOR HELPERS
# ============================================================

def hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def blend(c1, c2, t):
    a = hex_rgb(c1)
    b = hex_rgb(c2)
    return "#" + "".join(
        f"{round(a[i] + (b[i] - a[i]) * t):02x}"
        for i in range(3)
    )


def draw_gradient(canvas, width, height, start, end, horizontal=True):
    canvas.delete("gradient")
    if horizontal:
        steps = max(2, int(width))
        for i in range(steps):
            t = i / (steps - 1)
            color = blend(start, end, t)
            canvas.create_rectangle(
                i, 0, i + 1, height,
                fill=color, outline="", tags="gradient"
            )
    else:
        steps = max(2, int(height))
        for i in range(steps):
            t = i / (steps - 1)
            color = blend(start, end, t)
            canvas.create_rectangle(
                0, i, width, i + 1,
                fill=color, outline="", tags="gradient"
            )
    canvas.tag_lower("gradient")


# ============================================================
# MAIN APPLICATION
# ============================================================

class MaterialSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1450x900")
        self.root.minsize(1100, 700)
        self.root.configure(bg=C["bg"])

        self.materials = [row[:] for row in MATERIAL_DATA]
        self.current_page = "Database"
        self.pages = {}
        self.nav_buttons = {}
        self.db_sort_reverse = False

        self.setup_styles()
        self.build_shell()
        self.build_pages()
        self.show_page("Database")
        self.refresh_database()

    # ========================================================
    # TK / TTK STYLING
    # ========================================================

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Treeview
        style.configure(
            "Dark.Treeview",
            background=C["panel"],
            foreground=C["text"],
            fieldbackground=C["panel"],
            bordercolor=C["border"],
            lightcolor=C["border"],
            darkcolor=C["border"],
            rowheight=30,
            font=("Segoe UI", 10)
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", "#1E293B")],
            foreground=[("selected", "#FFFFFF")]
        )

        # Treeview headings
        style.configure(
            "Dark.Treeview.Heading",
            background=C["card2"],
            foreground=C["muted"],
            bordercolor=C["border"],
            relief="flat",
            font=("Segoe UI Semibold", 9),
            padding=(8, 8)
        )
        style.map(
            "Dark.Treeview.Heading",
            background=[("active", "#1F2937")],
            foreground=[("active", C["text"])]
        )

        # Scrollbars
        style.configure(
            "Dark.Vertical.TScrollbar",
            background=C["card2"],
            troughcolor=C["panel"],
            bordercolor=C["panel"],
            arrowcolor=C["muted"]
        )
        style.configure(
            "Dark.Horizontal.TScrollbar",
            background=C["card2"],
            troughcolor=C["panel"],
            bordercolor=C["panel"],
            arrowcolor=C["muted"]
        )

        # Combobox
        style.configure(
            "Dark.TCombobox",
            fieldbackground=C["card2"],
            background=C["card2"],
            foreground=C["text"],
            arrowcolor=C["muted"],
            bordercolor=C["border"],
            lightcolor=C["border"],
            darkcolor=C["border"],
            padding=7
        )
        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", C["card2"])],
            foreground=[("readonly", C["text"])],
            selectbackground=[("readonly", C["purple2"])],
            selectforeground=[("readonly", "#FFFFFF")]
        )

    # ========================================================
    # MAIN SHELL
    # ========================================================

    def build_shell(self):
        shell = tk.Frame(self.root, bg=C["bg"])
        shell.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(
            shell,
            bg=C["panel"],
            width=245,
            highlightthickness=1,
            highlightbackground=C["border"]
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Main area
        self.main = tk.Frame(shell, bg=C["bg"])
        self.main.pack(side="left", fill="both", expand=True)

        # Logo
        self.logo_canvas = tk.Canvas(
            self.sidebar,
            height=118,
            bg=C["panel"],
            highlightthickness=0
        )
        self.logo_canvas.pack(fill="x", padx=12, pady=(12, 10))
        self.logo_canvas.bind("<Configure>", lambda event: self.draw_logo())
        self.draw_logo()

        # Navigation label
        tk.Label(
            self.sidebar,
            text="WORKSPACE",
            bg=C["panel"],
            fg=C["muted"],
            font=("Segoe UI Semibold", 9),
            anchor="w"
        ).pack(fill="x", padx=24, pady=(4, 8))

        # Navigation buttons
        nav_items = [
            ("Database", "▦"),
            ("Compare", "⇄"),
            ("Ashby Plot", "◈"),
            ("Screening", "✓"),
        ]
        for name, icon in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=f"  {icon}   {name}",
                command=lambda n=name: self.show_page(n),
                bg=C["panel"],
                fg=C["muted"],
                activebackground=C["card2"],
                activeforeground=C["text"],
                relief="flat",
                bd=0,
                anchor="w",
                padx=14,
                pady=11,
                font=("Segoe UI Semibold", 10),
                cursor="hand2"
            )
            btn.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[name] = btn

        # Sidebar spacer
        tk.Frame(self.sidebar, bg=C["panel"]).pack(fill="both", expand=True)

        # Sidebar info card with neon glow
        info_outer = tk.Frame(
            self.sidebar,
            bg=C["bg"],
            highlightthickness=0
        )
        info_outer.pack(fill="x", padx=14, pady=(10, 14))

        glow = tk.Canvas(
            info_outer,
            height=80,
            bg=C["bg"],
            highlightthickness=0
        )
        glow.pack(fill="x")
        w = 200
        draw_gradient(glow, w, 80, C["blue_glow"], C["purple2"])
        glow.create_oval(
            5, 5, w - 5, 75,
            outline=C["cyan_glow"],
            width=2
        )

        info = tk.Frame(
            info_outer,
            bg=C["card"],
            highlightthickness=1,
            highlightbackground=C["border"]
        )
        info.place(relx=0.03, rely=0.08, relwidth=0.94, relheight=0.84)

        tk.Label(
            info,
            text="MATERIAL SELECTION",
            bg=C["card"],
            fg=C["text"],
            font=("Segoe UI Semibold", 9)
        ).pack(anchor="w", padx=12, pady=(11, 2))

        tk.Label(
            info,
            text="Ashby-style teaching workspace",
            bg=C["card"],
            fg=C["muted"],
            font=("Segoe UI", 8),
            wraplength=190,
            justify="left"
        ).pack(anchor="w", padx=12, pady=(0, 11))

        # Header
        self.header = tk.Canvas(
            self.main,
            height=116,
            bg=C["bg"],
            highlightthickness=0
        )
        self.header.pack(fill="x", padx=20, pady=(18, 8))
        self.header.bind("<Configure>", lambda event: self.draw_header())

        # Page content
        self.content = tk.Frame(self.main, bg=C["bg"])
        self.content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # ========================================================
    # LOGO
    # ========================================================

    def draw_logo(self):
        canvas = self.logo_canvas
        canvas.delete("all")
        width = max(canvas.winfo_width(), 220)
        height = max(canvas.winfo_height(), 118)

        draw_gradient(canvas, width, height, C["purple2"], C["pink"], horizontal=True)

        # Neon backglow bar
        canvas.create_rectangle(
            0, height - 10, width, height,
            fill=C["cyan_glow"], outline=""
        )

        canvas.create_text(
            18, 24,
            text="MATERIAL",
            anchor="w",
            fill="#FFFFFF",
            font=("Segoe UI", 18, "bold")
        )
        canvas.create_text(
            18, 48,
            text="SELECTION",
            anchor="w",
            fill="#FFFFFF",
            font=("Segoe UI", 18, "bold")
        )
        canvas.create_text(
            19, 84,
            text="DESIGN • COMPARE • EXPLORE",
            anchor="w",
            fill="#E0F2FE",
            font=("Segoe UI", 8, "bold")
        )

    # ========================================================
    # HEADER
    # ========================================================

    def draw_header(self):
        self.header.delete("all")
        width = max(self.header.winfo_width(), 600)
        height = max(self.header.winfo_height(), 116)

        draw_gradient(self.header, width, height, "#0F172A", "#1E1B4B", horizontal=True)

        # Accent line
        self.header.create_rectangle(
            0, height - 4, width, height,
            fill=C["pink"], outline=""
        )

        titles = {
            "Database": (
                "Material Database",
                "Browse engineering materials and their key properties."
            ),
            "Compare": (
                "Compare Materials",
                "Put candidate materials side-by-side before making a selection."
            ),
            "Ashby Plot": (
                "Ashby-Style Plot",
                "Visualize material-property relationships on linear or log axes."
            ),
            "Screening": (
                "Material Screening",
                "Apply engineering constraints and weighted preferences."
            ),
        }

        title, subtitle = titles[self.current_page]

        self.header.create_text(
            26, 27,
            text=self.current_page.upper(),
            anchor="w",
            fill=C["pink"],
            font=("Segoe UI Semibold", 9)
        )
        self.header.create_text(
            26, 55,
            text=title,
            anchor="w",
            fill=C["text"],
            font=("Segoe UI", 22, "bold")
        )
        self.header.create_text(
            28, 88,
            text=subtitle,
            anchor="w",
            fill=C["muted"],
            font=("Segoe UI", 10)
        )

        # Database count pill with glow
        pill_width = 190
        x0 = width - pill_width - 24

        self.header.create_oval(
            x0 - 6, 22, x0 + pill_width + 6, 58,
            outline=C["cyan_glow"],
            width=2
        )
        self.header.create_rectangle(
            x0, 26, x0 + pill_width, 54,
            fill=C["card2"], outline=C["border"]
        )
        self.header.create_text(
            x0 + pill_width / 2,
            40,
            text=f"{len(self.materials)} materials • local",
            fill=C["muted"],
            font=("Segoe UI Semibold", 8)
        )

    # ========================================================
    # CARD
    # ========================================================

    def make_card(self, parent, padx=16, pady=14):
        outer = tk.Frame(
            parent,
            bg=C["bg"],
            highlightthickness=0
        )
        outer.pack_propagate(False)

        glow = tk.Canvas(
            outer,
            bg=C["bg"],
            highlightthickness=0
        )
        glow.pack(fill="both", expand=True)

        def _resize(event):
            glow.delete("all")
            w = event.width
            h = event.height
            draw_gradient(glow, w, h, "#020617", "#0F172A", horizontal=False)
            glow.create_oval(
                6, 6, w - 6, h - 6,
                outline=C["blue_glow"],
                width=1
            )

        glow.bind("<Configure>", _resize)

        inner = tk.Frame(
            glow,
            bg=C["card"],
            highlightthickness=1,
            highlightbackground=C["border"]
        )
        inner.place(relx=0.03, rely=0.06, relwidth=0.94, relheight=0.88)

        content = tk.Frame(inner, bg=C["card"])
        content.pack(fill="both", expand=True, padx=padx, pady=pady)

        return outer, content

    # ========================================================
    # BUTTON
    # ========================================================

    def button(self, parent, text, command, accent=False, small=False):
        if accent:
            bg = C["purple2"]
            active = C["pink"]
            fg = "#FFFFFF"
        else:
            bg = C["card2"]
            active = "#1F2937"
            fg = C["text"]

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active,
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            padx=10 if small else 16,
            pady=6 if small else 9,
            font=("Segoe UI Semibold", 9 if small else 10),
            cursor="hand2"
        )
        return btn

    # ========================================================
    # PAGE CREATION
    # ========================================================

    def build_pages(self):
        for name in ("Database", "Compare", "Ashby Plot", "Screening"):
            page = tk.Frame(self.content, bg=C["bg"])
            self.pages[name] = page
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.build_database_page(self.pages["Database"])
        self.build_compare_page(self.pages["Compare"])
        self.build_plot_page(self.pages["Ashby Plot"])
        self.build_screening_page(self.pages["Screening"])

    # ========================================================
    # PAGE NAVIGATION
    # ========================================================

    def show_page(self, name):
        self.current_page = name
        self.pages[name].tkraise()

        for nav_name, btn in self.nav_buttons.items():
            if nav_name == name:
                btn.configure(
                    bg="#1D2340",
                    fg="#FFFFFF",
                    activebackground="#312E81"
                )
            else:
                btn.configure(
                    bg=C["panel"],
                    fg=C["muted"],
                    activebackground=C["card2"]
                )

        self.draw_header()

        if name == "Ashby Plot":
            self.root.after(50, self.update_plot)

    # ========================================================
    # DATABASE PAGE
    # ========================================================

    def build_database_page(self, page):
        # Filter card
        top_card, controls = self.make_card(page, padx=14, pady=12)
        top_card.pack(fill="x", pady=(0, 12))

        # Search
        tk.Label(
            controls,
            text="SEARCH",
            bg=C["card"],
            fg=C["muted"],
            font=("Segoe UI Semibold", 8)
        ).grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.search_var = tk.StringVar()
        search = tk.Entry(
            controls,
            textvariable=self.search_var,
            bg=C["card2"],
            fg=C["text"],
            insertbackground=C["text"],
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            highlightthickness=1,
            highlightbackground=C["border"],
            highlightcolor=C["cyan_glow"]
        )
        search.grid(row=1, column=0, sticky="ew", padx=(0, 10), ipady=7)
        search.bind("<KeyRelease>", lambda event: self.refresh_database())

        # Family
        tk.Label(
            controls,
            text="FAMILY",
            bg=C["card"],
            fg=C["muted"],
            font=("Segoe UI Semibold", 8)
        ).grid(row=0, column=1, sticky="w")

        self.family_var = tk.StringVar(value="All")
        self.family_combo = ttk.Combobox(
            controls,
            textvariable=self.family_var,
            state="readonly",
            style="Dark.TCombobox",
            values=["All"]
        )
        self.family_combo.grid(row=1, column=1, sticky="ew", padx=(0, 10))
        self.family_combo.bind("<<ComboboxSelected>>", lambda event: self.refresh_database())

        # Buttons
        self.button(
            controls,
            "＋ Add Material",
            self.add_material,
            accent=True
        ).grid(row=1, column=2, padx=4)

        self.button(
            controls,
            "↻ Reset",
            self.reset_filters
        ).grid(row=1, column=3, padx=4)

        self.button(
            controls,
            "⇩ Export CSV",
            self.export_csv
        ).grid(row=1, column=4, padx=(4, 0))

        controls.columnconfigure(0, weight=4)
        controls.columnconfigure(1, weight=2)

        # Database table
        table_card, table = self.make_card(page, padx=10, pady=10)
        table_card.pack(fill="both", expand=True)

        columns = [
            ("name", "Material", 220, "w"),
            ("family", "Family", 110, "center"),
            ("density", "Density\n(g/cm³)", 105, "center"),
            ("modulus", "E\n(GPa)", 100, "center"),
            ("yield", "Yield\n(MPa)", 100, "center"),
            ("tensile", "Tensile\n(MPa)", 105, "center"),
            ("thermal", "Thermal\n(W/m·K)", 120, "center"),
            ("cost", "Cost\n($/kg)", 100, "center"),
            ("poisson", "ν", 75, "center"),
        ]

        self.db_tree = ttk.Treeview(
            table,
            columns=[c[0] for c in columns],
            show="headings",
            style="Dark.Treeview",
            selectmode="extended"
        )

        for key, heading, width, anchor in columns:
            self.db_tree.heading(
                key,
                text=heading,
                command=lambda k=key: self.sort_database(k)
            )
            self.db_tree.column(
                key,
                width=width,
                anchor=anchor,
                stretch=(key == "name")
            )

        yscroll = ttk.Scrollbar(
            table,
            orient="vertical",
            command=self.db_tree.yview,
            style="Dark.Vertical.TScrollbar"
        )
        xscroll = ttk.Scrollbar(
            table,
            orient="horizontal",
            command=self.db_tree.xview,
            style="Dark.Horizontal.TScrollbar"
        )

        self.db_tree.configure(
            yscrollcommand=yscroll.set,
            xscrollcommand=xscroll.set
        )
        self.db_tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")
        xscroll.pack(side="bottom", fill="x")

        self.db_tree.bind("<<TreeviewSelect>>", lambda event: self.selection_changed())

        # Status
        status = tk.Frame(page, bg=C["bg"])
        status.pack(fill="x", pady=(8, 0))
        self.db_status = tk.Label(
            status,
            text="",
            bg=C["bg"],
            fg=C["muted"],
            font=("Segoe UI", 9)
        )
        self.db_status.pack(anchor="w")

    # ========================================================
    # DATABASE REFRESH
    # ========================================================

    def refresh_database(self):
        if not hasattr(self, "db_tree"):
            return

        query = self.search_var.get().strip().lower()
        family = self.family_var.get()

        for item in self.db_tree.get_children():
            self.db_tree.delete(item)

        families = sorted({material[1] for material in self.materials})
        self.family_combo["values"] = ["All"] + families

        count = 0
        for index, material in enumerate(self.materials):
            if query and query not in material[0].lower():
                continue
            if family != "All" and material[1] != family:
                continue

            self.db_tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    material[0],
                    material[1],
                    f"{material[2]:.3g}",
                    f"{material[3]:.3g}",
                    f"{material[4]:.3g}",
                    f"{material[5]:.3g}",
                    f"{material[6]:.3g}",
                    f"{material[7]:.3g}",
                    f"{material[8]:.3f}",
                )
            )
            count += 1

        self.db_status.config(
            text=(
                f"Showing {count} of {len(self.materials)} materials"
                " • Density: g/cm³"
            )
        )

    # ========================================================
    # RESET DATABASE FILTERS
    # ========================================================

    def reset_filters(self):
        self.search_var.set("")
        self.family_var.set("All")
        self.refresh_database()

    # ========================================================
    # SORT DATABASE
    # ========================================================

    def sort_database(self, key):
        index_map = {
            "name": 0,
            "family": 1,
            "density": 2,
            "modulus": 3,
            "yield": 4,
            "tensile": 5,
            "thermal": 6,
            "cost": 7,
            "poisson": 8,
        }
        index = index_map[key]
        self.db_sort_reverse = not self.db_sort_reverse

        self.materials.sort(
            key=lambda item: (
                str(item[index]).lower()
                if isinstance(item[index], str)
                else item[index]
            ),
            reverse=self.db_sort_reverse
        )
        self.refresh_database()

    # ========================================================
    # SELECTED MATERIALS
    # ========================================================

    def selected_materials(self):
        if not hasattr(self, "db_tree"):
            return []
        selected = []
        for iid in self.db_tree.selection():
            try:
                selected.append(self.materials[int(iid)])
            except (ValueError, IndexError):
                pass
        return selected

    # ========================================================
    # SELECTION CHANGED
    # ========================================================

    def selection_changed(self):
        selected = self.selected_materials()
        self.selection_label.config(
            text=f"{len(selected)} material(s) selected"
        )
        self.update_comparison()

    # ========================================================
    # ADD MATERIAL
    # ========================================================

    def add_material(self):
        win = tk.Toplevel(self.root)
        win.title("Add Material")
        win.geometry("520x570")
        win.configure(bg=C["bg"])
        win.transient(self.root)
        win.grab_set()

        outer = tk.Frame(
            win,
            bg=C["bg"],
            highlightthickness=0
        )
        outer.pack(fill="both", expand=True, padx=18, pady=18)

        card_outer, card = self.make_card(outer, padx=0, pady=0)
        card_outer.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="Add Material",
            bg=C["card"],
            fg=C["text"],
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", padx=22, pady=(20, 2))

        tk.Label(
            card,
            text="Enter values using the units shown below.",
            bg=C["card"],
            fg=C["muted"],
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=22, pady=(0, 16))

        fields = [
            ("Material Name", "name"),
            ("Family", "family"),
            ("Density (g/cm³)", "density"),
            ("Young's Modulus (GPa)", "modulus"),
            ("Yield Strength (MPa)", "yield"),
            ("Tensile Strength (MPa)", "tensile"),
            ("Thermal Conductivity (W/m·K)", "thermal"),
            ("Cost ($/kg)", "cost"),
            ("Poisson Ratio", "poisson"),
        ]

        entries = {}
        for caption, key in fields:
            tk.Label(
                card,
                text=caption,
                bg=C["card"],
                fg=C["muted"],
                font=("Segoe UI", 9)
            ).pack(fill="x", padx=22, pady=(3, 2))

            entry = tk.Entry(
                card,
                bg=C["card2"],
                fg=C["text"],
                insertbackground=C["text"],
                relief="flat",
                bd=0,
                highlightthickness=1,
                highlightbackground=C["border"],
                highlightcolor=C["cyan_glow"]
            )
            entry.pack(fill="x", padx=22, ipady=5)
            entries[key] = entry

        def save():
            try:
                name = entries["name"].get().strip()
                family = entries["family"].get().strip() or "Other"

                if not name:
                    raise ValueError("Material name is required.")

                values = [
                    name,
                    family,
                    float(entries["density"].get()),
                    float(entries["modulus"].get()),
                    float(entries["yield"].get()),
                    float(entries["tensile"].get()),
                    float(entries["thermal"].get()),
                    float(entries["cost"].get()),
                    float(entries["poisson"].get()),
                ]

                self.materials.append(values)
                win.destroy()
                self.refresh_database()
                self.draw_header()

            except ValueError as error:
                messagebox.showerror(
                    "Invalid entry",
                    str(error),
                    parent=win
                )

        self.button(
            card,
            "Save Material",
            save,
            accent=True
        ).pack(fill="x", padx=22, pady=(18, 8))

        self.button(
            card,
            "Cancel",
            win.destroy
        ).pack(fill="x", padx=22, pady=(0, 18))

    # ========================================================
    # COMPARE PAGE
    # ========================================================

    def build_compare_page(self, page):
        top_card, inner = self.make_card(page, padx=16, pady=14)
        top_card.pack(fill="x", pady=(0, 12))

        self.selection_label = tk.Label(
            inner,
            text="0 material(s) selected",
            bg=C["card"],
            fg=C["text"],
            font=("Segoe UI Semibold", 11)
        )
        self.selection_label.pack(side="left")

        tk.Label(
            inner,
            text="Select materials on the Database page, then return here.",
            bg=C["card"],
            fg=C["muted"],
            font=("Segoe UI", 9)
        ).pack(side="left", padx=18)

        self.button(
            inner,
            "Open Database",
            lambda: self.show_page("Database"),
            accent=True
        ).pack(side="right")

        card, body = self.make_card(page, padx=10, pady=10)
        card.pack(fill="both", expand=True)

        self.compare_tree = ttk.Treeview(
            body,
            columns=("property", "unit", "values"),
            show="headings",
            style="Dark.Treeview"
        )
        self.compare_tree.heading("property", text="Property")
        self.compare_tree.heading("unit", text="Unit")
        self.compare_tree.heading("values", text="Selected materials")

        self.compare_tree.column("property", width=220, anchor="w")
        self.compare_tree.column("unit", width=105, anchor="center")
        self.compare_tree.column("values", width=850, anchor="center")

        yscroll = ttk.Scrollbar(
            body,
            orient="vertical",
            command=self.compare_tree.yview,
            style="Dark.Vertical.TScrollbar"
        )
        self.compare_tree.configure(yscrollcommand=yscroll.set)
        self.compare_tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")

        self.update_comparison()

    # ========================================================
    # UPDATE COMPARISON
    # ========================================================

    def update_comparison(self):
        if not hasattr(self, "compare_tree"):
            return

        for item in self.compare_tree.get_children():
            self.compare_tree.delete(item)

        materials = self.selected_materials()
        if not materials:
            self.compare_tree["columns"] = ["property", "unit", "values"]
            self.compare_tree.heading("property", text="Property")
            self.compare_tree.heading("unit", text="Unit")
            self.compare_tree.heading("values", text="Selected materials")

            self.compare_tree.column("property", width=220)
            self.compare_tree.column("unit", width=105)
            self.compare_tree.column("values", width=850)

            self.compare_tree.insert(
                "",
                "end",
                values=(
                    "No materials selected",
                    "",
                    "Go to Database and select materials."
                )
            )
            return

        self.compare_tree["columns"] = ["property", "unit"] + [
            f"m{i}" for i in range(len(materials))
        ]

        self.compare_tree.heading("property", text="Property")
        self.compare_tree.heading("unit", text="Unit")
        self.compare_tree.column("property", width=220, anchor="w")
        self.compare_tree.column("unit", width=100, anchor="center")

        for i, material in enumerate(materials):
            key = f"m{i}"
            self.compare_tree.heading(key, text=material[0])
            self.compare_tree.column(key, width=170, anchor="center")

        property_rows = [
            ("Density", "g/cm³", 2),
            ("Young's Modulus", "GPa", 3),
            ("Yield Strength", "MPa", 4),
            ("Tensile Strength", "MPa", 5),
            ("Thermal Conductivity", "W/m·K", 6),
            ("Relative Cost", "$/kg", 7),
            ("Poisson Ratio", "", 8),
        ]

        for prop, unit, index in property_rows:
            self.compare_tree.insert(
                "",
                "end",
                values=[prop, unit] + [
                    f"{m[index]:.4g}" for m in materials
                ]
            )

    # ========================================================
    # ASHBY PLOT PAGE
    # ========================================================

    def build_plot_page(self, page):
        controls_card, controls = self.make_card(page, padx=14, pady=12)
        controls_card.pack(fill="x", pady=(0, 12))

        labels = ["X AXIS", "Y AXIS", "FILTER FAMILY"]
        for column, text in enumerate(labels):
            tk.Label(
                controls,
                text=text,
                bg=C["card"],
                fg=C["muted"],
                font=("Segoe UI Semibold", 8)
            ).grid(row=0, column=column, sticky="w")

        self.plot_x_var = tk.StringVar(value="density")
        self.plot_y_var = tk.StringVar(value="modulus")
        self.plot_family_var = tk.StringVar(value="All")

        properties = list(PROPERTY_INFO.keys())
        property_labels = [
            f"{PROPERTY_INFO[p][0]} ({PROPERTY_INFO[p][1]})"
            for p in properties
        ]
        self.plot_property_map = dict(zip(property_labels, properties))

        self.plot_x_combo = ttk.Combobox(
            controls,
            state="readonly",
            style="Dark.TCombobox",
            values=property_labels,
            width=29
        )
        self.plot_x_combo.set(property_labels[0])
        self.plot_x_combo.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        self.plot_y_combo = ttk.Combobox(
            controls,
            state="readonly",
            style="Dark.TCombobox",
            values=property_labels,
            width=29
        )
        self.plot_y_combo.set(property_labels[1])
        self.plot_y_combo.grid(row=1, column=1, sticky="ew", padx=(0, 10))

        self.plot_family_combo = ttk.Combobox(
            controls,
            textvariable=self.plot_family_var,
            state="readonly",
            style="Dark.TCombobox",
            values=["All"] + sorted({m[1] for m in self.materials}),
            width=18
        )
        self.plot_family_combo.grid(row=1, column=2, sticky="ew", padx=(0, 10))

        self.plot_x_log = tk.BooleanVar(value=True)
        self.plot_y_log = tk.BooleanVar(value=True)

        tk.Checkbutton(
            controls,
            text="Log X",
            variable=self.plot_x_log,
            command=self.update_plot,
            bg=C["card"],
            fg=C["text"],
            selectcolor=C["card2"],
            activebackground=C["card"],
            activeforeground=C["text"],
            font=("Segoe UI", 9)
        ).grid(row=1, column=3, padx=4)

        tk.Checkbutton(
            controls,
            text="Log Y",
            variable=self.plot_y_log,
            command=self.update_plot,
            bg=C["card"],
            fg=C["text"],
            selectcolor=C["card2"],
            activebackground=C["card"],
            activeforeground=C["text"],
            font=("Segoe UI", 9)
        ).grid(row=1, column=4, padx=4)

        self.button(
            controls,
            "↻ Update Plot",
            self.update_plot,
            accent=True
        ).grid(row=1, column=5, padx=(10, 0))

        # Zoom slider to "increase" graph
        tk.Label(
            controls,
            text="Zoom",
            bg=C["card"],
            fg=C["muted"],
            font=("Segoe UI Semibold", 8)
        ).grid(row=0, column=6, sticky="w", padx=(10, 0))

        self.plot_zoom = tk.DoubleVar(value=1.0)
        zoom_scale = tk.Scale(
            controls,
            from_=0.7,
            to=1.5,
            resolution=0.05,
            orient="horizontal",
            variable=self.plot_zoom,
            bg=C["card"],
            fg=C["text"],
            troughcolor=C["panel"],
            highlightthickness=0,
            length=120
        )
        zoom_scale.grid(row=1, column=6, padx=(10, 0))
        zoom_scale.bind("<ButtonRelease-1>", lambda e: self.update_plot())

        for combo in (self.plot_x_combo, self.plot_y_combo, self.plot_family_combo):
            combo.bind("<<ComboboxSelected>>", lambda event: self.update_plot())

        controls.columnconfigure(0, weight=2)
        controls.columnconfigure(1, weight=2)
        controls.columnconfigure(2, weight=1)

        plot_card, plot_body = self.make_card(page, padx=8, pady=8)
        plot_card.pack(fill="both", expand=True)

        self.plot_canvas = tk.Canvas(
            plot_body,
            bg=C["panel"],
            highlightthickness=0
        )
        self.plot_canvas.pack(fill="both", expand=True)
        self.plot_canvas.bind("<Configure>", lambda event: self.update_plot())

    # ========================================================
    # UPDATE ASHBY PLOT
    # ========================================================

    def update_plot(self):
        if not hasattr(self, "plot_canvas"):
            return

        canvas = self.plot_canvas
        canvas.delete("all")

        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width < 200 or height < 180:
            return

        x_label = self.plot_x_combo.get()
        y_label = self.plot_y_combo.get()
        if x_label not in self.plot_property_map or y_label not in self.plot_property_map:
            return

        x_property = self.plot_property_map[x_label]
        y_property = self.plot_property_map[y_label]
        x_index = PROPERTY_INDEX[x_property]
        y_index = PROPERTY_INDEX[y_property]

        family = self.plot_family_var.get()
        materials = [
            m for m in self.materials
            if family == "All" or m[1] == family
        ]

        points = [
            (m[x_index], m[y_index], m)
            for m in materials
            if m[x_index] is not None and m[y_index] is not None
            and m[x_index] > 0 and m[y_index] > 0
        ]

        if not points:
            canvas.create_text(
                width / 2,
                height / 2,
                text="No positive data available.",
                fill=C["muted"],
                font=("Segoe UI", 12)
            )
            return

        left = 76
        right = 35
        top = 40
        bottom = 64

        px0 = left
        px1 = width - right
        py0 = top
        py1 = height - bottom

        def transform(value, log):
            if log and value > 0:
                return math.log10(value)
            return value

        xs = [transform(p[0], self.plot_x_log.get()) for p in points]
        ys = [transform(p[1], self.plot_y_log.get()) for p in points]

        xmin = min(xs)
        xmax = max(xs)
        ymin = min(ys)
        ymax = max(ys)

        if xmin == xmax:
            xmin -= 1
            xmax += 1
        if ymin == ymax:
            ymin -= 1
            ymax += 1

        dx = xmax - xmin
        dy = ymax - ymin

        zoom = self.plot_zoom.get()
        xmin -= dx * 0.08 * zoom
        xmax += dx * 0.08 * zoom
        ymin -= dy * 0.08 * zoom
        ymax += dy * 0.08 * zoom

        def screen_x(value):
            transformed = transform(value, self.plot_x_log.get())
            return (
                px0 +
                (transformed - xmin) / (xmax - xmin) * (px1 - px0)
            )

        def screen_y(value):
            transformed = transform(value, self.plot_y_log.get())
            return (
                py1 -
                (transformed - ymin) / (ymax - ymin) * (py1 - py0)
            )

        # Grid
        for i in range(6):
            xx = px0 + i * (px1 - px0) / 5
            yy = py0 + i * (py1 - py0) / 5

            canvas.create_line(
                xx, py0, xx, py1,
                fill=C["grid"],
                dash=(2, 5)
            )
            canvas.create_line(
                px0, yy, px1, yy,
                fill=C["grid"],
                dash=(2, 5)
            )

        canvas.create_rectangle(
            px0, py0, px1, py1,
            outline=C["border"]
        )

        # Ticks
        for i in range(6):
            x_value = xmin + i * (xmax - xmin) / 5
            y_value = ymin + i * (ymax - ymin) / 5

            xx = px0 + i * (px1 - px0) / 5
            yy = py1 - i * (py1 - py0) / 5

            if self.plot_x_log.get():
                x_text = self.format_log_tick(x_value)
            else:
                x_text = f"{x_value:.3g}"

            if self.plot_y_log.get():
                y_text = self.format_log_tick(y_value)
            else:
                y_text = f"{y_value:.3g}"

            canvas.create_text(
                xx, py1 + 19,
                text=x_text,
                fill=C["muted"],
                font=("Segoe UI", 8)
            )
            canvas.create_text(
                px0 - 15, yy,
                text=y_text,
                fill=C["muted"],
                font=("Segoe UI", 8),
                anchor="e"
            )

        # Axis labels
        canvas.create_text(
            (px0 + px1) / 2,
            height - 20,
            text=x_label,
            fill=C["text"],
            font=("Segoe UI Semibold", 9)
        )
        canvas.create_text(
            20,
            (py0 + py1) / 2,
            text=y_label,
            fill=C["text"],
            angle=90,
            font=("Segoe UI Semibold", 9)
        )

        # Data points + neon backglow + transparent circles
        family_points = {}
        for x, y, material in points:
            xx = screen_x(x)
            yy = screen_y(y)
            color = FAMILY_COLORS.get(material[1], C["purple"])

            # Neon backglow behind rounded point
            canvas.create_oval(
                xx - 10, yy - 10, xx + 10, yy + 10,
                fill="", outline=C["cyan_glow"], width=1
            )

            # Point
            canvas.create_oval(
                xx - 5, yy - 5, xx + 5, yy + 5,
                fill=color,
                outline="#FFFFFF",
                width=1
            )

            # Label
            canvas.create_text(
                xx + 8, yy,
                text=material[0],
                anchor="w",
                fill=C["muted"],
                font=("Segoe UI", 7)
            )

            family_points.setdefault(material[1], []).append((xx, yy))

        # Transparent circles outlining material types (families)
        for fam, pts in family_points.items():
            if len(pts) < 2:
                continue
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            cx = sum(xs) / len(xs)
            cy = sum(ys) / len(ys)
            r = max(
                max(abs(x - cx) for x in xs),
                max(abs(y - cy) for y in ys)
            ) + 20
            color = FAMILY_COLORS.get(fam, C["purple"])
            canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline=color,
                width=1
            )

        # Legend
        families = sorted({m[1] for _, _, m in points})
        legend_x = px0 + 10
        legend_y = py0 + 10

        canvas.create_text(
            legend_x,
            legend_y - 3,
            text="FAMILY",
            anchor="w",
            fill=C["text"],
            font=("Segoe UI Semibold", 8)
        )

        for index, family_name in enumerate(families):
            yy = legend_y + 17 + index * 18
            color = FAMILY_COLORS.get(family_name, C["purple"])

            canvas.create_oval(
                legend_x, yy - 4, legend_x + 8, yy + 4,
                fill=color,
                outline=""
            )
            canvas.create_text(
                legend_x + 15, yy,
                text=family_name,
                anchor="w",
                fill=C["muted"],
                font=("Segoe UI", 8)
            )

    # ========================================================
    # LOG TICK FORMAT
    # ========================================================

    @staticmethod
    def format_log_tick(log_value):
        value = 10 ** log_value
        if value >= 1000 or value < 0.01:
            return f"{value:.1e}"
        if value >= 10:
            return f"{value:.0f}"
        return f"{value:.2g}"

    # ========================================================
    # SCREENING PAGE
    # ========================================================

    def build_screening_page(self, page):
        top_card, top = self.make_card(page, padx=14, pady=12)
        top_card.pack(fill="x", pady=(0, 12))

        tk.Label(
            top,
            text="SCREENING CRITERIA",
            bg=C["card"],
            fg=C["text"],
            font=("Segoe UI Semibold", 12)
        ).pack(anchor="w")

        tk.Label(
            top,
            text="Turn constraints on/off, choose a direction, and set a target value.",
            bg=C["card"],
            fg=C["muted"],
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(2, 12))

        self.screen_rows = {}

        criteria = [
            ("density", "Density", "g/cm³"),
            ("modulus", "Young's Modulus", "GPa"),
            ("yield", "Yield Strength", "MPa"),
            ("tensile", "Tensile Strength", "MPa"),
            ("thermal", "Thermal Conductivity", "W/m·K"),
            ("cost", "Relative Cost", "$/kg"),
        ]

        header = tk.Frame(top, bg=C["card"])
        header.pack(fill="x")

        headings = ["Use", "Property", "Direction", "Limit / target", "Unit", "Weight"]
        for column, heading in enumerate(headings):
            tk.Label(
                header,
                text=heading,
                bg=C["card"],
                fg=C["muted"],
                font=("Segoe UI Semibold", 8)
            ).grid(row=0, column=column, sticky="w", padx=5, pady=3)

        for row_index, (key, name, unit) in enumerate(criteria, start=1):
            row = tk.Frame(top, bg=C["card2"])
            row.pack(fill="x", pady=2)

            enabled = tk.BooleanVar(value=(key in ("density", "modulus")))
            direction = tk.StringVar(
                value="≤" if PROPERTY_INFO[key][2] == "lower" else "≥"
            )
            value = tk.DoubleVar(value=self.default_screen_value(key))
            weight = tk.DoubleVar(value=1.0)

            tk.Checkbutton(
                row,
                variable=enabled,
                bg=C["card2"],
                fg=C["text"],
                selectcolor=C["purple2"],
                activebackground=C["card2"],
                activeforeground=C["text"]
            ).grid(row=0, column=0, padx=7)

            tk.Label(
                row,
                text=name,
                bg=C["card2"],
                fg=C["text"],
                font=("Segoe UI", 9)
            ).grid(row=0, column=1, sticky="w", padx=5)

            combo = ttk.Combobox(
                row,
                textvariable=direction,
                values=["≤", "≥"],
                state="readonly",
                style="Dark.TCombobox",
                width=6
            )
            combo.grid(row=0, column=2, padx=5, pady=5)

            spin = tk.Spinbox(
                row,
                textvariable=value,
                from_=0,
                to=1000000,
                increment=self.screen_increment(key),
                width=12,
                bg=C["panel"],
                fg=C["text"],
                buttonbackground=C["card2"],
                insertbackground=C["text"],
                relief="flat",
                bd=0,
                highlightthickness=1,
                highlightbackground=C["border"]
            )
            spin.grid(row=0, column=3, padx=5)

            tk.Label(
                row,
                text=unit,
                bg=C["card2"],
                fg=C["muted"],
                font=("Segoe UI", 8)
            ).grid(row=0, column=4, sticky="w", padx=5)

            weight_spin = tk.Spinbox(
                row,
                textvariable=weight,
                from_=0,
                to=10,
                increment=0.5,
                width=8,
                bg=C["panel"],
                fg=C["text"],
                buttonbackground=C["card2"],
                insertbackground=C["text"],
                relief="flat",
                bd=0,
                highlightthickness=1,
                highlightbackground=C["border"]
            )
            weight_spin.grid(row=0, column=5, padx=5)

            for column, weight_value in enumerate([0, 2, 1, 1, 1, 1]):
                row.columnconfigure(column, weight=weight_value)

            self.screen_rows[key] = {
                "enabled": enabled,
                "direction": direction,
                "value": value,
                "weight": weight,
            }

        actions = tk.Frame(top, bg=C["card"])
        actions.pack(fill="x", pady=(10, 0))

        self.button(
            actions,
            "Run Screening",
            self.run_screening,
            accent=True
        ).pack(side="left")

        self.button(
            actions,
            "Reset Criteria",
            self.reset_screening
        ).pack(side="left", padx=8)

        result_card, result = self.make_card(page, padx=10, pady=10)
        result_card.pack(fill="both", expand=True)

        self.screen_tree = ttk.Treeview(
            result,
            columns=("rank", "material", "family", "score", "matched"),
            show="headings",
            style="Dark.Treeview"
        )

        result_columns = [
            ("rank", "Rank", 70),
            ("material", "Material", 270),
            ("family", "Family", 120),
            ("score", "Weighted Score", 150),
            ("matched", "Criteria Passed", 160),
        ]
        for key, heading, width in result_columns:
            self.screen_tree.heading(key, text=heading)
            self.screen_tree.column(
                key,
                width=width,
                anchor=("w" if key == "material" else "center")
            )

        yscroll = ttk.Scrollbar(
            result,
            orient="vertical",
            command=self.screen_tree.yview,
            style="Dark.Vertical.TScrollbar"
        )
        self.screen_tree.configure(yscrollcommand=yscroll.set)
        self.screen_tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")

        self.screen_tree.tag_configure(
            "top",
            background="#1D2340",
            foreground="#FFFFFF"
        )

    # ========================================================
    # SCREENING DEFAULT VALUES
    # ========================================================

    def default_screen_value(self, key):
        return {
            "density": 2.0,
            "modulus": 20.0,
            "yield": 100.0,
            "tensile": 100.0,
            "thermal": 1.0,
            "cost": 10.0,
        }.get(key, 1.0)

    # ========================================================
    # SCREENING INCREMENT
    # ========================================================

    def screen_increment(self, key):
        return {
            "density": 0.1,
            "modulus": 1,
            "yield": 10,
            "tensile": 10,
            "thermal": 0.1,
            "cost": 0.5,
        }.get(key, 0.1)

    # ========================================================
    # RESET SCREENING
    # ========================================================

    def reset_screening(self):
        for key, row in self.screen_rows.items():
            row["enabled"].set(key in ("density", "modulus"))
            row["direction"].set("≤" if PROPERTY_INFO[key][2] == "lower" else "≥")
            row["value"].set(self.default_screen_value(key))
            row["weight"].set(1.0)

        for item in self.screen_tree.get_children():
            self.screen_tree.delete(item)

    # ========================================================
    # RUN SCREENING
    # ========================================================

    def run_screening(self):
        criteria = []
        for key, row in self.screen_rows.items():
            if not row["enabled"].get():
                continue
            try:
                target = float(row["value"].get())
                weight = max(0.0, float(row["weight"].get()))
            except ValueError:
                messagebox.showerror(
                    "Invalid screening value",
                    f"Check the values entered for {key}.",
                    parent=self.root
                )
                return
            criteria.append((key, row["direction"].get(), target, weight))

        for item in self.screen_tree.get_children():
            self.screen_tree.delete(item)

        if not criteria:
            self.screen_tree.insert(
                "",
                "end",
                values=("_", "No criteria selected", "", "", "")
            )
            return

        results = []
        for material in self.materials:
            score = 0.0
            passed = 0
            for key, direction, target, weight in criteria:
                actual = material[PROPERTY_INDEX[key]]
                if direction == "≤":
                    ok = (actual <= target)
                    closeness = (target / actual) if actual > 0 else 0
                else:
                    ok = (actual >= target)
                    closeness = (actual / target) if target > 0 else 0

                if ok:
                    passed += 1
                    score += weight * min(2.0, max(0.0, closeness))

            results.append((score, passed, material))

        results.sort(key=lambda x: (x[1], x[0]), reverse=True)

        for rank, (score, passed, material) in enumerate(results, start=1):
            self.screen_tree.insert(
                "",
                "end",
                values=(
                    rank,
                    material[0],
                    material[1],
                    f"{score:.3f}",
                    f"{passed}/{len(criteria)}"
                ),
                tags=("top" if rank <= 3 else "")
            )

    # ========================================================
    # EXPORT CSV
    # ========================================================

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            title="Export Material Database",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return

        headers = [
            "Material",
            "Family",
            "Density (g/cm³)",
            "Young's Modulus (GPa)",
            "Yield Strength (MPa)",
            "Tensile Strength (MPa)",
            "Thermal Conductivity (W/m·K)",
            "Cost ($/kg)",
            "Poisson Ratio",
        ]

        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(self.materials)

            messagebox.showinfo(
                "Export complete",
                f"Material database exported to:\n\n{path}",
                parent=self.root
            )
        except OSError as error:
            messagebox.showerror(
                "Export failed",
                str(error),
                parent=self.root
            )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = MaterialSelectionApp(root)
    root.mainloop()
