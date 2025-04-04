import customtkinter as ctk
from components.sidebar import Sidebar
from components.panels.home import HomePanel
from components.panels.settings import SettingsPanel
from components.panels.sparx import SparxPanel
from components.panels.other import OtherPanel

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Star - EXE")
        self.geometry("1000x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.sidebar = Sidebar(self)
        self.current_panel = None
        self.show_panel("home")
    
    def show_panel(self, panel_name):
        if self.current_panel:
            self.current_panel.grid_forget()
        
        if panel_name == "home":
            self.current_panel = HomePanel(self)
        elif panel_name == "settings":
            self.current_panel = SettingsPanel(self)
        elif panel_name == "sparx":
            self.current_panel = SparxPanel(self)
        elif panel_name == "other":
            self.current_panel == OtherPanel(self)
            
        self.current_panel.grid(row=0, column=1, sticky="nsew")