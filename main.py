import tkinter as tk
from tkinter import ttk, scrolledtext
# Still importing core classes from the previously written modules
from sensor_node import AirQualitySensor, TrafficCamera, AbstractSensor
from network_manager import NetworkManager

class SmartCityGUI:
    def __init__(self, root):
        """Initialize GUI window and backend system"""
        self.root = root
        self.root.title("Smart City IoT Resource Manager")
        self.root.geometry("650x550")
        
        # 1. Backend Setup
        self.city_net = NetworkManager("Kowloon-HK Island Core")
        self.setup_backend()
        
        # 2. Frontend UI
        self.create_widgets()

    def setup_backend(self):
        """Backend logic: Instantiate sensors and build network topology"""
        self.sensor1 = AirQualitySensor("AQ-Central-01", "Central", "NO2")
        self.sensor2 = TrafficCamera("CAM-MongKok-01", "Mong Kok", "4K")
        
        self.city_net.register_device(self.sensor1)
        self.city_net.register_device(self.sensor2)

        # Build graph data structure connections (simulate city network)
        self.city_net.add_connection("AQ-Central-01", "Router-Admiralty", 2)
        self.city_net.add_connection("Router-Admiralty", "Router-TST", 5)
        self.city_net.add_connection("Router-TST", "CAM-MongKok-01", 3)
        self.city_net.add_connection("Router-Admiralty", "Server-HQ", 10)
        self.city_net.add_connection("Router-TST", "Server-HQ", 1)

    def create_widgets(self):
        """Build various UI components"""
        # --- Title ---
        title_label = tk.Label(self.root, text="Smart City IoT Dashboard", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # --- Section 1: Sensor Status Panel ---
        sensor_frame = tk.LabelFrame(self.root, text="Edge Devices (Sensors) Status", font=("Helvetica", 10, "bold"))
        sensor_frame.pack(fill="x", padx=15, pady=5)

        self.btn_status = tk.Button(sensor_frame, text="Initialize & Load Sensors", command=self.show_status, bg="#E1F5FE")
        self.btn_status.pack(pady=5)

        self.status_text = scrolledtext.ScrolledText(sensor_frame, height=6, width=70)
        self.status_text.pack(padx=10, pady=5)

        # --- Section 2: Network Routing Panel (Dijkstra) ---
        route_frame = tk.LabelFrame(self.root, text="Network Routing (Dijkstra's Algorithm)", font=("Helvetica", 10, "bold"))
        route_frame.pack(fill="x", padx=15, pady=15)

        # Dropdown menu control area
        control_frame = tk.Frame(route_frame)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Start Node:").grid(row=0, column=0, padx=5)
        nodes = ["AQ-Central-01", "CAM-MongKok-01", "Router-Admiralty", "Router-TST", "Server-HQ"]
        self.start_combo = ttk.Combobox(control_frame, values=nodes, state="readonly", width=18)
        self.start_combo.current(0) # Select the first one by default
        self.start_combo.grid(row=0, column=1, padx=5)

        tk.Label(control_frame, text="Target Node:").grid(row=0, column=2, padx=5)
        self.target_combo = ttk.Combobox(control_frame, values=nodes, state="readonly", width=18)
        self.target_combo.current(4) # Select the last one (Server-HQ) by default
        self.target_combo.grid(row=0, column=3, padx=5)

        self.btn_route = tk.Button(route_frame, text="Calculate Optimal Route", command=self.calculate_route, bg="#E8F5E9")
        self.btn_route.pack(pady=5)

        self.route_text = scrolledtext.ScrolledText(route_frame, height=5, width=70)
        self.route_text.pack(padx=10, pady=5)

    def show_status(self):
        """Button click event: Show sensor information"""
        self.status_text.delete(1.0, tk.END) # Clear the text box
        # Call the magic method __str__ and class method
        self.status_text.insert(tk.END, f"[Device Loaded] {self.sensor1}\n")
        self.status_text.insert(tk.END, f"[Device Loaded] {self.sensor2}\n")
        self.status_text.insert(tk.END, "-"*40 + "\n")
        self.status_text.insert(tk.END, f"[System] {AbstractSensor.get_network_status()}\n")

    def calculate_route(self):
        """Button click event: Execute Dijkstra's algorithm"""
        self.route_text.delete(1.0, tk.END)
        start = self.start_combo.get()
        target = self.target_combo.get()

        # Call the algorithm we wrote in network_manager
        path, latency = self.city_net.find_optimal_route(start, target)
        
        if path:
            self.route_text.insert(tk.END, "✅ Path Found!\n")
            self.route_text.insert(tk.END, f"Optimal Route: {' ➔ '.join(path)}\n")
            self.route_text.insert(tk.END, f"Total Network Latency: {latency} ms\n")
        else:
            self.route_text.insert(tk.END, "❌ Error: No valid route found between these nodes.\n")

# Top-level execution environment
if __name__ == "__main__":
    # Initialize Tkinter main window
    root = tk.Tk()
    # Instantiate our GUI application class
    app = SmartCityGUI(root)
    # Start the UI event loop
    root.mainloop()
