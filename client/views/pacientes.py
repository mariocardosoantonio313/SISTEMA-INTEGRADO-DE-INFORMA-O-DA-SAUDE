from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class PacientePanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(padding=16)
        ttk.Label(self, text="Gestão de Pacientes", font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(self, text="Módulo funcional em desenvolvimento para registo, pesquisa e histórico clínico.").pack(anchor="w", pady=(8, 16))
