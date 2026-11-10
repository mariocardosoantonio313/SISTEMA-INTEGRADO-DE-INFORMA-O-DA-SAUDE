from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from client.services.api_client import ApiClient


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("SIIS-UÍGE - Autenticação")
        self.root.geometry("820x520")
        self.root.minsize(700, 480)
        self.root.configure(bg="#f4f7fb")

        self.api_client = ApiClient()

        self.main_frame = ttk.Frame(root, padding=30)
        self.main_frame.pack(fill="both", expand=True)

        self.brand = ttk.Label(
            self.main_frame,
            text="SIIS-UÍGE",
            font=("Segoe UI", 26, "bold"),
            foreground="#0a3d62",
        )
        self.brand.pack(pady=(10, 4))

        self.subtitle = ttk.Label(
            self.main_frame,
            text="Sistema Integrado de Informação da Saúde",
            font=("Segoe UI", 12),
            foreground="#4a5a6a",
        )
        self.subtitle.pack(pady=(0, 20))

        self.card = ttk.Frame(self.main_frame, padding=24, style="Card.TFrame")
        self.card.pack(fill="both", expand=True)

        ttk.Style().configure("Card.TFrame", background="#ffffff")

        ttk.Label(self.card, text="Servidor", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.server_var = tk.StringVar(value="http://127.0.0.1:8000")
        ttk.Entry(self.card, textvariable=self.server_var, width=45).pack(fill="x", pady=(0, 12))

        ttk.Label(self.card, text="Nome de utilizador", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.username_var = tk.StringVar()
        ttk.Entry(self.card, textvariable=self.username_var).pack(fill="x", pady=(0, 12))

        ttk.Label(self.card, text="Palavra-passe", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.card, textvariable=self.password_var, show="*")
        self.password_entry.pack(fill="x", pady=(0, 8))

        self.show_password = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self.card,
            text="Mostrar palavra-passe",
            variable=self.show_password,
            command=self.toggle_password_visibility,
        ).pack(anchor="w", pady=(0, 12))

        self.status_var = tk.StringVar(value="Estado da ligação: não verificada")
        ttk.Label(self.card, textvariable=self.status_var, foreground="#666666").pack(anchor="w", pady=(0, 12))

        self.login_button = ttk.Button(self.card, text="Entrar", command=self.login)
        self.login_button.pack(fill="x", pady=(6, 0))

        self.root.bind("<Return>", lambda event: self.login())

    def toggle_password_visibility(self):
        self.password_entry.configure(show="" if self.show_password.get() else "*")

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        server_url = self.server_var.get().strip()

        if not username or not password:
            messagebox.showerror("Validação", "Preencha o nome de utilizador e a palavra-passe.")
            return

        self.api_client = ApiClient(server_url)
        ok, payload = self.api_client.ping()
        if not ok:
            self.status_var.set("Estado da ligação: servidor indisponível")
            messagebox.showerror("Ligação", "Não foi possível conectar ao servidor. Verifique o endereço IP e a porta.")
            return

        self.status_var.set("Estado da ligação: servidor disponível")
        response = self.api_client.post("/api/login", {"username": username, "password": password})

        if response.status_code == 200:
            data = response.json()
            messagebox.showinfo("Sucesso", f"Bem-vindo, {data.get('username')}.")
            self.root.destroy()
            import tkinter as tk

            app = tk.Tk()
            from client.views.dashboard import DashboardWindow
            DashboardWindow(app, username=data.get("username"), profile=data.get("profile"), server_url=server_url)
            app.mainloop()
            return

        try:
            detail = response.json().get("detail", "Credenciais inválidas.")
        except Exception:
            detail = "Credenciais inválidas."

        messagebox.showerror("Autenticação", detail)


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
