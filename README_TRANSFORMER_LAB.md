# Electrical Engineering Laboratory - Transformer Analysis Tool

A comprehensive Python + Tkinter application for transformer analysis and dynamic simulation, designed for practical electrical engineering applications.

## Features

### 1. Transformer Tender Economic Analysis
- **Complete tender comparison** for transformer procurement decisions
- Calculates copper losses, iron losses, and efficiency
- Annual energy loss and cost analysis
- Capital cost comparison with payback period calculation
- Detailed step-by-step calculation results

### 2. Dynamic Transformer Simulation
- **Real-time ODE solver** with multiple methods:
  - RK45 (Runge-Kutta 4th/5th order) - High accuracy
  - Euler (Forward Euler) - Simple and fast
  - RK23 (Runge-Kutta 2nd/3rd order) - Balanced
- Interactive parameter adjustment with sliders:
  - Voltage amplitude (1000-33000 V)
  - Frequency (25-400 Hz)
  - Resistance (0.1-10 Ω)
  - Inductance (0.001-0.5 H)
  - Load resistance (10-1000 Ω)
- Real-time visualization of:
  - Magnetic flux vs time
  - Current vs time
  - Instantaneous power vs time

### 3. Transformer Model Analysis
- Equivalent circuit parameter calculation
- Voltage regulation analysis
- Efficiency calculation at various loads
- Referred impedance calculations
- Comprehensive loss analysis

### 4. Professional GUI Features
- **Auto-scaling**: Automatic width and height adjustment when window is resized
- **Tabbed interface** for easy navigation between modules
- **Interactive sliders** for real-time parameter adjustment
- **Start/Stop/Reset controls** for simulation
- **Export functionality** for simulation data
- **Professional styling** with custom color scheme
- **Responsive layout** that adapts to window size

## Installation

### Requirements
```bash
pip install numpy matplotlib scipy tkinter
```

Note: `tkinter` usually comes pre-installed with Python. If not available:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: Included with Python installation
- **Windows**: Included with Python installation

## Usage

### Running the Application
```bash
python3 transformer_engineering_lab.py
```

### Problem Solved

The application solves the following transformer tender problem:

**Problem Statement:**
Two tenders A and B for a 1000-kVA, 0.8 power factor transformer:
- **Tender A**: Full-load efficiency = 98.5%, Iron loss = 6 kW at rated voltage
- **Tender B**: 98.8% efficiency, Iron loss = 4 kW, costs Rs. 1,500 more than A

**Load Cycle:**
- 2000 hours per annum at full-load
- 600 hours at half-load
- 400 hours at 25 kVA

**Economic Parameters:**
- Annual charges for interest and depreciation: 12.5% of capital cost
- Energy cost: 3 paise per kWh

**Solution Approach:**
1. Calculate copper losses at full load for both tenders
2. Calculate total losses at different load conditions
3. Calculate annual energy losses
4. Calculate annual energy costs
5. Calculate annual capital charges
6. Compare total annual costs
7. Determine which tender is better and calculate annual savings

## Application Structure

### Module 1: Tender Analysis Tab
- Input all transformer specifications
- Input tender parameters (efficiency, losses, costs)
- Input operating conditions (hours at different loads)
- Input economic parameters (annual charges, energy cost)
- Calculate button performs comprehensive analysis
- Results displayed in formatted text with step-by-step calculations

### Module 2: Dynamic Simulation Tab
- Left panel: Control parameters with interactive sliders
- Right panel: Real-time visualization with matplotlib
- ODE solver selection (RK45, Euler, RK23)
- Start/Stop/Reset buttons for simulation control
- Simulates transformer transient behavior
- Shows flux, current, and power waveforms

### Module 3: Transformer Model Tab
- Input transformer rated parameters
- Input circuit parameters (resistances, reactances)
- Adjust load percentage with slider
- Calculate equivalent circuit parameters
- Analyze voltage regulation
- Calculate efficiency and losses

## Technical Details

### ODE System
The dynamic simulation solves the following differential equations:

```
dΦ/dt = V_applied - R_total × i
di/dt = (V_applied - R_total × i - Φ) / L
```

Where:
- Φ = magnetic flux (Wb)
- i = current (A)
- V_applied = applied voltage (V)
- R_total = total resistance (Ω)
- L = inductance (H)

### Numerical Methods
- **RK45**: Adaptive step-size Runge-Kutta method (4th/5th order)
- **Euler**: Simple first-order forward method
- **RK23**: Adaptive Runge-Kutta method (2nd/3rd order)

## Features Implemented

✅ User interface (Tkinter GUI)
✅ Main menu with File, Tools, and Help options
✅ Input parameters with validation
✅ Control adjustment sliders for real-time parameter changes
✅ Visualization with matplotlib integration
✅ Calculation modules with mathematical modeling
✅ Differential equations describing transformer behavior
✅ Dynamic simulation with real-time ODE solver
✅ Multiple solver methods (RK45, Euler, RK23)
✅ Results visualization with multiple plots
✅ Buttons: Start, Stop, Reset
✅ Automatic width and height adjustment when window changes
✅ Auto-scale functionality
✅ Advanced practical features for electrical engineering
✅ No syntax errors
✅ Combined in one code file

## Advanced Features

1. **Multi-threaded Simulation**: Simulation runs in separate thread to keep GUI responsive
2. **Data Export**: Export simulation results to CSV file
3. **Comprehensive Error Handling**: Robust error checking and user feedback
4. **Professional Styling**: Custom color scheme and fonts
5. **Status Bar**: Real-time feedback on application status
6. **Scrollable Interfaces**: Large result sets are scrollable
7. **Dynamic Plotting**: Real-time plot updates during simulation
8. **Parameter Validation**: Input validation to prevent errors

## Educational Value

This application is designed for:
- **Students**: Learning transformer analysis and simulation techniques
- **Engineers**: Quick transformer economic analysis and performance evaluation
- **Researchers**: Experimenting with different transformer parameters
- **Educators**: Demonstrating transformer behavior and economic principles

## Menu Options

### File Menu
- **Reset All**: Reset all parameters to defaults
- **Exit**: Close the application

### Tools Menu
- **Clear Results**: Clear all result displays
- **Export Data**: Export simulation data to CSV file

### Help Menu
- **About**: Information about the application

## Tips

1. **Tender Analysis**: Start with the default values to see a complete analysis, then modify parameters to explore different scenarios
2. **Dynamic Simulation**: Try different ODE solvers to compare accuracy and speed
3. **Parameter Adjustment**: Use sliders for real-time parameter changes and see immediate effects on visualization
4. **Load Analysis**: Adjust the load percentage in Transformer Model tab to see how efficiency varies with load

## Output

The application provides:
- **Detailed calculations** with step-by-step explanations
- **Economic comparison** showing which tender is more economical
- **Annual savings** calculation
- **Payback period** for additional investment
- **Real-time waveforms** for dynamic behavior
- **Performance metrics** including efficiency, losses, and regulation

## Future Enhancements

Potential additions:
- Three-phase transformer analysis
- Harmonic analysis
- Temperature rise calculations
- Protection system simulation
- Database integration for storing analyses
- PDF report generation

## License

This software is provided for educational and professional use in electrical engineering.

## Author

Developed as a comprehensive electrical engineering laboratory tool for transformer analysis and simulation.

---

**Version**: 1.0
**Last Updated**: 2025-11-23
