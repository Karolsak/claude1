# Advanced Induction Motor Simulator

## Overview
This is a comprehensive Python + Tkinter application for analyzing and simulating three-phase induction motors with multi-physics capabilities.

## Problem Solution

The application solves the following induction motor problem:

**Given:**
- Four-pole induction motor
- Line-to-line voltage: 460 V, 50 Hz, three-phase
- Current: 25 A at power factor 0.85 (lagging)
- Stator winding loss: 1000 W
- Rotor winding loss: 500 W
- Rotational losses: 250 W
- Core loss: 800 W
- Stray load loss: 200 W

**Calculated Results:**
- (a) Electromagnetic (air gap) power: ~15,179 W
- (b) Mechanical power: ~14,679 W
- (c) Output power: ~14,429 W
- (d) Efficiency: ~83.3%
- (e) Slip: ~0.0329 (3.29%), Operating speed: ~1,451 rpm
- (f) Electromagnetic torque: ~96.7 N·m
- (g) Shaft torque: ~95.0 N·m

## Features

### 1. Static Analysis Tab
- **Input Parameters**: Adjustable motor parameters (voltage, current, frequency, losses)
- **Power Analysis**: Calculates electromagnetic, mechanical, and output power
- **Efficiency Calculation**: Determines motor efficiency with loss breakdown
- **Speed Analysis**: Computes slip, synchronous speed, and operating speed
- **Torque Analysis**: Electromagnetic and shaft torque calculations
- **Comprehensive Results Display**: Formatted output with all calculations

### 2. Dynamic Simulation Tab
- **Real-time ODE Solvers**:
  - RK45 (Runge-Kutta 4-5): High accuracy adaptive solver
  - Euler: Simple forward integration method
- **d-q Axis Model**: Complete induction motor dynamic equations
- **Interactive Controls**:
  - Simulation time adjustment
  - Load torque slider (0-200 N·m)
  - Voltage control (0-120% rated)
  - Frequency control (10-100 Hz)
- **Real-time Visualization** (6 plots):
  1. Rotor Speed vs Time
  2. Electromagnetic Torque vs Time
  3. Stator Current vs Time
  4. Power (Input and Mechanical) vs Time
  5. Stator Flux Linkage vs Time
  6. Efficiency vs Time
- **Start/Stop/Reset Controls**: Full simulation control

### 3. Multi-Physics Analysis Tab

#### Thermal Analysis
- Temperature rise calculation with heat transfer
- Radial temperature distribution
- Loss distribution pie chart
- Thermal time constant analysis
- Adjustable ambient temperature and cooling coefficient

#### Mechanical Stress Analysis
- Centrifugal stress distribution in rotor
- Von Mises stress calculation
- Safety factor analysis
- Radial deformation calculation
- Material properties consideration

#### Electromagnetic Field Analysis
- 2D magnetic flux density distribution
- Magnetic field lines visualization
- Radial flux density profile
- Pole configuration effects
- Air gap field analysis

#### Vibration Analysis
- Time-domain vibration signals
- FFT frequency spectrum
- Mechanical and electrical frequency components
- Pole pass and slot pass frequencies
- RMS vibration calculation

#### Combined Thermal-Electromagnetic Analysis
- Iterative coupling between thermal and EM domains
- Temperature-dependent resistance effects
- Convergence analysis
- Coupled field distribution
- Loss-temperature feedback loop

## Requirements

```bash
pip install numpy scipy matplotlib tkinter
```

## Usage

### Running the Application

```bash
python3 induction_motor_simulator.py
```

### Using Static Analysis
1. Navigate to the "Static Analysis" tab
2. Adjust input parameters as needed
3. Click "Calculate" to see results
4. Results are displayed in a formatted text area

### Using Dynamic Simulation
1. Navigate to the "Dynamic Simulation" tab
2. Set simulation time (default: 2.0 seconds)
3. Choose solver method (RK45 or Euler)
4. Adjust sliders for:
   - Load Torque
   - Voltage percentage
   - Frequency
5. Click "Start Simulation" to run
6. Observe real-time plots
7. Click "Stop" to halt simulation
8. Click "Reset" to clear plots

### Using Multi-Physics Analysis
1. Navigate to the "Multi-Physics Analysis" tab
2. Select analysis type from dropdown:
   - Thermal
   - Mechanical Stress
   - Electromagnetic Field
   - Vibration
   - Combined Thermal-Electromagnetic
3. Adjust parameters (ambient temp, cooling coefficient)
4. Click "Run Analysis" to see results
5. Click "Export Results" to save data

## Technical Details

### Dynamic Model Equations

The simulator uses d-q axis transformation with the following state variables:
- i_ds, i_qs: Stator currents (d-q axes)
- i_dr, i_qr: Rotor currents (d-q axes)
- omega_r: Rotor angular velocity
- theta_r: Rotor angle

### Differential Equations

```
di_ds/dt = f(v_ds, i_ds, i_qs, i_dr, i_qr, omega_r)
di_qs/dt = f(v_qs, i_ds, i_qs, i_dr, i_qr, omega_r)
di_dr/dt = f(i_ds, i_qs, i_dr, i_qr, omega_r)
di_qr/dt = f(i_ds, i_qs, i_dr, i_qr, omega_r)
d(omega_r)/dt = (T_em - T_load - B*omega_r) / J
d(theta_r)/dt = omega_r
```

### Motor Parameters (Adjustable in Code)
- rs: Stator resistance (0.5 Ω)
- rr: Rotor resistance (0.3 Ω)
- ls: Stator inductance (0.01 H)
- lr: Rotor inductance (0.01 H)
- lm: Magnetizing inductance (0.15 H)
- j: Moment of inertia (0.5 kg·m²)
- b: Friction coefficient (0.01 N·m·s)

### GUI Features
- **Auto-scaling**: Window automatically adjusts to content
- **Responsive Design**: Grid-based layout adapts to window size
- **Tabbed Interface**: Organized into three main analysis sections
- **Real-time Plotting**: Matplotlib integration for live visualization
- **Thread-safe Simulation**: Dynamic simulation runs in separate thread

## Applications in Electrical Engineering

This simulator is practical for:
1. **Motor Selection**: Evaluate motor performance for specific applications
2. **Efficiency Analysis**: Identify losses and optimization opportunities
3. **Thermal Management**: Assess cooling requirements
4. **Vibration Diagnostics**: Detect mechanical and electrical issues
5. **Control System Design**: Test different operating conditions
6. **Educational Purposes**: Understand induction motor principles
7. **Research**: Multi-physics interaction studies
8. **Predictive Maintenance**: Analyze degradation effects

## Mathematical Models

### Power Flow
```
P_in → [Stator Loss, Core Loss] → P_elm → [Rotor Loss] → P_m → [Rotational Loss] → P_out
```

### Efficiency
```
η = P_out / P_in × 100%
```

### Slip
```
s = (n_s - n) / n_s = P_rotor_loss / P_elm
```

### Torque
```
T_elm = P_elm / ω_s
T_out = P_out / ω_m
```

## Advanced Features

1. **Multiple ODE Solvers**: Compare RK45 vs Euler methods
2. **Real-time Parameter Adjustment**: Change conditions during simulation
3. **Multi-physics Coupling**: Thermal-EM interaction modeling
4. **Comprehensive Visualization**: 15+ different plots and charts
5. **Professional UI**: Clean, organized interface with tooltips
6. **Data Export**: Save results for further analysis

## Troubleshooting

### Import Errors
- Ensure all required packages are installed
- Use Python 3.6 or higher

### Display Issues
- Check Tkinter installation: `python3 -m tkinter`
- Update matplotlib backend if needed

### Simulation Errors
- Verify input parameters are within reasonable ranges
- Reduce simulation time step for stiff problems
- Check for division by zero conditions

## Future Enhancements

Potential additions:
- Export to CSV/Excel
- Parameter optimization algorithms
- 3D field visualization
- Harmonic analysis
- Bearing fault detection
- Machine learning integration

## License

This educational tool is provided for learning and research purposes.

## Author

Created as an advanced electrical engineering simulation tool combining:
- Analytical motor calculations
- Dynamic differential equation solving
- Multi-physics modeling
- Professional GUI development
