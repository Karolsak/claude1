# Quick Start Guide - Induction Motor Simulator

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

or install individually:

```bash
pip install numpy scipy matplotlib
```

### 2. Install Tkinter (if needed)

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
Tkinter is usually included with Python. If not:
```bash
brew install python-tk
```

**Windows:**
Tkinter is included with Python installer by default.

## Running the Application

### Option 1: Full GUI Application (Recommended)

```bash
python3 induction_motor_simulator.py
```

This opens the full GUI with three tabs:
- **Static Analysis**: Solve the specific problem
- **Dynamic Simulation**: Real-time motor simulation with ODE solvers
- **Multi-Physics**: Thermal, mechanical, EM, and vibration analysis

### Option 2: Command-line Calculations Only

If Tkinter is not available or you just want to see the calculations:

```bash
python3 motor_calculations_standalone.py
```

This displays the complete solution to the problem in the terminal.

## Quick Tutorial

### Static Analysis Tab

1. **Launch the application** and you'll see the "Static Analysis" tab
2. **Input parameters** are pre-filled with the problem values:
   - Poles: 4
   - Voltage: 460 V
   - Frequency: 50 Hz
   - Current: 25 A
   - Power Factor: 0.85
   - Losses: Various values
3. **Click "Calculate"** to see results
4. **View results** in the right panel showing:
   - (a) Electromagnetic Power: ~14,931 W
   - (b) Mechanical Power: ~14,431 W
   - (c) Output Power: ~14,181 W
   - (d) Efficiency: ~83.76%
   - (e) Slip: ~0.0335 (3.35%), Speed: ~1,450 rpm
   - (f) Electromagnetic Torque: ~95.05 N·m
   - (g) Shaft Torque: ~93.41 N·m

### Dynamic Simulation Tab

1. **Switch to "Dynamic Simulation" tab**
2. **Adjust parameters:**
   - Simulation Time: 2.0 seconds (default)
   - Solver Method: RK45 (recommended) or Euler
   - Load Torque: Use slider (0-200 N·m)
   - Voltage: Adjust percentage (0-120%)
   - Frequency: Adjust Hz (10-100)
3. **Click "Start Simulation"** to run
4. **Observe real-time plots:**
   - Rotor speed vs time
   - Torque vs time
   - Current vs time
   - Power vs time
   - Flux linkage vs time
   - Efficiency vs time
5. **Use controls:**
   - "Stop" to halt simulation
   - "Reset" to clear plots

### Multi-Physics Analysis Tab

1. **Switch to "Multi-Physics Analysis" tab**
2. **Select analysis type:**
   - Thermal: Temperature rise and distribution
   - Mechanical Stress: Rotor stress analysis
   - Electromagnetic Field: Field distribution
   - Vibration: Frequency analysis
   - Combined Thermal-EM: Coupled analysis
3. **Adjust parameters:**
   - Ambient Temperature: 0-50°C
   - Cooling Coefficient: 1-50
4. **Click "Run Analysis"** to see results
5. **View visualizations** (4 plots per analysis)

## Understanding the Results

### Power Flow

```
Input Power (16,931 W)
    ↓
[Stator Loss: 1,000 W]
[Core Loss: 800 W]
[Stray Loss: 200 W]
    ↓
Electromagnetic Power (14,931 W)
    ↓
[Rotor Loss: 500 W]
    ↓
Mechanical Power (14,431 W)
    ↓
[Rotational Loss: 250 W]
    ↓
Output Power (14,181 W)
```

### Key Equations

**Input Power:**
```
P_in = √3 × V_LL × I × cos(φ)
```

**Electromagnetic Power:**
```
P_elm = P_in - P_stator - P_core - P_stray
```

**Slip:**
```
s = P_rotor / P_elm
```

**Speed:**
```
n = n_s × (1 - s)
n_s = 120 × f / poles
```

**Torque:**
```
T_elm = P_elm / ω_s
T_out = P_out / ω_m
```

## Troubleshooting

### "No module named 'tkinter'"
- Install python3-tk as shown in Installation section
- Or use standalone version: `python3 motor_calculations_standalone.py`

### "ModuleNotFoundError: No module named 'numpy'"
- Run: `pip install numpy scipy matplotlib`

### GUI doesn't display correctly
- Update matplotlib: `pip install --upgrade matplotlib`
- Check display settings if using remote connection

### Simulation runs slowly
- Reduce simulation time
- Use Euler method instead of RK45
- Increase time step in code (advanced)

### Window too small/large
- The window auto-scales, but you can manually resize
- Plots will adjust automatically

## Advanced Usage

### Modifying Motor Parameters

Edit the `MotorParameters` class in `induction_motor_simulator.py`:

```python
# Dynamic parameters (for simulation)
rs: float = 0.5      # Stator resistance (Ohms)
rr: float = 0.3      # Rotor resistance (Ohms)
ls: float = 0.01     # Stator inductance (H)
lr: float = 0.01     # Rotor inductance (H)
lm: float = 0.15     # Magnetizing inductance (H)
j: float = 0.5       # Moment of inertia (kg·m²)
b: float = 0.01      # Friction coefficient (N·m·s)
```

### Changing Simulation Settings

In the `run_dynamic_simulation` method, adjust:
- `dt=0.0001`: Time step (smaller = more accurate, slower)
- `t_span`: Simulation duration

### Exporting Data

Results can be exported (basic implementation provided).
Modify `export_multiphysics` method for custom exports.

## Features Summary

✅ **Static Analysis**
- Complete power flow analysis
- Efficiency calculation
- Slip and speed determination
- Torque calculations

✅ **Dynamic Simulation**
- d-q axis motor model
- RK45 and Euler ODE solvers
- Real-time visualization
- Adjustable parameters

✅ **Multi-Physics**
- Thermal analysis with heat transfer
- Mechanical stress (Von Mises)
- Electromagnetic field distribution
- Vibration frequency analysis
- Coupled thermal-EM simulation

✅ **GUI Features**
- Tabbed interface
- Interactive sliders
- Real-time plotting
- Auto-scaling windows
- Professional layout

## Files Included

1. **induction_motor_simulator.py** - Full GUI application
2. **motor_calculations_standalone.py** - CLI version
3. **requirements.txt** - Python dependencies
4. **README_MOTOR_SIMULATOR.md** - Detailed documentation
5. **QUICKSTART.md** - This file

## Next Steps

1. **Experiment with parameters** to see how they affect performance
2. **Try different analysis types** in Multi-Physics tab
3. **Compare RK45 vs Euler** solvers in dynamic simulation
4. **Modify the code** to add custom features
5. **Use for learning** about induction motor operation

## Support

For issues or questions:
- Check the README_MOTOR_SIMULATOR.md for detailed info
- Review the code comments
- Verify all dependencies are installed

## Educational Value

This simulator helps understand:
- Power flow in induction motors
- Effect of losses on efficiency
- Dynamic motor behavior
- Multi-physics interactions
- Numerical ODE solving
- GUI development with Python

---

**Enjoy exploring induction motor dynamics!**
