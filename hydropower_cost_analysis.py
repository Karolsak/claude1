"""
Hydro-Power Station Cost Analysis with Visualization
Problem: Calculate generation cost in the form of A per kW plus B per kWh
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class HydroPowerCostAnalyzer:
    def __init__(self):
        # Given data
        self.capacity_kw = 50000  # kW
        self.capital_cost_per_kw = 1200  # Rs. per kW
        self.annual_charge_rate = 0.10  # 10%
        self.royalty_per_kw = 1  # Rs. per kW per year
        self.royalty_per_kwh = 0.01  # Rs. per kWh
        self.max_demand_kw = 40000  # kW
        self.load_factor = 0.80  # 80%
        self.total_maintenance = 650000  # Rs.
        self.fixed_maintenance_percent = 0.20  # 20%
        self.hours_per_year = 8760  # hours

        # Calculated values
        self.calculate()

    def calculate(self):
        """Perform all cost calculations"""
        # 1. Total capital cost
        self.total_capital_cost = self.capacity_kw * self.capital_cost_per_kw

        # 2. Annual charge on investment (depreciation)
        self.annual_investment_charge = self.total_capital_cost * self.annual_charge_rate

        # 3. Fixed royalty (on maximum demand)
        self.fixed_royalty = self.royalty_per_kw * self.max_demand_kw

        # 4. Fixed portion of maintenance
        self.fixed_maintenance = self.fixed_maintenance_percent * self.total_maintenance

        # 5. Total Fixed Charges
        self.total_fixed_charges = (self.annual_investment_charge +
                                   self.fixed_royalty +
                                   self.fixed_maintenance)

        # 6. Fixed cost per kW (A)
        self.cost_per_kw = self.total_fixed_charges / self.max_demand_kw

        # 7. Annual energy generated
        self.average_demand = self.load_factor * self.max_demand_kw
        self.annual_energy_kwh = self.average_demand * self.hours_per_year

        # 8. Variable royalty
        self.variable_royalty = self.royalty_per_kwh * self.annual_energy_kwh

        # 9. Variable portion of maintenance
        self.variable_maintenance = (1 - self.fixed_maintenance_percent) * self.total_maintenance

        # 10. Total Variable Charges
        self.total_variable_charges = self.variable_royalty + self.variable_maintenance

        # 11. Variable cost per kWh (B)
        self.cost_per_kwh = self.total_variable_charges / self.annual_energy_kwh

    def get_results_text(self):
        """Generate formatted results text"""
        results = f"""
╔══════════════════════════════════════════════════════════════════════╗
║           HYDRO-POWER STATION COST ANALYSIS RESULTS                  ║
╚══════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  GIVEN DATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Station Capacity            : {self.capacity_kw:,} kW
  • Capital Cost per kW         : Rs. {self.capital_cost_per_kw:,}
  • Total Capital Cost          : Rs. {self.total_capital_cost:,.2f}
  • Annual Charge Rate          : {self.annual_charge_rate*100}%
  • Maximum Demand              : {self.max_demand_kw:,} kW
  • Load Factor                 : {self.load_factor*100}%
  • Total Maintenance/Salaries  : Rs. {self.total_maintenance:,}
  • Fixed Maintenance Portion   : {self.fixed_maintenance_percent*100}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FIXED CHARGES CALCULATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Annual Investment Charge (10% of capital)
     = Rs. {self.annual_investment_charge:,.2f}

  2. Fixed Royalty (Rs. 1 per kW on max demand)
     = {self.max_demand_kw:,} kW × Rs. 1
     = Rs. {self.fixed_royalty:,.2f}

  3. Fixed Maintenance (20% of total maintenance)
     = 0.20 × Rs. {self.total_maintenance:,}
     = Rs. {self.fixed_maintenance:,.2f}

  ────────────────────────────────────────────────────────────────────
  TOTAL FIXED CHARGES = Rs. {self.total_fixed_charges:,.2f}
  ────────────────────────────────────────────────────────────────────

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ENERGY GENERATION CALCULATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Average Demand = Load Factor × Max Demand
                   = {self.load_factor} × {self.max_demand_kw:,} kW
                   = {self.average_demand:,.0f} kW

  • Annual Energy Generated = Average Demand × Hours per Year
                            = {self.average_demand:,.0f} kW × {self.hours_per_year} hrs
                            = {self.annual_energy_kwh:,.0f} kWh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VARIABLE CHARGES CALCULATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Variable Royalty (Rs. 0.01 per kWh generated)
     = {self.annual_energy_kwh:,.0f} kWh × Rs. 0.01
     = Rs. {self.variable_royalty:,.2f}

  2. Variable Maintenance (80% of total maintenance)
     = 0.80 × Rs. {self.total_maintenance:,}
     = Rs. {self.variable_maintenance:,.2f}

  ────────────────────────────────────────────────────────────────────
  TOTAL VARIABLE CHARGES = Rs. {self.total_variable_charges:,.2f}
  ────────────────────────────────────────────────────────────────────

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FINAL GENERATION COST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌────────────────────────────────────────────────────────────────┐
  │  Cost per kW (A) = Total Fixed Charges / Maximum Demand        │
  │                  = Rs. {self.total_fixed_charges:,.2f} / {self.max_demand_kw:,} kW           │
  │                  = Rs. {self.cost_per_kw:.4f} per kW                      │
  └────────────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────────────┐
  │  Cost per kWh (B) = Total Variable Charges / Annual Energy     │
  │                   = Rs. {self.total_variable_charges:,.2f} / {self.annual_energy_kwh:,.0f} kWh  │
  │                   = Rs. {self.cost_per_kwh:.6f} per kWh                  │
  └────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║                        FINAL ANSWER                                  ║
║                                                                      ║
║  Generation Cost = Rs. {self.cost_per_kw:.2f} per kW + Rs. {self.cost_per_kwh:.4f} per kWh      ║
╚══════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  COST BREAKDOWN SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Annual Cost = Fixed Charges + Variable Charges
                    = Rs. {self.total_fixed_charges:,.2f} + Rs. {self.total_variable_charges:,.2f}
                    = Rs. {self.total_fixed_charges + self.total_variable_charges:,.2f}

  Fixed Cost Percentage   : {(self.total_fixed_charges/(self.total_fixed_charges + self.total_variable_charges))*100:.2f}%
  Variable Cost Percentage: {(self.total_variable_charges/(self.total_fixed_charges + self.total_variable_charges))*100:.2f}%
"""
        return results


class HydroPowerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydro-Power Station Cost Analysis & Visualization")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')

        # Create analyzer
        self.analyzer = HydroPowerCostAnalyzer()

        # Create main container
        main_container = ttk.Frame(root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=2)
        main_container.rowconfigure(0, weight=1)

        # Create left panel (results text)
        self.create_results_panel(main_container)

        # Create right panel (visualizations)
        self.create_visualization_panel(main_container)

    def create_results_panel(self, parent):
        """Create left panel with calculation results"""
        results_frame = ttk.LabelFrame(parent, text="Detailed Calculations", padding="10")
        results_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            width=60,
            height=40,
            font=('Courier', 9)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Insert results
        self.results_text.insert(1.0, self.analyzer.get_results_text())
        self.results_text.config(state=tk.DISABLED)

    def create_visualization_panel(self, parent):
        """Create right panel with visualizations"""
        viz_frame = ttk.Frame(parent)
        viz_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # Create notebook for multiple visualizations
        notebook = ttk.Notebook(viz_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Cost Breakdown
        self.create_cost_breakdown_tab(notebook)

        # Tab 2: Fixed vs Variable
        self.create_fixed_variable_tab(notebook)

        # Tab 3: Load Factor Analysis
        self.create_load_factor_tab(notebook)

        # Tab 4: Cost Components
        self.create_cost_components_tab(notebook)

    def create_cost_breakdown_tab(self, notebook):
        """Create cost breakdown visualization"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Cost Breakdown")

        fig = Figure(figsize=(10, 8), facecolor='white')

        # Pie chart for total cost breakdown
        ax1 = fig.add_subplot(2, 1, 1)

        sizes = [self.analyzer.total_fixed_charges, self.analyzer.total_variable_charges]
        labels = ['Fixed Charges', 'Variable Charges']
        colors = ['#ff9999', '#66b3ff']
        explode = (0.05, 0.05)

        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90, textprops={'fontsize': 11})
        ax1.set_title('Total Annual Cost Distribution\n(Fixed vs Variable)', fontsize=14, fontweight='bold', pad=20)

        # Bar chart for detailed breakdown
        ax2 = fig.add_subplot(2, 1, 2)

        categories = [
            'Investment\nCharge',
            'Fixed\nRoyalty',
            'Fixed\nMaintenance',
            'Variable\nRoyalty',
            'Variable\nMaintenance'
        ]

        values = [
            self.analyzer.annual_investment_charge,
            self.analyzer.fixed_royalty,
            self.analyzer.fixed_maintenance,
            self.analyzer.variable_royalty,
            self.analyzer.variable_maintenance
        ]

        colors_bar = ['#ff9999', '#ff9999', '#ff9999', '#66b3ff', '#66b3ff']

        bars = ax2.bar(categories, values, color=colors_bar, edgecolor='black', linewidth=1.5)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'Rs. {height:,.0f}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

        ax2.set_ylabel('Cost (Rs.)', fontsize=11, fontweight='bold')
        ax2.set_title('Detailed Cost Components Breakdown', fontsize=13, fontweight='bold', pad=15)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        ax2.ticklabel_format(style='plain', axis='y')

        fig.tight_layout(pad=3.0)

        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_fixed_variable_tab(self, notebook):
        """Create fixed vs variable cost analysis"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Fixed vs Variable Analysis")

        fig = Figure(figsize=(10, 8), facecolor='white')

        # Stacked bar chart
        ax1 = fig.add_subplot(2, 1, 1)

        categories = ['Total Annual Cost']
        fixed = [self.analyzer.total_fixed_charges]
        variable = [self.analyzer.total_variable_charges]

        x = np.arange(len(categories))
        width = 0.5

        bars1 = ax1.bar(x, fixed, width, label='Fixed Charges', color='#ff9999', edgecolor='black')
        bars2 = ax1.bar(x, variable, width, bottom=fixed, label='Variable Charges', color='#66b3ff', edgecolor='black')

        # Add value labels
        ax1.text(0, fixed[0]/2, f'Rs. {fixed[0]:,.0f}\n({(fixed[0]/(fixed[0]+variable[0]))*100:.1f}%)',
                ha='center', va='center', fontsize=11, fontweight='bold')
        ax1.text(0, fixed[0] + variable[0]/2, f'Rs. {variable[0]:,.0f}\n({(variable[0]/(fixed[0]+variable[0]))*100:.1f}%)',
                ha='center', va='center', fontsize=11, fontweight='bold')

        ax1.set_ylabel('Cost (Rs.)', fontsize=11, fontweight='bold')
        ax1.set_title('Total Annual Cost: Fixed vs Variable', fontsize=13, fontweight='bold', pad=15)
        ax1.set_xticks(x)
        ax1.set_xticklabels(categories)
        ax1.legend(loc='upper right', fontsize=10)
        ax1.grid(axis='y', alpha=0.3, linestyle='--')

        # Cost per unit comparison
        ax2 = fig.add_subplot(2, 1, 2)

        unit_categories = ['Cost per kW\n(Fixed)', 'Cost per kWh\n(Variable)']
        unit_values = [self.analyzer.cost_per_kw, self.analyzer.cost_per_kwh]
        unit_colors = ['#ff9999', '#66b3ff']

        bars = ax2.bar(unit_categories, unit_values, color=unit_colors, edgecolor='black', linewidth=1.5, width=0.5)

        # Add value labels
        for i, bar in enumerate(bars):
            height = bar.get_height()
            if i == 0:
                label = f'Rs. {height:.2f}'
            else:
                label = f'Rs. {height:.4f}'
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    label, ha='center', va='bottom', fontsize=11, fontweight='bold')

        ax2.set_ylabel('Cost (Rs.)', fontsize=11, fontweight='bold')
        ax2.set_title('Unit Cost Comparison', fontsize=13, fontweight='bold', pad=15)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')

        fig.tight_layout(pad=3.0)

        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_load_factor_tab(self, notebook):
        """Create load factor impact analysis"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Load Factor Impact")

        fig = Figure(figsize=(10, 8), facecolor='white')

        # Analyze impact of load factor on variable cost
        load_factors = np.linspace(0.5, 1.0, 11)
        variable_costs_per_kwh = []
        total_costs_per_kw = []

        for lf in load_factors:
            avg_demand = lf * self.analyzer.max_demand_kw
            annual_energy = avg_demand * self.analyzer.hours_per_year
            var_royalty = self.analyzer.royalty_per_kwh * annual_energy
            total_var_charges = var_royalty + self.analyzer.variable_maintenance
            var_cost_per_kwh = total_var_charges / annual_energy
            variable_costs_per_kwh.append(var_cost_per_kwh)

            # Total cost per kW of demand
            total_annual_cost = self.analyzer.total_fixed_charges + total_var_charges
            total_cost_per_kw_demand = total_annual_cost / self.analyzer.max_demand_kw
            total_costs_per_kw.append(total_cost_per_kw_demand)

        # Plot 1: Variable cost per kWh vs load factor
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(load_factors * 100, variable_costs_per_kwh, 'b-o', linewidth=2, markersize=6)
        ax1.axvline(x=self.analyzer.load_factor * 100, color='r', linestyle='--', linewidth=2, label='Current Load Factor (80%)')
        ax1.axhline(y=self.analyzer.cost_per_kwh, color='g', linestyle='--', linewidth=2, label=f'Current Cost (Rs. {self.analyzer.cost_per_kwh:.4f}/kWh)')

        ax1.set_xlabel('Load Factor (%)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Variable Cost per kWh (Rs.)', fontsize=11, fontweight='bold')
        ax1.set_title('Impact of Load Factor on Variable Cost per kWh', fontsize=13, fontweight='bold', pad=15)
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=9)

        # Plot 2: Total annual cost per kW vs load factor
        ax2 = fig.add_subplot(2, 1, 2)
        ax2.plot(load_factors * 100, total_costs_per_kw, 'r-s', linewidth=2, markersize=6)
        ax2.axvline(x=self.analyzer.load_factor * 100, color='b', linestyle='--', linewidth=2, label='Current Load Factor (80%)')

        current_total_cost_per_kw = (self.analyzer.total_fixed_charges + self.analyzer.total_variable_charges) / self.analyzer.max_demand_kw
        ax2.axhline(y=current_total_cost_per_kw, color='g', linestyle='--', linewidth=2, label=f'Current Cost (Rs. {current_total_cost_per_kw:.2f}/kW)')

        ax2.set_xlabel('Load Factor (%)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Total Annual Cost per kW (Rs.)', fontsize=11, fontweight='bold')
        ax2.set_title('Impact of Load Factor on Total Annual Cost per kW of Demand', fontsize=13, fontweight='bold', pad=15)
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=9)

        fig.tight_layout(pad=3.0)

        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_cost_components_tab(self, notebook):
        """Create detailed cost components visualization"""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Cost Components")

        fig = Figure(figsize=(10, 8), facecolor='white')

        # Horizontal bar chart for all components
        ax1 = fig.add_subplot(2, 1, 1)

        components = [
            'Annual Investment Charge\n(10% of Capital)',
            'Fixed Royalty\n(Rs. 1/kW)',
            'Fixed Maintenance\n(20%)',
            'Variable Royalty\n(Rs. 0.01/kWh)',
            'Variable Maintenance\n(80%)'
        ]

        values = [
            self.analyzer.annual_investment_charge,
            self.analyzer.fixed_royalty,
            self.analyzer.fixed_maintenance,
            self.analyzer.variable_royalty,
            self.analyzer.variable_maintenance
        ]

        colors = ['#ff6b6b', '#ff9999', '#ffcccc', '#6699ff', '#99ccff']

        y_pos = np.arange(len(components))
        bars = ax1.barh(y_pos, values, color=colors, edgecolor='black', linewidth=1.2)

        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width, bar.get_y() + bar.get_height()/2.,
                    f' Rs. {width:,.0f}',
                    ha='left', va='center', fontsize=9, fontweight='bold')

        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(components, fontsize=9)
        ax1.set_xlabel('Cost (Rs.)', fontsize=11, fontweight='bold')
        ax1.set_title('Individual Cost Components', fontsize=13, fontweight='bold', pad=15)
        ax1.grid(axis='x', alpha=0.3, linestyle='--')

        # Waterfall chart
        ax2 = fig.add_subplot(2, 1, 2)

        # Prepare waterfall data
        categories_wf = ['Investment\nCharge', 'Fixed\nRoyalty', 'Fixed\nMaint.',
                         'Variable\nRoyalty', 'Variable\nMaint.', 'Total\nCost']

        values_wf = [
            self.analyzer.annual_investment_charge,
            self.analyzer.fixed_royalty,
            self.analyzer.fixed_maintenance,
            self.analyzer.variable_royalty,
            self.analyzer.variable_maintenance
        ]

        # Calculate cumulative values
        cumulative = np.cumsum([0] + values_wf)

        # Plot bars
        colors_wf = ['#ff9999', '#ff9999', '#ff9999', '#66b3ff', '#66b3ff', '#4CAF50']

        for i in range(len(values_wf)):
            ax2.bar(i, values_wf[i], bottom=cumulative[i], color=colors_wf[i],
                   edgecolor='black', linewidth=1.2, width=0.6)
            # Add value label
            ax2.text(i, cumulative[i] + values_wf[i]/2, f'{values_wf[i]/1000:.0f}k',
                    ha='center', va='center', fontsize=8, fontweight='bold')

        # Plot total bar
        total_cost = sum(values_wf)
        ax2.bar(len(values_wf), total_cost, color=colors_wf[-1],
               edgecolor='black', linewidth=1.5, width=0.6)
        ax2.text(len(values_wf), total_cost/2, f'{total_cost/1000:.0f}k\n(Total)',
                ha='center', va='center', fontsize=9, fontweight='bold', color='white')

        ax2.set_xticks(range(len(categories_wf)))
        ax2.set_xticklabels(categories_wf, fontsize=9)
        ax2.set_ylabel('Cumulative Cost (Rs.)', fontsize=11, fontweight='bold')
        ax2.set_title('Cumulative Cost Build-up (Waterfall Chart)', fontsize=13, fontweight='bold', pad=15)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')

        fig.tight_layout(pad=3.0)

        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def main():
    """Main function to run the application"""
    # Print results to console as well
    print("\n" + "="*80)
    print("HYDRO-POWER STATION COST ANALYSIS")
    print("="*80)

    analyzer = HydroPowerCostAnalyzer()
    print(analyzer.get_results_text())

    print("\n" + "="*80)
    print("Launching GUI for visualization...")
    print("="*80 + "\n")

    # Create and run GUI
    root = tk.Tk()
    app = HydroPowerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
