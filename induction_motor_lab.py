"""
Three-Phase Induction Motor Analysis Lab
Comprehensive GUI application for motor equivalent circuit calculation and dynamic simulation
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math


class InductionMotorLab:
    """Main application class for Induction Motor Analysis Lab"""

    def __init__(self, root):
        self.root = root
        self.root.title("Three-Phase Induction Motor Analysis Lab")
        self.root.geometry("1400x900")

        # Initialize parameters
        self.init_parameters()

        # Simulation control
        self.simulation_running = False
        self.simulation_time = 0
        self.time_data = []
        self.speed_data = []
        self.torque_data = []
        self.current_data = []

        # Create main UI
        self.create_main_menu()

        # Bind resize event
        self.root.bind('<Configure>', self.on_resize)

    def init_parameters(self):
        """Initialize motor parameters from the problem"""
        # Given parameters
        self.P_rated = 500e3  # W
        self.f = 50  # Hz
        self.VLL_rated = 6000  # V
        self.I_rated = 57  # A
        self.n_rated = 980  # rpm
        self.poles = 6  # calculated from sync speed

        # No-load test data
        self.VLL_noload = 6000  # V
        self.I_noload = 17  # A
        self.P_noload = 14000  # W
        self.P_rot = 3500  # W

        # Locked-rotor test data
        self.VLL_locked = 380  # V
        self.I_locked = 15  # A
        self.P_locked = 1000  # W
        self.R1 = 0.8  # Ohm

        # Calculated equivalent circuit parameters
        self.calculate_equivalent_circuit()

        # Dynamic simulation parameters
        self.J = 50  # kg.m^2 (moment of inertia)
        self.B = 0.1  # N.m.s/rad (friction coefficient)
        self.T_load = 0  # N.m (load torque)

        # Simulation settings
        self.solver_type = 'RK45'  # or 'Euler'
        self.dt = 0.001  # time step for Euler
        self.omega_m = 0  # mechanical speed (rad/s)

    def calculate_equivalent_circuit(self):
        """Calculate equivalent circuit parameters from test data"""
        # Phase voltage (Y-connection)
        V_phase = self.VLL_rated / math.sqrt(3)
        V_phase_noload = self.VLL_noload / math.sqrt(3)
        V_phase_locked = self.VLL_locked / math.sqrt(3)

        # Synchronous speed
        self.n_sync = 120 * self.f / self.poles  # rpm
        self.omega_sync = 2 * math.pi * self.n_sync / 60  # rad/s

        # No-load test analysis
        # Stator copper loss at no-load
        P_cu_noload = 3 * self.I_noload**2 * self.R1

        # Core loss
        self.P_core = self.P_noload - P_cu_noload - self.P_rot

        # No-load impedance
        Z_noload = V_phase_noload / self.I_noload
        R_noload = self.P_noload / (3 * self.I_noload**2)
        X_noload = math.sqrt(Z_noload**2 - R_noload**2)

        # Locked-rotor test analysis
        Z_locked = V_phase_locked / self.I_locked
        R_locked = self.P_locked / (3 * self.I_locked**2)
        X_locked = math.sqrt(Z_locked**2 - R_locked**2)

        # Equivalent circuit parameters
        self.R2 = R_locked - self.R1  # Rotor resistance
        self.X1 = X_locked / 2  # Stator reactance
        self.X2 = X_locked / 2  # Rotor reactance

        # Magnetizing parameters
        # Approximate: Xm >> X1, so Xm ≈ X_noload - X1
        self.Xm = X_noload - self.X1

        # Core loss resistance
        self.Rc = V_phase**2 / (self.P_core / 3)

        # Store phase voltage for calculations
        self.V_phase = V_phase

    def create_main_menu(self):
        """Create main menu and navigation"""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Reset All", command=self.reset_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Analysis menu
        analysis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Analysis", menu=analysis_menu)
        analysis_menu.add_command(label="Equivalent Circuit", command=self.show_equivalent_circuit)
        analysis_menu.add_command(label="Performance Curves", command=self.show_performance_curves)
        analysis_menu.add_command(label="Dynamic Simulation", command=self.show_dynamic_simulation)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Default view
        self.show_dynamic_simulation()

    def create_input_panel(self, parent):
        """Create input parameters panel"""
        input_frame = ttk.LabelFrame(parent, text="Motor Parameters", padding=10)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Create grid of parameters
        params = [
            ("Rated Power (kW):", self.P_rated/1000, "P_rated"),
            ("Frequency (Hz):", self.f, "f"),
            ("Line Voltage (kV):", self.VLL_rated/1000, "VLL_rated"),
            ("Rated Current (A):", self.I_rated, "I_rated"),
            ("Rated Speed (rpm):", self.n_rated, "n_rated"),
            ("Stator Resistance (Ω):", self.R1, "R1"),
            ("Rotor Resistance (Ω):", self.R2, "R2"),
            ("Stator Reactance (Ω):", self.X1, "X1"),
            ("Rotor Reactance (Ω):", self.X2, "X2"),
            ("Magnetizing Reactance (Ω):", self.Xm, "Xm"),
        ]

        self.param_entries = {}
        for i, (label, value, param_name) in enumerate(params):
            row = i // 2
            col = (i % 2) * 2

            ttk.Label(input_frame, text=label).grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(input_frame, width=15)
            entry.insert(0, f"{value:.4f}")
            entry.grid(row=row, column=col+1, padx=5, pady=2)
            self.param_entries[param_name] = entry

    def create_control_panel(self, parent):
        """Create control panel with sliders"""
        control_frame = ttk.LabelFrame(parent, text="Control & Simulation", padding=10)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        # Load torque slider
        ttk.Label(control_frame, text="Load Torque (N.m):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.load_torque_var = tk.DoubleVar(value=0)
        self.load_torque_slider = ttk.Scale(control_frame, from_=0, to=5000,
                                            variable=self.load_torque_var,
                                            orient=tk.HORIZONTAL, length=300)
        self.load_torque_slider.grid(row=0, column=1, padx=5, pady=5)
        self.load_torque_label = ttk.Label(control_frame, text="0.0 N.m")
        self.load_torque_label.grid(row=0, column=2, padx=5, pady=5)
        self.load_torque_var.trace_add('write', self.update_load_torque)

        # Supply voltage slider
        ttk.Label(control_frame, text="Supply Voltage (%):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.voltage_var = tk.DoubleVar(value=100)
        self.voltage_slider = ttk.Scale(control_frame, from_=0, to=120,
                                       variable=self.voltage_var,
                                       orient=tk.HORIZONTAL, length=300)
        self.voltage_slider.grid(row=1, column=1, padx=5, pady=5)
        self.voltage_label = ttk.Label(control_frame, text="100.0 %")
        self.voltage_label.grid(row=1, column=2, padx=5, pady=5)
        self.voltage_var.trace_add('write', self.update_voltage)

        # Inertia slider
        ttk.Label(control_frame, text="Inertia (kg.m²):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.inertia_var = tk.DoubleVar(value=50)
        self.inertia_slider = ttk.Scale(control_frame, from_=10, to=200,
                                       variable=self.inertia_var,
                                       orient=tk.HORIZONTAL, length=300)
        self.inertia_slider.grid(row=2, column=1, padx=5, pady=5)
        self.inertia_label = ttk.Label(control_frame, text="50.0 kg.m²")
        self.inertia_label.grid(row=2, column=2, padx=5, pady=5)
        self.inertia_var.trace_add('write', self.update_inertia)

        # Solver selection
        ttk.Label(control_frame, text="ODE Solver:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.solver_var = tk.StringVar(value='RK45')
        solver_combo = ttk.Combobox(control_frame, textvariable=self.solver_var,
                                    values=['RK45', 'Euler'], state='readonly', width=28)
        solver_combo.grid(row=3, column=1, padx=5, pady=5)

        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)

        self.start_button = ttk.Button(button_frame, text="Start Simulation",
                                       command=self.start_simulation, width=15)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop Simulation",
                                      command=self.stop_simulation, width=15, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(button_frame, text="Reset",
                                       command=self.reset_simulation, width=15)
        self.reset_button.pack(side=tk.LEFT, padx=5)

    def update_load_torque(self, *args):
        """Update load torque from slider"""
        self.T_load = self.load_torque_var.get()
        self.load_torque_label.config(text=f"{self.T_load:.1f} N.m")

    def update_voltage(self, *args):
        """Update voltage from slider"""
        voltage_percent = self.voltage_var.get()
        self.voltage_label.config(text=f"{voltage_percent:.1f} %")

    def update_inertia(self, *args):
        """Update inertia from slider"""
        self.J = self.inertia_var.get()
        self.inertia_label.config(text=f"{self.J:.1f} kg.m²")

    def show_equivalent_circuit(self):
        """Display equivalent circuit parameters"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Title
        title = ttk.Label(self.main_container, text="Equivalent Circuit Parameters",
                         font=('Arial', 16, 'bold'))
        title.pack(pady=10)

        # Create input panel
        self.create_input_panel(self.main_container)

        # Results frame
        results_frame = ttk.LabelFrame(self.main_container, text="Calculated Parameters", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Display results in text widget
        text_widget = tk.Text(results_frame, height=20, width=80, font=('Courier', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Format results
        results = f"""
THREE-PHASE INDUCTION MOTOR - EQUIVALENT CIRCUIT ANALYSIS
{'='*70}

GIVEN DATA:
-----------
Rated Power:              {self.P_rated/1000:.1f} kW
Frequency:                {self.f} Hz
Line-to-Line Voltage:     {self.VLL_rated/1000:.1f} kV
Rated Current:            {self.I_rated} A
Rated Speed:              {self.n_rated} rpm
Number of Poles:          {self.poles}
Synchronous Speed:        {self.n_sync:.1f} rpm

NO-LOAD TEST RESULTS:
--------------------
No-load Voltage:          {self.VLL_noload/1000:.1f} kV
No-load Current:          {self.I_noload} A
No-load Power:            {self.P_noload/1000:.1f} kW
Rotational Losses:        {self.P_rot/1000:.2f} kW
Core Losses:              {self.P_core/1000:.2f} kW

LOCKED-ROTOR TEST RESULTS:
-------------------------
Locked Voltage:           {self.VLL_locked} V
Locked Current:           {self.I_locked} A
Locked Power:             {self.P_locked/1000:.1f} kW

EQUIVALENT CIRCUIT PARAMETERS (per phase):
------------------------------------------
R1 (Stator Resistance):   {self.R1:.4f} Ω
R2 (Rotor Resistance):    {self.R2:.4f} Ω
X1 (Stator Reactance):    {self.X1:.4f} Ω
X2 (Rotor Reactance):     {self.X2:.4f} Ω
Xm (Magnetizing React.):  {self.Xm:.2f} Ω
Rc (Core Loss Resist.):   {self.Rc:.2f} Ω

RATED SLIP:
----------
Slip at rated speed:      {(1 - self.n_rated/self.n_sync)*100:.2f} %
        """

        text_widget.insert('1.0', results)
        text_widget.config(state=tk.DISABLED)

    def show_performance_curves(self):
        """Display motor performance curves"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Title
        title = ttk.Label(self.main_container, text="Motor Performance Curves",
                         font=('Arial', 16, 'bold'))
        title.pack(pady=10)

        # Create matplotlib figure
        fig = Figure(figsize=(12, 8), dpi=100)

        # Calculate performance curves
        slip = np.linspace(0.001, 1.0, 200)
        speed = (1 - slip) * self.n_sync

        voltage_factor = self.voltage_var.get() / 100
        V = self.V_phase * voltage_factor

        # Calculate torque, current, power, efficiency
        torque = np.zeros_like(slip)
        current = np.zeros_like(slip)
        power_out = np.zeros_like(slip)
        efficiency = np.zeros_like(slip)
        power_factor = np.zeros_like(slip)

        for i, s in enumerate(slip):
            # Thevenin equivalent
            Zth, Vth = self.thevenin_equivalent(V)
            Rth = Zth.real
            Xth = Zth.imag

            # Total impedance
            Z_total = Rth + self.R2/s + 1j*Xth
            I2 = Vth / Z_total
            current[i] = abs(I2)

            # Torque
            P_ag = 3 * abs(I2)**2 * self.R2 / s  # Air-gap power
            torque[i] = P_ag / self.omega_sync

            # Output power
            P_mech = P_ag * (1 - s)
            power_out[i] = (P_mech - self.P_rot) / 1000  # kW

            # Input power
            P_in = P_ag + 3 * abs(I2)**2 * Rth + self.P_core

            # Efficiency
            if P_in > 0:
                efficiency[i] = max(0, (P_mech - self.P_rot) / P_in * 100)

            # Power factor
            S = 3 * V * abs(I2)
            if S > 0:
                power_factor[i] = min(1.0, P_in / S)

        # Plot 1: Torque vs Speed
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.plot(speed, torque, 'b-', linewidth=2)
        ax1.set_xlabel('Speed (rpm)', fontsize=10)
        ax1.set_ylabel('Torque (N.m)', fontsize=10)
        ax1.set_title('Torque-Speed Characteristic', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)

        # Plot 2: Current vs Speed
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot(speed, current, 'r-', linewidth=2)
        ax2.set_xlabel('Speed (rpm)', fontsize=10)
        ax2.set_ylabel('Current (A)', fontsize=10)
        ax2.set_title('Current-Speed Characteristic', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # Plot 3: Power vs Speed
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.plot(speed, power_out, 'g-', linewidth=2)
        ax3.set_xlabel('Speed (rpm)', fontsize=10)
        ax3.set_ylabel('Output Power (kW)', fontsize=10)
        ax3.set_title('Power-Speed Characteristic', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)

        # Plot 4: Efficiency and Power Factor vs Speed
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.plot(speed, efficiency, 'b-', linewidth=2, label='Efficiency')
        ax4.plot(speed, power_factor*100, 'r-', linewidth=2, label='Power Factor')
        ax4.set_xlabel('Speed (rpm)', fontsize=10)
        ax4.set_ylabel('Percentage (%)', fontsize=10)
        ax4.set_title('Efficiency & Power Factor', fontsize=12, fontweight='bold')
        ax4.legend(loc='best')
        ax4.grid(True, alpha=0.3)

        fig.tight_layout()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.main_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_dynamic_simulation(self):
        """Display dynamic simulation interface"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Create left panel (controls)
        left_panel = ttk.Frame(self.main_container, width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        left_panel.pack_propagate(False)

        # Title
        title = ttk.Label(left_panel, text="Dynamic Simulation",
                         font=('Arial', 14, 'bold'))
        title.pack(pady=10)

        # Create control panel
        self.create_control_panel(left_panel)

        # Status display
        status_frame = ttk.LabelFrame(left_panel, text="Status", padding=10)
        status_frame.pack(fill=tk.X, padx=5, pady=5)

        self.status_labels = {}
        status_params = [
            ("Speed:", "speed", "rpm"),
            ("Torque:", "torque", "N.m"),
            ("Current:", "current", "A"),
            ("Power:", "power", "kW"),
            ("Slip:", "slip", "%"),
            ("Time:", "time", "s")
        ]

        for i, (label, key, unit) in enumerate(status_params):
            ttk.Label(status_frame, text=label, font=('Arial', 9, 'bold')).grid(
                row=i, column=0, sticky=tk.W, padx=5, pady=2)
            value_label = ttk.Label(status_frame, text=f"0.0 {unit}", font=('Arial', 9))
            value_label.grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
            self.status_labels[key] = value_label

        # Create right panel (plots)
        right_panel = ttk.Frame(self.main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create matplotlib figure for real-time plots
        self.sim_fig = Figure(figsize=(10, 8), dpi=100)

        self.ax_speed = self.sim_fig.add_subplot(3, 1, 1)
        self.ax_speed.set_ylabel('Speed (rpm)', fontsize=9)
        self.ax_speed.set_title('Motor Speed', fontsize=10, fontweight='bold')
        self.ax_speed.grid(True, alpha=0.3)

        self.ax_torque = self.sim_fig.add_subplot(3, 1, 2)
        self.ax_torque.set_ylabel('Torque (N.m)', fontsize=9)
        self.ax_torque.set_title('Electromagnetic Torque', fontsize=10, fontweight='bold')
        self.ax_torque.grid(True, alpha=0.3)

        self.ax_current = self.sim_fig.add_subplot(3, 1, 3)
        self.ax_current.set_xlabel('Time (s)', fontsize=9)
        self.ax_current.set_ylabel('Current (A)', fontsize=9)
        self.ax_current.set_title('Stator Current', fontsize=10, fontweight='bold')
        self.ax_current.grid(True, alpha=0.3)

        self.sim_fig.tight_layout()

        self.sim_canvas = FigureCanvasTkAgg(self.sim_fig, master=right_panel)
        self.sim_canvas.draw()
        self.sim_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def thevenin_equivalent(self, V_phase):
        """Calculate Thevenin equivalent circuit"""
        # Parallel combination of Rc and jXm
        Zm = 1 / (1/self.Rc + 1/(1j*self.Xm))

        # Thevenin impedance
        Zth = 1j*self.X1 * Zm / (1j*self.X1 + Zm) + self.R1

        # Thevenin voltage
        Vth = V_phase * Zm / (1j*self.X1 + Zm)

        return Zth, abs(Vth)

    def calculate_motor_quantities(self, omega_m):
        """Calculate motor electrical quantities at given mechanical speed"""
        # Slip
        s = (self.omega_sync - omega_m) / self.omega_sync
        s = max(0.001, min(s, 1.0))  # Limit slip

        # Voltage
        voltage_factor = self.voltage_var.get() / 100
        V = self.V_phase * voltage_factor

        # Thevenin equivalent
        Zth, Vth = self.thevenin_equivalent(V)
        Rth = Zth.real
        Xth = Zth.imag

        # Rotor current
        Z_total = Rth + self.R2/s + 1j*Xth
        I2 = Vth / Z_total

        # Electromagnetic torque
        P_ag = 3 * abs(I2)**2 * self.R2 / s
        T_em = P_ag / self.omega_sync

        # Stator current (approximate)
        I1 = abs(I2) * 1.1  # approximation

        # Output power
        P_out = P_ag * (1 - s) - self.P_rot

        return T_em, abs(I2), s, P_out/1000

    def motor_dynamics_rk45(self, t, omega_m):
        """Motor dynamics for RK45 solver"""
        T_em, _, _, _ = self.calculate_motor_quantities(omega_m)

        # Equation of motion: J * d(omega)/dt = T_em - T_load - B*omega
        domega_dt = (T_em - self.T_load - self.B * omega_m) / self.J

        return domega_dt

    def rk45_step(self, t, omega_m, dt):
        """Single step of RK45 (4th order Runge-Kutta) solver"""
        k1 = self.motor_dynamics_rk45(t, omega_m)
        k2 = self.motor_dynamics_rk45(t + dt/2, omega_m + dt*k1/2)
        k3 = self.motor_dynamics_rk45(t + dt/2, omega_m + dt*k2/2)
        k4 = self.motor_dynamics_rk45(t + dt, omega_m + dt*k3)

        omega_new = omega_m + dt * (k1 + 2*k2 + 2*k3 + k4) / 6
        return max(0, omega_new)  # Ensure non-negative speed

    def euler_step(self, t, omega_m, dt):
        """Single step of Euler solver"""
        domega_dt = self.motor_dynamics_rk45(t, omega_m)
        omega_new = omega_m + dt * domega_dt
        return max(0, omega_new)

    def start_simulation(self):
        """Start dynamic simulation"""
        self.simulation_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Reset data if starting fresh
        if self.simulation_time == 0:
            self.time_data = []
            self.speed_data = []
            self.torque_data = []
            self.current_data = []
            self.omega_m = 0

        self.run_simulation()

    def stop_simulation(self):
        """Stop dynamic simulation"""
        self.simulation_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def reset_simulation(self):
        """Reset simulation"""
        self.simulation_running = False
        self.simulation_time = 0
        self.omega_m = 0
        self.time_data = []
        self.speed_data = []
        self.torque_data = []
        self.current_data = []

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # Clear plots
        self.ax_speed.clear()
        self.ax_torque.clear()
        self.ax_current.clear()

        self.ax_speed.set_ylabel('Speed (rpm)', fontsize=9)
        self.ax_speed.set_title('Motor Speed', fontsize=10, fontweight='bold')
        self.ax_speed.grid(True, alpha=0.3)

        self.ax_torque.set_ylabel('Torque (N.m)', fontsize=9)
        self.ax_torque.set_title('Electromagnetic Torque', fontsize=10, fontweight='bold')
        self.ax_torque.grid(True, alpha=0.3)

        self.ax_current.set_xlabel('Time (s)', fontsize=9)
        self.ax_current.set_ylabel('Current (A)', fontsize=9)
        self.ax_current.set_title('Stator Current', fontsize=10, fontweight='bold')
        self.ax_current.grid(True, alpha=0.3)

        self.sim_canvas.draw()

        # Reset status
        for key in self.status_labels:
            if key == 'time':
                self.status_labels[key].config(text="0.0 s")
            elif key == 'speed':
                self.status_labels[key].config(text="0.0 rpm")
            elif key == 'torque':
                self.status_labels[key].config(text="0.0 N.m")
            elif key == 'current':
                self.status_labels[key].config(text="0.0 A")
            elif key == 'power':
                self.status_labels[key].config(text="0.0 kW")
            elif key == 'slip':
                self.status_labels[key].config(text="0.0 %")

    def run_simulation(self):
        """Run one step of simulation"""
        if not self.simulation_running:
            return

        # Time step
        dt = 0.01  # 10ms

        # Solve ODE
        if self.solver_var.get() == 'RK45':
            self.omega_m = self.rk45_step(self.simulation_time, self.omega_m, dt)
        else:  # Euler
            self.omega_m = self.euler_step(self.simulation_time, self.omega_m, dt)

        # Calculate motor quantities
        T_em, I_stator, slip, P_out = self.calculate_motor_quantities(self.omega_m)

        # Update time
        self.simulation_time += dt

        # Store data
        self.time_data.append(self.simulation_time)
        self.speed_data.append(self.omega_m * 60 / (2 * math.pi))  # Convert to rpm
        self.torque_data.append(T_em)
        self.current_data.append(I_stator)

        # Limit data points for performance
        max_points = 1000
        if len(self.time_data) > max_points:
            self.time_data = self.time_data[-max_points:]
            self.speed_data = self.speed_data[-max_points:]
            self.torque_data = self.torque_data[-max_points:]
            self.current_data = self.current_data[-max_points:]

        # Update plots every 5 steps
        if len(self.time_data) % 5 == 0:
            self.update_plots()

        # Update status
        self.status_labels['speed'].config(text=f"{self.speed_data[-1]:.1f} rpm")
        self.status_labels['torque'].config(text=f"{T_em:.1f} N.m")
        self.status_labels['current'].config(text=f"{I_stator:.1f} A")
        self.status_labels['power'].config(text=f"{P_out:.1f} kW")
        self.status_labels['slip'].config(text=f"{slip*100:.2f} %")
        self.status_labels['time'].config(text=f"{self.simulation_time:.2f} s")

        # Schedule next step
        self.root.after(10, self.run_simulation)

    def update_plots(self):
        """Update real-time plots"""
        # Clear axes
        self.ax_speed.clear()
        self.ax_torque.clear()
        self.ax_current.clear()

        # Plot speed
        self.ax_speed.plot(self.time_data, self.speed_data, 'b-', linewidth=1.5)
        self.ax_speed.set_ylabel('Speed (rpm)', fontsize=9)
        self.ax_speed.set_title('Motor Speed', fontsize=10, fontweight='bold')
        self.ax_speed.grid(True, alpha=0.3)
        self.ax_speed.set_xlim(max(0, self.simulation_time - 10), self.simulation_time + 0.5)

        # Plot torque
        self.ax_torque.plot(self.time_data, self.torque_data, 'r-', linewidth=1.5)
        self.ax_torque.axhline(y=self.T_load, color='k', linestyle='--',
                               linewidth=1, label='Load Torque')
        self.ax_torque.set_ylabel('Torque (N.m)', fontsize=9)
        self.ax_torque.set_title('Electromagnetic Torque', fontsize=10, fontweight='bold')
        self.ax_torque.legend(loc='upper right', fontsize=8)
        self.ax_torque.grid(True, alpha=0.3)
        self.ax_torque.set_xlim(max(0, self.simulation_time - 10), self.simulation_time + 0.5)

        # Plot current
        self.ax_current.plot(self.time_data, self.current_data, 'g-', linewidth=1.5)
        self.ax_current.set_xlabel('Time (s)', fontsize=9)
        self.ax_current.set_ylabel('Current (A)', fontsize=9)
        self.ax_current.set_title('Stator Current', fontsize=10, fontweight='bold')
        self.ax_current.grid(True, alpha=0.3)
        self.ax_current.set_xlim(max(0, self.simulation_time - 10), self.simulation_time + 0.5)

        self.sim_fig.tight_layout()
        self.sim_canvas.draw()

    def on_resize(self, event):
        """Handle window resize event for auto-scaling"""
        # Only handle resize of main window
        if event.widget == self.root:
            pass  # Plots auto-scale with tight_layout

    def reset_all(self):
        """Reset all parameters and simulation"""
        self.stop_simulation()
        self.reset_simulation()

        # Reset sliders
        self.load_torque_var.set(0)
        self.voltage_var.set(100)
        self.inertia_var.set(50)

        messagebox.showinfo("Reset", "All parameters and simulation have been reset.")

    def show_about(self):
        """Show about dialog"""
        about_text = """
Three-Phase Induction Motor Analysis Lab
Version 1.0

Features:
• Equivalent circuit parameter calculation
• Performance curve analysis
• Dynamic simulation with RK45 and Euler solvers
• Real-time visualization
• Interactive control of motor parameters

Developed for Electrical Engineering Education
        """
        messagebox.showinfo("About", about_text)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = InductionMotorLab(root)
    root.mainloop()


if __name__ == "__main__":
    main()
