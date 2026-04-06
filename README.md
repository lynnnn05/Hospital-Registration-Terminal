# 🏥 Smart Hospital: Triage & Queue Scheduling Engine

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-brightgreen)
![Architecture](https://img.shields.io/badge/Architecture-OOP%20%7C%20SOLID-orange)
![Algorithm](https://img.shields.io/badge/Algorithm-Multi--Tier%20Priority-red)

An enterprise-grade, OOP-driven hospital triage simulation and queue management terminal. 

This project is built entirely with Python's standard library to demonstrate advanced software design patterns. It goes far beyond a standard First-In-First-Out (FIFO) queue by implementing a **multi-dimensional, dynamic priority scheduling algorithm**, robust polymorphic service definitions, and a real-time fault-tolerant event loop.

---

## 🧠 Algorithmic Logic: The Multi-Dimensional Queue

The most powerful component of this system is the triage algorithm located in `patient.py`. In a real hospital, a queue is never strictly linear; it must constantly shift based on emergencies, demographics, and prior commitments. 

### The Tuple-Comparison Trick
Instead of writing complex nested `if/else` sorting loops, the engine utilizes Python's magic `__lt__` (less than) method combined with **tuple comparison**. 

When a `Patient` is enqueued, the system generates a priority tuple: `(category, sequence)`. Python evaluates tuples element-by-element. It first compares the `category` (Priority 0 to 5). If two patients share the exact same category, the algorithm naturally falls back to the `sequence` (the global arrival order), ensuring absolute FIFO stability within each specific tier.

| Category Weight | Patient Profile | Condition Trigger | Algorithmic Rationale |
| :--- | :--- | :--- | :--- |
| **Tier 0 (Highest)** | 🚨 **Emergency** | `is_emergency = True` | Overrides all standard logic. Processed immediately. |
| **Tier 1** | 👴 **Elderly (Online)** | `age >= 65` + `Online` | Honors seniority combined with the contract of an appointment. |
| **Tier 2** | 👴 **Elderly (Walk-in)** | `age >= 65` + `Walk-in` | Honors seniority, but penalized slightly for lacking a booking. |
| **Tier 3** | 📱 **Standard (Online)** | `< 65` + `Online` | Rewards the contract of a prior booking over standard walk-ins. |
| **Tier 4** | 🚶 **Standard (Walk-in)** | `< 65` + `Walk-in` | Standard sequential processing. |
| **Tier 5 (Lowest)** | ⚠️ **Missed Turn** | `is_late = True` | Punitive downgrade. See "Operational Logic" below. |

---

## 🧬 Architectural Logic: Object-Oriented Design

The codebase strictly adheres to SOLID principles, ensuring the system is scalable and easy to test.

* **Interface Segregation & Abstraction (ABC):** In `interfaces.py`, `MedicalService` acts as a strict contract. It forces any inheriting class to implement `get_fee()` and `process_patient()`. This means the UI doesn't need to know *what* kind of doctor is working, only that it can call these methods safely.
* **Polymorphism in Action:** In `doctor.py`, `ExpertDoctor` and `EmergencyDoctor` inherit from the base `Doctor` class. They override the base methods to dynamically alter consultation fees and generation logs without breaking the system's core loop.
* **Data Encapsulation:** Patient financial data (`__balance`) is strictly private. It cannot be accidentally altered by UI components. It can only be modified through the controlled `deduct_fee()` method, which verifies sufficient funds before returning a boolean success state.

---

## ⚙️ Operational Logic: Simulation & State Management

### The Stochastic "No-Show" Penalty
A real hospital queue must handle humans who don't pay attention. In `ui.py`, the `call_next_patient` method includes a **20% probabilistic failure rate**. 

If a patient fails to answer the call:
1.  They are dynamically popped from the front of the queue.
2.  Their `is_late` flag is triggered to `True`.
3.  Their sequence number (`seq`) is updated to the absolute latest global tick.
4.  They are re-enqueued.

Because of the Priority Algorithm, this patient instantly drops to **Tier 5** and moves to the very back of the line, ensuring the system doesn't stall while simultaneously not deleting the patient from the database entirely.

### Global State Synchronization
The `HospitalServerCore` acts as a Singleton-like data store. It maintains the registry of doctors and tracks the global `total_handled` count. When the UI asks to refresh the listboxes, it pulls directly from the individual `doctor.queue` states, ensuring the view layer and data layer are completely decoupled.

---

## 📂 Project Structure

```text
📦 Smart-Hospital-Queue-System
 ┣ 📜 interfaces.py   # The Blueprint: Defines the MedicalService Abstract Base Class (ADT).
 ┣ 📜 doctor.py       # The Providers: Concrete implementations of medical staff & local queues.
 ┣ 📜 patient.py      # The State: Encapsulates patient data, financials, and the sorting heuristic.
 ┣ 📜 server.py       # The Backend: Singleton-style core managing the provider pool & global metrics.
 ┣ 📜 ui.py           # The Frontend: Tkinter view layer handling user events & colorized rendering.
 ┗ 📜 main.py         # The Bootloader: Initializes the application window and event loop.
