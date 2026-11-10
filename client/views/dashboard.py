from __future__ import annotations

import json
from tkinter import messagebox, ttk
import tkinter as tk

import requests


class DashboardWindow:
    def __init__(self, root, username: str, profile: str, server_url: str):
        self.root = root
        self.root.title("SIIS-UÍGE - Dashboard")
        self.root.geometry("1300x760")
        self.root.configure(bg="#edf2f7")

        self.username = username
        self.profile = profile
        self.server_url = server_url
        self.data_shares = []

        self.sidebar = tk.Frame(root, bg="#0f2d3d", width=220)
        self.sidebar.pack(side="left", fill="y")

        title = tk.Label(
            self.sidebar,
            text="SIIS-UÍGE",
            bg="#0f2d3d",
            fg="#ffffff",
            font=("Segoe UI", 18, "bold"),
            pady=20,
        )
        title.pack(fill="x")

        nav_items = {
            "Painel Principal": self.show_dashboard,
            "Gestão de Pacientes": self.show_patients,
            "Unidades de Saúde": self.show_units,
            "Consultas": self.show_consultas,
            "Histórico Clínico": self.show_history,
            "Partilha de Dados": self.show_data_sharing,
            "Gestão de Utilizadores": self.show_users,
            "Relatórios": self.show_reports,
            "Configurações": self.show_settings,
            "Terminar Sessão": self.logout,
        }

        for item, action in nav_items.items():
            btn = tk.Button(
                self.sidebar,
                text=item,
                bg="#0f2d3d",
                fg="#dfeaf5",
                activebackground="#153f54",
                activeforeground="#ffffff",
                bd=0,
                height=2,
                padx=16,
                anchor="w",
                command=lambda _action=action: _action(),
            )
            btn.pack(fill="x", padx=12, pady=2)

        self.content = tk.Frame(root, bg="#edf2f7")
        self.content.pack(side="right", fill="both", expand=True)

        self.topbar = tk.Frame(self.content, bg="#ffffff")
        self.topbar.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(self.topbar, text=f"Utilizador: {username}", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#1d3557").pack(side="left", padx=16, pady=12)
        tk.Label(self.topbar, text=f"Perfil: {profile}", bg="#ffffff", font=("Segoe UI", 10), fg="#355c7d").pack(side="left")
        tk.Label(self.topbar, text=f"Servidor: {server_url}", bg="#ffffff", font=("Segoe UI", 10), fg="#355c7d").pack(side="right", padx=16)

        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def fetch_dashboard_stats(self):
        try:
            response = requests.get(f"{self.server_url}/api/dashboard", timeout=10)
            if response.ok:
                return response.json()
        except requests.RequestException:
            return {"pacientes": 0, "unidades": 0, "consultas": 0, "utilizadores": 0}
        return {"pacientes": 0, "unidades": 0, "consultas": 0, "utilizadores": 0}

    def show_dashboard(self):
        self.clear_content()
        stats = self.fetch_dashboard_stats()

        stats_frame = tk.Frame(self.content, bg="#edf2f7")
        stats_frame.pack(fill="x", padx=20, pady=(0, 10))

        cards = [
            ("Pacientes", stats.get("pacientes", 0), "#1f78b4"),
            ("Unidades", stats.get("unidades", 0), "#2e8b57"),
            ("Consultas", stats.get("consultas", 0), "#6a4c93"),
            ("Utilizadores", stats.get("utilizadores", 0), "#e76f51"),
        ]

        for label, value, color in cards:
            card = tk.Frame(stats_frame, bg="#ffffff", padx=18, pady=16, highlightbackground="#dfe3e8", highlightthickness=1)
            card.pack(side="left", fill="both", expand=True, padx=6)
            tk.Label(card, text=label, bg="#ffffff", fg="#666666", font=("Segoe UI", 10)).pack(anchor="w")
            tk.Label(card, text=str(value), bg="#ffffff", fg=color, font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(8, 0))

        table_panel = tk.Frame(self.content, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        table_panel.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(table_panel, text="Actividade recente", bg="#ffffff", font=("Segoe UI", 14, "bold"), fg="#0f2d3d").pack(anchor="w", padx=18, pady=(18, 8))

        columns = ("Evento", "Unidade", "Hora")
        tree = ttk.Treeview(table_panel, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=220, anchor="w")

        rows = [
            ("Registro de paciente", "Hospital Provincial do Uíge", "08:30"),
            ("Consulta agendada", "Centro de Saúde de Damba", "09:15"),
            ("Partilha de dados", "Hospital Municipal de Nzeto", "10:40"),
            ("Acesso autorizado", "Posto de Saúde de Bungo", "12:10"),
        ]
        for row in rows:
            tree.insert("", "end", values=row)
        tree.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def show_patients(self):
        self.clear_content()
        form_frame = tk.Frame(self.content, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        form_frame.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(form_frame, text="Registar paciente", bg="#ffffff", font=("Segoe UI", 14, "bold"), fg="#0f2d3d").pack(anchor="w", padx=16, pady=(16, 10))

        fields = {
            "full_name": tk.StringVar(),
            "birth_date": tk.StringVar(),
            "gender": tk.StringVar(value="Masculino"),
            "identity_card": tk.StringVar(),
            "nif": tk.StringVar(),
            "contact": tk.StringVar(),
            "address": tk.StringVar(),
        }

        for label_name, var in [
            ("Nome completo", fields["full_name"]),
            ("Data de nascimento (AAAA-MM-DD)", fields["birth_date"]),
            ("Género", fields["gender"]),
            ("Bilhete de identidade", fields["identity_card"]),
            ("NIF", fields["nif"]),
            ("Contacto", fields["contact"]),
            ("Endereço", fields["address"]),
        ]:
            row = tk.Frame(form_frame, bg="#ffffff")
            row.pack(fill="x", padx=16, pady=6)
            tk.Label(row, text=label_name, bg="#ffffff", width=22, anchor="w").pack(side="left")
            tk.Entry(row, textvariable=var, width=40).pack(side="left")

        def create_patient():
            payload = {
                "full_name": fields["full_name"].get().strip(),
                "birth_date": fields["birth_date"].get().strip() or None,
                "gender": fields["gender"].get().strip(),
                "identity_card": fields["identity_card"].get().strip() or None,
                "nif": fields["nif"].get().strip() or None,
                "contact": fields["contact"].get().strip() or None,
                "address": fields["address"].get().strip() or None,
                "health_unit_id": 1,
            }
            if not payload["full_name"]:
                messagebox.showerror("Validação", "O nome do paciente é obrigatório.")
                return
            try:
                response = requests.post(f"{self.server_url}/api/patients", json=payload, timeout=10)
                if response.ok:
                    messagebox.showinfo("Sucesso", "Paciente registado com sucesso.")
                    self.show_patients()
                else:
                    messagebox.showerror("Erro", response.json().get("detail", "Erro ao registar paciente."))
            except requests.RequestException:
                messagebox.showerror("Ligação", "Não foi possível comunicar com o servidor.")

        btn = tk.Button(form_frame, text="Guardar paciente", command=create_patient, bg="#0a3d62", fg="#ffffff")
        btn.pack(anchor="w", padx=16, pady=(10, 16))

        list_frame = tk.Frame(self.content, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tk.Label(list_frame, text="Pacientes registados", bg="#ffffff", font=("Segoe UI", 14, "bold"), fg="#0f2d3d").pack(anchor="w", padx=16, pady=(16, 10))

        try:
            response = requests.get(f"{self.server_url}/api/patients", timeout=10)
            rows = response.json() if response.ok else []
        except requests.RequestException:
            rows = []

        tree = ttk.Treeview(list_frame, columns=("ID", "Nome", "Data", "Contacto"), show="headings", height=12)
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Data", text="Nascimento")
        tree.heading("Contacto", text="Contacto")
        for col in ("ID", "Nome", "Data", "Contacto"):
            tree.column(col, width=180, anchor="w")
        for row in rows:
            tree.insert("", "end", values=(row.get("patient_identifier", "-"), row.get("full_name", "-"), row.get("birth_date", "-"), row.get("contact", "-")))
        tree.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def show_units(self):
        self.clear_content()
        form_frame = tk.Frame(self.content, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        form_frame.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(form_frame, text="Registar unidade de saúde", bg="#ffffff", font=("Segoe UI", 14, "bold"), fg="#0f2d3d").pack(anchor="w", padx=16, pady=(16, 10))

        fields = {
            "name": tk.StringVar(),
            "unit_type": tk.StringVar(value="Hospital"),
            "municipality": tk.StringVar(),
            "address": tk.StringVar(),
            "contact": tk.StringVar(),
            "status": tk.StringVar(value="active"),
        }

        for label_name, var in [
            ("Nome", fields["name"]),
            ("Tipo", fields["unit_type"]),
            ("Município", fields["municipality"]),
            ("Endereço", fields["address"]),
            ("Contacto", fields["contact"]),
            ("Estado", fields["status"]),
        ]:
            row = tk.Frame(form_frame, bg="#ffffff")
            row.pack(fill="x", padx=16, pady=6)
            tk.Label(row, text=label_name, bg="#ffffff", width=18, anchor="w").pack(side="left")
            tk.Entry(row, textvariable=var, width=40).pack(side="left")

        def create_unit():
            payload = {
                "name": fields["name"].get().strip(),
                "unit_type": fields["unit_type"].get().strip(),
                "municipality": fields["municipality"].get().strip(),
                "address": fields["address"].get().strip() or None,
                "contact": fields["contact"].get().strip() or None,
                "status": fields["status"].get().strip() or "active",
            }
            if not payload["name"] or not payload["municipality"]:
                messagebox.showerror("Validação", "Nome e município são obrigatórios.")
                return
            try:
                response = requests.post(f"{self.server_url}/api/health-units", json=payload, timeout=10)
                if response.ok:
                    messagebox.showinfo("Sucesso", "Unidade registada com sucesso.")
                    self.show_units()
                else:
                    messagebox.showerror("Erro", response.json().get("detail", "Erro ao registar unidade."))
            except requests.RequestException:
                messagebox.showerror("Ligação", "Não foi possível comunicar com o servidor.")

        btn = tk.Button(form_frame, text="Guardar unidade", command=create_unit, bg="#2e8b57", fg="#ffffff")
        btn.pack(anchor="w", padx=16, pady=(10, 16))

        list_frame = tk.Frame(self.content, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tk.Label(list_frame, text="Unidades registadas", bg="#ffffff", font=("Segoe UI", 14, "bold"), fg="#0f2d3d").pack(anchor="w", padx=16, pady=(16, 10))

        try:
            response = requests.get(f"{self.server_url}/api/health-units", timeout=10)
            rows = response.json() if response.ok else []
        except requests.RequestException:
            rows = []

        tree = ttk.Treeview(list_frame, columns=("Nome", "Tipo", "Município", "Contacto"), show="headings", height=12)
        for col in ("Nome", "Tipo", "Município", "Contacto"):
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="w")
        for row in rows:
            tree.insert("", "end", values=(row.get("name", "-"), row.get("unit_type", "-"), row.get("municipality", "-"), row.get("contact", "-")))
        tree.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def show_consultas(self):
        self.clear_content()
        panel = tk.Frame(self.content, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(panel, text="Registo de Consultas", bg="#ffffff", font=("Segoe UI", 18, "bold"), fg="#0f2d3d").pack(anchor="w", padx=18, pady=(18, 10))

        try:
            response = requests.get(f"{self.server_url}/api/patients", timeout=10)
            patients = response.json() if response.ok else []
        except requests.RequestException:
            patients = []

        patient_ids = [str(item["id"]) for item in patients]
        patient_names = {str(item["id"]): item["full_name"] for item in patients}

        fields = {
            "patient_id": tk.StringVar(value=patient_ids[0] if patient_ids else ""),
            "professional_name": tk.StringVar(),
            "health_unit_id": tk.StringVar(value="1"),
            "consultation_datetime": tk.StringVar(value="2026-11-10T09:00:00"),
            "diagnosis": tk.StringVar(),
            "observations": tk.StringVar(),
        }

        form = tk.Frame(panel, bg="#ffffff")
        form.pack(fill="x", padx=18, pady=(0, 10))

        for label_name, var, width in [
            ("Paciente", fields["patient_id"], 30),
            ("Profissional", fields["professional_name"], 30),
            ("Unidade", fields["health_unit_id"], 20),
            ("Data/Hora", fields["consultation_datetime"], 30),
            ("Diagnóstico", fields["diagnosis"], 40),
            ("Observações", fields["observations"], 40),
        ]:
            row = tk.Frame(form, bg="#ffffff")
            row.pack(fill="x", pady=6)
            tk.Label(row, text=label_name, bg="#ffffff", width=18, anchor="w").pack(side="left")
            if label_name == "Paciente":
                menu = ttk.Combobox(row, textvariable=var, values=[patient_names.get(pid, pid) for pid in patient_ids], width=35)
                menu.pack(side="left")
            else:
                tk.Entry(row, textvariable=var, width=width).pack(side="left")

        def create_consultation():
            selected_value = fields["patient_id"].get().strip()
            patient_id = None
            for item in patients:
                if str(item["id"]) == selected_value or item["full_name"] == selected_value:
                    patient_id = item["id"]
                    break
            if patient_id is None:
                try:
                    patient_id = int(selected_value)
                except ValueError:
                    messagebox.showerror("Validação", "Selecione um paciente válido.")
                    return

            payload = {
                "patient_id": patient_id,
                "professional_name": fields["professional_name"].get().strip(),
                "health_unit_id": int(fields["health_unit_id"].get().strip() or 1),
                "consultation_datetime": fields["consultation_datetime"].get().strip(),
                "diagnosis": fields["diagnosis"].get().strip() or None,
                "observations": fields["observations"].get().strip() or None,
            }
            if not payload["professional_name"]:
                messagebox.showerror("Validação", "O nome do profissional é obrigatório.")
                return
            try:
                response = requests.post(f"{self.server_url}/api/consultations", json=payload, timeout=10)
                if response.ok:
                    messagebox.showinfo("Sucesso", "Consulta registada com sucesso.")
                    self.show_consultas()
                else:
                    messagebox.showerror("Erro", response.json().get("detail", "Erro ao registar consulta."))
            except requests.RequestException:
                messagebox.showerror("Ligação", "Não foi possível comunicar com o servidor.")

        tk.Button(panel, text="Guardar consulta", command=create_consultation, bg="#6a4c93", fg="#ffffff").pack(anchor="w", padx=18, pady=(0, 12))

        list_panel = tk.Frame(panel, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        list_panel.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        tk.Label(list_panel, text="Consultas recentes", bg="#ffffff", font=("Segoe UI", 13, "bold"), fg="#0f2d3d").pack(anchor="w", padx=16, pady=(16, 10))

        try:
            response = requests.get(f"{self.server_url}/api/consultations", timeout=10)
            rows = response.json() if response.ok else []
        except requests.RequestException:
            rows = []

        tree = ttk.Treeview(list_panel, columns=("Paciente", "Profissional", "Diagnóstico", "Data"), show="headings", height=10)
        for col in ("Paciente", "Profissional", "Diagnóstico", "Data"):
            tree.heading(col, text=col)
            tree.column(col, width=180, anchor="w")
        for row in rows[:12]:
            patient_name = row.get("patient_name") or "Paciente"
            tree.insert("", "end", values=(patient_name, row.get("professional_name", "-"), row.get("diagnosis", "-"), str(row.get("consultation_datetime", "-")).split("T")[0]))
        tree.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def show_history(self):
        self.clear_content()
        panel = tk.Frame(self.content, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(panel, text="Histórico Clínico", bg="#ffffff", font=("Segoe UI", 18, "bold"), fg="#0f2d3d").pack(anchor="w", padx=18, pady=(18, 10))

        search_frame = tk.Frame(panel, bg="#ffffff")
        search_frame.pack(fill="x", padx=18, pady=(0, 12))
        tk.Label(search_frame, text="Pesquisar paciente", bg="#ffffff", width=18, anchor="w").pack(side="left")
        query = tk.StringVar()
        tk.Entry(search_frame, textvariable=query, width=40).pack(side="left")

        def load_history():
            value = query.get().strip()
            if not value:
                messagebox.showinfo("Informação", "Introduza um nome para pesquisar um paciente.")
                return
            try:
                response = requests.get(f"{self.server_url}/api/patients", params={"query": value}, timeout=10)
                patients = response.json() if response.ok else []
                if not patients:
                    messagebox.showinfo("Resultado", "Nenhum paciente encontrado.")
                    return
                patient = patients[0]
                history_response = requests.get(f"{self.server_url}/api/patients/{patient['id']}/history", timeout=10)
                if not history_response.ok:
                    messagebox.showerror("Erro", "Não foi possível obter o histórico.")
                    return
                data = history_response.json()
                history_panel = tk.Frame(panel, bg="#ffffff")
                history_panel.pack(fill="both", expand=True, padx=18, pady=(0, 18))

                for widget in history_panel.winfo_children():
                    widget.destroy()

                tk.Label(history_panel, text=f"Paciente: {data['patient']['full_name']}", bg="#ffffff", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 4))
                tk.Label(history_panel, text=f"NIF: {data['patient'].get('nif', '-')}", bg="#ffffff").pack(anchor="w", padx=10)
                tk.Label(history_panel, text=f"Contacto: {data['patient'].get('contact', '-')}", bg="#ffffff").pack(anchor="w", padx=10)

                tree = ttk.Treeview(history_panel, columns=("Data", "Profissional", "Diagnóstico", "Observações"), show="headings", height=8)
                for col in ("Data", "Profissional", "Diagnóstico", "Observações"):
                    tree.heading(col, text=col)
                    tree.column(col, width=180, anchor="w")
                for item in data.get("consultations", []):
                    tree.insert("", "end", values=(str(item.get("consultation_datetime", "-")).split("T")[0], item.get("professional_name", "-"), item.get("diagnosis", "-"), item.get("observations", "-")))
                tree.pack(fill="both", expand=True, padx=10, pady=(10, 10))
            except requests.RequestException:
                messagebox.showerror("Ligação", "Não foi possível comunicar com o servidor.")

        tk.Button(search_frame, text="Consultar histórico", command=load_history, bg="#1f78b4", fg="#ffffff").pack(side="left", padx=(8, 0))

    def show_data_sharing(self):
        self.clear_content()
        panel = tk.Frame(self.content, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(panel, text="Partilha de Dados", bg="#ffffff", font=("Segoe UI", 18, "bold"), fg="#0f2d3d").pack(anchor="w", padx=18, pady=(18, 10))

        try:
            units_response = requests.get(f"{self.server_url}/api/health-units", timeout=10)
            patients_response = requests.get(f"{self.server_url}/api/patients", timeout=10)
            units = units_response.json() if units_response.ok else []
            patients = patients_response.json() if patients_response.ok else []
        except requests.RequestException:
            units, patients = [], []

        form = tk.Frame(panel, bg="#ffffff")
        form.pack(fill="x", padx=18, pady=(0, 12))

        fields = {
            "source": tk.StringVar(value=units[0].get("name", "") if units else ""),
            "target": tk.StringVar(value=units[1].get("name", "") if len(units) > 1 else units[0].get("name", "") if units else ""),
            "patient": tk.StringVar(value=patients[0].get("full_name", "") if patients else ""),
            "permission": tk.StringVar(value="leitura"),
        }

        for label_name, var, values in [
            ("Origem", fields["source"], [unit.get("name", "") for unit in units]),
            ("Destino", fields["target"], [unit.get("name", "") for unit in units]),
            ("Paciente", fields["patient"], [patient.get("full_name", "") for patient in patients]),
            ("Permissão", fields["permission"], ["leitura", "escrita", "consulta"]),
        ]:
            row = tk.Frame(form, bg="#ffffff")
            row.pack(fill="x", pady=6)
            tk.Label(row, text=label_name, bg="#ffffff", width=16, anchor="w").pack(side="left")
            combo = ttk.Combobox(row, textvariable=var, values=values, width=42, state="readonly")
            combo.pack(side="left")

        def save_share():
            payload = {
                "source": fields["source"].get(),
                "target": fields["target"].get(),
                "patient": fields["patient"].get(),
                "permission": fields["permission"].get(),
            }
            if not payload["source"] or not payload["target"] or not payload["patient"]:
                messagebox.showerror("Validação", "Preencha todos os campos da partilha.")
                return
            self.data_shares.append(payload)
            messagebox.showinfo("Sucesso", "Partilha registada com sucesso.")
            self.show_data_sharing()

        tk.Button(panel, text="Guardar partilha", command=save_share, bg="#2e8b57", fg="#ffffff").pack(anchor="w", padx=18, pady=(0, 12))

        list_panel = tk.Frame(panel, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        list_panel.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        tk.Label(list_panel, text="Histórico de partilhas", bg="#ffffff", font=("Segoe UI", 13, "bold"), fg="#0f2d3d").pack(anchor="w", padx=16, pady=(16, 10))

        tree = ttk.Treeview(list_panel, columns=("Origem", "Destino", "Paciente", "Permissão"), show="headings", height=8)
        for col in ("Origem", "Destino", "Paciente", "Permissão"):
            tree.heading(col, text=col)
            tree.column(col, width=180, anchor="w")
        for item in self.data_shares:
            tree.insert("", "end", values=(item["source"], item["target"], item["patient"], item["permission"]))
        tree.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def show_users(self):
        self.clear_content()
        panel = tk.Frame(self.content, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(panel, text="Gestão de Utilizadores", bg="#ffffff", font=("Segoe UI", 18, "bold"), fg="#0f2d3d").pack(anchor="w", padx=18, pady=(18, 10))

        form = tk.Frame(panel, bg="#ffffff")
        form.pack(fill="x", padx=18, pady=(0, 12))

        fields = {
            "full_name": tk.StringVar(),
            "username": tk.StringVar(),
            "password": tk.StringVar(),
            "profile": tk.StringVar(value="Operador"),
        }

        for label_name, var in [
            ("Nome completo", fields["full_name"]),
            ("Utilizador", fields["username"]),
            ("Password", fields["password"]),
            ("Perfil", fields["profile"]),
        ]:
            row = tk.Frame(form, bg="#ffffff")
            row.pack(fill="x", pady=6)
            tk.Label(row, text=label_name, bg="#ffffff", width=18, anchor="w").pack(side="left")
            tk.Entry(row, textvariable=var, width=36).pack(side="left")

        def create_user():
            payload = {
                "full_name": fields["full_name"].get().strip(),
                "username": fields["username"].get().strip(),
                "password": fields["password"].get().strip(),
                "profile": fields["profile"].get().strip(),
            }
            if not payload["full_name"] or not payload["username"] or not payload["password"]:
                messagebox.showerror("Validação", "Preencha nome, nome de utilizador e password.")
                return
            try:
                response = requests.post(f"{self.server_url}/api/users", json=payload, timeout=10)
                if response.ok:
                    messagebox.showinfo("Sucesso", "Utilizador criado com sucesso.")
                    self.show_users()
                else:
                    messagebox.showerror("Erro", response.json().get("detail", "Erro ao criar utilizador."))
            except requests.RequestException:
                messagebox.showerror("Ligação", "Não foi possível comunicar com o servidor.")

        tk.Button(panel, text="Adicionar utilizador", command=create_user, bg="#0a3d62", fg="#ffffff").pack(anchor="w", padx=18, pady=(0, 12))

        try:
            response = requests.get(f"{self.server_url}/api/users", timeout=10)
            rows = response.json() if response.ok else []
        except requests.RequestException:
            rows = []

        list_panel = tk.Frame(panel, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        list_panel.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        tk.Label(list_panel, text="Utilizadores registados", bg="#ffffff", font=("Segoe UI", 13, "bold"), fg="#0f2d3d").pack(anchor="w", padx=16, pady=(16, 10))

        tree = ttk.Treeview(list_panel, columns=("Utilizador", "Nome", "Perfil", "Estado"), show="headings", height=10)
        for col in ("Utilizador", "Nome", "Perfil", "Estado"):
            tree.heading(col, text=col)
            tree.column(col, width=180, anchor="w")
        for row in rows:
            tree.insert("", "end", values=(row.get("username", "-"), row.get("full_name", "-"), row.get("profile", "-"), row.get("status", "-")))
        tree.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def show_reports(self):
        self.clear_content()
        panel = tk.Frame(self.content, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(panel, text="Relatórios", bg="#ffffff", font=("Segoe UI", 18, "bold"), fg="#0f2d3d").pack(anchor="w", padx=18, pady=(18, 10))

        try:
            response = requests.get(f"{self.server_url}/api/dashboard", timeout=10)
            stats = response.json() if response.ok else {"pacientes": 0, "unidades": 0, "consultas": 0, "utilizadores": 0}
        except requests.RequestException:
            stats = {"pacientes": 0, "unidades": 0, "consultas": 0, "utilizadores": 0}

        cards = tk.Frame(panel, bg="#ffffff")
        cards.pack(fill="x", padx=18, pady=(0, 12))
        for label, value, color in [
            ("Pacientes", stats.get("pacientes", 0), "#1f78b4"),
            ("Unidades", stats.get("unidades", 0), "#2e8b57"),
            ("Consultas", stats.get("consultas", 0), "#6a4c93"),
            ("Utilizadores", stats.get("utilizadores", 0), "#e76f51"),
        ]:
            card = tk.Frame(cards, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
            card.pack(side="left", fill="both", expand=True, padx=6)
            tk.Label(card, text=label, bg="#ffffff", fg="#666666", font=("Segoe UI", 10)).pack(anchor="w", padx=12, pady=(12, 0))
            tk.Label(card, text=str(value), bg="#ffffff", fg=color, font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=12, pady=(4, 12))

        list_panel = tk.Frame(panel, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        list_panel.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        tk.Label(list_panel, text="Resumo executivo", bg="#ffffff", font=("Segoe UI", 13, "bold"), fg="#0f2d3d").pack(anchor="w", padx=16, pady=(16, 10))

        summary = [
            ("Total de pacientes", stats.get("pacientes", 0)),
            ("Total de unidades", stats.get("unidades", 0)),
            ("Total de consultas", stats.get("consultas", 0)),
            ("Total de utilizadores", stats.get("utilizadores", 0)),
        ]
        for label, value in summary:
            row = tk.Frame(list_panel, bg="#ffffff")
            row.pack(fill="x", padx=16, pady=4)
            tk.Label(row, text=label, bg="#ffffff", width=22, anchor="w").pack(side="left")
            tk.Label(row, text=str(value), bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#0f2d3d").pack(side="left")

    def show_settings(self):
        self.clear_content()
        panel = tk.Frame(self.content, bg="#ffffff", highlightbackground="#dfe3e8", highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(panel, text="Configurações", bg="#ffffff", font=("Segoe UI", 18, "bold"), fg="#0f2d3d").pack(anchor="w", padx=18, pady=(18, 10))

        options = {
            "Ativar notificações": tk.BooleanVar(value=True),
            "Sincronização automática": tk.BooleanVar(value=True),
            "Modo de manutenção": tk.BooleanVar(value=False),
            "Registo de auditoria": tk.BooleanVar(value=True),
        }

        for label, var in options.items():
            row = tk.Frame(panel, bg="#ffffff")
            row.pack(fill="x", padx=18, pady=8)
            tk.Checkbutton(row, text=label, variable=var, bg="#ffffff", anchor="w").pack(anchor="w")

        def save_settings():
            selected = {key: value.get() for key, value in options.items()}
            messagebox.showinfo("Configurações", f"Configurações guardadas com sucesso.\n{selected}")

        tk.Button(panel, text="Guardar configurações", command=save_settings, bg="#0a3d62", fg="#ffffff").pack(anchor="w", padx=18, pady=(12, 18))

    def logout(self):
        messagebox.showinfo("Sessão", "Sessão terminada.")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    DashboardWindow(root, "admin", "Administrador", "http://127.0.0.1:8000")
    root.mainloop()
