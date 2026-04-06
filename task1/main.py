"""
Module: main.py
Description: The main entry point for the HKMU Smart Campus IoT Hub application.
             Initializes the Tkinter root window and launches the GUI.
"""
import tkinter as tk
from gui_app import CampusDashboardGUI

def main():
    """Initializes and runs the main application event loop."""
    root = tk.Tk()
    app = CampusDashboardGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()