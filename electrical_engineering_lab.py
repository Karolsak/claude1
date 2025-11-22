"""
Electrical Engineering Advanced Laboratory
Complete Python + Tkinter Application

Features:
- Tariff Calculation and Savings Analysis (with your specific problem)
- DC Motor Dynamic Simulation (RK45, Euler solvers)
- Synchronous Machine Simulator
- Real-time visualization with automatic scaling
- Professional UI with advanced controls
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.integrate import solve_ivp
import threading


class TariffCalculator(ttk.Frame):
    """Tariff Calculation and Analysis Module"""

    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = ttk.Label(self, text="Tariff Calculation & Savings Analysis",
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=3, pady=10)

        # Input Frame
        input_frame = ttk.LabelFrame(self, text="Input Parameters", padding=10)
        input_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Tariff parameters
        ttk.Label(input_frame, text="Fixed Charge (Rs/kVA/year):").grid(row=0, column=0, sticky='w', pady=5)
        self.fixed_charge = tk.DoubleVar(value=50.0)
        ttk.Entry(input_frame, textvariable=self.fixed_charge, width=15).grid(row=0, column=1, pady=5)

        ttk.Label(input_frame, text="Energy Charge (Paise/kWh):").grid(row=1, column=0, sticky='w', pady=5)
        self.energy_charge = tk.DoubleVar(value=10.0)
        ttk.Entry(input_frame, textvariable=self.energy_charge, width=15).grid(row=1, column=1, pady=5)

        ttk.Label(input_frame, text="Max Demand (kW):").grid(row=2, column=0, sticky='w', pady=5)
        self.max_demand = tk.DoubleVar(value=10.0)
        ttk.Entry(input_frame, textvariable=self.max_demand, width=15).grid(row=2, column=1, pady=5)

        ttk.Label(input_frame, text="Load Factor (%):").grid(row=3, column=0, sticky='w', pady=5)
        self.load_factor = tk.DoubleVar(value=60.0)
        ttk.Scale(input_frame, from_=10, to=100, variable=self.load_factor,
                 orient='horizontal', length=200).grid(row=3, column=1, pady=5)
        self.lf_label = ttk.Label(input_frame, text="60.0%")
        self.lf_label.grid(row=3, column=2, pady=5)
        self.load_factor.trace_add('write', lambda *args: self.lf_label.config(text=f"{self.load_factor.get():.1f}%"))

        ttk.Label(input_frame, text="Power Factor:").grid(row=4, column=0, sticky='w', pady=5)
        self.power_factor = tk.DoubleVar(value=0.8)
        ttk.Scale(input_frame, from_=0.5, to=1.0, variable=self.power_factor,
                 orient='horizontal', length=200).grid(row=4, column=1, pady=5)
        self.pf_label = ttk.Label(input_frame, text="0.80")
        self.pf_label.grid(row=4, column=2, pady=5)
        self.power_factor.trace_add('write', lambda *args: self.pf_label.config(text=f"{self.power_factor.get():.2f}"))

        # Improved parameters
        improved_frame = ttk.LabelFrame(self, text="Improved Conditions", padding=10)
        improved_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        ttk.Label(improved_frame, text="Improved Power Factor:").grid(row=0, column=0, sticky='w', pady=5)
        self.improved_pf = tk.DoubleVar(value=0.9)
        ttk.Scale(improved_frame, from_=0.5, to=1.0, variable=self.improved_pf,
                 orient='horizontal', length=200).grid(row=0, column=1, pady=5)
        self.ipf_label = ttk.Label(improved_frame, text="0.90")
        self.ipf_label.grid(row=0, column=2, pady=5)
        self.improved_pf.trace_add('write', lambda *args: self.ipf_label.config(text=f"{self.improved_pf.get():.2f}"))

        ttk.Label(improved_frame, text="Improved Load Factor (%):").grid(row=1, column=0, sticky='w', pady=5)
        self.improved_lf = tk.DoubleVar(value=80.0)
        ttk.Scale(improved_frame, from_=10, to=100, variable=self.improved_lf,
                 orient='horizontal', length=200).grid(row=1, column=1, pady=5)
        self.ilf_label = ttk.Label(improved_frame, text="80.0%")
        self.ilf_label.grid(row=1, column=2, pady=5)
        self.improved_lf.trace_add('write', lambda *args: self.ilf_label.config(text=f"{self.improved_lf.get():.1f}%"))

        # Calculate buttons
        button_frame = ttk.Frame(improved_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)

        ttk.Button(button_frame, text="Calculate Original Cost",
                  command=self.calculate_original).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Calculate PF Improvement Savings",
                  command=self.calculate_pf_improvement).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Calculate LF Improvement Effect",
                  command=self.calculate_lf_improvement).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Compare All",
                  command=self.compare_all).pack(side='left', padx=5)

        # Results Frame
        results_frame = ttk.LabelFrame(self, text="Results & Analysis", padding=10)
        results_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.results_text = tk.Text(results_frame, height=15, width=80, font=('Courier', 10))
        self.results_text.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.results_text.config(yscrollcommand=scrollbar.set)

        # Visualization Frame
        viz_frame = ttk.LabelFrame(self, text="Cost Comparison Visualization", padding=10)
        viz_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.fig = Figure(figsize=(10, 4), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Configure grid weights for resizing
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def calculate_tariff(self, max_demand_kw, load_factor, power_factor, fixed_charge, energy_charge):
        """Calculate annual tariff cost"""
        # Convert kW to kVA
        max_demand_kva = max_demand_kw / power_factor

        # Fixed cost (demand charge)
        fixed_cost = max_demand_kva * fixed_charge

        # Energy consumed per year
        # Load factor = Average demand / Max demand
        # Energy = Average demand * hours in year
        hours_per_year = 8760
        avg_demand_kw = (load_factor / 100.0) * max_demand_kw
        energy_kwh = avg_demand_kw * hours_per_year

        # Variable cost (energy charge) - convert paise to rupees
        variable_cost = energy_kwh * (energy_charge / 100.0)

        total_cost = fixed_cost + variable_cost
        cost_per_kwh = total_cost / energy_kwh if energy_kwh > 0 else 0

        return {
            'max_demand_kva': max_demand_kva,
            'fixed_cost': fixed_cost,
            'energy_kwh': energy_kwh,
            'variable_cost': variable_cost,
            'total_cost': total_cost,
            'cost_per_kwh': cost_per_kwh
        }

    def calculate_original(self):
        """Calculate original cost"""
        result = self.calculate_tariff(
            self.max_demand.get(),
            self.load_factor.get(),
            self.power_factor.get(),
            self.fixed_charge.get(),
            self.energy_charge.get()
        )

        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', "=" * 70 + "\n")
        self.results_text.insert(tk.END, "ORIGINAL TARIFF CALCULATION\n")
        self.results_text.insert(tk.END, "=" * 70 + "\n\n")
        self.results_text.insert(tk.END, f"Max Demand: {self.max_demand.get():.2f} kW\n")
        self.results_text.insert(tk.END, f"Power Factor: {self.power_factor.get():.2f} lag\n")
        self.results_text.insert(tk.END, f"Load Factor: {self.load_factor.get():.2f}%\n\n")
        self.results_text.insert(tk.END, f"Max Demand in kVA: {result['max_demand_kva']:.2f} kVA\n")
        self.results_text.insert(tk.END, f"Annual Energy Consumption: {result['energy_kwh']:.2f} kWh\n\n")
        self.results_text.insert(tk.END, f"Fixed Cost (Demand Charge): Rs. {result['fixed_cost']:.2f}\n")
        self.results_text.insert(tk.END, f"Variable Cost (Energy Charge): Rs. {result['variable_cost']:.2f}\n")
        self.results_text.insert(tk.END, f"TOTAL ANNUAL COST: Rs. {result['total_cost']:.2f}\n")
        self.results_text.insert(tk.END, f"Cost per kWh: Rs. {result['cost_per_kwh']:.4f}\n")

    def calculate_pf_improvement(self):
        """Calculate savings from power factor improvement"""
        original = self.calculate_tariff(
            self.max_demand.get(),
            self.load_factor.get(),
            self.power_factor.get(),
            self.fixed_charge.get(),
            self.energy_charge.get()
        )

        improved = self.calculate_tariff(
            self.max_demand.get(),
            self.load_factor.get(),
            self.improved_pf.get(),
            self.fixed_charge.get(),
            self.energy_charge.get()
        )

        savings = original['total_cost'] - improved['total_cost']
        savings_percent = (savings / original['total_cost']) * 100

        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', "=" * 70 + "\n")
        self.results_text.insert(tk.END, "POWER FACTOR IMPROVEMENT ANALYSIS\n")
        self.results_text.insert(tk.END, "=" * 70 + "\n\n")

        self.results_text.insert(tk.END, "ORIGINAL CONDITION:\n")
        self.results_text.insert(tk.END, f"  Power Factor: {self.power_factor.get():.2f} lag\n")
        self.results_text.insert(tk.END, f"  Max Demand: {original['max_demand_kva']:.2f} kVA\n")
        self.results_text.insert(tk.END, f"  Total Annual Cost: Rs. {original['total_cost']:.2f}\n\n")

        self.results_text.insert(tk.END, "IMPROVED CONDITION (PF improvement):\n")
        self.results_text.insert(tk.END, f"  Power Factor: {self.improved_pf.get():.2f} lag\n")
        self.results_text.insert(tk.END, f"  Max Demand: {improved['max_demand_kva']:.2f} kVA\n")
        self.results_text.insert(tk.END, f"  Total Annual Cost: Rs. {improved['total_cost']:.2f}\n\n")

        self.results_text.insert(tk.END, f"ANNUAL SAVINGS: Rs. {savings:.2f}\n")
        self.results_text.insert(tk.END, f"Savings Percentage: {savings_percent:.2f}%\n\n")

        self.results_text.insert(tk.END, "BREAKDOWN:\n")
        self.results_text.insert(tk.END, f"  Reduction in kVA demand: {original['max_demand_kva'] - improved['max_demand_kva']:.2f} kVA\n")
        self.results_text.insert(tk.END, f"  Fixed cost reduction: Rs. {original['fixed_cost'] - improved['fixed_cost']:.2f}\n")
        self.results_text.insert(tk.END, f"  Energy consumption: {improved['energy_kwh']:.2f} kWh (unchanged)\n")

    def calculate_lf_improvement(self):
        """Calculate effect of load factor improvement"""
        original = self.calculate_tariff(
            self.max_demand.get(),
            self.load_factor.get(),
            self.power_factor.get(),
            self.fixed_charge.get(),
            self.energy_charge.get()
        )

        improved = self.calculate_tariff(
            self.max_demand.get(),
            self.improved_lf.get(),
            self.power_factor.get(),
            self.fixed_charge.get(),
            self.energy_charge.get()
        )

        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', "=" * 70 + "\n")
        self.results_text.insert(tk.END, "LOAD FACTOR IMPROVEMENT ANALYSIS\n")
        self.results_text.insert(tk.END, "=" * 70 + "\n\n")

        self.results_text.insert(tk.END, "ORIGINAL CONDITION:\n")
        self.results_text.insert(tk.END, f"  Load Factor: {self.load_factor.get():.2f}%\n")
        self.results_text.insert(tk.END, f"  Energy Consumption: {original['energy_kwh']:.2f} kWh\n")
        self.results_text.insert(tk.END, f"  Total Annual Cost: Rs. {original['total_cost']:.2f}\n")
        self.results_text.insert(tk.END, f"  Cost per kWh: Rs. {original['cost_per_kwh']:.4f}\n\n")

        self.results_text.insert(tk.END, "IMPROVED CONDITION (LF improvement):\n")
        self.results_text.insert(tk.END, f"  Load Factor: {self.improved_lf.get():.2f}%\n")
        self.results_text.insert(tk.END, f"  Energy Consumption: {improved['energy_kwh']:.2f} kWh\n")
        self.results_text.insert(tk.END, f"  Total Annual Cost: Rs. {improved['total_cost']:.2f}\n")
        self.results_text.insert(tk.END, f"  Cost per kWh: Rs. {improved['cost_per_kwh']:.4f}\n\n")

        cost_reduction = original['cost_per_kwh'] - improved['cost_per_kwh']
        reduction_percent = (cost_reduction / original['cost_per_kwh']) * 100

        self.results_text.insert(tk.END, "EFFECT ON COST PER kWh:\n")
        self.results_text.insert(tk.END, f"  Reduction in cost per kWh: Rs. {cost_reduction:.4f}\n")
        self.results_text.insert(tk.END, f"  Percentage reduction: {reduction_percent:.2f}%\n\n")

        self.results_text.insert(tk.END, "EXPLANATION:\n")
        self.results_text.insert(tk.END, "  Improving load factor increases energy consumption (more utilization)\n")
        self.results_text.insert(tk.END, "  while keeping demand charge constant, thus reducing cost per kWh.\n")
        self.results_text.insert(tk.END, f"  Additional energy consumed: {improved['energy_kwh'] - original['energy_kwh']:.2f} kWh\n")
        self.results_text.insert(tk.END, f"  Additional cost: Rs. {improved['total_cost'] - original['total_cost']:.2f}\n")

    def compare_all(self):
        """Compare all scenarios"""
        original = self.calculate_tariff(
            self.max_demand.get(),
            self.load_factor.get(),
            self.power_factor.get(),
            self.fixed_charge.get(),
            self.energy_charge.get()
        )

        pf_improved = self.calculate_tariff(
            self.max_demand.get(),
            self.load_factor.get(),
            self.improved_pf.get(),
            self.fixed_charge.get(),
            self.energy_charge.get()
        )

        lf_improved = self.calculate_tariff(
            self.max_demand.get(),
            self.improved_lf.get(),
            self.power_factor.get(),
            self.fixed_charge.get(),
            self.energy_charge.get()
        )

        both_improved = self.calculate_tariff(
            self.max_demand.get(),
            self.improved_lf.get(),
            self.improved_pf.get(),
            self.fixed_charge.get(),
            self.energy_charge.get()
        )

        # Display results
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', "=" * 70 + "\n")
        self.results_text.insert(tk.END, "COMPREHENSIVE TARIFF COMPARISON\n")
        self.results_text.insert(tk.END, "=" * 70 + "\n\n")

        scenarios = [
            ("Original", original, self.power_factor.get(), self.load_factor.get()),
            ("PF Improved", pf_improved, self.improved_pf.get(), self.load_factor.get()),
            ("LF Improved", lf_improved, self.power_factor.get(), self.improved_lf.get()),
            ("Both Improved", both_improved, self.improved_pf.get(), self.improved_lf.get())
        ]

        for name, result, pf, lf in scenarios:
            self.results_text.insert(tk.END, f"{name}:\n")
            self.results_text.insert(tk.END, f"  PF: {pf:.2f}, LF: {lf:.2f}%\n")
            self.results_text.insert(tk.END, f"  Demand: {result['max_demand_kva']:.2f} kVA\n")
            self.results_text.insert(tk.END, f"  Energy: {result['energy_kwh']:.2f} kWh\n")
            self.results_text.insert(tk.END, f"  Total Cost: Rs. {result['total_cost']:.2f}\n")
            self.results_text.insert(tk.END, f"  Cost/kWh: Rs. {result['cost_per_kwh']:.4f}\n\n")

        # Savings
        self.results_text.insert(tk.END, "SAVINGS ANALYSIS:\n")
        self.results_text.insert(tk.END, f"  PF improvement only: Rs. {original['total_cost'] - pf_improved['total_cost']:.2f}\n")
        self.results_text.insert(tk.END, f"  LF improvement (cost increase): Rs. {lf_improved['total_cost'] - original['total_cost']:.2f}\n")
        self.results_text.insert(tk.END, f"  Both improvements: Rs. {original['total_cost'] - both_improved['total_cost']:.2f}\n")

        # Visualization
        self.fig.clear()

        # Plot 1: Total cost comparison
        ax1 = self.fig.add_subplot(1, 2, 1)
        names = ['Original', 'PF\nImproved', 'LF\nImproved', 'Both\nImproved']
        costs = [s[1]['total_cost'] for s in scenarios]
        colors = ['red', 'orange', 'yellow', 'green']
        bars = ax1.bar(names, costs, color=colors, alpha=0.7, edgecolor='black')
        ax1.set_ylabel('Total Annual Cost (Rs.)', fontweight='bold')
        ax1.set_title('Total Cost Comparison', fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'Rs. {height:.0f}',
                    ha='center', va='bottom', fontsize=9)

        # Plot 2: Cost per kWh comparison
        ax2 = self.fig.add_subplot(1, 2, 2)
        cost_per_kwh = [s[1]['cost_per_kwh'] for s in scenarios]
        bars = ax2.bar(names, cost_per_kwh, color=colors, alpha=0.7, edgecolor='black')
        ax2.set_ylabel('Cost per kWh (Rs.)', fontweight='bold')
        ax2.set_title('Unit Cost Comparison', fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}',
                    ha='center', va='bottom', fontsize=9)

        self.fig.tight_layout()
        self.canvas.draw()


class DCMotorSimulator(ttk.Frame):
    """DC Motor Dynamic Simulation with ODE Solvers"""

    def __init__(self, parent):
        super().__init__(parent)
        self.running = False
        self.simulation_data = None
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = ttk.Label(self, text="DC Motor Dynamic Simulation",
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Parameters Frame
        params_frame = ttk.LabelFrame(self, text="Motor Parameters", padding=10)
        params_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Motor parameters
        params = [
            ("Armature Resistance (Ra, Ω):", 0.5, 0.1, 5.0),
            ("Armature Inductance (La, H):", 0.05, 0.01, 0.5),
            ("Back EMF Constant (Ke, V·s/rad):", 0.1, 0.01, 1.0),
            ("Torque Constant (Kt, N·m/A):", 0.1, 0.01, 1.0),
            ("Moment of Inertia (J, kg·m²):", 0.01, 0.001, 0.1),
            ("Friction Coefficient (B, N·m·s/rad):", 0.001, 0.0001, 0.01),
            ("Applied Voltage (V):", 24.0, 0.0, 100.0),
            ("Load Torque (N·m):", 0.1, 0.0, 5.0)
        ]

        self.param_vars = {}
        for i, (label, default, min_val, max_val) in enumerate(params):
            ttk.Label(params_frame, text=label).grid(row=i, column=0, sticky='w', pady=3)
            var = tk.DoubleVar(value=default)
            self.param_vars[label.split('(')[0].strip()] = var

            scale = ttk.Scale(params_frame, from_=min_val, to=max_val, variable=var,
                            orient='horizontal', length=200)
            scale.grid(row=i, column=1, pady=3, padx=5)

            value_label = ttk.Label(params_frame, text=f"{default:.4f}")
            value_label.grid(row=i, column=2, pady=3)
            var.trace_add('write', lambda *args, v=var, l=value_label: l.config(text=f"{v.get():.4f}"))

        # Simulation Settings Frame
        settings_frame = ttk.LabelFrame(self, text="Simulation Settings", padding=10)
        settings_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        ttk.Label(settings_frame, text="ODE Solver:").grid(row=0, column=0, sticky='w', pady=5)
        self.solver_var = tk.StringVar(value="RK45")
        solvers = ["RK45", "Euler", "RK23", "DOP853"]
        solver_combo = ttk.Combobox(settings_frame, textvariable=self.solver_var,
                                   values=solvers, state='readonly', width=15)
        solver_combo.grid(row=0, column=1, pady=5)

        ttk.Label(settings_frame, text="Simulation Time (s):").grid(row=1, column=0, sticky='w', pady=5)
        self.sim_time = tk.DoubleVar(value=2.0)
        ttk.Scale(settings_frame, from_=0.5, to=10.0, variable=self.sim_time,
                 orient='horizontal', length=200).grid(row=1, column=1, pady=5)
        self.time_label = ttk.Label(settings_frame, text="2.0 s")
        self.time_label.grid(row=1, column=2, pady=5)
        self.sim_time.trace_add('write', lambda *args: self.time_label.config(text=f"{self.sim_time.get():.1f} s"))

        ttk.Label(settings_frame, text="Time Step (s):").grid(row=2, column=0, sticky='w', pady=5)
        self.time_step = tk.DoubleVar(value=0.001)
        ttk.Entry(settings_frame, textvariable=self.time_step, width=18).grid(row=2, column=1, pady=5)

        # Control Buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=15)

        self.start_btn = ttk.Button(button_frame, text="▶ Start", command=self.start_simulation)
        self.start_btn.pack(side='left', padx=5)

        self.stop_btn = ttk.Button(button_frame, text="■ Stop", command=self.stop_simulation, state='disabled')
        self.stop_btn.pack(side='left', padx=5)

        self.reset_btn = ttk.Button(button_frame, text="↺ Reset", command=self.reset_simulation)
        self.reset_btn.pack(side='left', padx=5)

        # Results Frame
        results_frame = ttk.LabelFrame(self, text="Simulation Results", padding=10)
        results_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Create matplotlib figure
        self.fig = Figure(figsize=(12, 6), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.fig, master=results_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Configure grid weights
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def dc_motor_ode(self, t, y, Ra, La, Ke, Kt, J, B, V, Tl):
        """
        DC Motor differential equations
        y[0] = ia (armature current)
        y[1] = omega (angular velocity)
        """
        ia, omega = y

        # dia/dt = (V - Ra*ia - Ke*omega) / La
        dia_dt = (V - Ra * ia - Ke * omega) / La

        # domega/dt = (Kt*ia - B*omega - Tl) / J
        domega_dt = (Kt * ia - B * omega - Tl) / J

        return [dia_dt, domega_dt]

    def euler_method(self, f, t_span, y0, dt, args):
        """Euler method for ODE solving"""
        t_start, t_end = t_span
        t = np.arange(t_start, t_end + dt, dt)
        y = np.zeros((len(t), len(y0)))
        y[0] = y0

        for i in range(1, len(t)):
            dydt = f(t[i-1], y[i-1], *args)
            y[i] = y[i-1] + np.array(dydt) * dt

        return t, y

    def start_simulation(self):
        """Start the simulation"""
        self.running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')

        # Run simulation in separate thread
        thread = threading.Thread(target=self.run_simulation)
        thread.daemon = True
        thread.start()

    def run_simulation(self):
        """Run the motor simulation"""
        # Get parameters
        Ra = self.param_vars["Armature Resistance"].get()
        La = self.param_vars["Armature Inductance"].get()
        Ke = self.param_vars["Back EMF Constant"].get()
        Kt = self.param_vars["Torque Constant"].get()
        J = self.param_vars["Moment of Inertia"].get()
        B = self.param_vars["Friction Coefficient"].get()
        V = self.param_vars["Applied Voltage"].get()
        Tl = self.param_vars["Load Torque"].get()

        # Initial conditions [ia, omega]
        y0 = [0.0, 0.0]

        # Time span
        t_span = (0, self.sim_time.get())
        dt = self.time_step.get()

        # Solve based on selected method
        solver = self.solver_var.get()

        try:
            if solver == "Euler":
                t, y = self.euler_method(
                    self.dc_motor_ode, t_span, y0, dt,
                    args=(Ra, La, Ke, Kt, J, B, V, Tl)
                )
                ia = y[:, 0]
                omega = y[:, 1]
            else:
                # Use scipy's solve_ivp
                sol = solve_ivp(
                    self.dc_motor_ode,
                    t_span,
                    y0,
                    method=solver,
                    args=(Ra, La, Ke, Kt, J, B, V, Tl),
                    dense_output=True,
                    max_step=dt
                )
                t = np.linspace(t_span[0], t_span[1], 1000)
                y = sol.sol(t)
                ia = y[0, :]
                omega = y[1, :]

            # Calculate derived quantities
            speed_rpm = omega * 60 / (2 * np.pi)  # Convert to RPM
            back_emf = Ke * omega
            torque = Kt * ia
            power = torque * omega

            # Store results
            self.simulation_data = {
                't': t,
                'ia': ia,
                'omega': omega,
                'speed_rpm': speed_rpm,
                'back_emf': back_emf,
                'torque': torque,
                'power': power
            }

            # Update plot
            self.after(0, self.update_plot)

        except Exception as e:
            messagebox.showerror("Simulation Error", f"Error during simulation: {str(e)}")

        finally:
            self.running = False
            self.after(0, lambda: self.start_btn.config(state='normal'))
            self.after(0, lambda: self.stop_btn.config(state='disabled'))

    def update_plot(self):
        """Update the visualization"""
        if self.simulation_data is None:
            return

        self.fig.clear()

        t = self.simulation_data['t']

        # Create subplots
        ax1 = self.fig.add_subplot(2, 2, 1)
        ax1.plot(t, self.simulation_data['speed_rpm'], 'b-', linewidth=2)
        ax1.set_xlabel('Time (s)', fontweight='bold')
        ax1.set_ylabel('Speed (RPM)', fontweight='bold')
        ax1.set_title('Motor Speed Response', fontweight='bold')
        ax1.grid(True, alpha=0.3)

        ax2 = self.fig.add_subplot(2, 2, 2)
        ax2.plot(t, self.simulation_data['ia'], 'r-', linewidth=2)
        ax2.set_xlabel('Time (s)', fontweight='bold')
        ax2.set_ylabel('Current (A)', fontweight='bold')
        ax2.set_title('Armature Current', fontweight='bold')
        ax2.grid(True, alpha=0.3)

        ax3 = self.fig.add_subplot(2, 2, 3)
        ax3.plot(t, self.simulation_data['torque'], 'g-', linewidth=2)
        ax3.set_xlabel('Time (s)', fontweight='bold')
        ax3.set_ylabel('Torque (N·m)', fontweight='bold')
        ax3.set_title('Motor Torque', fontweight='bold')
        ax3.grid(True, alpha=0.3)

        ax4 = self.fig.add_subplot(2, 2, 4)
        ax4.plot(t, self.simulation_data['power'], 'm-', linewidth=2)
        ax4.set_xlabel('Time (s)', fontweight='bold')
        ax4.set_ylabel('Power (W)', fontweight='bold')
        ax4.set_title('Mechanical Power', fontweight='bold')
        ax4.grid(True, alpha=0.3)

        self.fig.tight_layout()
        self.canvas.draw()

    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

    def reset_simulation(self):
        """Reset the simulation"""
        self.running = False
        self.simulation_data = None
        self.fig.clear()
        self.canvas.draw()
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')


class SynchronousMachineSimulator(ttk.Frame):
    """Synchronous Machine/Generator Simulator"""

    def __init__(self, parent):
        super().__init__(parent)
        self.running = False
        self.simulation_data = None
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = ttk.Label(self, text="Synchronous Machine Dynamic Simulator",
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Parameters Frame
        params_frame = ttk.LabelFrame(self, text="Machine Parameters", padding=10)
        params_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        params = [
            ("Rated Power (MVA):", 10.0, 1.0, 100.0),
            ("Rated Voltage (kV):", 11.0, 1.0, 50.0),
            ("Frequency (Hz):", 50.0, 50.0, 60.0),
            ("d-axis Reactance (Xd, pu):", 1.8, 0.5, 3.0),
            ("q-axis Reactance (Xq, pu):", 1.7, 0.5, 3.0),
            ("Inertia Constant (H, s):", 5.0, 1.0, 10.0),
            ("Damping Coefficient (D, pu):", 2.0, 0.5, 5.0),
            ("Excitation Voltage (Ef, pu):", 1.5, 0.5, 3.0)
        ]

        self.param_vars = {}
        for i, (label, default, min_val, max_val) in enumerate(params):
            ttk.Label(params_frame, text=label).grid(row=i, column=0, sticky='w', pady=3)
            var = tk.DoubleVar(value=default)
            self.param_vars[label.split('(')[0].strip()] = var

            scale = ttk.Scale(params_frame, from_=min_val, to=max_val, variable=var,
                            orient='horizontal', length=200)
            scale.grid(row=i, column=1, pady=3, padx=5)

            value_label = ttk.Label(params_frame, text=f"{default:.2f}")
            value_label.grid(row=i, column=2, pady=3)
            var.trace_add('write', lambda *args, v=var, l=value_label: l.config(text=f"{v.get():.2f}"))

        # Operating Conditions Frame
        conditions_frame = ttk.LabelFrame(self, text="Operating Conditions", padding=10)
        conditions_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        ttk.Label(conditions_frame, text="Initial Power Angle (deg):").grid(row=0, column=0, sticky='w', pady=5)
        self.delta0 = tk.DoubleVar(value=30.0)
        ttk.Scale(conditions_frame, from_=0.0, to=90.0, variable=self.delta0,
                 orient='horizontal', length=200).grid(row=0, column=1, pady=5)
        self.delta_label = ttk.Label(conditions_frame, text="30.0°")
        self.delta_label.grid(row=0, column=2, pady=5)
        self.delta0.trace_add('write', lambda *args: self.delta_label.config(text=f"{self.delta0.get():.1f}°"))

        ttk.Label(conditions_frame, text="Mechanical Power (pu):").grid(row=1, column=0, sticky='w', pady=5)
        self.pm = tk.DoubleVar(value=0.8)
        ttk.Scale(conditions_frame, from_=0.0, to=1.5, variable=self.pm,
                 orient='horizontal', length=200).grid(row=1, column=1, pady=5)
        self.pm_label = ttk.Label(conditions_frame, text="0.80")
        self.pm_label.grid(row=1, column=2, pady=5)
        self.pm.trace_add('write', lambda *args: self.pm_label.config(text=f"{self.pm.get():.2f}"))

        ttk.Label(conditions_frame, text="Fault/Disturbance:").grid(row=2, column=0, sticky='w', pady=5)
        self.fault_type = tk.StringVar(value="None")
        fault_combo = ttk.Combobox(conditions_frame, textvariable=self.fault_type,
                                  values=["None", "3-Phase Fault", "Load Change", "Voltage Dip"],
                                  state='readonly', width=15)
        fault_combo.grid(row=2, column=1, pady=5)

        ttk.Label(conditions_frame, text="Solver Method:").grid(row=3, column=0, sticky='w', pady=5)
        self.solver_var = tk.StringVar(value="RK45")
        solver_combo = ttk.Combobox(conditions_frame, textvariable=self.solver_var,
                                   values=["RK45", "Euler", "RK23"],
                                   state='readonly', width=15)
        solver_combo.grid(row=3, column=1, pady=5)

        # Control Buttons
        button_frame = ttk.Frame(conditions_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=15)

        self.start_btn = ttk.Button(button_frame, text="▶ Start", command=self.start_simulation)
        self.start_btn.pack(side='left', padx=5)

        self.stop_btn = ttk.Button(button_frame, text="■ Stop", command=self.stop_simulation, state='disabled')
        self.stop_btn.pack(side='left', padx=5)

        self.reset_btn = ttk.Button(button_frame, text="↺ Reset", command=self.reset_simulation)
        self.reset_btn.pack(side='left', padx=5)

        # Results Frame
        results_frame = ttk.LabelFrame(self, text="Transient Stability Analysis", padding=10)
        results_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.fig = Figure(figsize=(12, 6), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.fig, master=results_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Configure grid weights
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def sync_machine_ode(self, t, y, H, D, Pm, Ef, Xd, Xq, V, omega_s, fault_active):
        """
        Synchronous machine swing equation
        y[0] = delta (power angle in radians)
        y[1] = omega (angular velocity in rad/s)
        """
        delta, omega = y

        # Calculate electrical power
        if fault_active:
            Pe = 0  # During fault, electrical power is zero
        else:
            # Simplified power equation: Pe = (Ef * V / Xd) * sin(delta)
            Pe = (Ef * V / Xd) * np.sin(delta)

        # Swing equation
        # d(delta)/dt = omega - omega_s
        ddelta_dt = omega - omega_s

        # d(omega)/dt = (omega_s / (2*H)) * (Pm - Pe - D*(omega - omega_s))
        domega_dt = (omega_s / (2 * H)) * (Pm - Pe - D * (omega - omega_s))

        return [ddelta_dt, domega_dt]

    def euler_method(self, f, t_span, y0, dt, args_func):
        """Euler method with time-varying arguments"""
        t_start, t_end = t_span
        t = np.arange(t_start, t_end + dt, dt)
        y = np.zeros((len(t), len(y0)))
        y[0] = y0

        for i in range(1, len(t)):
            args = args_func(t[i-1])
            dydt = f(t[i-1], y[i-1], *args)
            y[i] = y[i-1] + np.array(dydt) * dt

        return t, y

    def start_simulation(self):
        """Start the simulation"""
        self.running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')

        thread = threading.Thread(target=self.run_simulation)
        thread.daemon = True
        thread.start()

    def run_simulation(self):
        """Run the synchronous machine simulation"""
        try:
            # Get parameters
            H = self.param_vars["Inertia Constant"].get()
            D = self.param_vars["Damping Coefficient"].get()
            Pm = self.pm.get()
            Ef = self.param_vars["Excitation Voltage"].get()
            Xd = self.param_vars["d-axis Reactance"].get()
            Xq = self.param_vars["q-axis Reactance"].get()
            freq = self.param_vars["Frequency"].get()
            V = 1.0  # Per unit voltage

            omega_s = 2 * np.pi * freq

            # Initial conditions
            delta0_rad = np.radians(self.delta0.get())
            omega0 = omega_s
            y0 = [delta0_rad, omega0]

            # Simulation time
            t_span = (0, 5.0)
            dt = 0.001

            # Determine fault timing
            fault_type = self.fault_type.get()
            fault_start = 1.0
            fault_end = 1.15

            # Create args function for time-varying fault
            def args_func(t):
                fault_active = (fault_type != "None" and fault_start <= t < fault_end)
                return (H, D, Pm, Ef, Xd, Xq, V, omega_s, fault_active)

            solver = self.solver_var.get()

            if solver == "Euler":
                t, y = self.euler_method(
                    self.sync_machine_ode, t_span, y0, dt, args_func
                )
                delta = y[:, 0]
                omega = y[:, 1]
            else:
                # For RK45, we need to handle time-varying fault differently
                t_eval = np.linspace(t_span[0], t_span[1], 5000)

                # Split into segments
                if fault_type != "None":
                    # Pre-fault
                    sol1 = solve_ivp(
                        self.sync_machine_ode,
                        (0, fault_start),
                        y0,
                        method=solver,
                        args=(H, D, Pm, Ef, Xd, Xq, V, omega_s, False),
                        dense_output=True
                    )

                    # During fault
                    sol2 = solve_ivp(
                        self.sync_machine_ode,
                        (fault_start, fault_end),
                        sol1.y[:, -1],
                        method=solver,
                        args=(H, D, Pm, Ef, Xd, Xq, V, omega_s, True),
                        dense_output=True
                    )

                    # Post-fault
                    sol3 = solve_ivp(
                        self.sync_machine_ode,
                        (fault_end, t_span[1]),
                        sol2.y[:, -1],
                        method=solver,
                        args=(H, D, Pm, Ef, Xd, Xq, V, omega_s, False),
                        dense_output=True
                    )

                    # Combine solutions
                    t1 = t_eval[t_eval < fault_start]
                    t2 = t_eval[(t_eval >= fault_start) & (t_eval < fault_end)]
                    t3 = t_eval[t_eval >= fault_end]

                    t = np.concatenate([t1, t2, t3])
                    y1 = sol1.sol(t1)
                    y2 = sol2.sol(t2)
                    y3 = sol3.sol(t3)

                    delta = np.concatenate([y1[0, :], y2[0, :], y3[0, :]])
                    omega = np.concatenate([y1[1, :], y2[1, :], y3[1, :]])
                else:
                    sol = solve_ivp(
                        self.sync_machine_ode,
                        t_span,
                        y0,
                        method=solver,
                        args=(H, D, Pm, Ef, Xd, Xq, V, omega_s, False),
                        dense_output=True
                    )
                    t = t_eval
                    y = sol.sol(t)
                    delta = y[0, :]
                    omega = y[1, :]

            # Calculate derived quantities
            delta_deg = np.degrees(delta)
            omega_pu = (omega - omega_s) / omega_s * 100  # Percentage deviation

            # Calculate electrical power
            Pe = np.zeros_like(t)
            for i, (ti, di) in enumerate(zip(t, delta)):
                fault_active = (fault_type != "None" and fault_start <= ti < fault_end)
                if not fault_active:
                    Pe[i] = (Ef * V / Xd) * np.sin(di)

            # Store results
            self.simulation_data = {
                't': t,
                'delta': delta_deg,
                'omega': omega_pu,
                'Pe': Pe,
                'Pm': Pm
            }

            self.after(0, self.update_plot)

        except Exception as e:
            messagebox.showerror("Simulation Error", f"Error: {str(e)}")

        finally:
            self.running = False
            self.after(0, lambda: self.start_btn.config(state='normal'))
            self.after(0, lambda: self.stop_btn.config(state='disabled'))

    def update_plot(self):
        """Update the visualization"""
        if self.simulation_data is None:
            return

        self.fig.clear()

        t = self.simulation_data['t']

        # Power angle
        ax1 = self.fig.add_subplot(2, 2, 1)
        ax1.plot(t, self.simulation_data['delta'], 'b-', linewidth=2)
        ax1.set_xlabel('Time (s)', fontweight='bold')
        ax1.set_ylabel('Power Angle (degrees)', fontweight='bold')
        ax1.set_title('Rotor Angle Swing', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=90, color='r', linestyle='--', alpha=0.5, label='Stability Limit')
        ax1.legend()

        # Speed deviation
        ax2 = self.fig.add_subplot(2, 2, 2)
        ax2.plot(t, self.simulation_data['omega'], 'r-', linewidth=2)
        ax2.set_xlabel('Time (s)', fontweight='bold')
        ax2.set_ylabel('Speed Deviation (%)', fontweight='bold')
        ax2.set_title('Rotor Speed Deviation', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)

        # Power
        ax3 = self.fig.add_subplot(2, 2, 3)
        ax3.plot(t, self.simulation_data['Pe'], 'g-', linewidth=2, label='Electrical Power')
        ax3.axhline(y=self.simulation_data['Pm'], color='orange', linestyle='--',
                   linewidth=2, label='Mechanical Power')
        ax3.set_xlabel('Time (s)', fontweight='bold')
        ax3.set_ylabel('Power (pu)', fontweight='bold')
        ax3.set_title('Power Balance', fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        # Phase plane (delta vs omega)
        ax4 = self.fig.add_subplot(2, 2, 4)
        ax4.plot(self.simulation_data['delta'], self.simulation_data['omega'], 'm-', linewidth=2)
        ax4.set_xlabel('Power Angle (degrees)', fontweight='bold')
        ax4.set_ylabel('Speed Deviation (%)', fontweight='bold')
        ax4.set_title('Phase Plane Trajectory', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        ax4.plot(self.simulation_data['delta'][0], self.simulation_data['omega'][0],
                'go', markersize=10, label='Start')
        ax4.plot(self.simulation_data['delta'][-1], self.simulation_data['omega'][-1],
                'ro', markersize=10, label='End')
        ax4.legend()

        self.fig.tight_layout()
        self.canvas.draw()

    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False

    def reset_simulation(self):
        """Reset the simulation"""
        self.running = False
        self.simulation_data = None
        self.fig.clear()
        self.canvas.draw()


class ElectricalEngineeringLab(tk.Tk):
    """Main Application Window"""

    def __init__(self):
        super().__init__()

        self.title("Electrical Engineering Advanced Laboratory")
        self.geometry("1200x800")

        # Configure window resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # Create tabs
        self.tariff_tab = TariffCalculator(self.notebook)
        self.notebook.add(self.tariff_tab, text="📊 Tariff Calculator")

        self.dc_motor_tab = DCMotorSimulator(self.notebook)
        self.notebook.add(self.dc_motor_tab, text="⚡ DC Motor Simulator")

        self.sync_machine_tab = SynchronousMachineSimulator(self.notebook)
        self.notebook.add(self.sync_machine_tab, text="🔄 Synchronous Machine")

        # Status bar
        self.status_bar = ttk.Label(self, text="Ready | Electrical Engineering Lab v2.0",
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky='ew')

        # Menu bar
        self.create_menu()

        # Bind resize event
        self.bind('<Configure>', self.on_resize)

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def show_about(self):
        """Show about dialog"""
        about_text = """
Electrical Engineering Advanced Laboratory
Version 2.0

Features:
• Tariff Calculation & Savings Analysis
• DC Motor Dynamic Simulation
• Synchronous Machine Transient Stability
• Multiple ODE Solvers (RK45, Euler, RK23, DOP853)
• Real-time Visualization
• Automatic Window Scaling

Developed for advanced electrical engineering education
        """
        messagebox.showinfo("About", about_text)

    def on_resize(self, event):
        """Handle window resize"""
        # Update status bar
        if event.widget == self:
            self.status_bar.config(text=f"Ready | Window: {self.winfo_width()}x{self.winfo_height()} | EE Lab v2.0")


def main():
    """Main entry point"""
    app = ElectricalEngineeringLab()
    app.mainloop()


if __name__ == "__main__":
    main()
