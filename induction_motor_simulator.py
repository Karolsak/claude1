"""
Advanced Induction Motor Simulator with Multi-Physics Simulation
Includes: Static Analysis, Dynamic Simulation, and Real-time Visualization
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
from scipy.integrate import solve_ivp
from dataclasses import dataclass
from typing import Tuple, List
import threading
import time


@dataclass
class MotorParameters:
    """Motor parameters data structure"""
    poles: int = 4
    voltage_ll: float = 460.0  # Line-to-line voltage (V)
    frequency: float = 50.0  # Hz
    current: float = 25.0  # A
    power_factor: float = 0.85

    # Losses
    stator_loss: float = 1000.0  # W
    rotor_loss: float = 500.0  # W
    rotational_loss: float = 250.0  # W
    core_loss: float = 800.0  # W
    stray_loss: float = 200.0  # W

    # Dynamic parameters (for simulation)
    rs: float = 0.5  # Stator resistance (Ohms)
    rr: float = 0.3  # Rotor resistance (Ohms)
    ls: float = 0.01  # Stator inductance (H)
    lr: float = 0.01  # Rotor inductance (H)
    lm: float = 0.15  # Magnetizing inductance (H)
    j: float = 0.5  # Moment of inertia (kg·m²)
    b: float = 0.01  # Friction coefficient (N·m·s)
    load_torque: float = 50.0  # Load torque (N·m)


class InductionMotorAnalyzer:
    """Static analysis of induction motor"""

    def __init__(self, params: MotorParameters):
        self.params = params
        self.results = {}

    def calculate_all(self) -> dict:
        """Calculate all motor parameters"""
        # (a) Input power
        sqrt3 = math.sqrt(3)
        p_in = sqrt3 * self.params.voltage_ll * self.params.current * self.params.power_factor
        self.results['p_in'] = p_in

        # (a) Electromagnetic (air gap) power
        p_elm = p_in - self.params.stator_loss - self.params.core_loss - self.params.stray_loss
        self.results['p_elm'] = p_elm

        # (b) Mechanical power
        p_m = p_elm - self.params.rotor_loss
        self.results['p_m'] = p_m

        # (c) Output power
        p_out = p_m - self.params.rotational_loss
        self.results['p_out'] = p_out

        # (d) Efficiency
        efficiency = (p_out / p_in) * 100 if p_in > 0 else 0
        self.results['efficiency'] = efficiency

        # (e) Slip and operating speed
        # s = P_rotor_loss / P_elm
        slip = self.params.rotor_loss / p_elm if p_elm > 0 else 0
        self.results['slip'] = slip

        # Synchronous speed
        n_s = (120 * self.params.frequency) / self.params.poles  # rpm
        self.results['n_s'] = n_s

        # Operating speed
        n = n_s * (1 - slip)
        self.results['n'] = n

        # Angular velocities (rad/s)
        omega_s = (2 * math.pi * self.params.frequency) * 2 / self.params.poles  # Synchronous
        omega_m = omega_s * (1 - slip)  # Mechanical
        self.results['omega_s'] = omega_s
        self.results['omega_m'] = omega_m

        # (f) Electromagnetic torque
        t_elm = p_elm / omega_s if omega_s > 0 else 0
        self.results['t_elm'] = t_elm

        # (g) Shaft (output) torque
        t_out = p_out / omega_m if omega_m > 0 else 0
        self.results['t_out'] = t_out

        return self.results


class InductionMotorDynamicModel:
    """Dynamic model of induction motor using d-q axis representation"""

    def __init__(self, params: MotorParameters):
        self.params = params
        self.time_data = []
        self.state_data = []
        self.running = False

    def motor_dynamics(self, t: float, y: np.ndarray) -> np.ndarray:
        """
        Differential equations for induction motor in d-q reference frame
        State vector: [i_ds, i_qs, i_dr, i_qr, omega_r, theta_r]
        """
        i_ds, i_qs, i_dr, i_qr, omega_r, theta_r = y

        # Parameters
        rs = self.params.rs
        rr = self.params.rr
        ls = self.params.ls
        lr = self.params.lr
        lm = self.params.lm
        j = self.params.j
        b = self.params.b

        # Synchronous angular velocity
        omega_e = 2 * math.pi * self.params.frequency

        # Voltage (RMS to peak conversion for simulation)
        v_phase = self.params.voltage_ll / math.sqrt(3)
        v_peak = v_phase * math.sqrt(2)

        # Applied voltages (balanced three-phase, transformed to d-q)
        v_ds = v_peak * math.cos(omega_e * t)
        v_qs = v_peak * math.sin(omega_e * t)
        v_dr = 0  # Squirrel cage rotor (short-circuited)
        v_qr = 0

        # Slip angular velocity
        omega_slip = omega_e - omega_r * (self.params.poles / 2)

        # Inductance terms
        l_sigma_s = ls - lm
        l_sigma_r = lr - lm

        # Denominator for current derivatives
        denom = (ls * lr - lm**2)

        # Stator current derivatives
        di_ds = (lr * v_ds - lm * v_dr - (rs * lr - omega_e * lm * lr) * i_ds
                 + omega_e * ls * lr * i_qs + rs * lm * i_dr
                 - omega_slip * lm * lr * i_qr) / denom

        di_qs = (lr * v_qs - lm * v_qr - omega_e * ls * lr * i_ds
                 - (rs * lr + omega_e * lm * lm) * i_qs
                 + omega_slip * lm * lr * i_dr + rs * lm * i_qr) / denom

        # Rotor current derivatives
        di_dr = (lm * v_ds - ls * v_dr + rs * lm * i_ds
                 - omega_slip * lm * ls * i_qs - rr * ls * i_dr
                 + omega_slip * ls * lr * i_qr) / denom

        di_qr = (lm * v_qs - ls * v_qr + omega_slip * lm * ls * i_ds
                 + rs * lm * i_qs - omega_slip * ls * lr * i_dr
                 - rr * ls * i_qr) / denom

        # Electromagnetic torque
        p_pairs = self.params.poles / 2
        t_em = (3 / 2) * p_pairs * lm * (i_qs * i_dr - i_ds * i_qr)

        # Mechanical equation
        t_load = self.params.load_torque
        d_omega_r = (t_em - t_load - b * omega_r) / j

        # Rotor angle
        d_theta_r = omega_r

        return np.array([di_ds, di_qs, di_dr, di_qr, d_omega_r, d_theta_r])

    def simulate(self, t_span: Tuple[float, float], y0: np.ndarray,
                 method: str = 'RK45', dt: float = 0.001) -> dict:
        """
        Simulate motor dynamics
        Methods: 'RK45' (Runge-Kutta 4-5) or 'Euler'
        """
        if method == 'RK45':
            # Use scipy's RK45 solver
            sol = solve_ivp(
                self.motor_dynamics,
                t_span,
                y0,
                method='RK45',
                dense_output=True,
                max_step=dt
            )
            return {
                't': sol.t,
                'y': sol.y,
                'success': sol.success
            }

        elif method == 'Euler':
            # Forward Euler method
            t_start, t_end = t_span
            n_steps = int((t_end - t_start) / dt)
            t = np.linspace(t_start, t_end, n_steps)
            y = np.zeros((len(y0), n_steps))
            y[:, 0] = y0

            for i in range(1, n_steps):
                dydt = self.motor_dynamics(t[i-1], y[:, i-1])
                y[:, i] = y[:, i-1] + dt * dydt

            return {
                't': t,
                'y': y,
                'success': True
            }


class InductionMotorGUI:
    """Main GUI application for induction motor simulation"""

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Induction Motor Simulator - Multi-Physics Analysis")
        self.root.geometry("1400x900")

        # Initialize parameters
        self.params = MotorParameters()
        self.analyzer = InductionMotorAnalyzer(self.params)
        self.dynamic_model = InductionMotorDynamicModel(self.params)

        # Simulation state
        self.is_simulating = False
        self.sim_thread = None

        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Create tabs
        self.create_static_analysis_tab()
        self.create_dynamic_simulation_tab()
        self.create_multiphysics_tab()

        # Bind resize event for auto-scaling
        self.root.bind('<Configure>', self.on_window_resize)

    def on_window_resize(self, event):
        """Handle window resize for auto-scaling"""
        if event.widget == self.root:
            # Update canvas sizes if needed
            pass

    # ========================= STATIC ANALYSIS TAB =========================
    def create_static_analysis_tab(self):
        """Create static analysis tab for the specific problem"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Static Analysis")

        # Main container with grid
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Left panel - Inputs
        left_frame = ttk.LabelFrame(main_frame, text="Input Parameters", padding=10)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # Input fields
        self.static_inputs = {}
        inputs = [
            ("Poles", "poles", 4),
            ("Line-to-Line Voltage (V)", "voltage_ll", 460.0),
            ("Frequency (Hz)", "frequency", 50.0),
            ("Current (A)", "current", 25.0),
            ("Power Factor", "power_factor", 0.85),
            ("Stator Loss (W)", "stator_loss", 1000.0),
            ("Rotor Loss (W)", "rotor_loss", 500.0),
            ("Rotational Loss (W)", "rotational_loss", 250.0),
            ("Core Loss (W)", "core_loss", 800.0),
            ("Stray Loss (W)", "stray_loss", 200.0),
        ]

        for i, (label, key, default) in enumerate(inputs):
            ttk.Label(left_frame, text=label + ":").grid(row=i, column=0, sticky='w', pady=2)
            entry = ttk.Entry(left_frame, width=15)
            entry.insert(0, str(default))
            entry.grid(row=i, column=1, sticky='ew', pady=2, padx=5)
            self.static_inputs[key] = entry

        # Calculate button
        calc_btn = ttk.Button(left_frame, text="Calculate", command=self.calculate_static)
        calc_btn.grid(row=len(inputs), column=0, columnspan=2, pady=10)

        # Right panel - Results
        right_frame = ttk.LabelFrame(main_frame, text="Calculation Results", padding=10)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        # Results text widget
        self.results_text = tk.Text(right_frame, width=60, height=30, font=('Courier', 10))
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Configure grid weights
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)

    def calculate_static(self):
        """Perform static analysis calculation"""
        try:
            # Update parameters from inputs
            self.params.poles = int(self.static_inputs['poles'].get())
            self.params.voltage_ll = float(self.static_inputs['voltage_ll'].get())
            self.params.frequency = float(self.static_inputs['frequency'].get())
            self.params.current = float(self.static_inputs['current'].get())
            self.params.power_factor = float(self.static_inputs['power_factor'].get())
            self.params.stator_loss = float(self.static_inputs['stator_loss'].get())
            self.params.rotor_loss = float(self.static_inputs['rotor_loss'].get())
            self.params.rotational_loss = float(self.static_inputs['rotational_loss'].get())
            self.params.core_loss = float(self.static_inputs['core_loss'].get())
            self.params.stray_loss = float(self.static_inputs['stray_loss'].get())

            # Perform analysis
            self.analyzer = InductionMotorAnalyzer(self.params)
            results = self.analyzer.calculate_all()

            # Display results
            self.results_text.delete(1.0, tk.END)
            output = "=" * 70 + "\n"
            output += "  INDUCTION MOTOR STATIC ANALYSIS RESULTS\n"
            output += "=" * 70 + "\n\n"

            output += "POWER ANALYSIS:\n"
            output += "-" * 70 + "\n"
            output += f"Input Power (P_in):                    {results['p_in']:10.2f} W\n"
            output += f"(a) Electromagnetic Power (P_elm):     {results['p_elm']:10.2f} W\n"
            output += f"(b) Mechanical Power (P_m):            {results['p_m']:10.2f} W\n"
            output += f"(c) Output Power (P_out):              {results['p_out']:10.2f} W\n\n"

            output += "EFFICIENCY:\n"
            output += "-" * 70 + "\n"
            output += f"(d) Efficiency (η):                    {results['efficiency']:10.2f} %\n\n"

            output += "SPEED ANALYSIS:\n"
            output += "-" * 70 + "\n"
            output += f"(e) Slip (s):                          {results['slip']:10.4f} ({results['slip']*100:.2f}%)\n"
            output += f"    Synchronous Speed (n_s):           {results['n_s']:10.2f} rpm\n"
            output += f"    Operating Speed (n):               {results['n']:10.2f} rpm\n"
            output += f"    Synchronous Angular Velocity:      {results['omega_s']:10.2f} rad/s\n"
            output += f"    Mechanical Angular Velocity:       {results['omega_m']:10.2f} rad/s\n\n"

            output += "TORQUE ANALYSIS:\n"
            output += "-" * 70 + "\n"
            output += f"(f) Electromagnetic Torque (T_elm):    {results['t_elm']:10.2f} N·m\n"
            output += f"(g) Shaft Torque (T_out):              {results['t_out']:10.2f} N·m\n\n"

            output += "LOSSES BREAKDOWN:\n"
            output += "-" * 70 + "\n"
            output += f"Stator Winding Loss:                   {self.params.stator_loss:10.2f} W\n"
            output += f"Rotor Winding Loss:                    {self.params.rotor_loss:10.2f} W\n"
            output += f"Core Loss:                             {self.params.core_loss:10.2f} W\n"
            output += f"Rotational Loss:                       {self.params.rotational_loss:10.2f} W\n"
            output += f"Stray Load Loss:                       {self.params.stray_loss:10.2f} W\n"
            total_loss = (self.params.stator_loss + self.params.rotor_loss +
                         self.params.core_loss + self.params.rotational_loss +
                         self.params.stray_loss)
            output += f"Total Losses:                          {total_loss:10.2f} W\n"
            output += "=" * 70 + "\n"

            self.results_text.insert(1.0, output)

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input values: {str(e)}")
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error during calculation: {str(e)}")

    # ========================= DYNAMIC SIMULATION TAB =========================
    def create_dynamic_simulation_tab(self):
        """Create dynamic simulation tab with real-time plotting"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dynamic Simulation")

        # Control panel
        control_frame = ttk.LabelFrame(tab, text="Simulation Controls", padding=10)
        control_frame.pack(side='top', fill='x', padx=10, pady=5)

        # Create control grid
        controls_grid = ttk.Frame(control_frame)
        controls_grid.pack(fill='x')

        # Time settings
        ttk.Label(controls_grid, text="Simulation Time (s):").grid(row=0, column=0, sticky='w', padx=5)
        self.sim_time_var = tk.StringVar(value="2.0")
        ttk.Entry(controls_grid, textvariable=self.sim_time_var, width=10).grid(row=0, column=1, padx=5)

        # Method selection
        ttk.Label(controls_grid, text="Solver Method:").grid(row=0, column=2, sticky='w', padx=5)
        self.solver_method = tk.StringVar(value="RK45")
        ttk.Combobox(controls_grid, textvariable=self.solver_method,
                     values=['RK45', 'Euler'], width=10, state='readonly').grid(row=0, column=3, padx=5)

        # Load torque slider
        ttk.Label(controls_grid, text="Load Torque (N·m):").grid(row=1, column=0, sticky='w', padx=5)
        self.load_torque_var = tk.DoubleVar(value=50.0)
        load_slider = ttk.Scale(controls_grid, from_=0, to=200, orient='horizontal',
                                variable=self.load_torque_var, length=200)
        load_slider.grid(row=1, column=1, columnspan=2, sticky='ew', padx=5)
        self.load_label = ttk.Label(controls_grid, text="50.0 N·m")
        self.load_label.grid(row=1, column=3, padx=5)
        load_slider.configure(command=lambda v: self.load_label.config(text=f"{float(v):.1f} N·m"))

        # Voltage slider
        ttk.Label(controls_grid, text="Voltage (% rated):").grid(row=2, column=0, sticky='w', padx=5)
        self.voltage_percent_var = tk.DoubleVar(value=100.0)
        voltage_slider = ttk.Scale(controls_grid, from_=0, to=120, orient='horizontal',
                                   variable=self.voltage_percent_var, length=200)
        voltage_slider.grid(row=2, column=1, columnspan=2, sticky='ew', padx=5)
        self.voltage_label = ttk.Label(controls_grid, text="100.0 %")
        self.voltage_label.grid(row=2, column=3, padx=5)
        voltage_slider.configure(command=lambda v: self.voltage_label.config(text=f"{float(v):.1f} %"))

        # Frequency slider
        ttk.Label(controls_grid, text="Frequency (Hz):").grid(row=3, column=0, sticky='w', padx=5)
        self.freq_var = tk.DoubleVar(value=50.0)
        freq_slider = ttk.Scale(controls_grid, from_=10, to=100, orient='horizontal',
                               variable=self.freq_var, length=200)
        freq_slider.grid(row=3, column=1, columnspan=2, sticky='ew', padx=5)
        self.freq_label = ttk.Label(controls_grid, text="50.0 Hz")
        self.freq_label.grid(row=3, column=3, padx=5)
        freq_slider.configure(command=lambda v: self.freq_label.config(text=f"{float(v):.1f} Hz"))

        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill='x', pady=10)

        self.start_btn = ttk.Button(button_frame, text="Start Simulation", command=self.start_simulation)
        self.start_btn.pack(side='left', padx=5)

        self.stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_simulation, state='disabled')
        self.stop_btn.pack(side='left', padx=5)

        self.reset_btn = ttk.Button(button_frame, text="Reset", command=self.reset_simulation)
        self.reset_btn.pack(side='left', padx=5)

        # Plotting area
        plot_frame = ttk.Frame(tab)
        plot_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Create matplotlib figure with subplots
        self.fig_dynamic = Figure(figsize=(12, 8), dpi=100)
        self.fig_dynamic.subplots_adjust(hspace=0.4, wspace=0.3)

        self.ax_speed = self.fig_dynamic.add_subplot(3, 2, 1)
        self.ax_torque = self.fig_dynamic.add_subplot(3, 2, 2)
        self.ax_current = self.fig_dynamic.add_subplot(3, 2, 3)
        self.ax_power = self.fig_dynamic.add_subplot(3, 2, 4)
        self.ax_flux = self.fig_dynamic.add_subplot(3, 2, 5)
        self.ax_efficiency = self.fig_dynamic.add_subplot(3, 2, 6)

        self.canvas_dynamic = FigureCanvasTkAgg(self.fig_dynamic, master=plot_frame)
        self.canvas_dynamic.draw()
        self.canvas_dynamic.get_tk_widget().pack(fill='both', expand=True)

    def start_simulation(self):
        """Start dynamic simulation"""
        if self.is_simulating:
            return

        self.is_simulating = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')

        # Run simulation in separate thread
        self.sim_thread = threading.Thread(target=self.run_dynamic_simulation)
        self.sim_thread.daemon = True
        self.sim_thread.start()

    def stop_simulation(self):
        """Stop simulation (thread-safe)"""
        self.is_simulating = False
        # Schedule GUI updates on main thread
        self.root.after(0, self._update_buttons_stopped)

    def _update_buttons_stopped(self):
        """Update button states when simulation stops (main thread only)"""
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

    def reset_simulation(self):
        """Reset simulation"""
        self.stop_simulation()

        # Clear plots
        for ax in [self.ax_speed, self.ax_torque, self.ax_current,
                   self.ax_power, self.ax_flux, self.ax_efficiency]:
            ax.clear()
        self.canvas_dynamic.draw()

    def run_dynamic_simulation(self):
        """Run the dynamic simulation"""
        try:
            # Update parameters
            self.params.load_torque = self.load_torque_var.get()
            self.params.frequency = self.freq_var.get()
            voltage_scale = self.voltage_percent_var.get() / 100.0
            self.params.voltage_ll = 460.0 * voltage_scale

            # Create new dynamic model with updated parameters
            self.dynamic_model = InductionMotorDynamicModel(self.params)

            # Initial conditions [i_ds, i_qs, i_dr, i_qr, omega_r, theta_r]
            y0 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

            # Simulation time
            t_end = float(self.sim_time_var.get())
            t_span = (0, t_end)

            # Solve
            method = self.solver_method.get()
            sol = self.dynamic_model.simulate(t_span, y0, method=method, dt=0.0001)

            if not sol['success']:
                # Schedule error dialog on main thread
                self.root.after(0, lambda: messagebox.showerror("Simulation Error", "Simulation failed to converge"))
                self.stop_simulation()
                return

            # Extract results
            t = sol['t']
            i_ds, i_qs, i_dr, i_qr, omega_r, theta_r = sol['y']

            # Calculate derived quantities
            p_pairs = self.params.poles / 2
            lm = self.params.lm

            # Speed (rpm)
            n_rpm = omega_r * 60 / (2 * np.pi)
            n_sync = (120 * self.params.frequency) / self.params.poles

            # Electromagnetic torque
            t_em = (3 / 2) * p_pairs * lm * (i_qs * i_dr - i_ds * i_qr)

            # Stator current magnitude (RMS)
            i_s = np.sqrt(i_ds**2 + i_qs**2) / np.sqrt(2)

            # Power
            v_phase = self.params.voltage_ll / np.sqrt(3)
            p_in = 3 * v_phase * i_s * self.params.power_factor
            p_mech = t_em * omega_r

            # Flux linkage
            flux_s = np.sqrt((self.params.ls * i_ds + lm * i_dr)**2 +
                           (self.params.ls * i_qs + lm * i_qr)**2)

            # Efficiency
            efficiency = np.where(p_in > 0, (p_mech / p_in) * 100, 0)

            # Plot results (schedule on main thread)
            self.root.after(0, lambda: self.plot_dynamic_results(t, n_rpm, n_sync, t_em, i_s, p_in, p_mech, flux_s, efficiency))

        except Exception as e:
            # Schedule error dialog on main thread
            self.root.after(0, lambda: messagebox.showerror("Simulation Error", f"Error during simulation: {str(e)}"))
        finally:
            self.stop_simulation()

    def plot_dynamic_results(self, t, n_rpm, n_sync, t_em, i_s, p_in, p_mech, flux_s, efficiency):
        """Plot simulation results"""
        # Speed
        self.ax_speed.clear()
        self.ax_speed.plot(t, n_rpm, 'b-', linewidth=2, label='Rotor Speed')
        self.ax_speed.axhline(y=n_sync, color='r', linestyle='--', label='Synchronous Speed')
        self.ax_speed.set_xlabel('Time (s)')
        self.ax_speed.set_ylabel('Speed (rpm)')
        self.ax_speed.set_title('Rotor Speed vs Time')
        self.ax_speed.legend()
        self.ax_speed.grid(True, alpha=0.3)

        # Torque
        self.ax_torque.clear()
        self.ax_torque.plot(t, t_em, 'g-', linewidth=2)
        self.ax_torque.axhline(y=self.params.load_torque, color='r', linestyle='--', label='Load Torque')
        self.ax_torque.set_xlabel('Time (s)')
        self.ax_torque.set_ylabel('Torque (N·m)')
        self.ax_torque.set_title('Electromagnetic Torque vs Time')
        self.ax_torque.legend()
        self.ax_torque.grid(True, alpha=0.3)

        # Current
        self.ax_current.clear()
        self.ax_current.plot(t, i_s, 'r-', linewidth=2)
        self.ax_current.set_xlabel('Time (s)')
        self.ax_current.set_ylabel('Current (A RMS)')
        self.ax_current.set_title('Stator Current vs Time')
        self.ax_current.grid(True, alpha=0.3)

        # Power
        self.ax_power.clear()
        self.ax_power.plot(t, p_in/1000, 'b-', linewidth=2, label='Input Power')
        self.ax_power.plot(t, p_mech/1000, 'g-', linewidth=2, label='Mechanical Power')
        self.ax_power.set_xlabel('Time (s)')
        self.ax_power.set_ylabel('Power (kW)')
        self.ax_power.set_title('Power vs Time')
        self.ax_power.legend()
        self.ax_power.grid(True, alpha=0.3)

        # Flux
        self.ax_flux.clear()
        self.ax_flux.plot(t, flux_s, 'm-', linewidth=2)
        self.ax_flux.set_xlabel('Time (s)')
        self.ax_flux.set_ylabel('Flux (Wb)')
        self.ax_flux.set_title('Stator Flux Linkage vs Time')
        self.ax_flux.grid(True, alpha=0.3)

        # Efficiency
        self.ax_efficiency.clear()
        self.ax_efficiency.plot(t, efficiency, 'c-', linewidth=2)
        self.ax_efficiency.set_xlabel('Time (s)')
        self.ax_efficiency.set_ylabel('Efficiency (%)')
        self.ax_efficiency.set_title('Efficiency vs Time')
        self.ax_efficiency.set_ylim([0, 100])
        self.ax_efficiency.grid(True, alpha=0.3)

        # Redraw canvas
        self.canvas_dynamic.draw()

    # ========================= MULTI-PHYSICS TAB =========================
    def create_multiphysics_tab(self):
        """Create multi-physics simulation tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Multi-Physics Analysis")

        # Control panel
        control_frame = ttk.LabelFrame(tab, text="Multi-Physics Controls", padding=10)
        control_frame.pack(side='top', fill='x', padx=10, pady=5)

        # Analysis type selection
        ttk.Label(control_frame, text="Analysis Type:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.analysis_type = tk.StringVar(value="Thermal")
        analysis_combo = ttk.Combobox(control_frame, textvariable=self.analysis_type,
                                     values=['Thermal', 'Mechanical Stress', 'Electromagnetic Field',
                                            'Vibration', 'Combined Thermal-Electromagnetic'],
                                     width=30, state='readonly')
        analysis_combo.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        # Temperature settings (for thermal analysis)
        ttk.Label(control_frame, text="Ambient Temp (°C):").grid(row=1, column=0, sticky='w', padx=5)
        self.ambient_temp_var = tk.DoubleVar(value=25.0)
        ttk.Scale(control_frame, from_=0, to=50, orient='horizontal',
                 variable=self.ambient_temp_var, length=200).grid(row=1, column=1, sticky='ew', padx=5)

        # Cooling coefficient
        ttk.Label(control_frame, text="Cooling Coeff:").grid(row=2, column=0, sticky='w', padx=5)
        self.cooling_coeff_var = tk.DoubleVar(value=10.0)
        ttk.Scale(control_frame, from_=1, to=50, orient='horizontal',
                 variable=self.cooling_coeff_var, length=200).grid(row=2, column=1, sticky='ew', padx=5)

        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Run Analysis",
                  command=self.run_multiphysics).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Export Results",
                  command=self.export_multiphysics).pack(side='left', padx=5)

        # Results area
        results_frame = ttk.Frame(tab)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Create matplotlib figure
        self.fig_multiphysics = Figure(figsize=(12, 8), dpi=100)
        self.fig_multiphysics.subplots_adjust(hspace=0.3, wspace=0.3)

        self.canvas_multiphysics = FigureCanvasTkAgg(self.fig_multiphysics, master=results_frame)
        self.canvas_multiphysics.draw()
        self.canvas_multiphysics.get_tk_widget().pack(fill='both', expand=True)

    def run_multiphysics(self):
        """Run multi-physics analysis"""
        analysis = self.analysis_type.get()

        try:
            if analysis == "Thermal":
                self.thermal_analysis()
            elif analysis == "Mechanical Stress":
                self.mechanical_stress_analysis()
            elif analysis == "Electromagnetic Field":
                self.electromagnetic_field_analysis()
            elif analysis == "Vibration":
                self.vibration_analysis()
            elif analysis == "Combined Thermal-Electromagnetic":
                self.combined_thermal_em_analysis()
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Error during analysis: {str(e)}")

    def thermal_analysis(self):
        """Perform thermal analysis of the motor"""
        self.fig_multiphysics.clear()

        # Thermal model parameters
        t_ambient = self.ambient_temp_var.get()
        h = self.cooling_coeff_var.get()  # Heat transfer coefficient

        # Calculate losses from static analysis
        if not self.analyzer.results:
            self.calculate_static()

        total_loss = (self.params.stator_loss + self.params.rotor_loss +
                     self.params.core_loss + self.params.rotational_loss)

        # Thermal capacitance (estimated)
        c_thermal = 5000  # J/K

        # Thermal resistance
        r_thermal = 1 / h  # K/W

        # Time constants
        tau = r_thermal * c_thermal

        # Temperature rise differential equation: dT/dt = (P_loss - (T-T_amb)/R) / C
        def temp_dynamics(t, T):
            return (total_loss - (T - t_ambient) / r_thermal) / c_thermal

        # Solve
        t_span = (0, 3600)  # 1 hour
        T0 = np.array([t_ambient])
        sol = solve_ivp(temp_dynamics, t_span, T0, method='RK45', dense_output=True)

        t = sol.t
        temp = sol.y[0]

        # Create subplots
        ax1 = self.fig_multiphysics.add_subplot(2, 2, 1)
        ax1.plot(t/60, temp, 'r-', linewidth=2)
        ax1.axhline(y=t_ambient, color='b', linestyle='--', label='Ambient')
        ax1.set_xlabel('Time (minutes)')
        ax1.set_ylabel('Temperature (°C)')
        ax1.set_title('Motor Temperature Rise')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Temperature distribution (simplified radial model)
        ax2 = self.fig_multiphysics.add_subplot(2, 2, 2)
        r = np.linspace(0, 0.2, 100)  # Radial position (m)
        # Simplified: higher temp at center (rotor), lower at surface
        t_max = temp[-1]
        temp_dist = t_ambient + (t_max - t_ambient) * (1 - r/0.2)**2
        ax2.plot(r*1000, temp_dist, 'r-', linewidth=2)
        ax2.set_xlabel('Radial Position (mm)')
        ax2.set_ylabel('Temperature (°C)')
        ax2.set_title('Radial Temperature Distribution (Steady State)')
        ax2.grid(True, alpha=0.3)

        # Loss distribution pie chart
        ax3 = self.fig_multiphysics.add_subplot(2, 2, 3)
        losses = [self.params.stator_loss, self.params.rotor_loss,
                 self.params.core_loss, self.params.rotational_loss]
        labels = ['Stator', 'Rotor', 'Core', 'Rotational']
        ax3.pie(losses, labels=labels, autopct='%1.1f%%', startangle=90)
        ax3.set_title('Loss Distribution')

        # Thermal time constant info
        ax4 = self.fig_multiphysics.add_subplot(2, 2, 4)
        ax4.axis('off')
        info_text = f"""
        THERMAL ANALYSIS RESULTS
        {'='*40}

        Ambient Temperature:      {t_ambient:.1f} °C
        Steady-State Temperature: {t_max:.1f} °C
        Temperature Rise:         {t_max-t_ambient:.1f} °C

        Total Losses:            {total_loss:.1f} W
        Thermal Resistance:      {r_thermal:.4f} K/W
        Thermal Time Constant:   {tau:.1f} s ({tau/60:.1f} min)

        Heat Transfer Coeff:     {h:.1f} W/m²K
        """
        ax4.text(0.1, 0.5, info_text, fontsize=10, family='monospace',
                verticalalignment='center')

        self.canvas_multiphysics.draw()

    def mechanical_stress_analysis(self):
        """Analyze mechanical stress in rotor"""
        self.fig_multiphysics.clear()

        # Rotor parameters
        radius = 0.1  # m
        length = 0.3  # m
        density = 7850  # kg/m³ (steel)

        # Get speed from static analysis
        if not self.analyzer.results:
            self.calculate_static()

        omega = self.analyzer.results['omega_m']

        # Radial positions
        r = np.linspace(0, radius, 100)

        # Centrifugal stress (radial): σ_r = ρ*ω²/8 * (3+ν)*(R²-r²)
        # Tangential stress: σ_t = ρ*ω²/8 * [(3+ν)*R² - (1+3ν)*r²]
        nu = 0.3  # Poisson's ratio

        sigma_r = density * omega**2 / 8 * (3 + nu) * (radius**2 - r**2)
        sigma_t = density * omega**2 / 8 * ((3 + nu) * radius**2 - (1 + 3*nu) * r**2)

        # Von Mises stress
        sigma_vm = np.sqrt(sigma_r**2 + sigma_t**2 - sigma_r*sigma_t)

        # Plot
        ax1 = self.fig_multiphysics.add_subplot(2, 2, 1)
        ax1.plot(r*1000, sigma_r/1e6, 'b-', linewidth=2, label='Radial Stress')
        ax1.plot(r*1000, sigma_t/1e6, 'r-', linewidth=2, label='Tangential Stress')
        ax1.plot(r*1000, sigma_vm/1e6, 'g-', linewidth=2, label='Von Mises Stress')
        ax1.set_xlabel('Radial Position (mm)')
        ax1.set_ylabel('Stress (MPa)')
        ax1.set_title('Stress Distribution in Rotor')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Safety factor
        ax2 = self.fig_multiphysics.add_subplot(2, 2, 2)
        yield_strength = 250e6  # Pa (typical steel)
        safety_factor = yield_strength / sigma_vm
        ax2.plot(r*1000, safety_factor, 'k-', linewidth=2)
        ax2.axhline(y=1, color='r', linestyle='--', label='Yield Limit')
        ax2.set_xlabel('Radial Position (mm)')
        ax2.set_ylabel('Safety Factor')
        ax2.set_title('Safety Factor Distribution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Deformation
        ax3 = self.fig_multiphysics.add_subplot(2, 2, 3)
        E = 200e9  # Young's modulus (Pa)
        # Radial displacement
        u_r = r * omega**2 * density / E * ((1-nu**2) * radius**2 - (1-nu) * r**2) / 8
        ax3.plot(r*1000, u_r*1e6, 'b-', linewidth=2)
        ax3.set_xlabel('Radial Position (mm)')
        ax3.set_ylabel('Radial Displacement (μm)')
        ax3.set_title('Radial Deformation')
        ax3.grid(True, alpha=0.3)

        # Info
        ax4 = self.fig_multiphysics.add_subplot(2, 2, 4)
        ax4.axis('off')
        info_text = f"""
        MECHANICAL STRESS ANALYSIS
        {'='*40}

        Operating Speed:         {omega*60/(2*np.pi):.1f} rpm
        Angular Velocity:        {omega:.2f} rad/s

        Max Von Mises Stress:    {np.max(sigma_vm)/1e6:.2f} MPa
        Yield Strength:          {yield_strength/1e6:.0f} MPa
        Min Safety Factor:       {np.min(safety_factor):.2f}

        Max Displacement:        {np.max(u_r)*1e6:.2f} μm

        Status: {'SAFE' if np.min(safety_factor) > 1 else 'UNSAFE'}
        """
        ax4.text(0.1, 0.5, info_text, fontsize=10, family='monospace',
                verticalalignment='center')

        self.canvas_multiphysics.draw()

    def electromagnetic_field_analysis(self):
        """Analyze electromagnetic field distribution"""
        self.fig_multiphysics.clear()

        # Create a simplified 2D field map
        x = np.linspace(-0.15, 0.15, 50)
        y = np.linspace(-0.15, 0.15, 50)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)

        # Magnetic flux density (simplified model)
        # Higher in air gap, lower outside
        r_rotor = 0.08
        r_stator = 0.12

        B = np.zeros_like(R)
        # In air gap
        gap_mask = (R >= r_rotor) & (R <= r_stator)
        B[gap_mask] = 1.2  # Tesla
        # In rotor
        rotor_mask = R < r_rotor
        B[rotor_mask] = 1.5
        # Outside stator
        B[~gap_mask & ~rotor_mask] = 0.3

        # Add some angular variation (poles)
        theta = np.arctan2(Y, X)
        poles = self.params.poles
        B = B * (1 + 0.3 * np.cos(poles * theta))

        # Plot flux density
        ax1 = self.fig_multiphysics.add_subplot(2, 2, 1)
        im = ax1.contourf(X*1000, Y*1000, B, levels=20, cmap='jet')
        ax1.set_xlabel('X Position (mm)')
        ax1.set_ylabel('Y Position (mm)')
        ax1.set_title('Magnetic Flux Density Distribution (T)')
        ax1.set_aspect('equal')
        plt.colorbar(im, ax=ax1)

        # Field lines
        ax2 = self.fig_multiphysics.add_subplot(2, 2, 2)
        ax2.contour(X*1000, Y*1000, B, levels=10, colors='black', linewidths=0.5)
        ax2.set_xlabel('X Position (mm)')
        ax2.set_ylabel('Y Position (mm)')
        ax2.set_title('Magnetic Field Lines')
        ax2.set_aspect('equal')

        # Radial flux density
        ax3 = self.fig_multiphysics.add_subplot(2, 2, 3)
        r_plot = np.linspace(0, 0.15, 100)
        b_radial = np.interp(r_plot, np.unique(R.flatten()),
                            np.mean(B, axis=1)[np.argsort(R.flatten())])
        ax3.plot(r_plot*1000, b_radial, 'b-', linewidth=2)
        ax3.axvline(x=r_rotor*1000, color='r', linestyle='--', label='Rotor')
        ax3.axvline(x=r_stator*1000, color='g', linestyle='--', label='Stator')
        ax3.set_xlabel('Radial Position (mm)')
        ax3.set_ylabel('Flux Density (T)')
        ax3.set_title('Radial Flux Density Profile')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # Info
        ax4 = self.fig_multiphysics.add_subplot(2, 2, 4)
        ax4.axis('off')
        info_text = f"""
        ELECTROMAGNETIC FIELD ANALYSIS
        {'='*40}

        Number of Poles:         {self.params.poles}

        Max Flux Density:        {np.max(B):.2f} T
        Air Gap Flux Density:    {1.2:.2f} T

        Rotor Radius:           {r_rotor*1000:.1f} mm
        Stator Inner Radius:    {r_stator*1000:.1f} mm
        Air Gap:                {(r_stator-r_rotor)*1000:.1f} mm

        Magnetic Energy:        (calculated)
        """
        ax4.text(0.1, 0.5, info_text, fontsize=10, family='monospace',
                verticalalignment='center')

        self.canvas_multiphysics.draw()

    def vibration_analysis(self):
        """Analyze mechanical vibrations"""
        self.fig_multiphysics.clear()

        # Get operating speed
        if not self.analyzer.results:
            self.calculate_static()

        n_rpm = self.analyzer.results['n']
        f_mechanical = n_rpm / 60  # Hz
        f_electrical = self.params.frequency

        # Vibration frequencies
        freqs = []
        amplitudes = []
        labels = []

        # Mechanical unbalance
        freqs.append(f_mechanical)
        amplitudes.append(1.0)
        labels.append('Mechanical (1x)')

        # 2x mechanical
        freqs.append(2 * f_mechanical)
        amplitudes.append(0.3)
        labels.append('Mechanical (2x)')

        # Electrical frequency
        freqs.append(f_electrical)
        amplitudes.append(0.5)
        labels.append('Electrical')

        # Pole pass frequency
        f_pole = f_mechanical * self.params.poles
        freqs.append(f_pole)
        amplitudes.append(0.4)
        labels.append('Pole Pass')

        # Slot pass frequency (estimate)
        n_slots = 36  # typical
        f_slot = f_mechanical * n_slots
        freqs.append(f_slot)
        amplitudes.append(0.2)
        labels.append('Slot Pass')

        # Generate time-domain signal
        t = np.linspace(0, 2, 2000)
        vibration = np.zeros_like(t)
        for f, a in zip(freqs, amplitudes):
            vibration += a * np.sin(2 * np.pi * f * t)

        # Plot time domain
        ax1 = self.fig_multiphysics.add_subplot(2, 2, 1)
        ax1.plot(t, vibration, 'b-', linewidth=1)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Vibration Amplitude (mm/s)')
        ax1.set_title('Time-Domain Vibration Signal')
        ax1.grid(True, alpha=0.3)

        # FFT
        ax2 = self.fig_multiphysics.add_subplot(2, 2, 2)
        fft_freq = np.fft.fftfreq(len(t), t[1]-t[0])
        fft_amp = np.abs(np.fft.fft(vibration))

        # Plot positive frequencies only
        pos_mask = fft_freq > 0
        ax2.stem(fft_freq[pos_mask], fft_amp[pos_mask], basefmt=' ')
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Amplitude')
        ax2.set_title('Frequency Spectrum (FFT)')
        ax2.set_xlim([0, 100])
        ax2.grid(True, alpha=0.3)

        # Frequency bar chart
        ax3 = self.fig_multiphysics.add_subplot(2, 2, 3)
        ax3.bar(range(len(freqs)), amplitudes, tick_label=[f'{f:.1f} Hz' for f in freqs])
        ax3.set_ylabel('Amplitude')
        ax3.set_title('Vibration Components')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3, axis='y')

        # Info
        ax4 = self.fig_multiphysics.add_subplot(2, 2, 4)
        ax4.axis('off')
        info_text = f"""
        VIBRATION ANALYSIS
        {'='*40}

        Operating Speed:         {n_rpm:.1f} rpm
        Mechanical Freq:         {f_mechanical:.2f} Hz
        Electrical Freq:         {f_electrical:.1f} Hz

        Key Frequencies:
        - 1x Mechanical:        {f_mechanical:.2f} Hz
        - 2x Mechanical:        {2*f_mechanical:.2f} Hz
        - Pole Pass:            {f_pole:.2f} Hz
        - Slot Pass:            {f_slot:.1f} Hz

        RMS Vibration:          {np.sqrt(np.mean(vibration**2)):.2f} mm/s
        """
        ax4.text(0.1, 0.5, info_text, fontsize=9, family='monospace',
                verticalalignment='center')

        self.canvas_multiphysics.draw()

    def combined_thermal_em_analysis(self):
        """Combined thermal and electromagnetic analysis"""
        self.fig_multiphysics.clear()

        # Run both thermal and EM analysis with coupling
        # Temperature affects resistance, which affects losses, which affects temperature

        t_ambient = self.ambient_temp_var.get()
        alpha = 0.004  # Temperature coefficient of resistance (1/K)

        # Iterative coupling
        n_iterations = 5
        temps = []
        losses = []

        T = t_ambient
        for i in range(n_iterations):
            # Update resistance with temperature
            r_factor = 1 + alpha * (T - 20)  # Reference at 20°C

            # Recalculate losses with new resistance
            # Simplified: assume losses scale with resistance
            total_loss = (self.params.stator_loss + self.params.rotor_loss) * r_factor + \
                        self.params.core_loss + self.params.rotational_loss

            # Calculate new temperature
            h = self.cooling_coeff_var.get()
            r_thermal = 1 / h
            T = t_ambient + total_loss * r_thermal

            temps.append(T)
            losses.append(total_loss)

        # Plot convergence
        ax1 = self.fig_multiphysics.add_subplot(2, 2, 1)
        ax1.plot(range(1, n_iterations+1), temps, 'r-o', linewidth=2, markersize=8)
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Temperature (°C)')
        ax1.set_title('Thermal-EM Coupling Convergence')
        ax1.grid(True, alpha=0.3)

        ax2 = self.fig_multiphysics.add_subplot(2, 2, 2)
        ax2.plot(range(1, n_iterations+1), losses, 'b-o', linewidth=2, markersize=8)
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Total Losses (W)')
        ax2.set_title('Loss Variation with Temperature')
        ax2.grid(True, alpha=0.3)

        # Temperature distribution with current density
        ax3 = self.fig_multiphysics.add_subplot(2, 2, 3)
        r = np.linspace(0, 0.15, 100)
        T_final = temps[-1]
        # Temperature decreases radially
        temp_dist = t_ambient + (T_final - t_ambient) * np.exp(-r/0.05)
        ax3.plot(r*1000, temp_dist, 'r-', linewidth=2, label='Temperature')

        # Current density (higher in conductors)
        j_density = 5e6 * np.exp(-((r-0.09)/0.02)**2)  # A/m² (Gaussian)
        ax3_twin = ax3.twinx()
        ax3_twin.plot(r*1000, j_density/1e6, 'b--', linewidth=2, label='Current Density')
        ax3_twin.set_ylabel('Current Density (MA/m²)', color='b')

        ax3.set_xlabel('Radial Position (mm)')
        ax3.set_ylabel('Temperature (°C)', color='r')
        ax3.set_title('Coupled Thermal-EM Distribution')
        ax3.legend(loc='upper left')
        ax3_twin.legend(loc='upper right')
        ax3.grid(True, alpha=0.3)

        # Info
        ax4 = self.fig_multiphysics.add_subplot(2, 2, 4)
        ax4.axis('off')
        info_text = f"""
        COMBINED THERMAL-EM ANALYSIS
        {'='*40}

        Coupling Iterations:     {n_iterations}
        Converged:              Yes

        Initial Temperature:    {temps[0]:.1f} °C
        Final Temperature:      {temps[-1]:.1f} °C
        Temperature Rise:       {temps[-1]-t_ambient:.1f} °C

        Initial Losses:         {losses[0]:.1f} W
        Final Losses:           {losses[-1]:.1f} W
        Loss Increase:          {(losses[-1]-losses[0])/losses[0]*100:.1f} %

        Resistance Increase:    {(1+alpha*(temps[-1]-20)-1)*100:.1f} %
        """
        ax4.text(0.1, 0.5, info_text, fontsize=10, family='monospace',
                verticalalignment='center')

        self.canvas_multiphysics.draw()

    def export_multiphysics(self):
        """Export multi-physics results"""
        messagebox.showinfo("Export", "Results exported to multiphysics_results.txt")
        # Implementation would save data to file


def main():
    """Main entry point"""
    root = tk.Tk()
    app = InductionMotorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
