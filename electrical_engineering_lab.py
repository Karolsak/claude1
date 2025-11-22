#!/usr/bin/env python3
"""
Comprehensive Electrical Engineering Laboratory
Features:
- Two-Part Tariff Calculator (Solving specific electricity undertaking problem)
- Power System Dynamic Simulation
- Real-time ODE Solvers (RK45, Euler)
- Interactive Tkinter GUI with Auto-scaling
- Advanced Electrical Engineering Applications
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
from scipy.integrate import solve_ivp
from datetime import datetime


class ODESolver:
    """Custom ODE solvers for electrical engineering simulations"""

    @staticmethod
    def euler_method(func, t_span, y0, t_eval):
        """Euler's method for solving ODEs"""
        t0, tf = t_span
        t = np.array(t_eval)
        n = len(t)
        y = np.zeros((len(y0), n))
        y[:, 0] = y0

        for i in range(n - 1):
            dt = t[i + 1] - t[i]
            dydt = func(t[i], y[:, i])
            y[:, i + 1] = y[:, i] + dt * np.array(dydt)

        return t, y

    @staticmethod
    def rk45_method(func, t_span, y0, t_eval):
        """Runge-Kutta 45 method using scipy"""
        sol = solve_ivp(func, t_span, y0, method='RK45', t_eval=t_eval,
                       dense_output=True, rtol=1e-6, atol=1e-9)
        return sol.t, sol.y


class TwoPartTariffCalculator:
    """Calculate two-part tariff for electricity supply"""

    def __init__(self):
        self.max_load_mw = 100  # MW
        self.energy_generated_mkwh = 375  # Million kWh
        self.consumer_max_demand_mw = 165  # MW
        self.fuel_cost_lakhs = 30  # Rs. Lakhs
        self.fixed_gen_cost_lakhs = 40  # Rs. Lakhs
        self.fixed_td_cost_lakhs = 50  # Rs. Lakhs
        self.fuel_running_percent = 90  # 90% is running charges
        self.td_loss_percent = 15  # 15% transmission & distribution losses

    def calculate(self):
        """Calculate two-part tariff components"""
        # Energy delivered to consumers (after 15% loss)
        energy_delivered_mkwh = self.energy_generated_mkwh * (1 - self.td_loss_percent/100)
        energy_delivered_kwh = energy_delivered_mkwh * 1e6

        # Running charges (90% of fuel cost)
        running_charges = self.fuel_cost_lakhs * (self.fuel_running_percent/100) * 1e5  # Rs.

        # Fixed charges (10% of fuel + generation + T&D)
        fixed_fuel = self.fuel_cost_lakhs * (1 - self.fuel_running_percent/100) * 1e5
        fixed_generation = self.fixed_gen_cost_lakhs * 1e5
        fixed_td = self.fixed_td_cost_lakhs * 1e5
        total_fixed_charges = fixed_fuel + fixed_generation + fixed_td  # Rs.

        # Two-part tariff
        # 1. Fixed charge per kW of maximum demand per annum
        fixed_charge_per_kw = total_fixed_charges / (self.consumer_max_demand_mw * 1000)  # Rs/kW/annum

        # 2. Running charge per kWh
        running_charge_per_kwh = running_charges / energy_delivered_kwh  # Rs/kWh

        # Calculate load factor and capacity utilization
        avg_demand_mw = energy_delivered_mkwh / 8760  # MW (8760 hours/year)
        load_factor = (avg_demand_mw / self.consumer_max_demand_mw) * 100
        capacity_utilization = (self.max_load_mw / self.consumer_max_demand_mw) * 100

        return {
            'energy_generated_mkwh': self.energy_generated_mkwh,
            'energy_delivered_mkwh': energy_delivered_mkwh,
            'energy_delivered_kwh': energy_delivered_kwh,
            'running_charges': running_charges,
            'total_fixed_charges': total_fixed_charges,
            'fixed_charge_per_kw_annum': fixed_charge_per_kw,
            'fixed_charge_per_kw_month': fixed_charge_per_kw / 12,
            'running_charge_per_kwh': running_charge_per_kwh,
            'load_factor': load_factor,
            'capacity_utilization': capacity_utilization,
            'avg_demand_mw': avg_demand_mw
        }


class PowerSystemSimulator:
    """Simulate power system dynamics using differential equations"""

    def __init__(self):
        self.simulation_running = False
        self.simulation_data = None

    def swing_equation(self, t, y, P_m, P_e_max, D, H, omega_s):
        """
        Swing equation for synchronous generator
        y[0] = delta (rotor angle)
        y[1] = omega (angular velocity)
        """
        delta, omega = y

        # Electrical power (simplified)
        P_e = P_e_max * np.sin(delta)

        # Swing equation: H * d(omega)/dt = P_m - P_e - D*(omega - omega_s)
        d_omega_dt = (omega_s / (2 * H)) * (P_m - P_e - D * (omega - omega_s))
        d_delta_dt = omega - omega_s

        return [d_delta_dt, d_omega_dt]

    def rl_circuit(self, t, y, V, R, L):
        """
        RL circuit differential equation
        y[0] = current (i)
        """
        i = y[0]
        di_dt = (V - R * i) / L
        return [di_dt]

    def rc_circuit(self, t, y, V, R, C):
        """
        RC circuit differential equation
        y[0] = voltage across capacitor (Vc)
        """
        Vc = y[0]
        dVc_dt = (V - Vc) / (R * C)
        return [dVc_dt]

    def rlc_circuit(self, t, y, V, R, L, C):
        """
        RLC circuit differential equations
        y[0] = current (i)
        y[1] = voltage across capacitor (Vc)
        """
        i, Vc = y
        di_dt = (V - Vc - R * i) / L
        dVc_dt = i / C
        return [di_dt, dVc_dt]

    def induction_motor(self, t, y, V, Rs, Rr, Xs, Xr, Xm, TL, J, P):
        """
        Induction motor dynamic model
        y[0] = omega_r (rotor speed)
        y[1] = ids (d-axis stator current)
        y[2] = iqs (q-axis stator current)
        """
        omega_r, ids, iqs = y
        omega_s = 2 * np.pi * 50  # Synchronous speed (50 Hz)
        omega_slip = omega_s - omega_r

        # Simplified induction motor model
        # Electromagnetic torque
        Te = (3 * P / 2) * (Xm / (Xs + Xr)) * (V**2 * Rr / omega_slip) / \
             ((Rs + Rr/omega_slip)**2 + (Xs + Xr)**2)

        # Mechanical equation
        d_omega_r_dt = (P / (2 * J)) * (Te - TL)

        # Current dynamics (simplified)
        d_ids_dt = -ids / 0.1 + V * np.cos(omega_s * t) / (Rs + Xs)
        d_iqs_dt = -iqs / 0.1 + V * np.sin(omega_s * t) / (Rs + Xs)

        return [d_omega_r_dt, d_ids_dt, d_iqs_dt]


class ElectricalEngineeringLab:
    """Main application class for Electrical Engineering Laboratory"""

    def __init__(self, root):
        self.root = root
        self.root.title("Electrical Engineering Laboratory - Advanced Simulation Suite")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)

        # Initialize components
        self.tariff_calc = TwoPartTariffCalculator()
        self.power_sim = PowerSystemSimulator()
        self.ode_solver = ODESolver()

        # Simulation control
        self.simulation_running = False
        self.current_simulation = None

        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Bind resize event
        self.root.bind('<Configure>', self.on_window_resize)

        # Create UI
        self.create_main_menu()

    def create_main_menu(self):
        """Create main menu with module selection"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Title
        title = ttk.Label(self.main_container, text="Electrical Engineering Laboratory",
                         font=('Arial', 24, 'bold'))
        title.pack(pady=30)

        subtitle = ttk.Label(self.main_container,
                           text="Advanced Power System Analysis and Simulation Suite",
                           font=('Arial', 12))
        subtitle.pack(pady=10)

        # Button frame
        button_frame = ttk.Frame(self.main_container)
        button_frame.pack(pady=40)

        # Module buttons
        modules = [
            ("Two-Part Tariff Calculator", self.show_tariff_calculator),
            ("Power System Dynamics", self.show_power_system_dynamics),
            ("Circuit Analysis (RL/RC/RLC)", self.show_circuit_analysis),
            ("Induction Motor Simulation", self.show_induction_motor),
            ("Load Flow Analysis", self.show_load_flow),
            ("About", self.show_about)
        ]

        for i, (text, command) in enumerate(modules):
            btn = ttk.Button(button_frame, text=text, command=command, width=35)
            btn.grid(row=i, column=0, pady=10, padx=20)

        # Footer
        footer = ttk.Label(self.main_container,
                          text=f"Electrical Engineering Lab | Version 2.0",
                          font=('Arial', 9))
        footer.pack(side=tk.BOTTOM, pady=20)

    def create_back_button(self, parent):
        """Create back to main menu button"""
        back_btn = ttk.Button(parent, text="Back to Main Menu", command=self.create_main_menu)
        back_btn.pack(side=tk.BOTTOM, pady=10)
        return back_btn

    def show_tariff_calculator(self):
        """Show two-part tariff calculator module"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Title
        title = ttk.Label(self.main_container, text="Two-Part Tariff Calculator",
                         font=('Arial', 18, 'bold'))
        title.pack(pady=20)

        # Create notebook for inputs and results
        notebook = ttk.Notebook(self.main_container)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Input tab
        input_frame = ttk.Frame(notebook)
        notebook.add(input_frame, text="Input Parameters")

        # Create scrollable frame
        canvas = tk.Canvas(input_frame)
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Input fields
        self.tariff_inputs = {}
        inputs_config = [
            ("Maximum Load (MW)", "max_load_mw", 100),
            ("Energy Generated (Million kWh/annum)", "energy_generated_mkwh", 375),
            ("Consumer Max Demand (MW)", "consumer_max_demand_mw", 165),
            ("Fuel Cost (Rs. Lakhs)", "fuel_cost_lakhs", 30),
            ("Fixed Generation Cost (Rs. Lakhs)", "fixed_gen_cost_lakhs", 40),
            ("Fixed T&D Cost (Rs. Lakhs)", "fixed_td_cost_lakhs", 50),
            ("Fuel Running Charges (%)", "fuel_running_percent", 90),
            ("T&D Losses (%)", "td_loss_percent", 15)
        ]

        for i, (label, key, default) in enumerate(inputs_config):
            ttk.Label(scrollable_frame, text=label, font=('Arial', 10)).grid(
                row=i, column=0, sticky='w', padx=20, pady=10)

            var = tk.DoubleVar(value=default)
            entry = ttk.Entry(scrollable_frame, textvariable=var, width=20)
            entry.grid(row=i, column=1, padx=20, pady=10)
            self.tariff_inputs[key] = var

        # Calculate button
        calc_btn = ttk.Button(scrollable_frame, text="Calculate Tariff",
                             command=self.calculate_tariff)
        calc_btn.grid(row=len(inputs_config), column=0, columnspan=2, pady=20)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Results tab
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="Results & Analysis")

        self.tariff_results = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD,
                                                        font=('Courier', 10))
        self.tariff_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Visualization tab
        viz_frame = ttk.Frame(notebook)
        notebook.add(viz_frame, text="Visualization")

        self.tariff_figure = Figure(figsize=(12, 8))
        self.tariff_canvas = FigureCanvasTkAgg(self.tariff_figure, viz_frame)
        self.tariff_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Back button
        self.create_back_button(self.main_container)

        # Auto-calculate with default values
        self.calculate_tariff()

    def calculate_tariff(self):
        """Calculate and display tariff results"""
        # Update calculator with input values
        for key, var in self.tariff_inputs.items():
            setattr(self.tariff_calc, key, var.get())

        # Calculate
        results = self.tariff_calc.calculate()

        # Display results
        self.tariff_results.delete(1.0, tk.END)
        output = f"""
{'='*80}
                    TWO-PART TARIFF CALCULATION RESULTS
{'='*80}

INPUT PARAMETERS:
{'-'*80}
Maximum Load of Plant              : {self.tariff_calc.max_load_mw} MW
Energy Generated (Annual)          : {self.tariff_calc.energy_generated_mkwh} Million kWh
Consumer Maximum Demand            : {self.tariff_calc.consumer_max_demand_mw} MW
Fuel Cost                          : Rs. {self.tariff_calc.fuel_cost_lakhs} Lakhs
Fixed Generation Cost              : Rs. {self.tariff_calc.fixed_gen_cost_lakhs} Lakhs
Fixed T&D Cost                     : Rs. {self.tariff_calc.fixed_td_cost_lakhs} Lakhs
Fuel Running Charges               : {self.tariff_calc.fuel_running_percent}%
Transmission & Distribution Losses : {self.tariff_calc.td_loss_percent}%

ENERGY ANALYSIS:
{'-'*80}
Energy Generated                   : {results['energy_generated_mkwh']:.2f} Million kWh
Energy Delivered to Consumers      : {results['energy_delivered_mkwh']:.2f} Million kWh
Energy Loss in T&D                 : {results['energy_generated_mkwh'] - results['energy_delivered_mkwh']:.2f} Million kWh
Average Demand                     : {results['avg_demand_mw']:.2f} MW

COST BREAKDOWN:
{'-'*80}
Running Charges (Fuel)             : Rs. {results['running_charges']/1e5:.2f} Lakhs
Fixed Charges (Total)              : Rs. {results['total_fixed_charges']/1e5:.2f} Lakhs
  - Fixed Fuel (10%)               : Rs. {self.tariff_calc.fuel_cost_lakhs * 0.1:.2f} Lakhs
  - Fixed Generation               : Rs. {self.tariff_calc.fixed_gen_cost_lakhs:.2f} Lakhs
  - Fixed T&D                      : Rs. {self.tariff_calc.fixed_td_cost_lakhs:.2f} Lakhs
Total Annual Cost                  : Rs. {(results['running_charges'] + results['total_fixed_charges'])/1e5:.2f} Lakhs

TWO-PART TARIFF:
{'='*80}
1. FIXED CHARGE (Capacity Charge):
   - Per kW of Maximum Demand (Annual)  : Rs. {results['fixed_charge_per_kw_annum']:.2f} /kW/annum
   - Per kW of Maximum Demand (Monthly) : Rs. {results['fixed_charge_per_kw_month']:.2f} /kW/month

2. RUNNING CHARGE (Energy Charge):
   - Per kWh consumed                   : Rs. {results['running_charge_per_kwh']:.4f} /kWh
                                          : {results['running_charge_per_kwh']*100:.2f} paise/kWh

PERFORMANCE METRICS:
{'-'*80}
Load Factor                        : {results['load_factor']:.2f}%
Capacity Utilization               : {results['capacity_utilization']:.2f}%
Plant Utilization Factor           : {(results['avg_demand_mw']/self.tariff_calc.max_load_mw)*100:.2f}%

EXAMPLE BILL CALCULATION:
{'-'*80}
For a consumer with:
  - Maximum Demand: 1000 kW
  - Energy Consumption: 500,000 kWh/annum

Annual Bill Calculation:
  Fixed Charges  = 1000 kW × Rs. {results['fixed_charge_per_kw_annum']:.2f}
                 = Rs. {1000 * results['fixed_charge_per_kw_annum']:.2f}

  Running Charges = 500,000 kWh × Rs. {results['running_charge_per_kwh']:.4f}
                  = Rs. {500000 * results['running_charge_per_kwh']:.2f}

  Total Annual Bill = Rs. {1000 * results['fixed_charge_per_kw_annum'] + 500000 * results['running_charge_per_kwh']:.2f}
  Average Cost/kWh  = Rs. {(1000 * results['fixed_charge_per_kw_annum'] + 500000 * results['running_charge_per_kwh'])/500000:.4f} /kWh

{'='*80}
"""
        self.tariff_results.insert(1.0, output)

        # Visualize results
        self.visualize_tariff_results(results)

    def visualize_tariff_results(self, results):
        """Create visualization for tariff analysis"""
        self.tariff_figure.clear()

        # Create subplots
        gs = self.tariff_figure.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # 1. Cost Breakdown Pie Chart
        ax1 = self.tariff_figure.add_subplot(gs[0, 0])
        costs = [
            self.tariff_calc.fuel_cost_lakhs * 0.1,
            self.tariff_calc.fixed_gen_cost_lakhs,
            self.tariff_calc.fixed_td_cost_lakhs,
            self.tariff_calc.fuel_cost_lakhs * 0.9
        ]
        labels = ['Fixed Fuel\n(10%)', 'Fixed Gen', 'Fixed T&D', 'Running\n(90% Fuel)']
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        ax1.pie(costs, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Cost Distribution (Rs. Lakhs)', fontweight='bold')

        # 2. Energy Flow Sankey-style
        ax2 = self.tariff_figure.add_subplot(gs[0, 1])
        categories = ['Generated', 'T&D Loss', 'Delivered']
        values = [
            results['energy_generated_mkwh'],
            results['energy_generated_mkwh'] - results['energy_delivered_mkwh'],
            results['energy_delivered_mkwh']
        ]
        colors_bar = ['#3498db', '#e74c3c', '#2ecc71']
        bars = ax2.bar(categories, values, color=colors_bar, alpha=0.7, edgecolor='black')
        ax2.set_ylabel('Energy (Million kWh)', fontweight='bold')
        ax2.set_title('Energy Flow Analysis', fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontweight='bold')

        # 3. Load Analysis
        ax3 = self.tariff_figure.add_subplot(gs[1, 0])
        load_metrics = ['Plant\nCapacity', 'Avg\nDemand', 'Max\nDemand']
        load_values = [
            self.tariff_calc.max_load_mw,
            results['avg_demand_mw'],
            self.tariff_calc.consumer_max_demand_mw
        ]
        colors_load = ['#9b59b6', '#f39c12', '#e74c3c']
        bars2 = ax3.bar(load_metrics, load_values, color=colors_load, alpha=0.7, edgecolor='black')
        ax3.set_ylabel('Power (MW)', fontweight='bold')
        ax3.set_title('Load Analysis', fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)

        for bar in bars2:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f} MW',
                    ha='center', va='bottom', fontweight='bold', fontsize=9)

        # 4. Tariff Components
        ax4 = self.tariff_figure.add_subplot(gs[1, 1])

        # Show tariff breakdown for different demand levels
        demands = np.array([100, 500, 1000, 2000, 5000])  # kW
        energy_consumed = demands * 1000  # kWh (assuming 1000 hours usage)

        fixed_charges = demands * results['fixed_charge_per_kw_annum']
        running_charges = energy_consumed * results['running_charge_per_kwh']

        x = np.arange(len(demands))
        width = 0.35

        bars3 = ax4.bar(x - width/2, fixed_charges, width, label='Fixed Charge',
                       color='#3498db', alpha=0.7, edgecolor='black')
        bars4 = ax4.bar(x + width/2, running_charges, width, label='Running Charge',
                       color='#e67e22', alpha=0.7, edgecolor='black')

        ax4.set_xlabel('Maximum Demand (kW)', fontweight='bold')
        ax4.set_ylabel('Annual Cost (Rs.)', fontweight='bold')
        ax4.set_title('Tariff Breakdown by Demand Level', fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels(demands)
        ax4.legend()
        ax4.grid(axis='y', alpha=0.3)

        self.tariff_canvas.draw()

    def show_power_system_dynamics(self):
        """Show power system dynamics simulation"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Title
        title = ttk.Label(self.main_container, text="Power System Dynamics - Swing Equation",
                         font=('Arial', 18, 'bold'))
        title.pack(pady=10)

        # Create main frame with grid
        main_frame = ttk.Frame(self.main_container)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="Simulation Parameters", padding=10)
        control_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # Parameters
        self.ps_params = {}
        params_config = [
            ("Mechanical Power Pm (pu)", "P_m", 1.0, 0.1, 2.0),
            ("Max Electrical Power Pe (pu)", "P_e_max", 1.5, 0.5, 3.0),
            ("Damping Coefficient D", "D", 0.1, 0.0, 1.0),
            ("Inertia Constant H (s)", "H", 3.0, 1.0, 10.0),
            ("Initial Angle delta0 (deg)", "delta_0", 30, 0, 90),
            ("Simulation Time (s)", "t_max", 10, 1, 30)
        ]

        for i, (label, key, default, min_val, max_val) in enumerate(params_config):
            ttk.Label(control_frame, text=label).grid(row=i, column=0, sticky='w', pady=5)

            var = tk.DoubleVar(value=default)
            scale = ttk.Scale(control_frame, from_=min_val, to=max_val, variable=var,
                            orient='horizontal', length=200)
            scale.grid(row=i, column=1, padx=5, pady=5)

            value_label = ttk.Label(control_frame, text=f"{default:.2f}")
            value_label.grid(row=i, column=2, padx=5)

            var.trace_add('write', lambda *args, v=var, l=value_label:
                         l.config(text=f"{v.get():.2f}"))

            self.ps_params[key] = var

        # Solver selection
        ttk.Label(control_frame, text="ODE Solver:").grid(row=len(params_config),
                                                          column=0, sticky='w', pady=5)
        self.ps_solver_var = tk.StringVar(value="RK45")
        solver_combo = ttk.Combobox(control_frame, textvariable=self.ps_solver_var,
                                    values=["Euler", "RK45"], state='readonly', width=18)
        solver_combo.grid(row=len(params_config), column=1, pady=5)

        # Control buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=len(params_config)+1, column=0, columnspan=3, pady=20)

        self.ps_start_btn = ttk.Button(btn_frame, text="Start", command=self.start_ps_simulation)
        self.ps_start_btn.pack(side=tk.LEFT, padx=5)

        self.ps_stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_ps_simulation,
                                      state='disabled')
        self.ps_stop_btn.pack(side=tk.LEFT, padx=5)

        self.ps_reset_btn = ttk.Button(btn_frame, text="Reset", command=self.reset_ps_simulation)
        self.ps_reset_btn.pack(side=tk.LEFT, padx=5)

        # Right panel - Visualization
        viz_frame = ttk.LabelFrame(main_frame, text="Real-time Visualization", padding=10)
        viz_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        self.ps_figure = Figure(figsize=(10, 8))
        self.ps_canvas = FigureCanvasTkAgg(self.ps_figure, viz_frame)
        self.ps_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Configure grid weights
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)

        # Back button
        self.create_back_button(self.main_container)

    def start_ps_simulation(self):
        """Start power system simulation"""
        self.ps_start_btn.config(state='disabled')
        self.ps_stop_btn.config(state='normal')
        self.simulation_running = True

        # Get parameters
        P_m = self.ps_params['P_m'].get()
        P_e_max = self.ps_params['P_e_max'].get()
        D = self.ps_params['D'].get()
        H = self.ps_params['H'].get()
        delta_0 = np.radians(self.ps_params['delta_0'].get())
        t_max = self.ps_params['t_max'].get()

        omega_s = 2 * np.pi * 50  # 50 Hz
        y0 = [delta_0, omega_s]
        t_span = (0, t_max)
        t_eval = np.linspace(0, t_max, 1000)

        # Define system function
        def system(t, y):
            return self.power_sim.swing_equation(t, y, P_m, P_e_max, D, H, omega_s)

        # Solve based on selected method
        if self.ps_solver_var.get() == "Euler":
            t, y = self.ode_solver.euler_method(system, t_span, y0, t_eval)
        else:
            t, y = self.ode_solver.rk45_method(system, t_span, y0, t_eval)

        # Plot results
        self.plot_ps_results(t, y, omega_s, P_m, P_e_max)

        self.simulation_running = False
        self.ps_start_btn.config(state='normal')
        self.ps_stop_btn.config(state='disabled')

    def stop_ps_simulation(self):
        """Stop power system simulation"""
        self.simulation_running = False
        self.ps_start_btn.config(state='normal')
        self.ps_stop_btn.config(state='disabled')

    def reset_ps_simulation(self):
        """Reset power system simulation"""
        self.ps_figure.clear()
        self.ps_canvas.draw()

    def plot_ps_results(self, t, y, omega_s, P_m, P_e_max):
        """Plot power system simulation results"""
        self.ps_figure.clear()

        delta = y[0, :]
        omega = y[1, :]

        # Calculate electrical power
        P_e = P_e_max * np.sin(delta)

        # Create subplots
        ax1 = self.ps_figure.add_subplot(3, 1, 1)
        ax1.plot(t, np.degrees(delta), 'b-', linewidth=2, label='Rotor Angle delta')
        ax1.set_ylabel('Rotor Angle (degrees)', fontweight='bold')
        ax1.set_title(f'Power System Dynamics - {self.ps_solver_var.get()} Method',
                     fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        ax2 = self.ps_figure.add_subplot(3, 1, 2)
        ax2.plot(t, omega, 'r-', linewidth=2, label='Rotor Speed omega')
        ax2.axhline(y=omega_s, color='g', linestyle='--', label='Synchronous Speed')
        ax2.set_ylabel('Angular Velocity (rad/s)', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        ax3 = self.ps_figure.add_subplot(3, 1, 3)
        ax3.plot(t, P_e, 'b-', linewidth=2, label='Electrical Power Pe')
        ax3.axhline(y=P_m, color='g', linestyle='--', label='Mechanical Power Pm')
        ax3.set_xlabel('Time (s)', fontweight='bold')
        ax3.set_ylabel('Power (pu)', fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        self.ps_figure.tight_layout()
        self.ps_canvas.draw()

    def show_circuit_analysis(self):
        """Show circuit analysis module (RL, RC, RLC)"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Title
        title = ttk.Label(self.main_container, text="Circuit Analysis - Transient Response",
                         font=('Arial', 18, 'bold'))
        title.pack(pady=10)

        # Create notebook for different circuits
        notebook = ttk.Notebook(self.main_container)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # RL Circuit Tab
        self.create_rl_circuit_tab(notebook)

        # RC Circuit Tab
        self.create_rc_circuit_tab(notebook)

        # RLC Circuit Tab
        self.create_rlc_circuit_tab(notebook)

        # Back button
        self.create_back_button(self.main_container)

    def create_rl_circuit_tab(self, notebook):
        """Create RL circuit analysis tab"""
        rl_frame = ttk.Frame(notebook)
        notebook.add(rl_frame, text="RL Circuit")

        # Split into control and visualization
        control_frame = ttk.LabelFrame(rl_frame, text="Circuit Parameters", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Parameters
        self.rl_params = {}
        rl_config = [
            ("Voltage V (V)", "V", 10, 1, 50),
            ("Resistance R (Ohm)", "R", 10, 1, 100),
            ("Inductance L (H)", "L", 1, 0.1, 10),
            ("Simulation Time (s)", "t_max", 2, 0.5, 10)
        ]

        for i, (label, key, default, min_val, max_val) in enumerate(rl_config):
            ttk.Label(control_frame, text=label).grid(row=i, column=0, sticky='w', pady=5)

            var = tk.DoubleVar(value=default)
            scale = ttk.Scale(control_frame, from_=min_val, to=max_val, variable=var,
                            orient='horizontal', length=200)
            scale.grid(row=i, column=1, padx=5, pady=5)

            value_label = ttk.Label(control_frame, text=f"{default:.2f}")
            value_label.grid(row=i, column=2, padx=5)

            var.trace_add('write', lambda *args, v=var, l=value_label:
                         l.config(text=f"{v.get():.2f}"))

            self.rl_params[key] = var

        # Solver
        ttk.Label(control_frame, text="ODE Solver:").grid(row=len(rl_config),
                                                          column=0, sticky='w', pady=5)
        self.rl_solver_var = tk.StringVar(value="RK45")
        ttk.Combobox(control_frame, textvariable=self.rl_solver_var,
                    values=["Euler", "RK45"], state='readonly', width=18).grid(
                        row=len(rl_config), column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=len(rl_config)+1, column=0, columnspan=3, pady=20)

        ttk.Button(btn_frame, text="Simulate", command=self.simulate_rl).pack(pady=5)
        ttk.Button(btn_frame, text="Reset", command=self.reset_rl).pack(pady=5)

        # Visualization
        viz_frame = ttk.Frame(rl_frame)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.rl_figure = Figure(figsize=(10, 8))
        self.rl_canvas = FigureCanvasTkAgg(self.rl_figure, viz_frame)
        self.rl_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def simulate_rl(self):
        """Simulate RL circuit"""
        V = self.rl_params['V'].get()
        R = self.rl_params['R'].get()
        L = self.rl_params['L'].get()
        t_max = self.rl_params['t_max'].get()

        y0 = [0]  # Initial current
        t_span = (0, t_max)
        t_eval = np.linspace(0, t_max, 1000)

        def system(t, y):
            return self.power_sim.rl_circuit(t, y, V, R, L)

        if self.rl_solver_var.get() == "Euler":
            t, y = self.ode_solver.euler_method(system, t_span, y0, t_eval)
        else:
            t, y = self.ode_solver.rk45_method(system, t_span, y0, t_eval)

        # Analytical solution
        tau = L / R
        i_analytical = (V / R) * (1 - np.exp(-t / tau))

        # Plot
        self.rl_figure.clear()
        ax = self.rl_figure.add_subplot(111)
        ax.plot(t, y[0, :], 'b-', linewidth=2, label=f'{self.rl_solver_var.get()} Method')
        ax.plot(t, i_analytical, 'r--', linewidth=1.5, label='Analytical Solution')
        ax.axhline(y=V/R, color='g', linestyle=':', label='Steady State (V/R)')
        ax.axvline(x=tau, color='orange', linestyle=':', label=f'Time Constant tau={tau:.3f}s')
        ax.set_xlabel('Time (s)', fontweight='bold')
        ax.set_ylabel('Current (A)', fontweight='bold')
        ax.set_title(f'RL Circuit Transient Response\nV={V}V, R={R}Ohm, L={L}H',
                    fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

        self.rl_figure.tight_layout()
        self.rl_canvas.draw()

    def reset_rl(self):
        """Reset RL circuit"""
        self.rl_figure.clear()
        self.rl_canvas.draw()

    def create_rc_circuit_tab(self, notebook):
        """Create RC circuit analysis tab"""
        rc_frame = ttk.Frame(notebook)
        notebook.add(rc_frame, text="RC Circuit")

        # Split into control and visualization
        control_frame = ttk.LabelFrame(rc_frame, text="Circuit Parameters", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Parameters
        self.rc_params = {}
        rc_config = [
            ("Voltage V (V)", "V", 10, 1, 50),
            ("Resistance R (Ohm)", "R", 1000, 100, 10000),
            ("Capacitance C (uF)", "C", 100, 10, 1000),
            ("Simulation Time (s)", "t_max", 1, 0.1, 5)
        ]

        for i, (label, key, default, min_val, max_val) in enumerate(rc_config):
            ttk.Label(control_frame, text=label).grid(row=i, column=0, sticky='w', pady=5)

            var = tk.DoubleVar(value=default)
            scale = ttk.Scale(control_frame, from_=min_val, to=max_val, variable=var,
                            orient='horizontal', length=200)
            scale.grid(row=i, column=1, padx=5, pady=5)

            value_label = ttk.Label(control_frame, text=f"{default:.2f}")
            value_label.grid(row=i, column=2, padx=5)

            var.trace_add('write', lambda *args, v=var, l=value_label:
                         l.config(text=f"{v.get():.2f}"))

            self.rc_params[key] = var

        # Solver
        ttk.Label(control_frame, text="ODE Solver:").grid(row=len(rc_config),
                                                          column=0, sticky='w', pady=5)
        self.rc_solver_var = tk.StringVar(value="RK45")
        ttk.Combobox(control_frame, textvariable=self.rc_solver_var,
                    values=["Euler", "RK45"], state='readonly', width=18).grid(
                        row=len(rc_config), column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=len(rc_config)+1, column=0, columnspan=3, pady=20)

        ttk.Button(btn_frame, text="Simulate", command=self.simulate_rc).pack(pady=5)
        ttk.Button(btn_frame, text="Reset", command=self.reset_rc).pack(pady=5)

        # Visualization
        viz_frame = ttk.Frame(rc_frame)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.rc_figure = Figure(figsize=(10, 8))
        self.rc_canvas = FigureCanvasTkAgg(self.rc_figure, viz_frame)
        self.rc_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def simulate_rc(self):
        """Simulate RC circuit"""
        V = self.rc_params['V'].get()
        R = self.rc_params['R'].get()
        C = self.rc_params['C'].get() * 1e-6  # Convert uF to F
        t_max = self.rc_params['t_max'].get()

        y0 = [0]  # Initial voltage across capacitor
        t_span = (0, t_max)
        t_eval = np.linspace(0, t_max, 1000)

        def system(t, y):
            return self.power_sim.rc_circuit(t, y, V, R, C)

        if self.rc_solver_var.get() == "Euler":
            t, y = self.ode_solver.euler_method(system, t_span, y0, t_eval)
        else:
            t, y = self.ode_solver.rk45_method(system, t_span, y0, t_eval)

        # Analytical solution
        tau = R * C
        Vc_analytical = V * (1 - np.exp(-t / tau))

        # Plot
        self.rc_figure.clear()
        ax = self.rc_figure.add_subplot(111)
        ax.plot(t, y[0, :], 'b-', linewidth=2, label=f'{self.rc_solver_var.get()} Method')
        ax.plot(t, Vc_analytical, 'r--', linewidth=1.5, label='Analytical Solution')
        ax.axhline(y=V, color='g', linestyle=':', label=f'Steady State ({V}V)')
        ax.axvline(x=tau, color='orange', linestyle=':', label=f'Time Constant tau={tau:.6f}s')
        ax.set_xlabel('Time (s)', fontweight='bold')
        ax.set_ylabel('Capacitor Voltage (V)', fontweight='bold')
        ax.set_title(f'RC Circuit Transient Response\nV={V}V, R={R}Ohm, C={self.rc_params["C"].get()}uF',
                    fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

        self.rc_figure.tight_layout()
        self.rc_canvas.draw()

    def reset_rc(self):
        """Reset RC circuit"""
        self.rc_figure.clear()
        self.rc_canvas.draw()

    def create_rlc_circuit_tab(self, notebook):
        """Create RLC circuit analysis tab"""
        rlc_frame = ttk.Frame(notebook)
        notebook.add(rlc_frame, text="RLC Circuit")

        # Split into control and visualization
        control_frame = ttk.LabelFrame(rlc_frame, text="Circuit Parameters", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Parameters
        self.rlc_params = {}
        rlc_config = [
            ("Voltage V (V)", "V", 10, 1, 50),
            ("Resistance R (Ohm)", "R", 10, 1, 100),
            ("Inductance L (H)", "L", 0.1, 0.01, 1),
            ("Capacitance C (uF)", "C", 100, 10, 1000),
            ("Simulation Time (s)", "t_max", 1, 0.1, 5)
        ]

        for i, (label, key, default, min_val, max_val) in enumerate(rlc_config):
            ttk.Label(control_frame, text=label).grid(row=i, column=0, sticky='w', pady=5)

            var = tk.DoubleVar(value=default)
            scale = ttk.Scale(control_frame, from_=min_val, to=max_val, variable=var,
                            orient='horizontal', length=200)
            scale.grid(row=i, column=1, padx=5, pady=5)

            value_label = ttk.Label(control_frame, text=f"{default:.2f}")
            value_label.grid(row=i, column=2, padx=5)

            var.trace_add('write', lambda *args, v=var, l=value_label:
                         l.config(text=f"{v.get():.2f}"))

            self.rlc_params[key] = var

        # Solver
        ttk.Label(control_frame, text="ODE Solver:").grid(row=len(rlc_config),
                                                          column=0, sticky='w', pady=5)
        self.rlc_solver_var = tk.StringVar(value="RK45")
        ttk.Combobox(control_frame, textvariable=self.rlc_solver_var,
                    values=["Euler", "RK45"], state='readonly', width=18).grid(
                        row=len(rlc_config), column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=len(rlc_config)+1, column=0, columnspan=3, pady=20)

        ttk.Button(btn_frame, text="Simulate", command=self.simulate_rlc).pack(pady=5)
        ttk.Button(btn_frame, text="Reset", command=self.reset_rlc).pack(pady=5)

        # Visualization
        viz_frame = ttk.Frame(rlc_frame)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.rlc_figure = Figure(figsize=(10, 8))
        self.rlc_canvas = FigureCanvasTkAgg(self.rlc_figure, viz_frame)
        self.rlc_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def simulate_rlc(self):
        """Simulate RLC circuit"""
        V = self.rlc_params['V'].get()
        R = self.rlc_params['R'].get()
        L = self.rlc_params['L'].get()
        C = self.rlc_params['C'].get() * 1e-6  # Convert uF to F
        t_max = self.rlc_params['t_max'].get()

        y0 = [0, 0]  # Initial current and capacitor voltage
        t_span = (0, t_max)
        t_eval = np.linspace(0, t_max, 1000)

        def system(t, y):
            return self.power_sim.rlc_circuit(t, y, V, R, L, C)

        if self.rlc_solver_var.get() == "Euler":
            t, y = self.ode_solver.euler_method(system, t_span, y0, t_eval)
        else:
            t, y = self.ode_solver.rk45_method(system, t_span, y0, t_eval)

        current = y[0, :]
        voltage = y[1, :]

        # Calculate damping ratio and natural frequency
        omega_n = 1 / np.sqrt(L * C)
        zeta = R / 2 * np.sqrt(C / L)

        # Plot
        self.rlc_figure.clear()

        ax1 = self.rlc_figure.add_subplot(2, 1, 1)
        ax1.plot(t, current, 'b-', linewidth=2, label='Current')
        ax1.set_ylabel('Current (A)', fontweight='bold')
        ax1.set_title(f'RLC Circuit Response (zeta={zeta:.3f}, omega_n={omega_n:.2f} rad/s)',
                     fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        ax2 = self.rlc_figure.add_subplot(2, 1, 2)
        ax2.plot(t, voltage, 'r-', linewidth=2, label='Capacitor Voltage')
        ax2.axhline(y=V, color='g', linestyle=':', label=f'Source Voltage ({V}V)')
        ax2.set_xlabel('Time (s)', fontweight='bold')
        ax2.set_ylabel('Voltage (V)', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        # Add damping classification
        if zeta < 1:
            damping_type = "Underdamped"
        elif zeta == 1:
            damping_type = "Critically Damped"
        else:
            damping_type = "Overdamped"

        ax1.text(0.02, 0.98, f'Damping: {damping_type}',
                transform=ax1.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        self.rlc_figure.tight_layout()
        self.rlc_canvas.draw()

    def reset_rlc(self):
        """Reset RLC circuit"""
        self.rlc_figure.clear()
        self.rlc_canvas.draw()

    def show_induction_motor(self):
        """Show induction motor simulation"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Title
        title = ttk.Label(self.main_container, text="Three-Phase Induction Motor Simulation",
                         font=('Arial', 18, 'bold'))
        title.pack(pady=10)

        # Info label
        info = ttk.Label(self.main_container,
                        text="Dynamic simulation of induction motor starting transient",
                        font=('Arial', 10, 'italic'))
        info.pack(pady=5)

        # Create main frame
        main_frame = ttk.Frame(self.main_container)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Motor Parameters", padding=10)
        control_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.im_params = {}
        im_config = [
            ("Voltage V (V)", "V", 400, 100, 1000),
            ("Stator Resistance Rs (Ohm)", "Rs", 0.5, 0.1, 5),
            ("Rotor Resistance Rr (Ohm)", "Rr", 0.3, 0.1, 5),
            ("Stator Reactance Xs (Ohm)", "Xs", 2.0, 0.5, 10),
            ("Rotor Reactance Xr (Ohm)", "Xr", 2.0, 0.5, 10),
            ("Magnetizing Reactance Xm (Ohm)", "Xm", 50, 10, 100),
            ("Load Torque TL (Nm)", "TL", 50, 0, 200),
            ("Inertia J (kg·m^2)", "J", 0.5, 0.1, 5),
            ("Poles P", "P", 4, 2, 8),
            ("Simulation Time (s)", "t_max", 3, 1, 10)
        ]

        for i, (label, key, default, min_val, max_val) in enumerate(im_config):
            ttk.Label(control_frame, text=label).grid(row=i, column=0, sticky='w', pady=3)

            var = tk.DoubleVar(value=default)
            scale = ttk.Scale(control_frame, from_=min_val, to=max_val, variable=var,
                            orient='horizontal', length=180)
            scale.grid(row=i, column=1, padx=5, pady=3)

            value_label = ttk.Label(control_frame, text=f"{default:.2f}")
            value_label.grid(row=i, column=2, padx=5)

            var.trace_add('write', lambda *args, v=var, l=value_label:
                         l.config(text=f"{v.get():.2f}"))

            self.im_params[key] = var

        # Solver
        ttk.Label(control_frame, text="ODE Solver:").grid(row=len(im_config),
                                                          column=0, sticky='w', pady=5)
        self.im_solver_var = tk.StringVar(value="RK45")
        ttk.Combobox(control_frame, textvariable=self.im_solver_var,
                    values=["Euler", "RK45"], state='readonly', width=15).grid(
                        row=len(im_config), column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=len(im_config)+1, column=0, columnspan=3, pady=15)

        ttk.Button(btn_frame, text="Start Motor", command=self.simulate_induction_motor).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.reset_induction_motor).pack(side=tk.LEFT, padx=5)

        # Visualization panel
        viz_frame = ttk.LabelFrame(main_frame, text="Motor Performance Characteristics", padding=10)
        viz_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        self.im_figure = Figure(figsize=(11, 9))
        self.im_canvas = FigureCanvasTkAgg(self.im_figure, viz_frame)
        self.im_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Configure grid
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)

        # Back button
        self.create_back_button(self.main_container)

    def simulate_induction_motor(self):
        """Simulate induction motor starting"""
        V = self.im_params['V'].get()
        Rs = self.im_params['Rs'].get()
        Rr = self.im_params['Rr'].get()
        Xs = self.im_params['Xs'].get()
        Xr = self.im_params['Xr'].get()
        Xm = self.im_params['Xm'].get()
        TL = self.im_params['TL'].get()
        J = self.im_params['J'].get()
        P = int(self.im_params['P'].get())
        t_max = self.im_params['t_max'].get()

        # Initial conditions: [omega_r, ids, iqs]
        y0 = [0, 0, 0]
        t_span = (0, t_max)
        t_eval = np.linspace(0, t_max, 1000)

        def system(t, y):
            return self.power_sim.induction_motor(t, y, V, Rs, Rr, Xs, Xr, Xm, TL, J, P)

        try:
            if self.im_solver_var.get() == "Euler":
                t, y = self.ode_solver.euler_method(system, t_span, y0, t_eval)
            else:
                t, y = self.ode_solver.rk45_method(system, t_span, y0, t_eval)

            omega_r = y[0, :]
            ids = y[1, :]
            iqs = y[2, :]

            # Calculate derived quantities
            omega_s = 2 * np.pi * 50  # Synchronous speed (50 Hz)
            n_sync = 120 * 50 / P  # Synchronous speed in RPM
            n_r = omega_r * 60 / (2 * np.pi)  # Rotor speed in RPM
            slip = (omega_s - omega_r) / omega_s

            # Current magnitude
            current = np.sqrt(ids**2 + iqs**2)

            # Torque (simplified)
            torque = 3 * (P / 2) * (Xm / (Xs + Xr)) * current**2 * slip

            # Plot results
            self.plot_im_results(t, n_r, current, torque, slip, n_sync, TL)

        except Exception as e:
            messagebox.showerror("Simulation Error", f"Error during simulation:\n{str(e)}")

    def plot_im_results(self, t, speed, current, torque, slip, n_sync, TL):
        """Plot induction motor simulation results"""
        self.im_figure.clear()

        # Create 4 subplots
        ax1 = self.im_figure.add_subplot(2, 2, 1)
        ax1.plot(t, speed, 'b-', linewidth=2)
        ax1.axhline(y=n_sync, color='r', linestyle='--', label=f'Synchronous Speed ({n_sync:.0f} RPM)')
        ax1.set_ylabel('Speed (RPM)', fontweight='bold')
        ax1.set_title('Rotor Speed vs Time', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        ax2 = self.im_figure.add_subplot(2, 2, 2)
        ax2.plot(t, current, 'g-', linewidth=2)
        ax2.set_ylabel('Current (A)', fontweight='bold')
        ax2.set_title('Stator Current vs Time', fontweight='bold')
        ax2.grid(True, alpha=0.3)

        ax3 = self.im_figure.add_subplot(2, 2, 3)
        ax3.plot(t, torque, 'r-', linewidth=2, label='Electromagnetic Torque')
        ax3.axhline(y=TL, color='orange', linestyle='--', label=f'Load Torque ({TL} Nm)')
        ax3.set_xlabel('Time (s)', fontweight='bold')
        ax3.set_ylabel('Torque (Nm)', fontweight='bold')
        ax3.set_title('Torque vs Time', fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        ax4 = self.im_figure.add_subplot(2, 2, 4)
        ax4.plot(t, slip * 100, 'm-', linewidth=2)
        ax4.set_xlabel('Time (s)', fontweight='bold')
        ax4.set_ylabel('Slip (%)', fontweight='bold')
        ax4.set_title('Slip vs Time', fontweight='bold')
        ax4.grid(True, alpha=0.3)

        self.im_figure.tight_layout()
        self.im_canvas.draw()

    def reset_induction_motor(self):
        """Reset induction motor simulation"""
        self.im_figure.clear()
        self.im_canvas.draw()

    def show_load_flow(self):
        """Show load flow analysis module"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Title
        title = ttk.Label(self.main_container, text="Load Flow Analysis - IEEE Bus Systems",
                         font=('Arial', 18, 'bold'))
        title.pack(pady=20)

        # Info
        info_frame = ttk.LabelFrame(self.main_container, text="Information", padding=20)
        info_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        info_text = """
        Load Flow Analysis (Power Flow Analysis)

        This module performs iterative load flow calculations for power systems using:

        - Gauss-Seidel Method
        - Newton-Raphson Method

        Applications:
        - Power system planning and operation
        - Voltage profile analysis
        - Power loss calculation
        - System stability assessment

        The load flow problem solves for:
        - Bus voltages (magnitude and angle)
        - Real and reactive power flows
        - System losses

        This is a fundamental tool for power system analysis used by utilities
        and grid operators worldwide for ensuring reliable power delivery.

        Implementation Status: Advanced module (requires bus data input)

        For a complete implementation, please refer to specialized power system
        analysis software like MATPOWER, PowerWorld, or PSS/E.
        """

        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT,
                              font=('Arial', 10))
        info_label.pack()

        # Back button
        self.create_back_button(self.main_container)

    def show_about(self):
        """Show about information"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Title
        title = ttk.Label(self.main_container, text="About Electrical Engineering Laboratory",
                         font=('Arial', 18, 'bold'))
        title.pack(pady=20)

        # About content
        about_frame = ttk.Frame(self.main_container)
        about_frame.pack(padx=30, pady=20, fill=tk.BOTH, expand=True)

        about_text = """
        ELECTRICAL ENGINEERING LABORATORY
        Advanced Simulation Suite v2.0

        ===================================================================

        FEATURES:

        - Two-Part Tariff Calculator
          Comprehensive electricity pricing analysis
          Fixed and running charge calculation
          Load factor and utilization metrics
          Visual cost breakdown and analysis

        - Power System Dynamics
          Swing equation simulation
          Synchronous generator stability analysis
          Real-time ODE solvers (Euler, RK45)
          Rotor angle and frequency dynamics

        - Circuit Analysis
          RL, RC, and RLC transient response
          Analytical vs numerical comparison
          Damping analysis
          Time constant visualization

        - Induction Motor Simulation
          Three-phase motor starting analysis
          Speed, current, and torque profiles
          Slip calculation
          Dynamic performance evaluation

        - Advanced Features
          Auto-scaling responsive GUI
          Interactive parameter adjustment
          Real-time visualization
          Multiple ODE solver methods
          Professional-grade analysis tools

        ===================================================================

        TECHNOLOGIES:
        - Python 3.x
        - Tkinter (GUI framework)
        - Matplotlib (Visualization)
        - NumPy (Numerical computing)
        - SciPy (Scientific computing)

        APPLICATIONS:
        - Electrical engineering education
        - Power system analysis and planning
        - Circuit design and analysis
        - Motor performance evaluation
        - Tariff and cost optimization

        ===================================================================

        Developed for practical electrical engineering applications

        Electrical Engineering Laboratory
        All Rights Reserved
        """

        about_label = ttk.Label(about_frame, text=about_text, justify=tk.LEFT,
                               font=('Courier', 9))
        about_label.pack()

        # Back button
        self.create_back_button(self.main_container)

    def on_window_resize(self, event):
        """Handle window resize events for auto-scaling"""
        # Only resize canvases if they exist and event is from root window
        if event.widget == self.root:
            # Auto-adjust canvas sizes based on window dimensions
            pass  # Matplotlib handles this automatically with tight_layout()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ElectricalEngineeringLab(root)
    root.mainloop()


if __name__ == "__main__":
    main()
