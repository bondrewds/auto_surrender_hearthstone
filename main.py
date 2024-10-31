#-*- coding:utf-8 -*-

import tkinter as tk
from app import ClickAutomationApp

def run_gui():
    """启动 GUI 应用程序。"""
    root = tk.Tk()
    app = ClickAutomationApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()


