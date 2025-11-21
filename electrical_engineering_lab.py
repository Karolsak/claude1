"""
Comprehensive Electrical Engineering Lab
Includes: Example calculations, Dynamic simulations, ODE solvers, Interactive GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from scipy.integrate import ode, solve_ivp
import math
import threading
import time


class ElectricalEngineeringLab:
    """Main application class for Electrical Engineering Lab"""

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Electrical Engineering Lab")
        self.root.geometry("1400x900")

        # Simulation control variables
        self.simulation_running = False
        self.simulation_thread = None
        self.time_data = []
        self.current_data = []
        self.voltage_data = []
        self.speed_data = []
        self.torque_data = []

        # Create main menu
        self.create_main_menu()

        # Bind resize event
        self.root.bind('<Configure>', self.on_window_resize)

    def create_main_menu(self):
        """Create the main menu interface"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Electrical Engineering Laboratory",
            font=('Arial', 28, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=40)

        # Menu buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#2c3e50')
        buttons_frame.pack(expand=True)

        # Menu options
        menu_options = [
            ("Example 50.3: Depreciation Analysis", self.show_depreciation_example),
            ("Example 50.4: Load & Energy Analysis", self.show_load_example),
            ("DC Motor Dynamic Simulation", self.show_dc_motor_simulation),
            ("Induction Motor Simulation", self.show_induction_motor_simulation),
            ("RLC Circuit Analysis", self.show_rlc_circuit),
            ("Power System Transient Analysis", self.show_power_system)
        ]

        for i, (text, command) in enumerate(menu_options):
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                font=('Arial', 14),
                bg='#3498db',
                fg='white',
                width=40,
                height=2,
                relief=tk.RAISED,
                bd=3
            )
            btn.pack(pady=10)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#2980b9'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#3498db'))

        # Exit button
        exit_btn = tk.Button(
            buttons_frame,
            text="Exit",
            command=self.root.quit,
            font=('Arial', 14),
            bg='#e74c3c',
            fg='white',
            width=40,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        exit_btn.pack(pady=20)
        exit_btn.bind('<Enter>', lambda e: exit_btn.config(bg='#c0392b'))
        exit_btn.bind('<Leave>', lambda e: exit_btn.config(bg='#e74c3c'))

    def show_depreciation_example(self):
        """Example 50.3: Depreciation calculation"""
        self.clear_window()

        frame = tk.Frame(self.root, bg='white')
        frame.pack(fill=tk.BOTH, expand=True)

        # Back button
        back_btn = tk.Button(frame, text="← Back to Menu", command=self.create_main_menu,
                            font=('Arial', 10), bg='#95a5a6', fg='white')
        back_btn.pack(anchor='nw', padx=10, pady=10)

        # Title
        title = tk.Label(frame, text="Example 50.3: Plant Depreciation Analysis",
                        font=('Arial', 20, 'bold'), bg='white')
        title.pack(pady=20)

        # Input frame
        input_frame = tk.LabelFrame(frame, text="Input Parameters", font=('Arial', 12, 'bold'),
                                   bg='white', padx=20, pady=20)
        input_frame.pack(padx=20, pady=10, fill='x')

        # Initial cost
        tk.Label(input_frame, text="Initial Cost (Rs. Lakhs):", bg='white', font=('Arial', 11)).grid(row=0, column=0, sticky='w', pady=5)
        initial_cost_var = tk.DoubleVar(value=5.0)
        tk.Entry(input_frame, textvariable=initial_cost_var, font=('Arial', 11), width=15).grid(row=0, column=1, pady=5)

        # Salvage value
        tk.Label(input_frame, text="Salvage Value (Rs. Lakhs):", bg='white', font=('Arial', 11)).grid(row=1, column=0, sticky='w', pady=5)
        salvage_var = tk.DoubleVar(value=1.0)
        tk.Entry(input_frame, textvariable=salvage_var, font=('Arial', 11), width=15).grid(row=1, column=1, pady=5)

        # Useful life
        tk.Label(input_frame, text="Useful Life (years):", bg='white', font=('Arial', 11)).grid(row=2, column=0, sticky='w', pady=5)
        life_var = tk.IntVar(value=20)
        tk.Entry(input_frame, textvariable=life_var, font=('Arial', 11), width=15).grid(row=2, column=1, pady=5)

        # Interest rate for sinking fund
        tk.Label(input_frame, text="Interest Rate (%):", bg='white', font=('Arial', 11)).grid(row=3, column=0, sticky='w', pady=5)
        rate_var = tk.DoubleVar(value=8.0)
        tk.Entry(input_frame, textvariable=rate_var, font=('Arial', 11), width=15).grid(row=3, column=1, pady=5)

        # Results frame
        results_frame = tk.LabelFrame(frame, text="Results", font=('Arial', 12, 'bold'),
                                     bg='white', padx=20, pady=20)
        results_frame.pack(padx=20, pady=10, fill='both', expand=True)

        results_text = scrolledtext.ScrolledText(results_frame, font=('Courier', 10), height=15, width=80)
        results_text.pack(fill='both', expand=True)

        def calculate():
            try:
                C = initial_cost_var.get() * 100000  # Convert lakhs to rupees
                S = salvage_var.get() * 100000
                n = life_var.get()
                i = rate_var.get() / 100
                t = n / 2  # Half-way through life

                results_text.delete(1.0, tk.END)
                results_text.insert(tk.END, "="*70 + "\n")
                results_text.insert(tk.END, "PLANT DEPRECIATION ANALYSIS\n")
                results_text.insert(tk.END, "="*70 + "\n\n")

                results_text.insert(tk.END, f"Initial Cost: Rs. {C:,.2f}\n")
                results_text.insert(tk.END, f"Salvage Value: Rs. {S:,.2f}\n")
                results_text.insert(tk.END, f"Useful Life: {n} years\n")
                results_text.insert(tk.END, f"Interest Rate: {rate_var.get()}%\n")
                results_text.insert(tk.END, f"Evaluation Time: {t} years (half-way)\n\n")

                # (a) Straight-line depreciation
                results_text.insert(tk.END, "-"*70 + "\n")
                results_text.insert(tk.END, "(a) STRAIGHT-LINE DEPRECIATION METHOD\n")
                results_text.insert(tk.END, "-"*70 + "\n\n")

                annual_depreciation = (C - S) / n
                total_depreciation = annual_depreciation * t
                book_value_sl = C - total_depreciation

                results_text.insert(tk.END, f"Annual Depreciation = (C - S) / n\n")
                results_text.insert(tk.END, f"                   = ({C:,.2f} - {S:,.2f}) / {n}\n")
                results_text.insert(tk.END, f"                   = Rs. {annual_depreciation:,.2f} per year\n\n")

                results_text.insert(tk.END, f"Total Depreciation after {t} years = {annual_depreciation:,.2f} × {t}\n")
                results_text.insert(tk.END, f"                                    = Rs. {total_depreciation:,.2f}\n\n")

                results_text.insert(tk.END, f"Book Value after {t} years = {C:,.2f} - {total_depreciation:,.2f}\n")
                results_text.insert(tk.END, f"                           = Rs. {book_value_sl:,.2f}\n\n")
                results_text.insert(tk.END, f"RESULT: Rs. {book_value_sl/100000:.2f} Lakhs\n\n")

                # (b) Sinking fund method
                results_text.insert(tk.END, "-"*70 + "\n")
                results_text.insert(tk.END, "(b) SINKING FUND METHOD\n")
                results_text.insert(tk.END, "-"*70 + "\n\n")

                # Sinking fund formula: A = P * [(1+i)^n - 1] / i
                # where A is the amount to be accumulated (C - S)
                # We need to find the accumulated amount after t years

                # Annual deposit
                annual_deposit = (C - S) * i / ((1 + i)**n - 1)

                # Accumulated amount after t years
                accumulated = annual_deposit * (((1 + i)**t - 1) / i)
                book_value_sf = C - accumulated

                results_text.insert(tk.END, f"Annual Sinking Fund Deposit:\n")
                results_text.insert(tk.END, f"D = (C - S) × i / [(1+i)^n - 1]\n")
                results_text.insert(tk.END, f"  = ({C:,.2f} - {S:,.2f}) × {i} / [(1+{i})^{n} - 1]\n")
                results_text.insert(tk.END, f"  = Rs. {annual_deposit:,.2f} per year\n\n")

                results_text.insert(tk.END, f"Accumulated Fund after {t} years:\n")
                results_text.insert(tk.END, f"F = D × [(1+i)^t - 1] / i\n")
                results_text.insert(tk.END, f"  = {annual_deposit:,.2f} × [(1+{i})^{t} - 1] / {i}\n")
                results_text.insert(tk.END, f"  = Rs. {accumulated:,.2f}\n\n")

                results_text.insert(tk.END, f"Book Value after {t} years = {C:,.2f} - {accumulated:,.2f}\n")
                results_text.insert(tk.END, f"                           = Rs. {book_value_sf:,.2f}\n\n")
                results_text.insert(tk.END, f"RESULT: Rs. {book_value_sf/100000:.2f} Lakhs\n\n")

                results_text.insert(tk.END, "="*70 + "\n")
                results_text.insert(tk.END, "COMPARISON\n")
                results_text.insert(tk.END, "="*70 + "\n")
                results_text.insert(tk.END, f"Straight-line method: Rs. {book_value_sl/100000:.2f} Lakhs\n")
                results_text.insert(tk.END, f"Sinking fund method:  Rs. {book_value_sf/100000:.2f} Lakhs\n")
                results_text.insert(tk.END, f"Difference:           Rs. {abs(book_value_sl - book_value_sf)/100000:.2f} Lakhs\n")

            except Exception as e:
                messagebox.showerror("Error", f"Calculation error: {str(e)}")

        # Calculate button
        calc_btn = tk.Button(frame, text="Calculate", command=calculate,
                           font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                           width=20, height=2)
        calc_btn.pack(pady=10)

    def show_load_example(self):
        """Example 50.4: Load and Energy Analysis"""
        self.clear_window()

        frame = tk.Frame(self.root, bg='white')
        frame.pack(fill=tk.BOTH, expand=True)

        # Back button
        back_btn = tk.Button(frame, text="← Back to Menu", command=self.create_main_menu,
                            font=('Arial', 10), bg='#95a5a6', fg='white')
        back_btn.pack(anchor='nw', padx=10, pady=10)

        # Title
        title = tk.Label(frame, text="Example 50.4: Load and Energy Consumption Analysis",
                        font=('Arial', 20, 'bold'), bg='white')
        title.pack(pady=20)

        # Input frame
        input_frame = tk.LabelFrame(frame, text="Connected Load", font=('Arial', 12, 'bold'),
                                   bg='white', padx=20, pady=20)
        input_frame.pack(padx=20, pady=10, fill='x')

        # Lamps
        tk.Label(input_frame, text="Number of Lamps:", bg='white', font=('Arial', 11)).grid(row=0, column=0, sticky='w', pady=5)
        num_lamps_var = tk.IntVar(value=10)
        tk.Entry(input_frame, textvariable=num_lamps_var, font=('Arial', 11), width=15).grid(row=0, column=1, pady=5)

        tk.Label(input_frame, text="Lamp Power (W):", bg='white', font=('Arial', 11)).grid(row=1, column=0, sticky='w', pady=5)
        lamp_power_var = tk.IntVar(value=60)
        tk.Entry(input_frame, textvariable=lamp_power_var, font=('Arial', 11), width=15).grid(row=1, column=1, pady=5)

        tk.Label(input_frame, text="Lamps Used Daily:", bg='white', font=('Arial', 11)).grid(row=2, column=0, sticky='w', pady=5)
        lamps_used_var = tk.IntVar(value=8)
        tk.Entry(input_frame, textvariable=lamps_used_var, font=('Arial', 11), width=15).grid(row=2, column=1, pady=5)

        tk.Label(input_frame, text="Lamp Usage (hours/day):", bg='white', font=('Arial', 11)).grid(row=3, column=0, sticky='w', pady=5)
        lamp_hours_var = tk.IntVar(value=5)
        tk.Entry(input_frame, textvariable=lamp_hours_var, font=('Arial', 11), width=15).grid(row=3, column=1, pady=5)

        # Heaters
        tk.Label(input_frame, text="Number of Heaters:", bg='white', font=('Arial', 11)).grid(row=0, column=2, sticky='w', pady=5, padx=(20,0))
        num_heaters_var = tk.IntVar(value=2)
        tk.Entry(input_frame, textvariable=num_heaters_var, font=('Arial', 11), width=15).grid(row=0, column=3, pady=5)

        tk.Label(input_frame, text="Heater Power (W):", bg='white', font=('Arial', 11)).grid(row=1, column=2, sticky='w', pady=5, padx=(20,0))
        heater_power_var = tk.IntVar(value=1000)
        tk.Entry(input_frame, textvariable=heater_power_var, font=('Arial', 11), width=15).grid(row=1, column=3, pady=5)

        tk.Label(input_frame, text="Heater Usage (hours/day):", bg='white', font=('Arial', 11)).grid(row=2, column=2, sticky='w', pady=5, padx=(20,0))
        heater_hours_var = tk.IntVar(value=3)
        tk.Entry(input_frame, textvariable=heater_hours_var, font=('Arial', 11), width=15).grid(row=2, column=3, pady=5)

        # Maximum demand
        tk.Label(input_frame, text="Maximum Demand (W):", bg='white', font=('Arial', 11)).grid(row=4, column=0, sticky='w', pady=5)
        max_demand_var = tk.IntVar(value=1500)
        tk.Entry(input_frame, textvariable=max_demand_var, font=('Arial', 11), width=15).grid(row=4, column=1, pady=5)

        # Results frame
        results_frame = tk.LabelFrame(frame, text="Results", font=('Arial', 12, 'bold'),
                                     bg='white', padx=20, pady=20)
        results_frame.pack(padx=20, pady=10, fill='both', expand=True)

        results_text = scrolledtext.ScrolledText(results_frame, font=('Courier', 10), height=15, width=80)
        results_text.pack(fill='both', expand=True)

        def calculate():
            try:
                num_lamps = num_lamps_var.get()
                lamp_power = lamp_power_var.get()
                lamps_used = lamps_used_var.get()
                lamp_hours = lamp_hours_var.get()

                num_heaters = num_heaters_var.get()
                heater_power = heater_power_var.get()
                heater_hours = heater_hours_var.get()

                max_demand = max_demand_var.get()

                results_text.delete(1.0, tk.END)
                results_text.insert(tk.END, "="*70 + "\n")
                results_text.insert(tk.END, "LOAD AND ENERGY CONSUMPTION ANALYSIS\n")
                results_text.insert(tk.END, "="*70 + "\n\n")

                # Connected Load
                results_text.insert(tk.END, "CONNECTED LOAD CALCULATION:\n")
                results_text.insert(tk.END, "-"*70 + "\n")

                lamp_total = num_lamps * lamp_power
                heater_total = num_heaters * heater_power
                total_connected_load = lamp_total + heater_total

                results_text.insert(tk.END, f"Lamps:   {num_lamps} × {lamp_power}W = {lamp_total}W\n")
                results_text.insert(tk.END, f"Heaters: {num_heaters} × {heater_power}W = {heater_total}W\n")
                results_text.insert(tk.END, f"\nTotal Connected Load = {total_connected_load}W = {total_connected_load/1000:.2f}kW\n\n")

                # Daily Energy Consumption
                results_text.insert(tk.END, "DAILY ENERGY CONSUMPTION:\n")
                results_text.insert(tk.END, "-"*70 + "\n")

                lamp_energy = lamps_used * lamp_power * lamp_hours  # Wh
                heater_energy = num_heaters * heater_power * heater_hours  # Wh
                daily_energy = lamp_energy + heater_energy  # Wh

                results_text.insert(tk.END, f"Lamps:   {lamps_used} × {lamp_power}W × {lamp_hours}h = {lamp_energy}Wh\n")
                results_text.insert(tk.END, f"Heaters: {num_heaters} × {heater_power}W × {heater_hours}h = {heater_energy}Wh\n")
                results_text.insert(tk.END, f"\nDaily Energy Consumption = {daily_energy}Wh = {daily_energy/1000:.2f}kWh\n\n")

                # Monthly Energy Consumption (assuming 30 days)
                monthly_energy = daily_energy * 30 / 1000  # kWh
                results_text.insert(tk.END, "MONTHLY ENERGY CONSUMPTION (30 days):\n")
                results_text.insert(tk.END, "-"*70 + "\n")
                results_text.insert(tk.END, f"Monthly Energy = {daily_energy}Wh × 30 days = {monthly_energy:.2f}kWh\n\n")

                # Load Factor
                results_text.insert(tk.END, "LOAD FACTOR CALCULATION:\n")
                results_text.insert(tk.END, "-"*70 + "\n")

                # Average Load = Total Energy / Total Time (24 hours)
                average_load = daily_energy / 24  # W
                load_factor = (average_load / max_demand) * 100

                results_text.insert(tk.END, f"Average Load = Daily Energy / 24 hours\n")
                results_text.insert(tk.END, f"             = {daily_energy}Wh / 24h\n")
                results_text.insert(tk.END, f"             = {average_load:.2f}W\n\n")

                results_text.insert(tk.END, f"Load Factor = (Average Load / Maximum Demand) × 100\n")
                results_text.insert(tk.END, f"            = ({average_load:.2f}W / {max_demand}W) × 100\n")
                results_text.insert(tk.END, f"            = {load_factor:.2f}%\n\n")

                # Summary
                results_text.insert(tk.END, "="*70 + "\n")
                results_text.insert(tk.END, "SUMMARY\n")
                results_text.insert(tk.END, "="*70 + "\n")
                results_text.insert(tk.END, f"Total Connected Load:        {total_connected_load/1000:.2f} kW\n")
                results_text.insert(tk.END, f"Maximum Demand:              {max_demand/1000:.2f} kW\n")
                results_text.insert(tk.END, f"Daily Energy Consumption:    {daily_energy/1000:.2f} kWh\n")
                results_text.insert(tk.END, f"Monthly Energy Consumption:  {monthly_energy:.2f} kWh\n")
                results_text.insert(tk.END, f"Average Load:                {average_load/1000:.2f} kW\n")
                results_text.insert(tk.END, f"Load Factor:                 {load_factor:.2f}%\n")

                # Demand Factor
                demand_factor = (max_demand / total_connected_load) * 100
                results_text.insert(tk.END, f"Demand Factor:               {demand_factor:.2f}%\n")

            except Exception as e:
                messagebox.showerror("Error", f"Calculation error: {str(e)}")

        # Calculate button
        calc_btn = tk.Button(frame, text="Calculate", command=calculate,
                           font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                           width=20, height=2)
        calc_btn.pack(pady=10)

    def show_dc_motor_simulation(self):
        """DC Motor Dynamic Simulation with ODE solvers"""
        self.clear_window()

        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Back button
        back_btn = tk.Button(main_frame, text="← Back to Menu", command=self.create_main_menu,
                            font=('Arial', 10), bg='#95a5a6', fg='white')
        back_btn.pack(anchor='nw', padx=10, pady=10)

        # Title
        title = tk.Label(main_frame, text="DC Motor Dynamic Simulation",
                        font=('Arial', 20, 'bold'), bg='white')
        title.pack(pady=10)

        # Control panel
        control_frame = tk.LabelFrame(main_frame, text="Motor Parameters",
                                      font=('Arial', 11, 'bold'), bg='white', padx=15, pady=15)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Parameters
        params = {}

        param_list = [
            ("Voltage (V):", "voltage", 220, 0, 500),
            ("Armature Resistance (Ω):", "Ra", 0.5, 0.1, 5),
            ("Armature Inductance (H):", "La", 0.01, 0.001, 0.1),
            ("Back EMF Constant (Vs/rad):", "Ke", 0.8, 0.1, 2),
            ("Torque Constant (Nm/A):", "Kt", 0.8, 0.1, 2),
            ("Inertia (kg·m²):", "J", 0.02, 0.001, 0.5),
            ("Friction Coefficient:", "B", 0.001, 0, 0.01),
            ("Load Torque (Nm):", "TL", 10, 0, 50)
        ]

        for i, (label, key, default, min_val, max_val) in enumerate(param_list):
            tk.Label(control_frame, text=label, bg='white', font=('Arial', 9)).grid(row=i, column=0, sticky='w', pady=3)

            var = tk.DoubleVar(value=default)
            params[key] = var

            slider = tk.Scale(control_frame, from_=min_val, to=max_val, resolution=(max_val-min_val)/100,
                            orient=tk.HORIZONTAL, variable=var, length=200)
            slider.grid(row=i, column=1, pady=3)

            entry = tk.Entry(control_frame, textvariable=var, width=8, font=('Arial', 9))
            entry.grid(row=i, column=2, pady=3, padx=5)

        # Solver selection
        tk.Label(control_frame, text="ODE Solver:", bg='white', font=('Arial', 9, 'bold')).grid(row=len(param_list), column=0, sticky='w', pady=10)
        solver_var = tk.StringVar(value="RK45")
        solver_combo = ttk.Combobox(control_frame, textvariable=solver_var,
                                    values=["RK45", "Euler", "RK23", "DOP853"],
                                    state='readonly', width=15)
        solver_combo.grid(row=len(param_list), column=1, pady=10)

        # Simulation time
        tk.Label(control_frame, text="Simulation Time (s):", bg='white', font=('Arial', 9)).grid(row=len(param_list)+1, column=0, sticky='w', pady=3)
        sim_time_var = tk.DoubleVar(value=5.0)
        tk.Entry(control_frame, textvariable=sim_time_var, width=8, font=('Arial', 9)).grid(row=len(param_list)+1, column=1, sticky='w', pady=3)

        # Control buttons
        button_frame = tk.Frame(control_frame, bg='white')
        button_frame.grid(row=len(param_list)+2, column=0, columnspan=3, pady=20)

        self.dc_motor_running = False

        def start_simulation():
            if self.dc_motor_running:
                messagebox.showwarning("Warning", "Simulation already running!")
                return

            self.dc_motor_running = True
            start_btn.config(state='disabled')
            stop_btn.config(state='normal')

            # Get parameters
            V = params['voltage'].get()
            Ra = params['Ra'].get()
            La = params['La'].get()
            Ke = params['Ke'].get()
            Kt = params['Kt'].get()
            J = params['J'].get()
            B = params['B'].get()
            TL = params['TL'].get()
            sim_time = sim_time_var.get()
            solver = solver_var.get()

            # DC Motor differential equations:
            # di/dt = (V - Ra*i - Ke*ω) / La
            # dω/dt = (Kt*i - TL - B*ω) / J

            def dc_motor_ode(t, y):
                i, omega = y
                di_dt = (V - Ra * i - Ke * omega) / La
                domega_dt = (Kt * i - TL - B * omega) / J
                return [di_dt, domega_dt]

            # Initial conditions: [current, angular velocity]
            y0 = [0, 0]

            # Solve ODE
            if solver == "Euler":
                # Euler method
                t_span = (0, sim_time)
                t_eval = np.linspace(0, sim_time, 1000)
                dt = t_eval[1] - t_eval[0]

                t_result = [0]
                y_result = [y0]

                for _ in range(len(t_eval) - 1):
                    y_current = y_result[-1]
                    dydt = dc_motor_ode(t_result[-1], y_current)
                    y_new = [y_current[j] + dydt[j] * dt for j in range(len(y_current))]
                    t_result.append(t_result[-1] + dt)
                    y_result.append(y_new)

                t_result = np.array(t_result)
                y_result = np.array(y_result)
                current = y_result[:, 0]
                omega = y_result[:, 1]
            else:
                # Use scipy solve_ivp
                sol = solve_ivp(dc_motor_ode, (0, sim_time), y0, method=solver,
                              t_eval=np.linspace(0, sim_time, 1000), dense_output=True)
                t_result = sol.t
                current = sol.y[0]
                omega = sol.y[1]

            # Calculate derived quantities
            speed_rpm = omega * 60 / (2 * np.pi)
            voltage_rms = np.full_like(t_result, V)
            current_rms = np.abs(current)
            torque = Kt * current
            power = voltage_rms * current_rms / 1000  # kW

            # Plot results
            ax1.clear()
            ax2.clear()
            ax3.clear()
            ax4.clear()

            ax1.plot(t_result, current_rms, 'b-', linewidth=2, label='Current (A)')
            ax1.set_ylabel('Current (A)', fontsize=10, fontweight='bold')
            ax1.set_xlabel('Time (s)', fontsize=10)
            ax1.grid(True, alpha=0.3)
            ax1.legend(loc='upper right')
            ax1.set_title('Armature Current', fontweight='bold')

            ax2.plot(t_result, speed_rpm, 'r-', linewidth=2, label='Speed (RPM)')
            ax2.set_ylabel('Speed (RPM)', fontsize=10, fontweight='bold')
            ax2.set_xlabel('Time (s)', fontsize=10)
            ax2.grid(True, alpha=0.3)
            ax2.legend(loc='upper right')
            ax2.set_title('Motor Speed', fontweight='bold')

            ax3.plot(t_result, voltage_rms, 'g-', linewidth=2, label='Voltage (V)')
            ax3.set_ylabel('Voltage (V)', fontsize=10, fontweight='bold')
            ax3.set_xlabel('Time (s)', fontsize=10)
            ax3.grid(True, alpha=0.3)
            ax3.legend(loc='upper right')
            ax3.set_title('Supply Voltage (RMS)', fontweight='bold')

            ax4.plot(t_result, torque, 'm-', linewidth=2, label='Torque (Nm)')
            ax4.set_ylabel('Torque (Nm)', fontsize=10, fontweight='bold')
            ax4.set_xlabel('Time (s)', fontsize=10)
            ax4.grid(True, alpha=0.3)
            ax4.legend(loc='upper right')
            ax4.set_title('Motor Torque', fontweight='bold')

            fig.tight_layout()
            canvas.draw()

            # Update info
            info_text.delete(1.0, tk.END)
            info_text.insert(tk.END, f"Solver: {solver}\n")
            info_text.insert(tk.END, f"Simulation Time: {sim_time:.2f} s\n\n")
            info_text.insert(tk.END, f"Steady-State Results:\n")
            info_text.insert(tk.END, f"  Current: {current[-1]:.2f} A (RMS)\n")
            info_text.insert(tk.END, f"  Speed: {speed_rpm[-1]:.2f} RPM\n")
            info_text.insert(tk.END, f"  Torque: {torque[-1]:.2f} Nm\n")
            info_text.insert(tk.END, f"  Power: {power[-1]:.3f} kW\n")

            self.dc_motor_running = False
            start_btn.config(state='normal')
            stop_btn.config(state='disabled')

        def stop_simulation():
            self.dc_motor_running = False
            start_btn.config(state='normal')
            stop_btn.config(state='disabled')

        def reset_simulation():
            self.dc_motor_running = False
            ax1.clear()
            ax2.clear()
            ax3.clear()
            ax4.clear()
            fig.tight_layout()
            canvas.draw()
            info_text.delete(1.0, tk.END)
            start_btn.config(state='normal')
            stop_btn.config(state='disabled')

        start_btn = tk.Button(button_frame, text="Start", command=start_simulation,
                            bg='#27ae60', fg='white', font=('Arial', 10, 'bold'), width=10)
        start_btn.pack(side=tk.LEFT, padx=5)

        stop_btn = tk.Button(button_frame, text="Stop", command=stop_simulation,
                           bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'), width=10, state='disabled')
        stop_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = tk.Button(button_frame, text="Reset", command=reset_simulation,
                            bg='#f39c12', fg='white', font=('Arial', 10, 'bold'), width=10)
        reset_btn.pack(side=tk.LEFT, padx=5)

        # Info panel
        info_frame = tk.LabelFrame(control_frame, text="Simulation Info",
                                   font=('Arial', 10, 'bold'), bg='white', padx=10, pady=10)
        info_frame.grid(row=len(param_list)+3, column=0, columnspan=3, pady=10, sticky='ew')

        info_text = tk.Text(info_frame, height=10, width=35, font=('Courier', 8))
        info_text.pack()

        # Visualization frame
        viz_frame = tk.Frame(main_frame, bg='white')
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create matplotlib figure
        fig = Figure(figsize=(10, 8))
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)

        canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_induction_motor_simulation(self):
        """Induction Motor Simulation"""
        self.clear_window()

        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Back button
        back_btn = tk.Button(main_frame, text="← Back to Menu", command=self.create_main_menu,
                            font=('Arial', 10), bg='#95a5a6', fg='white')
        back_btn.pack(anchor='nw', padx=10, pady=10)

        # Title
        title = tk.Label(main_frame, text="Three-Phase Induction Motor Simulation",
                        font=('Arial', 20, 'bold'), bg='white')
        title.pack(pady=10)

        # Control panel
        control_frame = tk.LabelFrame(main_frame, text="Motor Parameters",
                                      font=('Arial', 11, 'bold'), bg='white', padx=15, pady=15)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Parameters
        params = {}

        param_list = [
            ("Line Voltage (V):", "voltage", 415, 100, 690),
            ("Frequency (Hz):", "freq", 50, 25, 60),
            ("Stator Resistance (Ω):", "Rs", 0.5, 0.1, 2),
            ("Rotor Resistance (Ω):", "Rr", 0.3, 0.1, 2),
            ("Stator Reactance (Ω):", "Xs", 2.0, 0.5, 5),
            ("Rotor Reactance (Ω):", "Xr", 2.0, 0.5, 5),
            ("Magnetizing Reactance (Ω):", "Xm", 50, 10, 100),
            ("Number of Poles:", "poles", 4, 2, 8),
            ("Load Torque (Nm):", "TL", 50, 0, 200)
        ]

        for i, (label, key, default, min_val, max_val) in enumerate(param_list):
            tk.Label(control_frame, text=label, bg='white', font=('Arial', 9)).grid(row=i, column=0, sticky='w', pady=3)

            var = tk.DoubleVar(value=default)
            params[key] = var

            if key == "poles":
                slider = tk.Scale(control_frame, from_=min_val, to=max_val, resolution=2,
                                orient=tk.HORIZONTAL, variable=var, length=200)
            else:
                slider = tk.Scale(control_frame, from_=min_val, to=max_val, resolution=(max_val-min_val)/100,
                                orient=tk.HORIZONTAL, variable=var, length=200)
            slider.grid(row=i, column=1, pady=3)

            entry = tk.Entry(control_frame, textvariable=var, width=8, font=('Arial', 9))
            entry.grid(row=i, column=2, pady=3, padx=5)

        # Control buttons
        button_frame = tk.Frame(control_frame, bg='white')
        button_frame.grid(row=len(param_list), column=0, columnspan=3, pady=20)

        def calculate_performance():
            try:
                V_line = params['voltage'].get()
                f = params['freq'].get()
                Rs = params['Rs'].get()
                Rr = params['Rr'].get()
                Xs = params['Xs'].get()
                Xr = params['Xr'].get()
                Xm = params['Xm'].get()
                poles = int(params['poles'].get())

                # Synchronous speed
                ns = 120 * f / poles  # RPM
                ws = 2 * np.pi * ns / 60  # rad/s

                # Phase voltage
                V_ph = V_line / np.sqrt(3)

                # Calculate performance for range of slips
                slip = np.linspace(0.001, 1, 100)

                current = []
                torque = []
                power_out = []
                efficiency = []
                pf = []

                for s in slip:
                    # Rotor impedance referred to stator
                    Zr = Rr / s + 1j * Xr

                    # Parallel combination of Xm and Zr
                    Z_parallel = (1j * Xm * Zr) / (1j * Xm + Zr)

                    # Total impedance
                    Z_total = Rs + 1j * Xs + Z_parallel

                    # Stator current (RMS)
                    I_s = V_ph / Z_total
                    I_s_mag = abs(I_s)
                    current.append(I_s_mag)

                    # Power factor
                    angle = np.angle(Z_total)
                    pf_val = np.cos(angle)
                    pf.append(pf_val)

                    # Air gap power
                    I_r = V_ph / (Rs + 1j * Xs + Zr)
                    P_ag = 3 * abs(I_r)**2 * Rr / s

                    # Mechanical power
                    P_mech = P_ag * (1 - s)

                    # Torque
                    n = ns * (1 - s)
                    w = 2 * np.pi * n / 60
                    T = P_mech / w if w > 0 else 0
                    torque.append(T)

                    # Output power
                    power_out.append(P_mech / 1000)  # kW

                    # Input power
                    P_in = 3 * V_ph * I_s_mag * pf_val

                    # Efficiency
                    eff = (P_mech / P_in * 100) if P_in > 0 else 0
                    efficiency.append(eff)

                speed = ns * (1 - slip)

                # Plot results
                ax1.clear()
                ax2.clear()
                ax3.clear()
                ax4.clear()

                ax1.plot(speed, current, 'b-', linewidth=2)
                ax1.set_ylabel('Current (A)', fontsize=10, fontweight='bold')
                ax1.set_xlabel('Speed (RPM)', fontsize=10)
                ax1.grid(True, alpha=0.3)
                ax1.set_title('Stator Current vs Speed', fontweight='bold')

                ax2.plot(speed, torque, 'r-', linewidth=2)
                ax2.set_ylabel('Torque (Nm)', fontsize=10, fontweight='bold')
                ax2.set_xlabel('Speed (RPM)', fontsize=10)
                ax2.grid(True, alpha=0.3)
                ax2.set_title('Torque-Speed Characteristic', fontweight='bold')

                ax3.plot(speed, power_out, 'g-', linewidth=2)
                ax3.set_ylabel('Power (kW)', fontsize=10, fontweight='bold')
                ax3.set_xlabel('Speed (RPM)', fontsize=10)
                ax3.grid(True, alpha=0.3)
                ax3.set_title('Output Power vs Speed', fontweight='bold')

                ax4.plot(speed, efficiency, 'm-', linewidth=2)
                ax4.set_ylabel('Efficiency (%)', fontsize=10, fontweight='bold')
                ax4.set_xlabel('Speed (RPM)', fontsize=10)
                ax4.grid(True, alpha=0.3)
                ax4.set_title('Efficiency vs Speed', fontweight='bold')

                fig.tight_layout()
                canvas.draw()

                # Find maximum torque and starting torque
                max_torque = max(torque)
                max_torque_idx = torque.index(max_torque)
                starting_torque = torque[-1]

                # Update info
                info_text.delete(1.0, tk.END)
                info_text.insert(tk.END, f"Motor Specifications:\n")
                info_text.insert(tk.END, f"  Synchronous Speed: {ns:.2f} RPM\n")
                info_text.insert(tk.END, f"  Poles: {int(poles)}\n")
                info_text.insert(tk.END, f"  Frequency: {f} Hz\n\n")
                info_text.insert(tk.END, f"Performance:\n")
                info_text.insert(tk.END, f"  Starting Torque: {starting_torque:.2f} Nm\n")
                info_text.insert(tk.END, f"  Max Torque: {max_torque:.2f} Nm\n")
                info_text.insert(tk.END, f"  @ Speed: {speed[max_torque_idx]:.2f} RPM\n")
                info_text.insert(tk.END, f"  Max Efficiency: {max(efficiency):.2f}%\n")
                info_text.insert(tk.END, f"  Max Power Factor: {max(pf):.3f}\n")

            except Exception as e:
                messagebox.showerror("Error", f"Calculation error: {str(e)}")

        calc_btn = tk.Button(button_frame, text="Calculate", command=calculate_performance,
                            bg='#27ae60', fg='white', font=('Arial', 10, 'bold'), width=15, height=2)
        calc_btn.pack(pady=5)

        reset_btn = tk.Button(button_frame, text="Reset", command=lambda: [ax.clear() for ax in [ax1, ax2, ax3, ax4]] or canvas.draw(),
                            bg='#f39c12', fg='white', font=('Arial', 10, 'bold'), width=15)
        reset_btn.pack(pady=5)

        # Info panel
        info_frame = tk.LabelFrame(control_frame, text="Motor Info",
                                   font=('Arial', 10, 'bold'), bg='white', padx=10, pady=10)
        info_frame.grid(row=len(param_list)+1, column=0, columnspan=3, pady=10, sticky='ew')

        info_text = tk.Text(info_frame, height=12, width=35, font=('Courier', 8))
        info_text.pack()

        # Visualization frame
        viz_frame = tk.Frame(main_frame, bg='white')
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create matplotlib figure
        fig = Figure(figsize=(10, 8))
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)

        canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_rlc_circuit(self):
        """RLC Circuit Analysis with Dynamic Simulation"""
        self.clear_window()

        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Back button
        back_btn = tk.Button(main_frame, text="← Back to Menu", command=self.create_main_menu,
                            font=('Arial', 10), bg='#95a5a6', fg='white')
        back_btn.pack(anchor='nw', padx=10, pady=10)

        # Title
        title = tk.Label(main_frame, text="RLC Circuit Transient Analysis",
                        font=('Arial', 20, 'bold'), bg='white')
        title.pack(pady=10)

        # Control panel
        control_frame = tk.LabelFrame(main_frame, text="Circuit Parameters",
                                      font=('Arial', 11, 'bold'), bg='white', padx=15, pady=15)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Parameters
        params = {}

        param_list = [
            ("Voltage (V):", "voltage", 100, 0, 500),
            ("Resistance (Ω):", "R", 10, 0.1, 100),
            ("Inductance (mH):", "L", 100, 1, 1000),
            ("Capacitance (μF):", "C", 100, 1, 1000),
            ("Frequency (Hz):", "freq", 50, 10, 1000)
        ]

        for i, (label, key, default, min_val, max_val) in enumerate(param_list):
            tk.Label(control_frame, text=label, bg='white', font=('Arial', 9)).grid(row=i, column=0, sticky='w', pady=3)

            var = tk.DoubleVar(value=default)
            params[key] = var

            slider = tk.Scale(control_frame, from_=min_val, to=max_val, resolution=(max_val-min_val)/100,
                            orient=tk.HORIZONTAL, variable=var, length=200)
            slider.grid(row=i, column=1, pady=3)

            entry = tk.Entry(control_frame, textvariable=var, width=8, font=('Arial', 9))
            entry.grid(row=i, column=2, pady=3, padx=5)

        # Circuit type
        tk.Label(control_frame, text="Circuit Type:", bg='white', font=('Arial', 9, 'bold')).grid(row=len(param_list), column=0, sticky='w', pady=10)
        circuit_type_var = tk.StringVar(value="Series RLC")
        circuit_combo = ttk.Combobox(control_frame, textvariable=circuit_type_var,
                                    values=["Series RLC", "Parallel RLC", "Step Response"],
                                    state='readonly', width=15)
        circuit_combo.grid(row=len(param_list), column=1, pady=10)

        # Solver selection
        tk.Label(control_frame, text="ODE Solver:", bg='white', font=('Arial', 9, 'bold')).grid(row=len(param_list)+1, column=0, sticky='w', pady=5)
        solver_var = tk.StringVar(value="RK45")
        solver_combo = ttk.Combobox(control_frame, textvariable=solver_var,
                                    values=["RK45", "Euler", "RK23"],
                                    state='readonly', width=15)
        solver_combo.grid(row=len(param_list)+1, column=1, pady=5)

        # Control buttons
        button_frame = tk.Frame(control_frame, bg='white')
        button_frame.grid(row=len(param_list)+2, column=0, columnspan=3, pady=20)

        def simulate():
            try:
                V0 = params['voltage'].get()
                R = params['R'].get()
                L = params['L'].get() / 1000  # Convert mH to H
                C = params['C'].get() / 1e6  # Convert μF to F
                freq = params['freq'].get()
                circuit_type = circuit_type_var.get()
                solver = solver_var.get()

                omega = 2 * np.pi * freq
                sim_time = 0.1  # 100ms

                if circuit_type == "Step Response":
                    # Step response of series RLC
                    # Differential equation: L*d²i/dt² + R*di/dt + i/C = dV/dt
                    # State variables: x1 = i, x2 = di/dt

                    def rlc_ode(t, y):
                        i, di_dt = y
                        vc = (1/C) * i  # Simplified
                        d2i_dt2 = (V0 - R * di_dt - vc) / L
                        return [di_dt, d2i_dt2]

                    y0 = [0, 0]

                elif circuit_type == "Series RLC":
                    # Series RLC with sinusoidal source
                    def rlc_ode(t, y):
                        i, q = y  # current and charge
                        V = V0 * np.sin(omega * t)
                        di_dt = (V - R * i - q / C) / L
                        dq_dt = i
                        return [di_dt, dq_dt]

                    y0 = [0, 0]

                else:  # Parallel RLC
                    def rlc_ode(t, y):
                        vc, i_L = y
                        V = V0 * np.sin(omega * t)
                        dvc_dt = (V / R - vc / R - i_L) / C
                        di_L_dt = vc / L
                        return [dvc_dt, di_L_dt]

                    y0 = [0, 0]

                # Solve
                if solver == "Euler":
                    t_eval = np.linspace(0, sim_time, 2000)
                    dt = t_eval[1] - t_eval[0]

                    t_result = [0]
                    y_result = [y0]

                    for _ in range(len(t_eval) - 1):
                        y_current = y_result[-1]
                        dydt = rlc_ode(t_result[-1], y_current)
                        y_new = [y_current[j] + dydt[j] * dt for j in range(len(y_current))]
                        t_result.append(t_result[-1] + dt)
                        y_result.append(y_new)

                    t_result = np.array(t_result)
                    y_result = np.array(y_result)
                else:
                    sol = solve_ivp(rlc_ode, (0, sim_time), y0, method=solver,
                                  t_eval=np.linspace(0, sim_time, 2000))
                    t_result = sol.t
                    y_result = sol.y.T

                # Extract results
                if circuit_type == "Parallel RLC":
                    voltage = y_result[:, 0]
                    current = y_result[:, 1]
                else:
                    current = y_result[:, 0]
                    if circuit_type == "Series RLC":
                        charge = y_result[:, 1]
                        voltage = charge / C
                    else:
                        voltage = np.array([V0 * (1 - np.exp(-5*t)) for t in t_result])

                # RMS values
                current_rms = np.sqrt(np.mean(current**2))
                voltage_rms = np.sqrt(np.mean(voltage**2))

                # Power
                power = voltage * current
                avg_power = np.mean(power)

                # Impedance
                if circuit_type == "Series RLC":
                    XL = omega * L
                    XC = 1 / (omega * C)
                    Z = np.sqrt(R**2 + (XL - XC)**2)
                    resonant_freq = 1 / (2 * np.pi * np.sqrt(L * C))

                # Plot
                ax1.clear()
                ax2.clear()
                ax3.clear()
                ax4.clear()

                t_ms = t_result * 1000  # Convert to ms

                ax1.plot(t_ms, current, 'b-', linewidth=2)
                ax1.set_ylabel('Current (A)', fontsize=10, fontweight='bold')
                ax1.set_xlabel('Time (ms)', fontsize=10)
                ax1.grid(True, alpha=0.3)
                ax1.set_title('Current vs Time', fontweight='bold')

                ax2.plot(t_ms, voltage, 'r-', linewidth=2)
                ax2.set_ylabel('Voltage (V)', fontsize=10, fontweight='bold')
                ax2.set_xlabel('Time (ms)', fontsize=10)
                ax2.grid(True, alpha=0.3)
                ax2.set_title('Voltage vs Time', fontweight='bold')

                ax3.plot(t_ms, power, 'g-', linewidth=2)
                ax3.set_ylabel('Power (W)', fontsize=10, fontweight='bold')
                ax3.set_xlabel('Time (ms)', fontsize=10)
                ax3.grid(True, alpha=0.3)
                ax3.set_title('Instantaneous Power', fontweight='bold')

                # Phase diagram
                ax4.plot(current, voltage, 'm-', linewidth=1.5)
                ax4.set_xlabel('Current (A)', fontsize=10, fontweight='bold')
                ax4.set_ylabel('Voltage (V)', fontsize=10, fontweight='bold')
                ax4.grid(True, alpha=0.3)
                ax4.set_title('Phase Diagram (V-I)', fontweight='bold')

                fig.tight_layout()
                canvas.draw()

                # Update info
                info_text.delete(1.0, tk.END)
                info_text.insert(tk.END, f"Circuit: {circuit_type}\n")
                info_text.insert(tk.END, f"Solver: {solver}\n\n")
                info_text.insert(tk.END, f"Parameters:\n")
                info_text.insert(tk.END, f"  R = {R:.2f} Ω\n")
                info_text.insert(tk.END, f"  L = {L*1000:.2f} mH\n")
                info_text.insert(tk.END, f"  C = {C*1e6:.2f} μF\n\n")
                info_text.insert(tk.END, f"Results:\n")
                info_text.insert(tk.END, f"  I(RMS) = {current_rms:.4f} A\n")
                info_text.insert(tk.END, f"  V(RMS) = {voltage_rms:.2f} V\n")
                info_text.insert(tk.END, f"  P(avg) = {avg_power:.2f} W\n")

                if circuit_type == "Series RLC":
                    info_text.insert(tk.END, f"  Z = {Z:.2f} Ω\n")
                    info_text.insert(tk.END, f"  f₀ = {resonant_freq:.2f} Hz\n")
                    Q = (omega * L) / R
                    info_text.insert(tk.END, f"  Q = {Q:.2f}\n")

            except Exception as e:
                messagebox.showerror("Error", f"Simulation error: {str(e)}")

        start_btn = tk.Button(button_frame, text="Simulate", command=simulate,
                            bg='#27ae60', fg='white', font=('Arial', 10, 'bold'), width=15, height=2)
        start_btn.pack(pady=5)

        reset_btn = tk.Button(button_frame, text="Reset", command=lambda: [ax.clear() for ax in [ax1, ax2, ax3, ax4]] or canvas.draw(),
                            bg='#f39c12', fg='white', font=('Arial', 10, 'bold'), width=15)
        reset_btn.pack(pady=5)

        # Info panel
        info_frame = tk.LabelFrame(control_frame, text="Circuit Info",
                                   font=('Arial', 10, 'bold'), bg='white', padx=10, pady=10)
        info_frame.grid(row=len(param_list)+3, column=0, columnspan=3, pady=10, sticky='ew')

        info_text = tk.Text(info_frame, height=14, width=35, font=('Courier', 8))
        info_text.pack()

        # Visualization frame
        viz_frame = tk.Frame(main_frame, bg='white')
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create matplotlib figure
        fig = Figure(figsize=(10, 8))
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)

        canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_power_system(self):
        """Power System Transient Analysis"""
        self.clear_window()

        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Back button
        back_btn = tk.Button(main_frame, text="← Back to Menu", command=self.create_main_menu,
                            font=('Arial', 10), bg='#95a5a6', fg='white')
        back_btn.pack(anchor='nw', padx=10, pady=10)

        # Title
        title = tk.Label(main_frame, text="Power System Transient Analysis",
                        font=('Arial', 20, 'bold'), bg='white')
        title.pack(pady=10)

        # Control panel
        control_frame = tk.LabelFrame(main_frame, text="System Parameters",
                                      font=('Arial', 11, 'bold'), bg='white', padx=15, pady=15)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Parameters
        params = {}

        param_list = [
            ("Line Voltage (kV):", "voltage", 11, 1, 33),
            ("Generator Inertia (MJ/MVA):", "H", 5, 2, 10),
            ("Load Power (MW):", "P_load", 50, 10, 200),
            ("Damping Coefficient:", "D", 2, 0.5, 5),
            ("Fault Duration (ms):", "fault_time", 150, 50, 500),
            ("Line Reactance (%):", "X", 10, 5, 30)
        ]

        for i, (label, key, default, min_val, max_val) in enumerate(param_list):
            tk.Label(control_frame, text=label, bg='white', font=('Arial', 9)).grid(row=i, column=0, sticky='w', pady=3)

            var = tk.DoubleVar(value=default)
            params[key] = var

            slider = tk.Scale(control_frame, from_=min_val, to=max_val, resolution=(max_val-min_val)/100,
                            orient=tk.HORIZONTAL, variable=var, length=200)
            slider.grid(row=i, column=1, pady=3)

            entry = tk.Entry(control_frame, textvariable=var, width=8, font=('Arial', 9))
            entry.grid(row=i, column=2, pady=3, padx=5)

        # Fault type
        tk.Label(control_frame, text="Fault Type:", bg='white', font=('Arial', 9, 'bold')).grid(row=len(param_list), column=0, sticky='w', pady=10)
        fault_type_var = tk.StringVar(value="Three-Phase")
        fault_combo = ttk.Combobox(control_frame, textvariable=fault_type_var,
                                   values=["Three-Phase", "Line-to-Ground", "Line-to-Line", "Load Variation"],
                                   state='readonly', width=15)
        fault_combo.grid(row=len(param_list), column=1, pady=10)

        # Solver
        tk.Label(control_frame, text="Solver:", bg='white', font=('Arial', 9, 'bold')).grid(row=len(param_list)+1, column=0, sticky='w', pady=5)
        solver_var = tk.StringVar(value="RK45")
        solver_combo = ttk.Combobox(control_frame, textvariable=solver_var,
                                    values=["RK45", "RK23", "DOP853"],
                                    state='readonly', width=15)
        solver_combo.grid(row=len(param_list)+1, column=1, pady=5)

        # Control buttons
        button_frame = tk.Frame(control_frame, bg='white')
        button_frame.grid(row=len(param_list)+2, column=0, columnspan=3, pady=20)

        def simulate():
            try:
                V = params['voltage'].get()
                H = params['H'].get()
                P_load = params['P_load'].get()
                D = params['D'].get()
                fault_duration = params['fault_time'].get() / 1000  # Convert to seconds
                X = params['X'].get() / 100
                fault_type = fault_type_var.get()
                solver = solver_var.get()

                # Swing equation: 2H/ω₀ * d²δ/dt² + D*dδ/dt = Pm - Pe
                # State variables: δ (angle), ω (angular velocity deviation)

                omega_0 = 2 * np.pi * 50  # 50 Hz
                P_m = P_load  # Mechanical power

                def swing_equation(t, y):
                    delta, omega_dev = y

                    # Determine electrical power based on fault condition
                    if t < fault_duration:
                        # During fault
                        if fault_type == "Three-Phase":
                            P_e = 0  # Complete loss of electrical power
                        elif fault_type == "Line-to-Ground":
                            P_e = 0.5 * P_load * np.sin(delta)
                        elif fault_type == "Line-to-Line":
                            P_e = 0.7 * P_load * np.sin(delta)
                        else:  # Load variation
                            P_e = 0.3 * P_load * np.sin(delta)
                    else:
                        # Post-fault
                        if fault_type == "Load Variation":
                            P_e = 1.5 * P_load * np.sin(delta)
                        else:
                            P_e = P_load * np.sin(delta) / X

                    d_delta = omega_dev
                    d_omega = (omega_0 / (2 * H)) * (P_m - P_e - D * omega_dev)

                    return [d_delta, d_omega]

                # Initial conditions: steady-state
                delta_0 = np.arcsin(P_load * X / P_load)  # Initial power angle
                y0 = [delta_0, 0]

                sim_time = 2.0  # 2 seconds

                sol = solve_ivp(swing_equation, (0, sim_time), y0, method=solver,
                              t_eval=np.linspace(0, sim_time, 2000))

                t_result = sol.t
                delta = sol.y[0]
                omega_dev = sol.y[1]

                # Convert to degrees
                delta_deg = np.degrees(delta)

                # Frequency deviation
                freq_dev = omega_dev * 50 / omega_0
                frequency = 50 + freq_dev

                # Calculate power
                P_e = np.array([P_load * np.sin(d) / X if t >= fault_duration else 0
                               for t, d in zip(t_result, delta)])

                # Voltage (simplified)
                V_pu = np.abs(np.cos(delta))
                voltage = V * V_pu

                # Plot
                ax1.clear()
                ax2.clear()
                ax3.clear()
                ax4.clear()

                ax1.plot(t_result * 1000, delta_deg, 'b-', linewidth=2)
                ax1.axvline(fault_duration * 1000, color='r', linestyle='--', label='Fault Cleared')
                ax1.set_ylabel('Power Angle (°)', fontsize=10, fontweight='bold')
                ax1.set_xlabel('Time (ms)', fontsize=10)
                ax1.grid(True, alpha=0.3)
                ax1.legend()
                ax1.set_title('Power Angle Response', fontweight='bold')

                ax2.plot(t_result * 1000, frequency, 'r-', linewidth=2)
                ax2.axhline(50, color='k', linestyle='--', alpha=0.5)
                ax2.axvline(fault_duration * 1000, color='r', linestyle='--', label='Fault Cleared')
                ax2.set_ylabel('Frequency (Hz)', fontsize=10, fontweight='bold')
                ax2.set_xlabel('Time (ms)', fontsize=10)
                ax2.grid(True, alpha=0.3)
                ax2.set_title('Frequency Deviation', fontweight='bold')

                ax3.plot(t_result * 1000, P_e, 'g-', linewidth=2, label='Electrical Power')
                ax3.axhline(P_m, color='b', linestyle='--', label='Mechanical Power')
                ax3.axvline(fault_duration * 1000, color='r', linestyle='--', label='Fault Cleared')
                ax3.set_ylabel('Power (MW)', fontsize=10, fontweight='bold')
                ax3.set_xlabel('Time (ms)', fontsize=10)
                ax3.grid(True, alpha=0.3)
                ax3.legend()
                ax3.set_title('Power Response', fontweight='bold')

                ax4.plot(t_result * 1000, voltage, 'm-', linewidth=2)
                ax4.axvline(fault_duration * 1000, color='r', linestyle='--', label='Fault Cleared')
                ax4.set_ylabel('Voltage (kV)', fontsize=10, fontweight='bold')
                ax4.set_xlabel('Time (ms)', fontsize=10)
                ax4.grid(True, alpha=0.3)
                ax4.set_title('Voltage Profile', fontweight='bold')

                fig.tight_layout()
                canvas.draw()

                # Stability check
                max_angle = np.max(np.abs(delta_deg))
                is_stable = max_angle < 90

                # Update info
                info_text.delete(1.0, tk.END)
                info_text.insert(tk.END, f"Fault Type: {fault_type}\n")
                info_text.insert(tk.END, f"Solver: {solver}\n")
                info_text.insert(tk.END, f"Fault Duration: {fault_duration*1000:.0f} ms\n\n")
                info_text.insert(tk.END, f"System Parameters:\n")
                info_text.insert(tk.END, f"  Voltage: {V:.1f} kV\n")
                info_text.insert(tk.END, f"  Inertia: {H:.1f} MJ/MVA\n")
                info_text.insert(tk.END, f"  Load: {P_load:.1f} MW\n\n")
                info_text.insert(tk.END, f"Transient Response:\n")
                info_text.insert(tk.END, f"  Max Angle: {max_angle:.2f}°\n")
                info_text.insert(tk.END, f"  Max Freq Dev: ±{np.max(np.abs(freq_dev)):.3f} Hz\n")
                info_text.insert(tk.END, f"  Min Voltage: {np.min(voltage):.2f} kV\n\n")

                if is_stable:
                    info_text.insert(tk.END, "Status: STABLE ✓\n", 'stable')
                    info_text.tag_config('stable', foreground='green')
                else:
                    info_text.insert(tk.END, "Status: UNSTABLE ✗\n", 'unstable')
                    info_text.tag_config('unstable', foreground='red')

            except Exception as e:
                messagebox.showerror("Error", f"Simulation error: {str(e)}")

        start_btn = tk.Button(button_frame, text="Simulate", command=simulate,
                            bg='#27ae60', fg='white', font=('Arial', 10, 'bold'), width=15, height=2)
        start_btn.pack(pady=5)

        reset_btn = tk.Button(button_frame, text="Reset", command=lambda: [ax.clear() for ax in [ax1, ax2, ax3, ax4]] or canvas.draw(),
                            bg='#f39c12', fg='white', font=('Arial', 10, 'bold'), width=15)
        reset_btn.pack(pady=5)

        # Info panel
        info_frame = tk.LabelFrame(control_frame, text="System Info",
                                   font=('Arial', 10, 'bold'), bg='white', padx=10, pady=10)
        info_frame.grid(row=len(param_list)+3, column=0, columnspan=3, pady=10, sticky='ew')

        info_text = tk.Text(info_frame, height=16, width=35, font=('Courier', 8))
        info_text.pack()

        # Visualization frame
        viz_frame = tk.Frame(main_frame, bg='white')
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create matplotlib figure
        fig = Figure(figsize=(10, 8))
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)

        canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_window_resize(self, event):
        """Handle window resize events for auto-scaling"""
        # This will be called on resize, matplotlib canvas auto-adjusts
        pass


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ElectricalEngineeringLab(root)
    root.mainloop()


if __name__ == "__main__":
    main()
