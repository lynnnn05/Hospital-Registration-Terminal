# main.py
import tkinter as tk
from tkinter import ttk
from ui import HospitalAppUI

if __name__ == '__main__':
    # Initialize the top-level application root
    root = tk.Tk()
    root.title("🏥 Smart Hospital - Department Queue Scheduling System")
    root.geometry("1200x800")
    
    # Apply a modern system theme if available
    style = ttk.Style()
    if "clam" in style.theme_names(): 
        style.theme_use("clam")
        
    # Launch the User Interface
    app = HospitalAppUI(root)
    
    # Start the event loop
    root.mainloop()