# 🏥 Smart Hospital: Triage & Queue Scheduling Engine

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-brightgreen)
![Architecture](https://img.shields.io/badge/Architecture-OOP%20%7C%20SOLID-orange)
![Algorithm](https://img.shields.io/badge/Algorithm-Multi--Tier%20Priority-red)

An enterprise-grade, OOP-driven hospital triage simulation and queue management terminal. This project demonstrates advanced software design patterns by implementing a **multi-dimensional, dynamic priority scheduling algorithm**, robust polymorphic service definitions, and a real-time fault-tolerant event loop.

---

## 🏛️ Deep Dive: The OOP Architecture

This system is a practical implementation of the four pillars of Object-Oriented Programming (OOP), ensuring the codebase is modular, scalable, and maintainable.

### 1. Abstraction (The Design Contract)
The system utilizes an **Abstract Base Class (ABC)** to define the essential "contract" for all medical services.
* **Implementation**: The `MedicalService` class in `interfaces.py`.
* **Mechanism**: Using the `@abstractmethod` decorator, it mandates that any inheriting class (e.g., different types of doctors) *must* implement `get_fee()` and `process_patient()`.
* **Logic**: This allows the UI and server to interact with any medical provider through a unified interface without needing to know the internal department logic.

### 2. Inheritance (Hierarchical Specialization)
Code reusability is maximized through a clear class hierarchy where child classes inherit and extend the functionality of the parent.
* **Implementation**: The `Doctor` base class and its descendants in `doctor.py`.
* **Mechanism**: `ExpertDoctor` and `EmergencyDoctor` inherit from the `Doctor` class. They use `super().__init__` to initialize common attributes like `name` and `dept` while adding specialized attributes like `title`.
* **Logic**: All doctors share the `enqueue()` logic and the sorting mechanism, but specialize in their department-specific roles.

### 3. Polymorphism (Dynamic Method Dispatch)
The application demonstrates **Method Overriding**, where different objects respond to the same method call with unique behaviors tailored to their type.
* **Implementation**: Overridden methods in `doctor.py`.
* **Mechanism**: 
    * `Doctor.get_fee()` returns a standard fee of **50.0**.
    * `ExpertDoctor.get_fee()` returns a premium fee of **150.0**.
    * `EmergencyDoctor.get_fee()` returns an urgent fee of **200.0**.
* **Logic**: In `ui.py`, when a patient registers, the system calls `doctor.get_fee()`. The UI doesn't need to check the doctor's type; the correct fee is automatically determined at runtime based on the object instance.

### 4. Encapsulation (Information Hiding)
Sensitive data and internal states are shielded from external interference to maintain data integrity.
* **Implementation**: The `Patient` class in `patient.py`.
* **Mechanism**: The patient's financial balance is stored as a **private attribute** `self.__balance`.
* **Logic**: External modules (like the UI) cannot directly modify the balance. Instead, they must use the `deduct_fee()` method, which performs a safety check (verifying sufficient funds) before allowing a transaction.

---

## 🧠 Algorithmic Logic: Multi-Dimensional Triage

The triage engine in `patient.py` uses a sophisticated **Tuple-Comparison Priority Algorithm**. Instead of a simple "first-come, first-served" approach, it calculates a priority tuple to determine a patient's rank.

### The Priority Heuristic
The `get_priority_tuple()` method returns a tuple: `(category, sequence)`. Python compares tuples element-by-element; if the `category` is the same, it falls back to the `sequence` (global arrival order) to ensure **FIFO stability** within tiers.

| Priority Tier | Description | Condition Trigger | Rationale |
| :--- | :--- | :--- | :--- |
| **Tier 0** | 🚨 Emergency | `is_emergency = True` | Highest priority for life-saving care. |
| **Tier 1** | 👴 Elderly (Online) | `age >= 65` & `Online` | Seniority combined with a prior appointment. |
| **Tier 2** | 👴 Elderly (Walk-in)| `age >= 65` & `Walk-in`| Seniority, slightly penalized for no booking. |
| **Tier 3** | 📱 Standard (Online) | `< 65` & `Online` | Contractual appointment priority. |
| **Tier 4** | 🚶 Standard (Walk-in)| `< 65` & `Walk-in`| Standard sequential processing. |
| **Tier 5** | ⚠️ Missed Turn | `is_late = True` | Punitive downgrade for no-shows. |

---

## ⚙️ Operational Flow: The "No-Show" Mechanism

To mirror real-world hospital challenges, the system includes a stochastic event handler in `ui.py`.

1. **Probability**: When "Call Next Patient" is triggered, there is a **20% chance** the patient will be marked as a no-show.
2. **State Transition**: If a no-show occurs, the `mark_late()` method is called.
3. **Dynamic Re-Ranking**: Their `is_late` flag is set to `True`, and their `seq` is updated to the latest global tick. 
4. **Automatic Downgrade**: Upon re-enqueuing, the sorting algorithm pushes them to the absolute end of the queue (Tier 5).

---

## 📂 Project Structure

* `interfaces.py`: Defines the **Abstract Data Type (ADT)** contract.
* `doctor.py`: Implements **Inheritance** and **Polymorphism** for medical staff.
* `patient.py`: Manages **Encapsulation** and the core **Priority Algorithm**.
* `server.py`: The **Backend Registry** managing doctor objects and global stats.
* `ui.py`: The **View Layer** handling the Tkinter GUI and event orchestration.
* `main.py`: The **Bootloader** that initializes the system.

---

## 💻 Quick Start

**1. Prerequisites**
* Python 3.8 or higher.
* Tkinter (standard on most Python installations).

**2. Launch**
```bash
python main.py
