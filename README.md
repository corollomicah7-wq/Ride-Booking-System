# Ride-Booking-System
* This Python-Tkinter project is a ride-booking utility featuring a vibrant, maroon-and-gold themed desktop interface. Key features include an interactive booking log, dynamic pricing computations based on distance, and flexible vehicle configurations.

## Features
* Custom UI: styled with a Maroon (`#600404`) and Gold (`#E69317`) palette
* Dynamic Pricing: Real time distance and fare computation based on selected pickup and dropoff place and specific vehicle rates.
* Capacity Selection: Automatically updates and displays specific passenger capacities depending on the vehicle class selected.
* Booking Dashboard: A data grid built using `ttk.Treeview` that maps out active booking logs.
* Cancellations: Implemented mouse event bindings (<Button-1>) on the data grid, triggering a secure confirmation dialog 'messagebox' before deleting a record.
* Group  Portfolio: Features a custom canvas panel that smoothly displays interactive member profile cards and developer credits.

## Structure
* Language Used: Python
* Gui Framework: Tkk/Tkinter
* Data Storage: ('bookings.txt')

## Project Architecture
* gui.py             # Main Application Window, Styles, Pages & UI bindings
* booking_manager.py # File Operations
* Booking.py         # Booking Entity Class blueprints
* vehicle.py         # Fare matrices, calculations, and vehicle properties
