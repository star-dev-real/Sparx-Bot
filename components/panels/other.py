import customtkinter as ctk
from PIL import Image

class OtherPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self._create_widgets()
    
    def _create_widgets(self):
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.header = ctk.CTkLabel(
            self,
            text="Other",
            font=("Arial", 28, "bold"),
            text_color=("#2B65EC", "#4FC3F7")
        )
        self.header.grid(row=0, column=0, pady=(30, 20), sticky="n")
        
        # Settings frame
        self.other_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.other_frame.grid(row=1, column=0, sticky="nsew", padx=100)