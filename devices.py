"""
Module: devices.py
Description: Defines the OOP hierarchy for Smart Campus IoT devices.
             Demonstrates Abstraction, Encapsulation, Inheritance, Polymorphism,
             Class/Static Methods, and Magic Methods.
"""
from abc import ABC, abstractmethod

class CampusDevice(ABC):
    """
    Abstract Base Class for all IoT edge devices in the campus network.
    """
    
    total_active_devices = 0
    CLP_BASE_TARIFF = 1.04  # CLP Power base tariff per kWh (HKD)

    def __init__(self, device_id, location):
        self._device_id = device_id
        self._location = location
        self._is_on = False
        CampusDevice.total_active_devices += 1

    def get_id(self):
        """Returns the encapsulated device ID."""
        return self._device_id
        
    def get_location(self):
        """Returns the encapsulated physical location."""
        return self._location
        
    def get_status(self):
        """Returns the current power status (True for ON, False for OFF)."""
        return self._is_on

    def turn_on(self):
        """Powers on the device."""
        self._is_on = True
        
    def turn_off(self):
        """Powers off the device."""
        self._is_on = False

    @abstractmethod
    def get_power_consumption(self):
        """
        Abstract method to be overridden by child classes.
        Returns the real-time power consumption in Watts (W).
        """
        pass

    def calculate_hourly_cost(self):
        """Calculates the estimated cost of running this device for one hour."""
        power_kw = self.get_power_consumption() / 1000.0
        return power_kw * CampusDevice.CLP_BASE_TARIFF

    @classmethod
    def get_system_device_count(cls):
        """Class method returning the total number of instantiated devices."""
        return f"System currently monitoring {cls.total_active_devices} devices."

    @staticmethod
    def validate_hkmu_room(room_code):
        """Static method to validate if the room string follows standard format."""
        return isinstance(room_code, str) and len(room_code) >= 5 and room_code[0] in ['A', 'B', 'C', 'D', 'E']

    def __str__(self):
        """Magic method for string representation of the object."""
        status_str = "ON" if self._is_on else "OFF"
        return f"[{self._device_id}] at {self._location} | Status: {status_str}"

    def __eq__(self, other):
        """Magic method defining equality logic based on device ID."""
        if isinstance(other, CampusDevice):
            return self._device_id == other._device_id
        return False

    def __add__(self, other):
        """Magic method allowing addition of power consumptions between devices."""
        if isinstance(other, CampusDevice):
            return self.get_power_consumption() + other.get_power_consumption()
        return self.get_power_consumption()


class SmartAC(CampusDevice):
    """
    Subclass representing a Smart Air Conditioner.
    Demonstrates Inheritance and Polymorphism.
    """
    
    def __init__(self, device_id, location, base_power=2000):
        super().__init__(device_id, location)
        self._base_power = base_power
        self._target_temp = 24  
        self._ambient_temp = 28 

    def set_temperature(self, temp):
        """Sets the target temperature within a valid range (18-30)."""
        if 18 <= temp <= 30:
            self._target_temp = temp

    def get_power_consumption(self):
        """Polymorphic implementation: Power varies by temperature difference."""
        if not self._is_on:
            return 0.0
        temp_diff = max(0, self._ambient_temp - self._target_temp)
        return self._base_power + (temp_diff * 150)

    def __str__(self):
        return "[AC] " + super().__str__() + f" | Temp: {self._target_temp}°C"


class LabOscilloscope(CampusDevice):
    """
    Subclass representing an Oscilloscope in an ECE laboratory.
    Demonstrates Inheritance and Polymorphism with state-based power draw.
    """
    
    def __init__(self, device_id, location):
        super().__init__(device_id, location)
        self._mode = "Standby" 

    def set_active_mode(self):
        """Sets the device to high-power measurement mode."""
        if self._is_on:
            self._mode = "Active"
            
    def set_standby_mode(self):
        """Sets the device to low-power idle mode."""
        if self._is_on:
            self._mode = "Standby"

    def turn_off(self):
        """Overrides parent method to also reset the operational mode."""
        super().turn_off()
        self._mode = "Standby" 

    def get_power_consumption(self):
        """Polymorphic implementation: Power depends on the operational mode."""
        if not self._is_on:
            return 0.0
        return 350.0 if self._mode == "Active" else 15.0 

    def __str__(self):
        return "[Lab Eqpt] " + super().__str__() + f" | Mode: {self._mode}"