"""
Comprehensive Electrical Engineering Laboratory
Transformer Analysis and Dynamic Simulation Tool

Features:
- Transformer Tender Economic Analysis
- Dynamic Transformer Modeling with ODE Solvers
- Real-time visualization and simulation
- Professional GUI with auto-scaling
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
from scipy.integrate import solve_ivp


class TransformerLab:
    """Main application class for Electrical Engineering Laboratory"""

    def __init__(self, root):
        self.root = root
        self.root.title("Electrical Engineering Laboratory - Transformer Analysis")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)

        # Simulation control
        self.simulation_running = False
        self.simulation_thread = None

        # Data storage
        self.time_data = []
        self.flux_data = []
        self.current_data = []
        self.voltage_data = []
        self.power_data = []

        # Configure style
        self.setup_styles()

        # Create main menu
        self.create_menu()

        # Create notebook for different modules
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self.create_tender_analysis_tab()
        self.create_dynamic_simulation_tab()
        self.create_transformer_model_tab()

        # Bind resize event for auto-scaling
        self.root.bind('<Configure>', self.on_window_resize)

        # Status bar
        self.create_status_bar()

    def setup_styles(self):
        """Setup custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')

        # Custom colors
        bg_color = '#f0f0f0'
        fg_color = '#333333'
        accent_color = '#0066cc'

        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground=accent_color)
        style.configure('TButton', font=('Arial', 10))
        style.configure('TNotebook', background=bg_color)
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'))

    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Reset All", command=self.reset_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Clear Results", command=self.clear_results)
        tools_menu.add_command(label="Export Data", command=self.export_data)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_tender_analysis_tab(self):
        """Create transformer tender analysis tab"""
        tender_frame = ttk.Frame(self.notebook)
        self.notebook.add(tender_frame, text="Tender Analysis")

        # Main container with scrollbar
        canvas = tk.Canvas(tender_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(tender_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Header
        header = ttk.Label(scrollable_frame, text="Transformer Tender Economic Analysis",
                          style='Header.TLabel')
        header.grid(row=0, column=0, columnspan=4, pady=20)

        # Input parameters frame
        input_frame = ttk.LabelFrame(scrollable_frame, text="Input Parameters", padding=15)
        input_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Transformer specifications
        row = 0
        ttk.Label(input_frame, text="Transformer Rating (kVA):", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky='w', pady=5)
        self.kva_rating = tk.DoubleVar(value=1000)
        ttk.Entry(input_frame, textvariable=self.kva_rating, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(input_frame, text="Power Factor:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky='w', pady=5)
        self.power_factor = tk.DoubleVar(value=0.8)
        ttk.Entry(input_frame, textvariable=self.power_factor, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        # Tender A parameters
        row += 1
        ttk.Label(input_frame, text="\nTender A Parameters",
                 font=('Arial', 11, 'bold'), foreground='#0066cc').grid(
            row=row, column=0, columnspan=2, pady=10)

        row += 1
        ttk.Label(input_frame, text="Full-load Efficiency A (%):").grid(
            row=row, column=0, sticky='w', pady=5)
        self.eff_a = tk.DoubleVar(value=98.5)
        ttk.Entry(input_frame, textvariable=self.eff_a, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(input_frame, text="Iron Loss A (kW):").grid(
            row=row, column=0, sticky='w', pady=5)
        self.iron_loss_a = tk.DoubleVar(value=6.0)
        ttk.Entry(input_frame, textvariable=self.iron_loss_a, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        # Tender B parameters
        row += 1
        ttk.Label(input_frame, text="\nTender B Parameters",
                 font=('Arial', 11, 'bold'), foreground='#cc6600').grid(
            row=row, column=0, columnspan=2, pady=10)

        row += 1
        ttk.Label(input_frame, text="Full-load Efficiency B (%):").grid(
            row=row, column=0, sticky='w', pady=5)
        self.eff_b = tk.DoubleVar(value=98.8)
        ttk.Entry(input_frame, textvariable=self.eff_b, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(input_frame, text="Iron Loss B (kW):").grid(
            row=row, column=0, sticky='w', pady=5)
        self.iron_loss_b = tk.DoubleVar(value=4.0)
        ttk.Entry(input_frame, textvariable=self.iron_loss_b, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(input_frame, text="Additional Cost B (Rs.):").grid(
            row=row, column=0, sticky='w', pady=5)
        self.cost_diff = tk.DoubleVar(value=1500)
        ttk.Entry(input_frame, textvariable=self.cost_diff, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        # Operating conditions frame
        op_frame = ttk.LabelFrame(scrollable_frame, text="Annual Operating Conditions", padding=15)
        op_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=10, sticky='ew')

        row = 0
        ttk.Label(op_frame, text="Full-load Hours (hrs/year):").grid(
            row=row, column=0, sticky='w', pady=5)
        self.hours_full = tk.DoubleVar(value=2000)
        ttk.Entry(op_frame, textvariable=self.hours_full, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(op_frame, text="Half-load Hours (hrs/year):").grid(
            row=row, column=0, sticky='w', pady=5)
        self.hours_half = tk.DoubleVar(value=600)
        ttk.Entry(op_frame, textvariable=self.hours_half, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(op_frame, text="Light-load Hours (hrs/year):").grid(
            row=row, column=0, sticky='w', pady=5)
        self.hours_light = tk.DoubleVar(value=400)
        ttk.Entry(op_frame, textvariable=self.hours_light, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(op_frame, text="Light Load (kVA):").grid(
            row=row, column=0, sticky='w', pady=5)
        self.light_load_kva = tk.DoubleVar(value=25)
        ttk.Entry(op_frame, textvariable=self.light_load_kva, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(op_frame, text="Annual Charges (% of cost):").grid(
            row=row, column=0, sticky='w', pady=5)
        self.annual_charge_rate = tk.DoubleVar(value=12.5)
        ttk.Entry(op_frame, textvariable=self.annual_charge_rate, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(op_frame, text="Energy Cost (paise/kWh):").grid(
            row=row, column=0, sticky='w', pady=5)
        self.energy_cost = tk.DoubleVar(value=3.0)
        ttk.Entry(op_frame, textvariable=self.energy_cost, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        # Calculate button
        calc_btn = ttk.Button(scrollable_frame, text="Calculate Analysis",
                             command=self.calculate_tender_analysis)
        calc_btn.grid(row=2, column=0, columnspan=4, pady=20)

        # Results frame
        results_frame = ttk.LabelFrame(scrollable_frame, text="Analysis Results", padding=15)
        results_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        self.tender_results = scrolledtext.ScrolledText(results_frame, height=20, width=120,
                                                        font=('Courier', 10))
        self.tender_results.pack(fill=tk.BOTH, expand=True)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_dynamic_simulation_tab(self):
        """Create dynamic transformer simulation tab"""
        sim_frame = ttk.Frame(self.notebook)
        self.notebook.add(sim_frame, text="Dynamic Simulation")

        # Split into left (controls) and right (visualization)
        left_frame = ttk.Frame(sim_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        right_frame = ttk.Frame(sim_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        header = ttk.Label(left_frame, text="Dynamic Simulation Control",
                          style='Header.TLabel')
        header.pack(pady=10)

        # Simulation parameters
        param_frame = ttk.LabelFrame(left_frame, text="Simulation Parameters", padding=10)
        param_frame.pack(fill=tk.X, padx=5, pady=10)

        # Voltage amplitude
        ttk.Label(param_frame, text="Voltage Amplitude (V):").grid(row=0, column=0, sticky='w', pady=5)
        self.sim_voltage = tk.DoubleVar(value=11000)
        self.voltage_scale = ttk.Scale(param_frame, from_=1000, to=33000,
                                      variable=self.sim_voltage, orient=tk.HORIZONTAL, length=200)
        self.voltage_scale.grid(row=0, column=1, padx=5, pady=5)
        self.voltage_label = ttk.Label(param_frame, text="11000 V")
        self.voltage_label.grid(row=0, column=2, padx=5)
        self.sim_voltage.trace('w', lambda *args: self.voltage_label.config(
            text=f"{self.sim_voltage.get():.0f} V"))

        # Frequency
        ttk.Label(param_frame, text="Frequency (Hz):").grid(row=1, column=0, sticky='w', pady=5)
        self.sim_frequency = tk.DoubleVar(value=50)
        self.freq_scale = ttk.Scale(param_frame, from_=25, to=400,
                                   variable=self.sim_frequency, orient=tk.HORIZONTAL, length=200)
        self.freq_scale.grid(row=1, column=1, padx=5, pady=5)
        self.freq_label = ttk.Label(param_frame, text="50 Hz")
        self.freq_label.grid(row=1, column=2, padx=5)
        self.sim_frequency.trace('w', lambda *args: self.freq_label.config(
            text=f"{self.sim_frequency.get():.0f} Hz"))

        # Resistance
        ttk.Label(param_frame, text="Resistance (Ω):").grid(row=2, column=0, sticky='w', pady=5)
        self.sim_resistance = tk.DoubleVar(value=2.5)
        self.res_scale = ttk.Scale(param_frame, from_=0.1, to=10,
                                  variable=self.sim_resistance, orient=tk.HORIZONTAL, length=200)
        self.res_scale.grid(row=2, column=1, padx=5, pady=5)
        self.res_label = ttk.Label(param_frame, text="2.5 Ω")
        self.res_label.grid(row=2, column=2, padx=5)
        self.sim_resistance.trace('w', lambda *args: self.res_label.config(
            text=f"{self.sim_resistance.get():.2f} Ω"))

        # Inductance
        ttk.Label(param_frame, text="Inductance (H):").grid(row=3, column=0, sticky='w', pady=5)
        self.sim_inductance = tk.DoubleVar(value=0.05)
        self.ind_scale = ttk.Scale(param_frame, from_=0.001, to=0.5,
                                  variable=self.sim_inductance, orient=tk.HORIZONTAL, length=200)
        self.ind_scale.grid(row=3, column=1, padx=5, pady=5)
        self.ind_label = ttk.Label(param_frame, text="0.05 H")
        self.ind_label.grid(row=3, column=2, padx=5)
        self.sim_inductance.trace('w', lambda *args: self.ind_label.config(
            text=f"{self.sim_inductance.get():.3f} H"))

        # Load resistance
        ttk.Label(param_frame, text="Load Resistance (Ω):").grid(row=4, column=0, sticky='w', pady=5)
        self.sim_load = tk.DoubleVar(value=100)
        self.load_scale = ttk.Scale(param_frame, from_=10, to=1000,
                                   variable=self.sim_load, orient=tk.HORIZONTAL, length=200)
        self.load_scale.grid(row=4, column=1, padx=5, pady=5)
        self.load_label = ttk.Label(param_frame, text="100 Ω")
        self.load_label.grid(row=4, column=2, padx=5)
        self.sim_load.trace('w', lambda *args: self.load_label.config(
            text=f"{self.sim_load.get():.0f} Ω"))

        # Simulation time
        ttk.Label(param_frame, text="Simulation Time (s):").grid(row=5, column=0, sticky='w', pady=5)
        self.sim_time = tk.DoubleVar(value=0.1)
        ttk.Entry(param_frame, textvariable=self.sim_time, width=10).grid(
            row=5, column=1, sticky='w', padx=5, pady=5)

        # ODE Solver selection
        solver_frame = ttk.LabelFrame(left_frame, text="ODE Solver Method", padding=10)
        solver_frame.pack(fill=tk.X, padx=5, pady=10)

        self.solver_method = tk.StringVar(value="RK45")
        ttk.Radiobutton(solver_frame, text="RK45 (Runge-Kutta 4th/5th order)",
                       variable=self.solver_method, value="RK45").pack(anchor='w', pady=3)
        ttk.Radiobutton(solver_frame, text="Euler (Forward Euler)",
                       variable=self.solver_method, value="Euler").pack(anchor='w', pady=3)
        ttk.Radiobutton(solver_frame, text="RK23 (Runge-Kutta 2nd/3rd order)",
                       variable=self.solver_method, value="RK23").pack(anchor='w', pady=3)

        # Control buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=20)

        self.start_btn = ttk.Button(btn_frame, text="▶ Start Simulation",
                                    command=self.start_simulation)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="⏸ Stop",
                                   command=self.stop_simulation, state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = ttk.Button(btn_frame, text="⟲ Reset",
                                    command=self.reset_simulation)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        # Visualization area
        viz_header = ttk.Label(right_frame, text="Real-time Visualization",
                              style='Header.TLabel')
        viz_header.pack(pady=10)

        # Create matplotlib figure
        self.sim_figure = Figure(figsize=(10, 8), dpi=100)
        self.sim_canvas = FigureCanvasTkAgg(self.sim_figure, right_frame)
        self.sim_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Create subplots
        self.ax1 = self.sim_figure.add_subplot(311)
        self.ax2 = self.sim_figure.add_subplot(312)
        self.ax3 = self.sim_figure.add_subplot(313)

        self.ax1.set_ylabel('Flux (Wb)', fontsize=10)
        self.ax1.grid(True, alpha=0.3)

        self.ax2.set_ylabel('Current (A)', fontsize=10)
        self.ax2.grid(True, alpha=0.3)

        self.ax3.set_ylabel('Power (W)', fontsize=10)
        self.ax3.set_xlabel('Time (s)', fontsize=10)
        self.ax3.grid(True, alpha=0.3)

        self.sim_figure.tight_layout()

    def create_transformer_model_tab(self):
        """Create transformer model analysis tab"""
        model_frame = ttk.Frame(self.notebook)
        self.notebook.add(model_frame, text="Transformer Model")

        # Header
        header = ttk.Label(model_frame, text="Transformer Equivalent Circuit Analysis",
                          style='Header.TLabel')
        header.pack(pady=20)

        # Split into input and output
        content_frame = ttk.Frame(model_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Input parameters
        input_frame = ttk.LabelFrame(content_frame, text="Transformer Parameters", padding=15)
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        row = 0
        ttk.Label(input_frame, text="Rated Power (kVA):").grid(row=row, column=0, sticky='w', pady=5)
        self.model_power = tk.DoubleVar(value=1000)
        ttk.Entry(input_frame, textvariable=self.model_power, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(input_frame, text="Primary Voltage (V):").grid(row=row, column=0, sticky='w', pady=5)
        self.model_v1 = tk.DoubleVar(value=11000)
        ttk.Entry(input_frame, textvariable=self.model_v1, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(input_frame, text="Secondary Voltage (V):").grid(row=row, column=0, sticky='w', pady=5)
        self.model_v2 = tk.DoubleVar(value=415)
        ttk.Entry(input_frame, textvariable=self.model_v2, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(input_frame, text="Primary Resistance (Ω):").grid(row=row, column=0, sticky='w', pady=5)
        self.model_r1 = tk.DoubleVar(value=1.5)
        ttk.Entry(input_frame, textvariable=self.model_r1, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(input_frame, text="Secondary Resistance (Ω):").grid(row=row, column=0, sticky='w', pady=5)
        self.model_r2 = tk.DoubleVar(value=0.02)
        ttk.Entry(input_frame, textvariable=self.model_r2, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(input_frame, text="Primary Reactance (Ω):").grid(row=row, column=0, sticky='w', pady=5)
        self.model_x1 = tk.DoubleVar(value=2.0)
        ttk.Entry(input_frame, textvariable=self.model_x1, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(input_frame, text="Secondary Reactance (Ω):").grid(row=row, column=0, sticky='w', pady=5)
        self.model_x2 = tk.DoubleVar(value=0.03)
        ttk.Entry(input_frame, textvariable=self.model_x2, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(input_frame, text="Load Power Factor:").grid(row=row, column=0, sticky='w', pady=5)
        self.model_pf = tk.DoubleVar(value=0.8)
        ttk.Entry(input_frame, textvariable=self.model_pf, width=15).grid(
            row=row, column=1, padx=5, pady=5)

        row += 1
        ttk.Label(input_frame, text="Load (%):").grid(row=row, column=0, sticky='w', pady=5)
        self.model_load_pct = tk.DoubleVar(value=100)
        ttk.Scale(input_frame, from_=0, to=150, variable=self.model_load_pct,
                 orient=tk.HORIZONTAL, length=150).grid(row=row, column=1, padx=5, pady=5)

        row += 1
        calc_model_btn = ttk.Button(input_frame, text="Calculate Model",
                                    command=self.calculate_transformer_model)
        calc_model_btn.grid(row=row, column=0, columnspan=2, pady=20)

        # Results area
        results_frame = ttk.LabelFrame(content_frame, text="Analysis Results", padding=15)
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        self.model_results = scrolledtext.ScrolledText(results_frame, height=25, width=70,
                                                       font=('Courier', 10))
        self.model_results.pack(fill=tk.BOTH, expand=True)

    def create_status_bar(self):
        """Create status bar at bottom of window"""
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def calculate_tender_analysis(self):
        """Calculate transformer tender economic analysis"""
        try:
            self.tender_results.delete(1.0, tk.END)

            # Get parameters
            S_rated = self.kva_rating.get()  # kVA
            pf = self.power_factor.get()

            # Tender A
            eff_a = self.eff_a.get() / 100
            iron_loss_a = self.iron_loss_a.get()  # kW

            # Tender B
            eff_b = self.eff_b.get() / 100
            iron_loss_b = self.iron_loss_b.get()  # kW
            cost_diff = self.cost_diff.get()

            # Operating conditions
            hours_full = self.hours_full.get()
            hours_half = self.hours_half.get()
            hours_light = self.hours_light.get()
            light_load_kva = self.light_load_kva.get()

            # Economic parameters
            annual_charge_rate = self.annual_charge_rate.get() / 100
            energy_cost_paise = self.energy_cost.get()
            energy_cost_rs = energy_cost_paise / 100  # Convert paise to Rs

            output = "="*80 + "\n"
            output += "TRANSFORMER TENDER ECONOMIC ANALYSIS\n"
            output += "="*80 + "\n\n"

            output += "GIVEN DATA:\n"
            output += "-"*80 + "\n"
            output += f"Transformer Rating:           {S_rated} kVA at {pf} power factor\n"
            output += f"Tender A - Efficiency:        {eff_a*100}%,  Iron Loss: {iron_loss_a} kW\n"
            output += f"Tender B - Efficiency:        {eff_b*100}%,  Iron Loss: {iron_loss_b} kW\n"
            output += f"Additional Cost of B:         Rs. {cost_diff}\n"
            output += f"Annual Charges:               {annual_charge_rate*100}% of capital cost\n"
            output += f"Energy Cost:                  {energy_cost_paise} paise/kWh = Rs. {energy_cost_rs}/kWh\n"
            output += f"\nLoad Cycle:\n"
            output += f"  - Full Load ({S_rated} kVA):     {hours_full} hours/year\n"
            output += f"  - Half Load ({S_rated/2} kVA):   {hours_half} hours/year\n"
            output += f"  - Light Load ({light_load_kva} kVA):  {hours_light} hours/year\n"
            output += "\n" + "="*80 + "\n\n"

            # Calculate output power at full load
            P_out_full = S_rated * pf  # kW

            # Calculate copper losses at full load
            # At full load: efficiency = P_out / (P_out + P_iron + P_copper_full)
            # P_copper_full = P_out/eff - P_out - P_iron

            copper_loss_full_a = P_out_full / eff_a - P_out_full - iron_loss_a
            copper_loss_full_b = P_out_full / eff_b - P_out_full - iron_loss_b

            output += "STEP 1: CALCULATE COPPER LOSSES AT FULL LOAD\n"
            output += "-"*80 + "\n"
            output += f"Output power at full load = {S_rated} × {pf} = {P_out_full} kW\n\n"

            output += "For Tender A:\n"
            output += f"  Total losses at full load = P_out/η - P_out = {P_out_full}/{eff_a} - {P_out_full}\n"
            output += f"                             = {P_out_full/eff_a:.3f} - {P_out_full} = {P_out_full/eff_a - P_out_full:.3f} kW\n"
            output += f"  Copper loss (full load) = Total losses - Iron loss\n"
            output += f"                          = {P_out_full/eff_a - P_out_full:.3f} - {iron_loss_a}\n"
            output += f"                          = {copper_loss_full_a:.3f} kW\n\n"

            output += "For Tender B:\n"
            output += f"  Total losses at full load = {P_out_full}/{eff_b} - {P_out_full}\n"
            output += f"                             = {P_out_full/eff_b:.3f} - {P_out_full} = {P_out_full/eff_b - P_out_full:.3f} kW\n"
            output += f"  Copper loss (full load) = {P_out_full/eff_b - P_out_full:.3f} - {iron_loss_b}\n"
            output += f"                          = {copper_loss_full_b:.3f} kW\n\n"

            # Calculate losses at different loads
            # Copper loss varies as square of load ratio
            output += "\nSTEP 2: CALCULATE LOSSES AT DIFFERENT LOAD CONDITIONS\n"
            output += "-"*80 + "\n"
            output += "Note: Copper loss ∝ (load)², Iron loss remains constant\n\n"

            # Full load losses
            total_loss_full_a = iron_loss_a + copper_loss_full_a
            total_loss_full_b = iron_loss_b + copper_loss_full_b

            # Half load losses (copper loss = (0.5)² × full load copper loss)
            copper_loss_half_a = copper_loss_full_a * (0.5)**2
            copper_loss_half_b = copper_loss_full_b * (0.5)**2
            total_loss_half_a = iron_loss_a + copper_loss_half_a
            total_loss_half_b = iron_loss_b + copper_loss_half_b

            # Light load losses
            load_ratio_light = light_load_kva / S_rated
            copper_loss_light_a = copper_loss_full_a * load_ratio_light**2
            copper_loss_light_b = copper_loss_full_b * load_ratio_light**2
            total_loss_light_a = iron_loss_a + copper_loss_light_a
            total_loss_light_b = iron_loss_b + copper_loss_light_b

            output += f"Tender A:\n"
            output += f"  Full Load ({S_rated} kVA):  Iron loss = {iron_loss_a} kW, "\
                     f"Copper loss = {copper_loss_full_a:.3f} kW, Total = {total_loss_full_a:.3f} kW\n"
            output += f"  Half Load ({S_rated/2} kVA):  Iron loss = {iron_loss_a} kW, "\
                     f"Copper loss = {copper_loss_half_a:.3f} kW, Total = {total_loss_half_a:.3f} kW\n"
            output += f"  Light Load ({light_load_kva} kVA): Iron loss = {iron_loss_a} kW, "\
                     f"Copper loss = {copper_loss_light_a:.3f} kW, Total = {total_loss_light_a:.3f} kW\n\n"

            output += f"Tender B:\n"
            output += f"  Full Load ({S_rated} kVA):  Iron loss = {iron_loss_b} kW, "\
                     f"Copper loss = {copper_loss_full_b:.3f} kW, Total = {total_loss_full_b:.3f} kW\n"
            output += f"  Half Load ({S_rated/2} kVA):  Iron loss = {iron_loss_b} kW, "\
                     f"Copper loss = {copper_loss_half_b:.3f} kW, Total = {total_loss_half_b:.3f} kW\n"
            output += f"  Light Load ({light_load_kva} kVA): Iron loss = {iron_loss_b} kW, "\
                     f"Copper loss = {copper_loss_light_b:.3f} kW, Total = {total_loss_light_b:.3f} kW\n\n"

            # Calculate annual energy losses
            output += "\nSTEP 3: CALCULATE ANNUAL ENERGY LOSSES\n"
            output += "-"*80 + "\n"

            annual_loss_a = (total_loss_full_a * hours_full +
                           total_loss_half_a * hours_half +
                           total_loss_light_a * hours_light)

            annual_loss_b = (total_loss_full_b * hours_full +
                           total_loss_half_b * hours_half +
                           total_loss_light_b * hours_light)

            output += f"Tender A:\n"
            output += f"  Annual energy loss = ({total_loss_full_a:.3f} × {hours_full}) + "\
                     f"({total_loss_half_a:.3f} × {hours_half}) + ({total_loss_light_a:.3f} × {hours_light})\n"
            output += f"                     = {annual_loss_a:.2f} kWh/year\n\n"

            output += f"Tender B:\n"
            output += f"  Annual energy loss = ({total_loss_full_b:.3f} × {hours_full}) + "\
                     f"({total_loss_half_b:.3f} × {hours_half}) + ({total_loss_light_b:.3f} × {hours_light})\n"
            output += f"                     = {annual_loss_b:.2f} kWh/year\n\n"

            # Calculate annual energy cost
            output += "\nSTEP 4: CALCULATE ANNUAL ENERGY COST\n"
            output += "-"*80 + "\n"

            annual_energy_cost_a = annual_loss_a * energy_cost_rs
            annual_energy_cost_b = annual_loss_b * energy_cost_rs

            output += f"Tender A: {annual_loss_a:.2f} kWh/year × Rs. {energy_cost_rs}/kWh = Rs. {annual_energy_cost_a:.2f}/year\n"
            output += f"Tender B: {annual_loss_b:.2f} kWh/year × Rs. {energy_cost_rs}/kWh = Rs. {annual_energy_cost_b:.2f}/year\n\n"

            # Calculate annual capital charges
            output += "\nSTEP 5: CALCULATE ANNUAL CAPITAL CHARGES\n"
            output += "-"*80 + "\n"

            annual_capital_charge_diff = cost_diff * annual_charge_rate

            output += f"Additional cost of Tender B = Rs. {cost_diff}\n"
            output += f"Annual capital charges on difference = Rs. {cost_diff} × {annual_charge_rate*100}%\n"
            output += f"                                     = Rs. {annual_capital_charge_diff:.2f}/year\n\n"

            # Total annual cost comparison
            output += "\nSTEP 6: TOTAL ANNUAL COST COMPARISON\n"
            output += "-"*80 + "\n"

            # Taking Tender A as reference (cost = 0 additional)
            total_cost_a = annual_energy_cost_a  # Only energy cost
            total_cost_b = annual_capital_charge_diff + annual_energy_cost_b  # Capital + energy

            output += f"Tender A:\n"
            output += f"  Annual energy cost        = Rs. {annual_energy_cost_a:.2f}\n"
            output += f"  Annual capital charges    = Rs. 0.00 (reference)\n"
            output += f"  TOTAL ANNUAL COST         = Rs. {total_cost_a:.2f}\n\n"

            output += f"Tender B:\n"
            output += f"  Annual energy cost        = Rs. {annual_energy_cost_b:.2f}\n"
            output += f"  Annual capital charges    = Rs. {annual_capital_charge_diff:.2f}\n"
            output += f"  TOTAL ANNUAL COST         = Rs. {total_cost_b:.2f}\n\n"

            # Determine winner and savings
            output += "\n" + "="*80 + "\n"
            output += "FINAL RESULT\n"
            output += "="*80 + "\n\n"

            if total_cost_a < total_cost_b:
                winner = "TENDER A"
                savings = total_cost_b - total_cost_a
                output += f"★ TENDER A IS BETTER ★\n\n"
                output += f"Annual savings by choosing Tender A = Rs. {total_cost_b:.2f} - Rs. {total_cost_a:.2f}\n"
                output += f"                                     = Rs. {savings:.2f}/year\n\n"
            else:
                winner = "TENDER B"
                savings = total_cost_a - total_cost_b
                output += f"★ TENDER B IS BETTER ★\n\n"
                output += f"Annual savings by choosing Tender B = Rs. {total_cost_a:.2f} - Rs. {total_cost_b:.2f}\n"
                output += f"                                     = Rs. {savings:.2f}/year\n\n"

            output += f"Summary:\n"
            output += f"  - Winner: {winner}\n"
            output += f"  - Annual Savings: Rs. {savings:.2f}\n"
            output += f"  - Energy Savings: {annual_loss_a - annual_loss_b:.2f} kWh/year\n"

            if savings > 0:
                payback_years = cost_diff / savings if winner == "TENDER B" else float('inf')
                if payback_years < 100:
                    output += f"  - Payback Period: {payback_years:.2f} years\n"

            output += "\n" + "="*80 + "\n"

            self.tender_results.insert(1.0, output)
            self.status_bar.config(text=f"Analysis Complete - {winner} is better with Rs. {savings:.2f} annual savings")

        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
            self.status_bar.config(text="Error in calculation")

    def transformer_ode_system(self, t, y, V0, omega, R, L, R_load):
        """
        Differential equations for transformer circuit
        y[0] = flux (Wb)
        y[1] = current (A)
        """
        flux = y[0]
        current = y[1]

        # Applied voltage
        V_applied = V0 * np.sin(omega * t)

        # Total resistance
        R_total = R + R_load

        # Differential equations:
        # dflux/dt = V_applied - R_total * current
        # di/dt = (V_applied - R_total * current) / L

        dflux_dt = V_applied - R_total * current
        di_dt = (V_applied - R_total * current - flux) / L

        return [dflux_dt, di_dt]

    def euler_method(self, f, t_span, y0, num_points, args=()):
        """Simple Euler method for ODE solving"""
        t_start, t_end = t_span
        dt = (t_end - t_start) / num_points

        t_values = np.linspace(t_start, t_end, num_points)
        y_values = np.zeros((num_points, len(y0)))
        y_values[0] = y0

        for i in range(1, num_points):
            t = t_values[i-1]
            y = y_values[i-1]
            dy = f(t, y, *args)
            y_values[i] = y + dt * np.array(dy)

        return t_values, y_values

    def start_simulation(self):
        """Start the dynamic simulation"""
        if self.simulation_running:
            return

        self.simulation_running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_bar.config(text="Simulation running...")

        # Clear previous data
        self.time_data = []
        self.flux_data = []
        self.current_data = []
        self.voltage_data = []
        self.power_data = []

        # Run simulation in separate thread
        self.simulation_thread = threading.Thread(target=self.run_simulation)
        self.simulation_thread.start()

    def run_simulation(self):
        """Run the ODE simulation"""
        try:
            # Get parameters
            V0 = self.sim_voltage.get()
            f = self.sim_frequency.get()
            omega = 2 * np.pi * f
            R = self.sim_resistance.get()
            L = self.sim_inductance.get()
            R_load = self.sim_load.get()
            t_end = self.sim_time.get()

            # Initial conditions
            y0 = [0.0, 0.0]  # [flux, current]

            solver_method = self.solver_method.get()

            if solver_method == "Euler":
                # Use custom Euler method
                num_points = int(t_end * 10000)
                t_values, y_values = self.euler_method(
                    self.transformer_ode_system,
                    (0, t_end),
                    y0,
                    num_points,
                    args=(V0, omega, R, L, R_load)
                )
                flux_values = y_values[:, 0]
                current_values = y_values[:, 1]
            else:
                # Use scipy's solve_ivp
                solution = solve_ivp(
                    self.transformer_ode_system,
                    (0, t_end),
                    y0,
                    method=solver_method,
                    args=(V0, omega, R, L, R_load),
                    dense_output=True,
                    max_step=t_end/1000
                )

                t_values = np.linspace(0, t_end, 5000)
                y_values = solution.sol(t_values)
                flux_values = y_values[0]
                current_values = y_values[1]

            # Calculate voltage and power
            voltage_values = V0 * np.sin(omega * t_values)
            power_values = voltage_values * current_values

            # Store data
            self.time_data = t_values
            self.flux_data = flux_values
            self.current_data = current_values
            self.voltage_data = voltage_values
            self.power_data = power_values

            # Update plots
            self.update_plots()

        except Exception as e:
            print(f"Simulation error: {e}")
        finally:
            self.simulation_running = False
            self.root.after(100, self.simulation_complete)

    def update_plots(self):
        """Update the visualization plots"""
        try:
            # Clear previous plots
            self.ax1.clear()
            self.ax2.clear()
            self.ax3.clear()

            # Plot flux
            self.ax1.plot(self.time_data, self.flux_data, 'b-', linewidth=1.5)
            self.ax1.set_ylabel('Flux (Wb)', fontsize=10)
            self.ax1.set_title('Magnetic Flux vs Time', fontsize=11, fontweight='bold')
            self.ax1.grid(True, alpha=0.3)

            # Plot current
            self.ax2.plot(self.time_data, self.current_data, 'r-', linewidth=1.5)
            self.ax2.set_ylabel('Current (A)', fontsize=10)
            self.ax2.set_title('Current vs Time', fontsize=11, fontweight='bold')
            self.ax2.grid(True, alpha=0.3)

            # Plot power
            self.ax3.plot(self.time_data, self.power_data, 'g-', linewidth=1.5)
            self.ax3.set_ylabel('Power (W)', fontsize=10)
            self.ax3.set_xlabel('Time (s)', fontsize=10)
            self.ax3.set_title('Instantaneous Power vs Time', fontsize=11, fontweight='bold')
            self.ax3.grid(True, alpha=0.3)

            self.sim_figure.tight_layout()
            self.sim_canvas.draw()

        except Exception as e:
            print(f"Plot update error: {e}")

    def simulation_complete(self):
        """Called when simulation completes"""
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_bar.config(text=f"Simulation complete - {len(self.time_data)} points calculated")

    def stop_simulation(self):
        """Stop the running simulation"""
        self.simulation_running = False
        self.status_bar.config(text="Simulation stopped")

    def reset_simulation(self):
        """Reset the simulation"""
        self.simulation_running = False
        self.time_data = []
        self.flux_data = []
        self.current_data = []
        self.voltage_data = []
        self.power_data = []

        # Clear plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        self.ax1.set_ylabel('Flux (Wb)', fontsize=10)
        self.ax1.grid(True, alpha=0.3)

        self.ax2.set_ylabel('Current (A)', fontsize=10)
        self.ax2.grid(True, alpha=0.3)

        self.ax3.set_ylabel('Power (W)', fontsize=10)
        self.ax3.set_xlabel('Time (s)', fontsize=10)
        self.ax3.grid(True, alpha=0.3)

        self.sim_figure.tight_layout()
        self.sim_canvas.draw()

        self.status_bar.config(text="Simulation reset")

    def calculate_transformer_model(self):
        """Calculate transformer equivalent circuit parameters"""
        try:
            self.model_results.delete(1.0, tk.END)

            # Get parameters
            S_rated = self.model_power.get()  # kVA
            V1 = self.model_v1.get()  # Primary voltage
            V2 = self.model_v2.get()  # Secondary voltage
            R1 = self.model_r1.get()  # Primary resistance
            R2 = self.model_r2.get()  # Secondary resistance
            X1 = self.model_x1.get()  # Primary reactance
            X2 = self.model_x2.get()  # Secondary reactance
            pf = self.model_pf.get()  # Power factor
            load_pct = self.model_load_pct.get() / 100  # Load percentage

            output = "="*80 + "\n"
            output += "TRANSFORMER EQUIVALENT CIRCUIT ANALYSIS\n"
            output += "="*80 + "\n\n"

            output += "TRANSFORMER SPECIFICATIONS:\n"
            output += "-"*80 + "\n"
            output += f"Rated Power:          {S_rated} kVA\n"
            output += f"Primary Voltage:      {V1} V\n"
            output += f"Secondary Voltage:    {V2} V\n"
            output += f"Transformation Ratio: {V1/V2:.4f}\n\n"

            output += "CIRCUIT PARAMETERS:\n"
            output += "-"*80 + "\n"
            output += f"Primary:   R1 = {R1} Ω,  X1 = {X1} Ω,  Z1 = {np.sqrt(R1**2 + X1**2):.4f} Ω\n"
            output += f"Secondary: R2 = {R2} Ω,  X2 = {X2} Ω,  Z2 = {np.sqrt(R2**2 + X2**2):.4f} Ω\n\n"

            # Calculate transformation ratio
            a = V1 / V2

            # Referred secondary parameters to primary
            R2_ref = R2 * a**2
            X2_ref = X2 * a**2

            # Equivalent impedance
            R_eq = R1 + R2_ref
            X_eq = X1 + X2_ref
            Z_eq = np.sqrt(R_eq**2 + X_eq**2)

            output += "EQUIVALENT CIRCUIT (referred to primary):\n"
            output += "-"*80 + "\n"
            output += f"R2' = R2 × a² = {R2} × {a:.4f}² = {R2_ref:.4f} Ω\n"
            output += f"X2' = X2 × a² = {X2} × {a:.4f}² = {X2_ref:.4f} Ω\n"
            output += f"R_eq = R1 + R2' = {R1} + {R2_ref:.4f} = {R_eq:.4f} Ω\n"
            output += f"X_eq = X1 + X2' = {X1} + {X2_ref:.4f} = {X_eq:.4f} Ω\n"
            output += f"Z_eq = √(R_eq² + X_eq²) = {Z_eq:.4f} Ω\n\n"

            # Load calculations
            S_load = S_rated * load_pct  # kVA
            P_load = S_load * pf  # kW

            # Current
            I2_rated = (S_rated * 1000) / V2  # Secondary current at rated load
            I2 = I2_rated * load_pct  # Actual secondary current
            I1 = I2 / a  # Primary current (approximately)

            output += f"LOAD ANALYSIS ({load_pct*100}% load, pf = {pf}):\n"
            output += "-"*80 + "\n"
            output += f"Load Power:           {S_load} kVA,  {P_load} kW\n"
            output += f"Secondary Current:    {I2:.2f} A\n"
            output += f"Primary Current:      {I1:.2f} A\n\n"

            # Voltage drop
            cos_phi = pf
            sin_phi = np.sqrt(1 - pf**2)

            V_drop = I1 * (R_eq * cos_phi + X_eq * sin_phi)
            V_drop_pct = (V_drop / V1) * 100

            output += "VOLTAGE REGULATION:\n"
            output += "-"*80 + "\n"
            output += f"Voltage drop = I1 × (R_eq×cosφ + X_eq×sinφ)\n"
            output += f"             = {I1:.2f} × ({R_eq:.4f}×{cos_phi} + {X_eq:.4f}×{sin_phi:.4f})\n"
            output += f"             = {V_drop:.2f} V\n"
            output += f"Voltage regulation = {V_drop_pct:.3f}%\n\n"

            # Losses
            copper_loss = I1**2 * R_eq / 1000  # kW

            output += "LOSSES:\n"
            output += "-"*80 + "\n"
            output += f"Copper loss = I1² × R_eq = {I1:.2f}² × {R_eq:.4f} = {copper_loss:.4f} kW\n"

            # Efficiency
            total_loss = copper_loss  # Simplified (not including iron loss here)
            efficiency = (P_load / (P_load + total_loss)) * 100

            output += f"\nEFFICIENCY:\n"
            output += "-"*80 + "\n"
            output += f"Output power:    {P_load:.3f} kW\n"
            output += f"Copper loss:     {copper_loss:.4f} kW\n"
            output += f"Efficiency:      {efficiency:.3f}%\n\n"

            output += "="*80 + "\n"

            self.model_results.insert(1.0, output)
            self.status_bar.config(text=f"Model analysis complete - Efficiency: {efficiency:.2f}%")

        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
            self.status_bar.config(text="Error in model calculation")

    def on_window_resize(self, event):
        """Handle window resize for auto-scaling"""
        # Only update if it's the root window being resized
        if event.widget == self.root:
            try:
                # Update canvas if it exists
                if hasattr(self, 'sim_canvas'):
                    self.sim_figure.tight_layout()
                    self.sim_canvas.draw_idle()
            except:
                pass

    def reset_all(self):
        """Reset all parameters to default"""
        self.stop_simulation()
        self.reset_simulation()
        self.tender_results.delete(1.0, tk.END)
        self.model_results.delete(1.0, tk.END)
        self.status_bar.config(text="All data reset")

    def clear_results(self):
        """Clear all results"""
        self.tender_results.delete(1.0, tk.END)
        self.model_results.delete(1.0, tk.END)
        self.status_bar.config(text="Results cleared")

    def export_data(self):
        """Export simulation data"""
        if len(self.time_data) == 0:
            messagebox.showinfo("Info", "No simulation data to export")
            return

        try:
            with open('simulation_data.csv', 'w') as f:
                f.write("Time(s),Flux(Wb),Current(A),Voltage(V),Power(W)\n")
                for i in range(len(self.time_data)):
                    f.write(f"{self.time_data[i]},{self.flux_data[i]},{self.current_data[i]},"
                           f"{self.voltage_data[i]},{self.power_data[i]}\n")
            messagebox.showinfo("Success", "Data exported to simulation_data.csv")
            self.status_bar.config(text="Data exported successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Export error: {str(e)}")

    def show_about(self):
        """Show about dialog"""
        about_text = """
Electrical Engineering Laboratory
Transformer Analysis Tool

Version 1.0

Features:
• Transformer Tender Economic Analysis
• Dynamic Transformer Modeling
• Real-time ODE Simulation (RK45, Euler, RK23)
• Professional Visualization
• Auto-scaling Interface

Developed for educational and professional use
in electrical engineering applications.
        """
        messagebox.showinfo("About", about_text)


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = TransformerLab(root)
    root.mainloop()


if __name__ == "__main__":
    main()
