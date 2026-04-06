"""
Module: gui_app.py
Description: Modern Dark-Mode GUI handling user interactions and queue visualization.
             Ensures separation of concerns by keeping UI logic distinct from business logic.
"""
import tkinter as tk
from tkinter import messagebox, simpledialog
from devices import SmartAC, LabOscilloscope
from hub_controller import CampusIoTHub

# --- UI Color Palette ---
BG_MAIN = "#121212"
BG_CARD = "#1E1E1E"
FG_TEXT = "#FFFFFF"
ACCENT_BLUE = "#007ACC"
COLOR_ON = "#2EA043"
COLOR_OFF = "#F85149"
QUEUE_BG = "#252526"

class CampusDashboardGUI:
    """Class responsible for rendering the Tkinter GUI and binding events."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("HKMU Smart Campus - Edge IoT Dashboard")
        self.root.geometry("850x550")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        self.hub = CampusIoTHub("HKMU EECS Zone")
        self._init_devices()

        self._build_header()
        self._build_main_layout()
        self.update_ui()

    def _init_devices(self):
        """Pre-loads the hub with sample Edge devices."""
        ac1 = SmartAC("AC-A0411", "Block A 0411")
        ac2 = SmartAC("AC-E0712", "Block E Lab", base_power=2500)
        osc1 = LabOscilloscope("OSC-01", "Block E Lab")
        self.hub.register_device(ac1)
        self.hub.register_device(ac2)
        self.hub.register_device(osc1)

    def _build_header(self):
        """Constructs the top information panel."""
        self.header_frame = tk.Frame(self.root, bg=BG_CARD, pady=15)
        self.header_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(self.header_frame, text="⚡ IoT Edge Energy Controller", font=("Segoe UI", 18, "bold"), bg=BG_CARD, fg=ACCENT_BLUE).pack()
        
        self.lbl_power = tk.Label(self.header_frame, text="Real-time Draw: 0.00 W", font=("Segoe UI", 14), bg=BG_CARD, fg=FG_TEXT)
        self.lbl_power.pack(pady=(5, 0))

    def _build_main_layout(self):
        """Constructs the split-pane layout for devices (left) and task queue (right)."""
        main_pane = tk.Frame(self.root, bg=BG_MAIN)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=15)

        # Left Pane: Device List
        self.left_frame = tk.Frame(main_pane, bg=BG_MAIN)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.device_widgets = {}
        for device in self.hub.get_all_devices():
            card = tk.Frame(self.left_frame, bg=BG_CARD, pady=15, padx=15)
            card.pack(fill=tk.X, pady=8)
            
            name_lbl = tk.Label(card, text=f"{device.get_id()}", font=("Segoe UI", 12, "bold"), bg=BG_CARD, fg=FG_TEXT)
            name_lbl.pack(side=tk.LEFT)
            
            status_lbl = tk.Label(card, text="OFF", font=("Consolas", 12, "bold"), bg=BG_CARD, fg=COLOR_OFF, width=12)
            status_lbl.pack(side=tk.LEFT, padx=10)
            
            btn_toggle = tk.Button(card, text="+ Queue Pwr", font=("Segoe UI", 9, "bold"), bg="#444444", fg=FG_TEXT, relief="flat", cursor="hand2",
                                   command=lambda d=device: self.queue_power_toggle(d))
            btn_toggle.pack(side=tk.RIGHT, padx=5)

            btn_setting = tk.Button(card, text="+ Queue Set", font=("Segoe UI", 9), bg="#333333", fg=FG_TEXT, relief="flat", cursor="hand2",
                                    command=lambda d=device: self.queue_setting(d))
            btn_setting.pack(side=tk.RIGHT)

            self.device_widgets[device.get_id()] = {"status_lbl": status_lbl, "btn_toggle": btn_toggle}

        btn_eco = tk.Button(self.left_frame, text="🍃 Instant Eco-Mode", font=("Segoe UI", 12, "bold"), bg=COLOR_ON, fg="#000000", relief="flat", cursor="hand2", pady=5, command=self.trigger_eco)
        btn_eco.pack(fill=tk.X, pady=15)

        # Right Pane: Task Queue
        self.right_frame = tk.Frame(main_pane, bg=QUEUE_BG, padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(self.right_frame, text="Task Queue (FIFO)", font=("Segoe UI", 12, "bold"), bg=QUEUE_BG, fg=ACCENT_BLUE).pack(pady=(0, 10))
        
        self.queue_listbox = tk.Listbox(self.right_frame, bg="#000000", fg="#00FF00", font=("Consolas", 10), width=35, height=15, borderwidth=0, highlightthickness=0)
        self.queue_listbox.pack(fill=tk.BOTH, expand=True)

        btn_execute = tk.Button(self.right_frame, text="▶ Execute All (FIFO)", font=("Segoe UI", 11, "bold"), bg="#005A9E", fg=FG_TEXT, relief="flat", cursor="hand2", pady=8, command=self.execute_queue)
        btn_execute.pack(fill=tk.X, pady=(15, 0))

    def queue_power_toggle(self, device):
        """Encapsulates a power toggle action into the command queue."""
        action = lambda: device.turn_off() if device.get_status() else device.turn_on()
        desc = f"Toggle Power: {device.get_id()}"
        self.hub.command_queue.enqueue(desc, action)
        self.refresh_queue_ui()

    def queue_setting(self, device):
        """Encapsulates a setting change action into the command queue based on device type."""
        if isinstance(device, SmartAC):
            temp = simpledialog.askinteger("AC Control", f"Target temp for {device.get_id()} (18-30):", minvalue=18, maxvalue=30)
            if temp:
                action = lambda: device.set_temperature(temp)
                self.hub.command_queue.enqueue(f"Set Temp: {device.get_id()} to {temp}°C", action)
                self.refresh_queue_ui()
        elif isinstance(device, LabOscilloscope):
            ans = messagebox.askyesno("Oscilloscope Control", "Switch to Active Mode?")
            if ans:
                self.hub.command_queue.enqueue(f"Set Mode: {device.get_id()} to Active", lambda: device.set_active_mode())
            else:
                self.hub.command_queue.enqueue(f"Set Mode: {device.get_id()} to Standby", lambda: device.set_standby_mode())
            self.refresh_queue_ui()

    def refresh_queue_ui(self):
        """Updates the visual listbox to reflect the current state of the queue."""
        self.queue_listbox.delete(0, tk.END)
        for i, desc in enumerate(self.hub.command_queue.get_descriptions()):
            self.queue_listbox.insert(tk.END, f"[{i+1}] {desc}")

    def execute_queue(self):
        """Fires the hub's sequential execution process for all queued commands."""
        if self.hub.command_queue.is_empty():
            messagebox.showinfo("Queue Empty", "No tasks in the queue.")
            return
            
        executed = self.hub.execute_all_queued_commands()
        self.refresh_queue_ui()
        self.update_ui()
        messagebox.showinfo("Execution Complete", f"{executed} tasks executed sequentially.")

    def trigger_eco(self):
        """Triggers the global eco-mode and refreshes UI."""
        self.hub.trigger_eco_mode()
        self.refresh_queue_ui()
        self.update_ui()

    def update_ui(self):
        """Dynamically recalculates power draw and updates device status labels."""
        total_w = self.hub.calculate_total_zone_power()
        self.lbl_power.config(text=f"Real-time Draw: {total_w:.1f} W", fg=COLOR_OFF if total_w > 4000 else FG_TEXT)

        for device in self.hub.get_all_devices():
            widgets = self.device_widgets[device.get_id()]
            if device.get_status():
                status_text = f"ON ({device._target_temp}°C)" if isinstance(device, SmartAC) else f"ON ({device._mode})"
                widgets["status_lbl"].config(text=status_text, fg=COLOR_ON)
            else:
                widgets["status_lbl"].config(text="OFF", fg=COLOR_OFF)