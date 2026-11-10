from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class UnidadePanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(padding=16)
        ttk.Label(self, text="Unidades de Saúde", font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(self, text="Módulo funcional para hospitais, centros de saúde e postos de saúde.").pack(anchor="w", pady=(8, 16))
