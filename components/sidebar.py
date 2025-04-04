import customtkinter as ctk
from PIL import Image, UnidentifiedImageError

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=250, corner_radius=0)
        self.parent = parent
        self._setup_layout()
        self._create_widgets()
    
    def _setup_layout(self):
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_propagate(False)
    
    def _create_widgets(self):
        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open("logo.png"),
                dark_image=Image.open("logo.png"),
                size=(110, 110)
            )
            logo = ctk.CTkLabel(self, image=logo_img, text="")
        except (FileNotFoundError, UnidentifiedImageError):
            logo = ctk.CTkLabel(
                self, 
                text="Star - EXE", 
                font=("Arial", 24),
                text_color=("#333333", "#FFFFFF")
            )
        logo.pack(pady=(30, 20), anchor="center")

        nav_buttons = [
            ("Home", "home"),
            ("Sparx", "sparx"),
            ("Other", "other"),
            ("Settings", "settings"),
            ("Exit", "exit")
        ]
        
        for text, panel in nav_buttons:
            btn = ctk.CTkButton(
                self,
                text=text,
                command=lambda p=panel: self._navigate(p),
                height=40,
                anchor="w",
                fg_color="transparent",
                hover_color=("#EEEEEE", "#2A2A2A"),
                font=("Arial", 14)
            )
            btn.pack(fill="x", padx=10, pady=2)
        
        # Contributors section
        self._create_contributors()
    
    def _create_contributors(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(side="bottom", fill="x", pady=20)
        
        ctk.CTkLabel(
            frame,
            text="CONTRIBUTORS",
            font=("Arial", 10, "bold"),
            text_color=("#666666", "#AAAAAA")
        ).pack(anchor="w", padx=10)
        
        contributors = [
            ("Giro", "Developer"),
            ("Star", "Developer"),
            ("Nikoo", "Owner"),
            ("TNAR", "Co-Owner")
        ]
        
        for name, role in contributors:
            ctk.CTkLabel(
                frame,
                text=f"• {name} ({role})",
                font=("Arial", 10)
            ).pack(anchor="w", padx=20, pady=1)
    
    def _navigate(self, panel):
        if panel == "exit":
            self.parent.quit()
        else:
            self.parent.show_panel(panel)