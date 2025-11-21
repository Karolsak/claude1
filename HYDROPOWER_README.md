# Hydro-Power Station Cost Analysis

## Problem Statement

A hydro-power station with the following specifications needs cost analysis:

- **Capacity**: 50,000 kW
- **Capital Cost**: Rs. 1,200 per kW
- **Annual Charge on Investment**: 10% (including depreciation)
- **Royalty**:
  - Rs. 1 per kW per year (on maximum demand)
  - Rs. 0.01 per kWh generated
- **Maximum Demand**: 40,000 kW
- **Load Factor**: 80%
- **Maintenance & Salaries**: Rs. 6,50,000 per year
  - 20% fixed charges
  - 80% variable charges

**Objective**: Determine the generation cost in the form of **A per kW + B per kWh**

## Solution

### Final Answer

```
Generation Cost = Rs. 154.25 per kW + Rs. 0.0119 per kWh
```

Where:
- **A = Rs. 154.25 per kW** (Fixed Cost Component)
- **B = Rs. 0.0119 per kWh** (Variable Cost Component)

### Detailed Calculations

#### 1. Fixed Charges Calculation

| Component | Calculation | Amount (Rs.) |
|-----------|-------------|--------------|
| Annual Investment Charge | 10% × (50,000 kW × Rs. 1,200) | 6,000,000.00 |
| Fixed Royalty | 40,000 kW × Rs. 1 | 40,000.00 |
| Fixed Maintenance | 20% × Rs. 650,000 | 130,000.00 |
| **Total Fixed Charges** | | **6,170,000.00** |

**Fixed Cost per kW (A)** = 6,170,000 / 40,000 = **Rs. 154.25 per kW**

#### 2. Energy Generation Calculation

- Average Demand = Load Factor × Maximum Demand
- Average Demand = 0.80 × 40,000 = 32,000 kW
- Annual Energy = 32,000 kW × 8,760 hours = **280,320,000 kWh**

#### 3. Variable Charges Calculation

| Component | Calculation | Amount (Rs.) |
|-----------|-------------|--------------|
| Variable Royalty | 280,320,000 kWh × Rs. 0.01 | 2,803,200.00 |
| Variable Maintenance | 80% × Rs. 650,000 | 520,000.00 |
| **Total Variable Charges** | | **3,323,200.00** |

**Variable Cost per kWh (B)** = 3,323,200 / 280,320,000 = **Rs. 0.011855 per kWh**

### Cost Breakdown Summary

- **Total Annual Cost**: Rs. 9,493,200.00
- **Fixed Cost Percentage**: 65.0%
- **Variable Cost Percentage**: 35.0%

## Python Implementation

Four Python scripts are provided:

### 1. `hydropower_solution.py`
The main solution with detailed formatted output showing all calculation steps.

**Run:**
```bash
python hydropower_solution.py
```

**Features:**
- Step-by-step calculations
- Formatted tables and boxes
- ASCII art visualization
- Cost breakdown summary

### 2. `hydropower_visual.py`
Enhanced version with comprehensive ASCII visualizations.

**Run:**
```bash
python hydropower_visual.py
```

**Features:**
- Cost formula breakdown with practical examples
- Fixed vs Variable distribution (pie chart style)
- Detailed component breakdown (bar chart)
- Load factor sensitivity analysis
- Cost comparison at different loads
- Key findings summary

### 3. `hydropower_visualization.py` ⭐ **RECOMMENDED**
Professional matplotlib visualization with comprehensive charts.

**Run:**
```bash
python hydropower_visualization.py
```

**Features:**
- High-resolution output (300 DPI) saved as PNG
- 7 comprehensive visualizations in one figure:
  - Final answer prominently displayed
  - Fixed vs Variable cost pie chart
  - Detailed component breakdown (horizontal bars)
  - Stacked cost view
  - Load factor sensitivity analysis
  - Percentage distribution chart
  - Cost comparison table for different loads
- Professional styling and color coding
- Exports as `hydropower_analysis_full.png`

**Requirements:**
```bash
pip install matplotlib
```

### 4. `hydropower_cost_analysis.py`
GUI version using Tkinter (requires tkinter - may not be available in all environments)

**Features:**
- Interactive GUI with multiple tabs
- Multiple visualization charts
- Detailed calculations panel

## Key Insights

1. **Investment Charge Dominates**: At 63.2% of total cost, the annual investment charge (depreciation) is the largest component.

2. **Fixed Cost Heavy**: Fixed costs account for 65% of total annual costs, making the plant economics relatively stable.

3. **Load Factor Impact**: Higher load factors reduce the variable cost per kWh:
   - At 50% LF: Rs. 0.01297/kWh
   - At 80% LF: Rs. 0.01186/kWh (current)
   - At 100% LF: Rs. 0.01148/kWh

4. **Practical Application**:
   - For a customer using 1,000 kW demand and 100,000 kWh energy:
   - Cost = 154.25 × 1,000 + 0.0119 × 100,000 = Rs. 155,435.50

## Usage Examples

```python
from hydropower_solution import HydroPowerCostAnalyzer

# Create analyzer
analyzer = HydroPowerCostAnalyzer()

# Access calculated values
print(f"Fixed cost per kW: Rs. {analyzer.cost_per_kw:.2f}")
print(f"Variable cost per kWh: Rs. {analyzer.cost_per_kwh:.4f}")
print(f"Total annual cost: Rs. {analyzer.total_fixed_charges + analyzer.total_variable_charges:,.2f}")

# Print full report
analyzer.print_detailed_report()
```

## Visualization Output

The `hydropower_visualization.py` script generates a comprehensive visualization (`hydropower_analysis_full.png`) that includes:

### Visual Components:

1. **Final Answer Box** - Green highlighted box with the generation cost formula
2. **Fixed vs Variable Distribution** - Pie chart showing 65.0% fixed and 35.0% variable
3. **Detailed Cost Components** - Horizontal bar chart with all 5 cost categories
4. **Stacked Cost View** - Combined visualization of total annual costs
5. **Load Factor Impact** - Line graph showing sensitivity from 50% to 100% load factor
6. **Percentage Distribution** - Bar chart showing each component's share of total cost
7. **Cost Comparison Table** - Practical examples at 10k, 20k, 30k, and 40k kW demand levels

The visualization is saved as a high-resolution PNG (300 DPI) suitable for reports and presentations.

## Requirements

- Python 3.6+
- No external dependencies for basic scripts (hydropower_solution.py, hydropower_visual.py)
- **Recommended**: `matplotlib` for professional visualizations
  ```bash
  pip install matplotlib
  ```
- Optional: `tkinter` for GUI version (may require system installation)

## Author

Solution developed using Python with comprehensive cost analysis and visualization capabilities.

## License

Educational use - Electrical Engineering Power Systems Analysis
