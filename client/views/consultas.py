from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class ConsultaPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(padding=16)
        ttk.Label(self, text="Consultas", font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(self, text="Registo de consultas, diagnósticos e observações clínicas.").pack(anchor="w", pady=(8, 16))
