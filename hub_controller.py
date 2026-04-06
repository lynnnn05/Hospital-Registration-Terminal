"""
Module: hub_controller.py
Description: The central IoT Hub with an integrated FIFO Command Queue.
             Demonstrates Aggregation, Polymorphism, and Data Structures (Queue).
"""
from devices import CampusDevice

class CommandQueue:
    """
    A custom First-In-First-Out (FIFO) Queue data structure.
    Used to handle asynchronous IoT commands safely.
    """
    def __init__(self):
        self._queue = [] 

    def enqueue(self, description, action_func):
        """Appends a command to the tail of the queue."""
        self._queue.append((description, action_func))

    def dequeue(self):
        """Removes and returns the command at the head of the queue."""
        if not self.is_empty():
            return self._queue.pop(0)
        return None

    def is_empty(self):
        """Checks if the queue contains no pending commands."""
        return len(self._queue) == 0
        
    def clear_queue(self):
        """Empties all pending commands from the queue."""
        self._queue.clear()

    def get_descriptions(self):
        """Returns a list of descriptions for all queued commands."""
        return [desc for desc, func in self._queue]


class CampusIoTHub:
    """
    Central controller class managing a collection of CampusDevice objects.
    Demonstrates Aggregation.
    """
    def __init__(self, zone_name):
        self._zone_name = zone_name
        self._device_registry = {} 
        self.command_queue = CommandQueue() 

    def register_device(self, device):
        """Registers a new CampusDevice into the hub's registry."""
        if isinstance(device, CampusDevice) and device.get_id() not in self._device_registry:
            self._device_registry[device.get_id()] = device
            return True
        return False

    def get_all_devices(self):
        """Returns a list of all managed devices."""
        return list(self._device_registry.values())

    def calculate_total_zone_power(self):
        """
        Polymorphic calculation: Iterates through all devices to sum real-time power.
        """
        total_power = 0.0
        for device in self._device_registry.values():
            total_power += device.get_power_consumption()
        return total_power

    def calculate_total_hourly_cost(self):
        """
        Polymorphic calculation: Iterates through all devices to sum estimated costs.
        """
        total_cost = 0.0
        for device in self._device_registry.values():
            total_cost += device.calculate_hourly_cost()
        return total_cost

    def execute_all_queued_commands(self):
        """
        Processes all pending commands in the FIFO queue sequentially.
        """
        executed_count = 0
        while not self.command_queue.is_empty():
            description, action_func = self.command_queue.dequeue()
            action_func() 
            executed_count += 1
        return executed_count

    def trigger_eco_mode(self):
        """
        A centralized emergency command to turn off all active devices.
        """
        self.command_queue.clear_queue() 
        count = 0
        for device in self._device_registry.values():
            if device.get_status():
                device.turn_off()
                count += 1
        return f"Eco Mode activated: {count} devices powered down."