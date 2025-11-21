# Advanced Electrical Engineering Laboratory

A comprehensive Python + Tkinter application for electrical engineering calculations and dynamic simulations.

## Features

### 1. **Example Calculations**
- **Example 50.3**: Plant Depreciation Analysis
  - Straight-line depreciation method
  - Sinking fund method
  - Comparative analysis

- **Example 50.4**: Load and Energy Consumption Analysis
  - Connected load calculation
  - Daily and monthly energy consumption
  - Load factor and demand factor analysis

### 2. **Dynamic Simulations**

#### DC Motor Simulation
- Real-time ODE solver (RK45, Euler, RK23, DOP853)
- Differential equations for armature current and speed
- RMS voltage and current calculations
- Torque and power analysis
- Interactive parameter adjustment with sliders

#### Induction Motor Simulation
- Three-phase induction motor performance analysis
- Torque-speed characteristics
- Efficiency and power factor curves
- Starting and maximum torque calculations

#### RLC Circuit Analysis
- Series and parallel RLC configurations
- Step response analysis
- Transient analysis with multiple ODE solvers
- Resonance frequency and quality factor calculations
- Phase diagrams

#### Power System Transient Analysis
- Swing equation simulation
- Three-phase fault analysis
- Line-to-ground and line-to-line faults
- Frequency and voltage transients
- Stability assessment

## Installation

### Prerequisites

```bash
# Install required Python packages
pip install numpy scipy matplotlib

# For Debian/Ubuntu (if tkinter is not available)
sudo apt-get install python3-tk

# For macOS
brew install python-tk

# For Windows
# tkinter comes pre-installed with Python
```

### Dependencies

- **Python 3.7+**
- **tkinter**: GUI framework (usually comes with Python)
- **numpy**: Numerical computations
- **scipy**: Scientific computing and ODE solvers
- **matplotlib**: Data visualization

## Usage

### Running the Application

```bash
python3 electrical_engineering_lab.py
```

### Main Menu

The application presents a main menu with six options:

1. **Example 50.3: Depreciation Analysis**
   - Input initial cost, salvage value, useful life, and interest rate
   - Calculate book value using two different methods
   - Compare results

2. **Example 50.4: Load & Energy Analysis**
   - Enter connected load details (lamps and heaters)
   - Specify usage patterns
   - Calculate energy consumption and load factor

3. **DC Motor Dynamic Simulation**
   - Adjust motor parameters using sliders
   - Select ODE solver (RK45, Euler, RK23, DOP853)
   - Visualize current, speed, voltage, and torque responses
   - Real-time simulation with start/stop/reset controls

4. **Induction Motor Simulation**
   - Configure motor parameters
   - Calculate performance characteristics
   - View torque-speed curves and efficiency plots

5. **RLC Circuit Analysis**
   - Choose circuit configuration (Series/Parallel)
   - Adjust R, L, C values
   - Simulate transient response
   - View phase diagrams

6. **Power System Transient Analysis**
   - Select fault type
   - Configure system parameters
   - Simulate power angle, frequency, and voltage transients
   - Assess system stability

## Technical Details

### Differential Equations

#### DC Motor
```
di/dt = (V - Ra*i - Ke*ω) / La
dω/dt = (Kt*i - TL - B*ω) / J
```

#### RLC Circuit (Series)
```
L*(d²i/dt²) + R*(di/dt) + i/C = dV/dt
```

#### Power System (Swing Equation)
```
(2H/ω₀)*(d²δ/dt²) + D*(dδ/dt) = Pm - Pe
```

### ODE Solvers

1. **RK45**: Runge-Kutta 4th/5th order adaptive solver (recommended)
2. **Euler**: Simple Euler method (fast but less accurate)
3. **RK23**: Runge-Kutta 2nd/3rd order adaptive solver
4. **DOP853**: 8th order Runge-Kutta method (high precision)

### RMS Values

All voltage and current calculations use RMS (Root Mean Square) values:
```
V_rms = V_peak / √2
I_rms = √(∫i²(t)dt / T)
```

## Features

### User Interface
- ✓ Modern, intuitive Tkinter GUI
- ✓ Interactive sliders for parameter adjustment
- ✓ Real-time visualization with matplotlib
- ✓ Responsive design with auto-scaling
- ✓ Start, Stop, Reset controls

### Calculations
- ✓ Accurate mathematical models
- ✓ Multiple ODE solvers
- ✓ RMS voltage and current calculations
- ✓ Comprehensive results display

### Visualization
- ✓ Multi-panel plotting
- ✓ Real-time graph updates
- ✓ Professional formatting
- ✓ Grid and labels
- ✓ Auto-scaling axes

## Example Results

### Example 50.3
- **Initial Cost**: Rs. 5,00,000
- **Salvage Value**: Rs. 1,00,000
- **Useful Life**: 20 years
- **Interest Rate**: 8%

**Results at 10 years:**
- Straight-line method: Rs. 3.00 Lakhs
- Sinking fund method: Rs. 3.73 Lakhs

### Example 50.4
- **Connected Load**: 2.6 kW (10×60W lamps + 2×1000W heaters)
- **Maximum Demand**: 1.5 kW
- **Daily Usage**: 8 lamps × 5h + 2 heaters × 3h
- **Monthly Energy**: 252 kWh
- **Load Factor**: 23.33%

## Practical Applications

1. **Educational Tool**: Learn electrical machine dynamics
2. **Design Analysis**: Evaluate motor and circuit performance
3. **System Studies**: Analyze power system transients
4. **Parameter Optimization**: Find optimal operating conditions
5. **Fault Analysis**: Study system behavior under faults

## Troubleshooting

### ImportError: No module named 'tkinter'
Install tkinter for your system (see Installation section)

### ImportError: No module named 'numpy'
```bash
pip install numpy scipy matplotlib
```

### Display Issues
The application requires a graphical environment. For headless servers, use:
```bash
# X11 forwarding (Linux/Mac)
ssh -X user@server

# Or use VNC/Remote Desktop
```

## File Structure

```
electrical_engineering_lab.py    # Main application
test_app.py                      # Test suite
README_ELECTRICAL_LAB.md         # This file
```

## System Requirements

- **OS**: Windows, macOS, Linux
- **Python**: 3.7 or higher
- **RAM**: 512 MB minimum
- **Display**: Required for GUI

## License

Educational and research use.

## Author

Created for comprehensive electrical engineering education and practical applications.

## Version

1.0.0 - Complete implementation with all features

---

**Note**: All simulations use standard electrical engineering equations and conventions. RMS values are used throughout for practical applicability.
