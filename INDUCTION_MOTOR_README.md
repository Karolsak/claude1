# Three-Phase Induction Motor Analysis Lab

## Problem Solution

### Given Data
- **Three-phase, Y-connected cage induction motor**
- Rated Power: 500 kW
- Frequency: 50 Hz
- Line-to-Line Voltage: 6 kV
- Rated Current: 57 A
- Rated Speed: 980 rpm

### No-Load Test Results
- Input Voltage (L-L): 6 kV
- No-load Current: 17 A
- No-load Losses: 14 kW
- Rotational Losses: 3.5 kW

### Locked-Rotor Test Results
- Input Voltage (L-L): 380 V
- Line Current: 15 A
- Input Power: 1 kW
- Stator Resistance: 0.8 Ω

## Calculated Equivalent Circuit Parameters

### Methodology

#### 1. Synchronous Speed
```
n_sync = 120 × f / p = 120 × 50 / 6 = 1000 rpm
ω_sync = 2π × n_sync / 60 = 104.72 rad/s
```

#### 2. From No-Load Test

**Phase Voltage (Y-connection):**
```
V_phase = 6000 / √3 = 3464.1 V
```

**Core Losses:**
```
P_cu_noload = 3 × I₀² × R₁ = 3 × 17² × 0.8 = 693.6 W
P_core = P₀ - P_cu_noload - P_rot = 14000 - 693.6 - 3500 = 9806.4 W
```

**No-load Impedance:**
```
Z₀ = V_phase / I₀ = 3464.1 / 17 = 203.8 Ω
R₀ = P₀ / (3 × I₀²) = 14000 / (3 × 17²) = 16.16 Ω
X₀ = √(Z₀² - R₀²) = 203.16 Ω
```

#### 3. From Locked-Rotor Test

**Phase Voltage:**
```
V_phase_locked = 380 / √3 = 219.4 V
```

**Locked Impedance:**
```
Z_locked = V_phase_locked / I_locked = 219.4 / 15 = 14.63 Ω
R_locked = P_locked / (3 × I_locked²) = 1000 / (3 × 15²) = 1.48 Ω
X_locked = √(Z_locked² - R_locked²) = 14.56 Ω
```

#### 4. Equivalent Circuit Parameters

**Rotor Resistance:**
```
R₂ = R_locked - R₁ = 1.48 - 0.8 = 0.68 Ω
```

**Leakage Reactances (assuming X₁ = X₂):**
```
X₁ = X₂ = X_locked / 2 = 14.56 / 2 = 7.28 Ω
```

**Magnetizing Reactance:**
```
X_m ≈ X₀ - X₁ = 203.16 - 7.28 = 195.88 Ω
```

**Core Loss Resistance:**
```
R_c = V_phase² / (P_core / 3) = 3464.1² / 3268.8 = 3672 Ω
```

### Final Results

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Stator Resistance | R₁ | 0.8000 | Ω |
| Rotor Resistance | R₂ | 0.6800 | Ω |
| Stator Reactance | X₁ | 7.2800 | Ω |
| Rotor Reactance | X₂ | 7.2800 | Ω |
| Magnetizing Reactance | X_m | 195.88 | Ω |
| Core Loss Resistance | R_c | 3672 | Ω |

## Lab Features

### 1. Main Menu System
- **File Menu**: Reset all, Exit
- **Analysis Menu**:
  - Equivalent Circuit Parameters
  - Performance Curves
  - Dynamic Simulation
- **Help Menu**: About

### 2. Equivalent Circuit Analysis
- Displays all calculated parameters
- Shows comprehensive test results
- Formatted engineering report

### 3. Performance Curves
Four comprehensive plots:
- **Torque-Speed Characteristic**: Shows motor torque vs. speed
- **Current-Speed Characteristic**: Stator current variation
- **Power-Speed Characteristic**: Output power curve
- **Efficiency & Power Factor**: Combined performance metrics

### 4. Dynamic Simulation

#### Mathematical Model
The motor dynamics are governed by the differential equation:

```
J × dω/dt = T_em - T_load - B × ω
```

Where:
- J = Moment of inertia (kg·m²)
- ω = Mechanical angular velocity (rad/s)
- T_em = Electromagnetic torque (N·m)
- T_load = Load torque (N·m)
- B = Friction coefficient (N·m·s/rad)

#### ODE Solvers

**1. RK45 (Runge-Kutta 4th/5th Order)**
- High accuracy adaptive solver
- Automatically adjusts step size
- Best for precise simulations
- Equations:
  ```
  k₁ = f(t, ω)
  k₂ = f(t + dt/2, ω + dt×k₁/2)
  k₃ = f(t + dt/2, ω + dt×k₂/2)
  k₄ = f(t + dt, ω + dt×k₃)
  ω_new = ω + dt × (k₁ + 2k₂ + 2k₃ + k₄) / 6
  ```

**2. Euler Method**
- Simple first-order solver
- Fixed step size
- Faster but less accurate
- Equation:
  ```
  ω_new = ω + dt × f(t, ω)
  ```

#### Control Panel Features
- **Load Torque Slider**: 0 - 5000 N·m
- **Supply Voltage Slider**: 0 - 120% of rated
- **Inertia Slider**: 10 - 200 kg·m²
- **Solver Selection**: RK45 or Euler
- **Control Buttons**: Start, Stop, Reset

#### Real-Time Visualization
Three synchronized plots:
1. **Motor Speed** (rpm vs. time)
2. **Electromagnetic Torque** (N·m vs. time) with load torque reference
3. **Stator Current** (A vs. time)

#### Status Display
Real-time monitoring:
- Current speed (rpm)
- Electromagnetic torque (N·m)
- Stator current (A)
- Output power (kW)
- Slip (%)
- Simulation time (s)

### 5. Auto-Scaling
- Window resize handling
- Automatic plot adjustment
- Responsive layout

## Installation & Usage

### Requirements
```bash
pip install numpy matplotlib
```

### Running the Lab
```bash
python3 induction_motor_lab.py
```

### Quick Start Guide

1. **Launch Application**: Run the Python script
2. **View Equivalent Circuit**: Menu → Analysis → Equivalent Circuit
3. **Analyze Performance**: Menu → Analysis → Performance Curves
4. **Run Simulation**:
   - Menu → Analysis → Dynamic Simulation
   - Adjust load torque, voltage, and inertia
   - Select ODE solver (RK45 recommended)
   - Click "Start Simulation"
   - Observe real-time motor behavior
   - Adjust parameters during simulation
   - Click "Stop" to pause, "Reset" to restart

## Practical Applications

### 1. Motor Starting Analysis
- Observe high inrush current
- Monitor torque development
- Analyze acceleration time

### 2. Load Impact Studies
- Change load torque during simulation
- Observe transient response
- Study stability margins

### 3. Voltage Variation Effects
- Reduce voltage to simulate grid sag
- Observe torque reduction (proportional to V²)
- Study motor behavior under weak grid

### 4. Inertia Effects
- Compare high vs. low inertia systems
- Analyze acceleration profiles
- Design flywheel requirements

### 5. Solver Comparison
- Compare RK45 vs. Euler accuracy
- Understand numerical methods
- Educational tool for control engineers

## Technical Details

### Thevenin Equivalent Circuit
The lab uses Thevenin equivalent for accurate motor modeling:

```
Z_th = R₁ + (jX₁ || (R_c || jX_m))
V_th = V_phase × (R_c || jX_m) / (jX₁ + (R_c || jX_m))
```

### Electromagnetic Torque Calculation
```
I₂ = V_th / (R_th + R₂/s + jX_th)
P_airgap = 3 × I₂² × R₂/s
T_em = P_airgap / ω_sync
```

### Performance Metrics
- **Slip**: s = (ω_sync - ω_m) / ω_sync
- **Output Power**: P_out = P_airgap × (1 - s) - P_rot
- **Efficiency**: η = P_out / P_in
- **Power Factor**: pf = P_in / (√3 × V_L × I_L)

## Advanced Features

1. **Real-time Parameter Adjustment**: Change load, voltage, and inertia during simulation
2. **Multiple ODE Solvers**: Educational comparison of numerical methods
3. **Comprehensive Visualization**: Multiple synchronized plots
4. **Professional UI**: Industry-standard layout and controls
5. **Auto-scaling**: Responsive design for different screen sizes
6. **Status Monitoring**: Real-time display of all motor quantities

## Educational Value

This lab provides:
- **Theoretical Understanding**: Equivalent circuit parameters from test data
- **Practical Analysis**: Performance curves for motor selection
- **Dynamic Behavior**: Transient response simulation
- **Numerical Methods**: ODE solver comparison
- **Engineering Skills**: GUI design, data visualization, real-time control

## Future Enhancements

Potential additions:
- Vector control simulation
- Fault analysis (broken rotor bars, unbalanced supply)
- Harmonic analysis
- Thermal modeling
- Multi-motor systems
- Data export functionality
- Parameter optimization tools

## Author Notes

This comprehensive lab combines:
- Rigorous electrical engineering calculations
- Modern Python GUI development
- Real-time numerical simulation
- Professional visualization

Perfect for:
- Electrical engineering students
- Motor control engineers
- Research and development
- Industrial training programs

## License

Educational use - Open source for learning and teaching purposes.
