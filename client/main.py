from __future__ import annotations

import tkinter as tk

from client.views.login import LoginWindow


def main():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
