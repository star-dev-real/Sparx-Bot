import customtkinter as ctk
from PIL import Image
import webbrowser
import aiohttp
import asyncio
import random
import time
import threading

class SparxPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._create_widgets()

    def _create_widgets(self):
        ctk.CTkLabel(
            self,
            text="This has not been released yet...\nJoin the Discord for updates!",
            font=("Arial", 50),
            fg_color="transparent"
        ).pack(pady=20)
