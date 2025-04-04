import customtkinter as ctk
from PIL import Image
import webbrowser

class HomePanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self._create_widgets()
    
    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.header = ctk.CTkLabel(
            self,
            text="🌟 Welcome to Star - EXE 🌟",
            font=("Arial", 28, "bold"),
            text_color=("#2B65EC", "#4FC3F7")
        )
        self.header.grid(row=0, column=0, pady=(30, 10), sticky="n")

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=50)
        
  
        try:
            self.logo_img = ctk.CTkImage(
                light_image=Image.open("logo.png"),
                dark_image=Image.open("logo.png"),
                size=(200, 200)
            )
            self.logo = ctk.CTkLabel(self.content_frame, image=self.logo_img, text="")
        except:
            self.logo = ctk.CTkLabel(
                self.content_frame,
                text="★ Star - EXE ★",
                font=("Arial", 24),
                text_color=("#2B65EC", "#4FC3F7")
            )
        self.logo.grid(row=0, column=0, pady=(0, 30))
        

        self.welcome_text = ctk.CTkLabel(
            self.content_frame,
            text="""✨ Welcome to our application! ✨\n
This tool is completely free and safe to use.\n
Created by @star_dev & @giro0147 - please credit if you use this.\n
⚠️ Remember: We're not responsible for any trouble you might get into!""",
            font=("Arial", 14),
            wraplength=600,
            justify="center"
        )
        self.welcome_text.grid(row=1, column=0, pady=(0, 40))
        

        self.button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.button_frame.grid(row=2, column=0)
        
        buttons = [
            ("💬 Join Discord", "https://discord.gg/8WCm3ySS", "#5865F2"),
            ("🐱 GitHub", "https://github.com/star-dev-real", "#333333"),
            ("💸 Donate", "https://paypal.me/starfnofficial@gmail.com", "#009DEA"),
            ("⚠️ Report Issue", "https://discord.gg/sUrw9Svzb6", "#FF4500")
        ]
        
        for i, (text, url, color) in enumerate(buttons):
            btn = ctk.CTkButton(
                self.button_frame,
                text=text,
                command=lambda u=url: webbrowser.open(u),
                width=140,
                height=40,
                fg_color=color,
                hover_color=color,
                corner_radius=8,
                font=("Arial", 14)
            )
            btn.grid(row=0, column=i, padx=10, pady=10)