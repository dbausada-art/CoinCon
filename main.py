import customtkinter as ctk

from api import get_rate, get_supported_currencies

COMMON_CURRENCIES = [
    ("USD", "United States"),
    ("EUR", "Eurozone"),
    ("GBP", "Great Britain"),
    ("JPY", "Japan"),
    ("CNY", "China"),
    ("CHF", "Switzerland"),
    ("CAD", "Canada"),
    ("AUD", "Australia"),
    ("NZD", "New Zealand"),
    ("SEK", "Sweden"),
    ("NOK", "Norway"),
    ("DKK", "Denmark"),
    ("SGD", "Singapore"),
    ("HKD", "Hong Kong"),
    ("INR", "India"),
    ("KRW", "South Korea"),
    ("MXN", "Mexico"),
    ("BRL", "Brazil"),
    ("ZAR", "South Africa"),
    ("AED", "United Arab Emirates"),
]

CURRENCY_OPTIONS = [f"{code} ({country})" for code, country in COMMON_CURRENCIES]


def extract_code(value: str) -> str:
    return value.split(" ", 1)[0].strip().upper()


class CurrencyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title("Conversor de Monedas")
        self.geometry("760x520")
        self.minsize(700, 500)

        self.dropdown_options = self._load_dropdown_options()

        self.from_currency_var = ctk.StringVar(value="USD")
        self.to_currency_var = ctk.StringVar(value="EUR")
        self.amount_var = ctk.StringVar()
        self.result_var = ctk.StringVar(value="Resultado: -")
        self.status_var = ctk.StringVar(value="Listo para convertir")

        self._build_ui()

    def _load_dropdown_options(self):
        try:
            supported = get_supported_currencies()
            if supported:
                return supported
        except (RuntimeError, ValueError):
            pass

        return [code for code, _country in COMMON_CURRENCIES]

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(self, corner_radius=16)
        container.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)

        top_row = ctk.CTkFrame(container, fg_color="transparent")
        top_row.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))
        top_row.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            top_row,
            text="Conversor de Monedas",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        title_label.grid(row=0, column=0, sticky="w")

        theme_menu = ctk.CTkOptionMenu(
            top_row,
            values=["System", "Light", "Dark"],
            command=ctk.set_appearance_mode,
            width=120,
        )
        theme_menu.set("System")
        theme_menu.grid(row=0, column=1, sticky="e")

        subtitle = ctk.CTkLabel(
            container,
            text="Selecciona monedas, escribe cantidad y convierte en un clic",
            text_color=("gray30", "gray70"),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=18)

        currencies_text = "Monedas comunes: " + ", ".join(CURRENCY_OPTIONS)
        info_box = ctk.CTkTextbox(container, height=80, corner_radius=10)
        info_box.grid(row=2, column=0, sticky="ew", padx=18, pady=(10, 12))
        info_box.insert("1.0", currencies_text)
        info_box.configure(state="disabled")

        form = ctk.CTkFrame(container, corner_radius=12)
        form.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 12))
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form, text="Moneda origen").grid(row=0, column=0, sticky="w", padx=14, pady=(12, 6))
        from_selector = ctk.CTkFrame(form, fg_color="transparent")
        from_selector.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 12))
        from_selector.grid_columnconfigure(0, weight=1)

        from_value = ctk.CTkEntry(from_selector, textvariable=self.from_currency_var, state="readonly")
        from_value.grid(row=0, column=0, sticky="ew")

        from_pick = ctk.CTkButton(
            from_selector,
            text="Elegir moneda",
            width=130,
            command=lambda: self._open_currency_picker(self.from_currency_var, "Moneda origen"),
        )
        from_pick.grid(row=0, column=1, padx=(8, 0))

        ctk.CTkLabel(form, text="Moneda destino").grid(row=0, column=1, sticky="w", padx=14, pady=(12, 6))
        to_selector = ctk.CTkFrame(form, fg_color="transparent")
        to_selector.grid(row=1, column=1, sticky="ew", padx=14, pady=(0, 12))
        to_selector.grid_columnconfigure(0, weight=1)

        to_value = ctk.CTkEntry(to_selector, textvariable=self.to_currency_var, state="readonly")
        to_value.grid(row=0, column=0, sticky="ew")

        to_pick = ctk.CTkButton(
            to_selector,
            text="Elegir moneda",
            width=130,
            command=lambda: self._open_currency_picker(self.to_currency_var, "Moneda destino"),
        )
        to_pick.grid(row=0, column=1, padx=(8, 0))

        buttons_row = ctk.CTkFrame(form, fg_color="transparent")
        buttons_row.grid(row=2, column=0, columnspan=2, sticky="ew", padx=14, pady=(0, 12))
        buttons_row.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(buttons_row, text="Cantidad (ej. 10.50)").grid(row=0, column=0, sticky="w", pady=(0, 6))
        amount_entry = ctk.CTkEntry(buttons_row, textvariable=self.amount_var, width=180)
        amount_entry.grid(row=1, column=0, sticky="w")
        amount_entry.focus()

        swap_button = ctk.CTkButton(buttons_row, text="Intercambiar", width=130, command=self.swap_currencies)
        swap_button.grid(row=1, column=1, padx=(12, 10), sticky="w")

        convert_button = ctk.CTkButton(buttons_row, text="Convertir", width=130, command=self.convert)
        convert_button.grid(row=1, column=2, sticky="e")

        exit_button = ctk.CTkButton(buttons_row, text="Salir", width=110, command=self.destroy)
        exit_button.grid(row=1, column=3, padx=(10, 0), sticky="e")

        result_card = ctk.CTkFrame(container, corner_radius=12)
        result_card.grid(row=4, column=0, sticky="ew", padx=18, pady=(0, 10))
        result_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            result_card,
            text="Resultado",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(10, 4))

        ctk.CTkLabel(
            result_card,
            textvariable=self.result_var,
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=1, column=0, sticky="w", padx=14, pady=(0, 12))

        status_label = ctk.CTkLabel(
            container,
            textvariable=self.status_var,
            text_color=("gray35", "gray70"),
        )
        status_label.grid(row=5, column=0, sticky="w", padx=18, pady=(0, 14))

        self.bind("<Return>", lambda _event: self.convert())

    def swap_currencies(self):
        current_from = self.from_currency_var.get()
        current_to = self.to_currency_var.get()
        self.from_currency_var.set(current_to)
        self.to_currency_var.set(current_from)
        self.status_var.set("Monedas intercambiadas")

    def convert(self):
        from_value = self.from_currency_var.get().strip()
        to_value = self.to_currency_var.get().strip()
        amount_text = self.amount_var.get().strip().replace(",", ".")

        if not from_value or not to_value:
            self.status_var.set("Selecciona moneda origen y destino")
            self._show_error("Selecciona moneda origen y destino.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            self.status_var.set("Cantidad invalida")
            self._show_error("La cantidad debe ser un numero (ej. 10.50).")
            return

        if amount < 0:
            self.status_var.set("Cantidad invalida")
            self._show_error("La cantidad no puede ser negativa.")
            return

        from_code = extract_code(from_value)
        to_code = extract_code(to_value)

        if len(from_code) != 3 or not from_code.isascii() or not from_code.isalpha():
            self.status_var.set("Moneda origen invalida")
            self._show_error("La moneda origen debe ser un codigo de 3 letras (ej. USD).")
            return

        if len(to_code) != 3 or not to_code.isascii() or not to_code.isalpha():
            self.status_var.set("Moneda destino invalida")
            self._show_error("La moneda destino debe ser un codigo de 3 letras (ej. EUR).")
            return

        self.status_var.set("Consultando tasa de cambio...")
        self.update_idletasks()

        try:
            rate = get_rate(from_code, to_code)
        except (RuntimeError, ValueError) as error:
            self.status_var.set("No se pudo convertir")
            self._show_error(str(error))
            return

        result = amount * rate
        self.result_var.set(f"{amount:.2f} {from_code} = {result:.2f} {to_code}")
        self.status_var.set("Conversion completada")

    def _show_error(self, message: str):
        popup = ctk.CTkToplevel(self)
        popup.title("Error")
        popup.geometry("380x150")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        frame = ctk.CTkFrame(popup, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(frame, text="Error", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=12, pady=(12, 4))
        ctk.CTkLabel(frame, text=message, wraplength=330, justify="left").pack(anchor="w", padx=12, pady=(0, 12))
        ctk.CTkButton(frame, text="Aceptar", width=100, command=popup.destroy).pack(anchor="e", padx=12, pady=(0, 12))

    def _open_currency_picker(self, target_var: ctk.StringVar, title: str):
        popup = ctk.CTkToplevel(self)
        popup.title(title)
        popup.geometry("360x460")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        frame = ctk.CTkFrame(popup, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(frame, text=f"{title}: elige una moneda", font=ctk.CTkFont(size=16, weight="bold")).pack(
            anchor="w", padx=12, pady=(12, 6)
        )

        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(frame, textvariable=search_var, placeholder_text="Buscar codigo (ej. USD)")
        search_entry.pack(fill="x", padx=12, pady=(0, 8))

        list_frame = ctk.CTkScrollableFrame(frame, corner_radius=10, height=320)
        list_frame.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        def render_options(*_args):
            for child in list_frame.winfo_children():
                child.destroy()

            query = search_var.get().strip().upper()
            options = [code for code in self.dropdown_options if query in code]

            if not options:
                ctk.CTkLabel(list_frame, text="No hay coincidencias.").pack(anchor="w", padx=6, pady=6)
                return

            for code in options:
                ctk.CTkButton(
                    list_frame,
                    text=code,
                    anchor="w",
                    command=lambda value=code: self._select_currency(value, target_var, popup),
                ).pack(fill="x", padx=6, pady=4)

        search_var.trace_add("write", render_options)
        render_options()
        search_entry.focus()

    def _select_currency(self, value: str, target_var: ctk.StringVar, popup: ctk.CTkToplevel):
        target_var.set(value)
        popup.destroy()


if __name__ == "__main__":
    app = CurrencyApp()
    app.mainloop()
