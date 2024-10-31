#-*- coding:utf-8 -*-

import tkinter as tk
from tkinter import messagebox, filedialog
import pyautogui
import requests
import os
from PIL import Image, ImageTk
from utils import update_surrender_count, find_and_click
import threading
import time

class ClickAutomationApp:
    """点击自动化应用程序的主类。"""

    def __init__(self, master):
        """初始化应用程序。

        Args:
            master: 主窗口对象。
        """
        self.master = master
        self.master.title("Click Automation")
        self.surrender_count = tk.IntVar(value=0)
        self.is_running = False
        self.current_image = None
        self.images_directory = None
        self.can_throw_image = None
        self.setup_ui()

    def setup_ui(self):
        """设置用户界面。"""
        tk.Label(self.master, text="当前投降次数:").pack()
        self.surrender_count_label = tk.Label(self.master, textvariable=self.surrender_count)
        self.surrender_count_label.pack()
        tk.Label(self.master, text="设置关闭次数:").pack()
        self.close_threshold = tk.IntVar(value=5)
        tk.Entry(self.master, textvariable=self.close_threshold, width=5).pack()
        self.image_label = tk.Label(self.master)
        self.image_label.pack()
        tk.Button(self.master, text="选择图片目录", command=self.select_images_directory).pack()
        tk.Button(self.master, text="选择投降条件图片", command=self.select_can_throw_image).pack()
        tk.Button(self.master, text="获取说明", command=self.fetch_instructions).pack()
        self.start_button = tk.Button(self.master, text="开始点击", command=self.toggle_clicking)
        self.start_button.pack()
        tk.Button(self.master, text="退出", command=self.master.quit).pack()

    def select_images_directory(self):
        """选择要加载的图片目录。"""
        self.images_directory = filedialog.askdirectory()
        if self.images_directory:
            messagebox.showinfo("信息", f"选择的图片目录: {self.images_directory}")

    def fetch_instructions(self):
        """从指定 URL 获取说明并显示。"""
        url = "https://dhwass.pages.dev/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            instructions = response.text
            messagebox.showinfo("说明", instructions)
        except requests.RequestException as e:
            messagebox.showerror("错误", f"无法获取说明: {e}")

    def select_can_throw_image(self):
        """选择用于投降的条件图片。"""
        self.can_throw_image = filedialog.askopenfilename(title="选择投降条件图片",
                                                          filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        self.can_throw_image = os.path.normpath(self.can_throw_image)
        if self.can_throw_image:
            messagebox.showinfo("信息", f"选择的投降条件图片: {self.can_throw_image}")

    def toggle_clicking(self):
        """切换点击状态，开始或停止点击。"""
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="开始点击")
        else:
            if not self.images_directory or not self.can_throw_image:
                messagebox.showwarning("警告", "请确保选择图片目录和投降条件图片。")
                return
            self.is_running = True
            self.start_button.config(text="停止点击")
            self.start_clicking_thread()

    def start_clicking_thread(self):
        """启动一个线程以执行点击操作。"""
        threading.Thread(target=self.start_clicking).start()

    def start_clicking(self):
        """执行点击操作的主逻辑。"""
        images = [os.path.normpath(os.path.join(self.images_directory, filename))
                  for filename in os.listdir(self.images_directory)
                  if filename.lower().endswith(('.png', '.jpg', '.jpeg'))]

        count_threshold = self.close_threshold.get()
        while self.is_running:
            for image in images:
                self.current_image = image
                self.update_image_display()
                found = find_and_click(image)
                if found and image == self.can_throw_image:
                    pyautogui.press('esc')
                    self.surrender_count.set(self.surrender_count.get() + 1)
                if self.surrender_count.get() >= count_threshold:
                    messagebox.showinfo("提示", "已达到关闭次数，程序将停止。")
                    self.is_running = False
                    self.start_button.config(text="开始点击")
                    break
                time.sleep(0.5)

    def update_image_display(self):
        """更新当前显示的图片。"""
        if self.current_image:
            img = Image.open(self.current_image)
            img = img.resize((200, 200), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo
