"""
Hydro-Power Station Cost Analysis with Matplotlib Visualization
Problem: Calculate generation cost in the form of A per kW plus B per kWh
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

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

    def print_results(self):
        """Print formatted results"""
        print(f"""
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
""")

    def create_visualizations(self):
        """Create comprehensive visualizations"""
        # Create figure with subplots
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle('Hydro-Power Station Cost Analysis & Visualization',
                     fontsize=18, fontweight='bold', y=0.98)

        gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)

        # 1. Pie chart - Fixed vs Variable
        ax1 = fig.add_subplot(gs[0, 0])
        sizes = [self.total_fixed_charges, self.total_variable_charges]
        labels = ['Fixed Charges\nRs. {:,.0f}\n({:.1f}%)'.format(
                  self.total_fixed_charges,
                  100*self.total_fixed_charges/(sum(sizes))),
                 'Variable Charges\nRs. {:,.0f}\n({:.1f}%)'.format(
                  self.total_variable_charges,
                  100*self.total_variable_charges/(sum(sizes)))]
        colors = ['#ff9999', '#66b3ff']
        explode = (0.05, 0.05)

        wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels,
                                            colors=colors, autopct='',
                                            shadow=True, startangle=90,
                                            textprops={'fontsize': 10, 'fontweight': 'bold'})
        ax1.set_title('Total Annual Cost Distribution\n(Fixed vs Variable)',
                     fontsize=13, fontweight='bold', pad=15)

        # 2. Bar chart - Detailed components
        ax2 = fig.add_subplot(gs[0, 1])
        categories = ['Investment\nCharge', 'Fixed\nRoyalty', 'Fixed\nMaintenance',
                     'Variable\nRoyalty', 'Variable\nMaintenance']
        values = [self.annual_investment_charge, self.fixed_royalty,
                 self.fixed_maintenance, self.variable_royalty,
                 self.variable_maintenance]
        colors_bar = ['#ff6666', '#ff9999', '#ffcccc', '#6699ff', '#99ccff']

        bars = ax2.bar(categories, values, color=colors_bar, edgecolor='black', linewidth=1.5)

        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    'Rs. {:,.0f}'.format(height),
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

        ax2.set_ylabel('Cost (Rs.)', fontsize=11, fontweight='bold')
        ax2.set_title('Detailed Cost Components Breakdown', fontsize=13, fontweight='bold', pad=15)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        ax2.ticklabel_format(style='plain', axis='y')

        # 3. Stacked bar - Fixed vs Variable
        ax3 = fig.add_subplot(gs[1, 0])
        categories_stack = ['Total Annual\nCost']
        fixed = [self.total_fixed_charges]
        variable = [self.total_variable_charges]

        x = np.arange(len(categories_stack))
        width = 0.5

        bars1 = ax3.bar(x, fixed, width, label='Fixed Charges', color='#ff9999', edgecolor='black')
        bars2 = ax3.bar(x, variable, width, bottom=fixed, label='Variable Charges',
                       color='#66b3ff', edgecolor='black')

        # Add value labels
        ax3.text(0, fixed[0]/2, 'Rs. {:,.0f}\n({:.1f}%)'.format(
                 fixed[0], 100*fixed[0]/(fixed[0]+variable[0])),
                ha='center', va='center', fontsize=10, fontweight='bold')
        ax3.text(0, fixed[0] + variable[0]/2, 'Rs. {:,.0f}\n({:.1f}%)'.format(
                 variable[0], 100*variable[0]/(fixed[0]+variable[0])),
                ha='center', va='center', fontsize=10, fontweight='bold')

        ax3.set_ylabel('Cost (Rs.)', fontsize=11, fontweight='bold')
        ax3.set_title('Annual Cost: Fixed vs Variable (Stacked)',
                     fontsize=13, fontweight='bold', pad=15)
        ax3.set_xticks(x)
        ax3.set_xticklabels(categories_stack)
        ax3.legend(loc='upper right', fontsize=10)
        ax3.grid(axis='y', alpha=0.3, linestyle='--')
        ax3.ticklabel_format(style='plain', axis='y')

        # 4. Unit costs
        ax4 = fig.add_subplot(gs[1, 1])
        unit_categories = ['Cost per kW\n(Fixed - A)', 'Cost per kWh\n(Variable - B)']
        unit_values = [self.cost_per_kw, self.cost_per_kwh]
        unit_colors = ['#ff9999', '#66b3ff']

        bars = ax4.bar(unit_categories, unit_values, color=unit_colors,
                      edgecolor='black', linewidth=1.5, width=0.5)

        for i, bar in enumerate(bars):
            height = bar.get_height()
            if i == 0:
                label = 'Rs. {:.2f}'.format(height)
            else:
                label = 'Rs. {:.4f}'.format(height)
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    label, ha='center', va='bottom', fontsize=11, fontweight='bold')

        ax4.set_ylabel('Cost (Rs.)', fontsize=11, fontweight='bold')
        ax4.set_title('Unit Cost Analysis\n(A per kW + B per kWh)',
                     fontsize=13, fontweight='bold', pad=15)
        ax4.grid(axis='y', alpha=0.3, linestyle='--')

        # 5. Load factor impact on variable cost
        ax5 = fig.add_subplot(gs[2, 0])
        load_factors = np.linspace(0.5, 1.0, 11)
        variable_costs_per_kwh = []

        for lf in load_factors:
            avg_demand = lf * self.max_demand_kw
            annual_energy = avg_demand * self.hours_per_year
            var_royalty = self.royalty_per_kwh * annual_energy
            total_var_charges = var_royalty + self.variable_maintenance
            var_cost_per_kwh = total_var_charges / annual_energy
            variable_costs_per_kwh.append(var_cost_per_kwh)

        ax5.plot(load_factors * 100, variable_costs_per_kwh, 'b-o',
                linewidth=2.5, markersize=7, label='Variable Cost per kWh')
        ax5.axvline(x=self.load_factor * 100, color='r', linestyle='--',
                   linewidth=2, label='Current Load Factor (80%)')
        ax5.axhline(y=self.cost_per_kwh, color='g', linestyle='--',
                   linewidth=2, label='Current Cost (Rs. {:.4f}/kWh)'.format(self.cost_per_kwh))

        ax5.set_xlabel('Load Factor (%)', fontsize=11, fontweight='bold')
        ax5.set_ylabel('Variable Cost per kWh (Rs.)', fontsize=11, fontweight='bold')
        ax5.set_title('Impact of Load Factor on Variable Cost per kWh',
                     fontsize=13, fontweight='bold', pad=15)
        ax5.grid(True, alpha=0.3)
        ax5.legend(fontsize=9)

        # 6. Horizontal bar - Cost component percentages
        ax6 = fig.add_subplot(gs[2, 1])

        total_cost = self.total_fixed_charges + self.total_variable_charges
        components_pct = [
            ('Annual Investment\nCharge', self.annual_investment_charge/total_cost*100),
            ('Fixed Royalty', self.fixed_royalty/total_cost*100),
            ('Fixed Maintenance', self.fixed_maintenance/total_cost*100),
            ('Variable Royalty', self.variable_royalty/total_cost*100),
            ('Variable Maintenance', self.variable_maintenance/total_cost*100)
        ]

        labels_pct = [c[0] for c in components_pct]
        values_pct = [c[1] for c in components_pct]
        colors_pct = ['#ff6666', '#ff9999', '#ffcccc', '#6699ff', '#99ccff']

        y_pos = np.arange(len(labels_pct))
        bars = ax6.barh(y_pos, values_pct, color=colors_pct,
                       edgecolor='black', linewidth=1.2)

        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax6.text(width, bar.get_y() + bar.get_height()/2.,
                    ' {:.1f}%'.format(width),
                    ha='left', va='center', fontsize=10, fontweight='bold')

        ax6.set_yticks(y_pos)
        ax6.set_yticklabels(labels_pct, fontsize=9)
        ax6.set_xlabel('Percentage of Total Cost (%)', fontsize=11, fontweight='bold')
        ax6.set_title('Cost Component Distribution (%)',
                     fontsize=13, fontweight='bold', pad=15)
        ax6.grid(axis='x', alpha=0.3, linestyle='--')

        # Add text box with final answer
        textstr = 'FINAL ANSWER:\nGeneration Cost = Rs. {:.2f} per kW + Rs. {:.4f} per kWh'.format(
                  self.cost_per_kw, self.cost_per_kwh)
        props = dict(boxstyle='round', facecolor='lightgreen', alpha=0.8, edgecolor='black', linewidth=2)
        fig.text(0.5, 0.02, textstr, fontsize=14, fontweight='bold',
                ha='center', bbox=props)

        plt.savefig('hydropower_analysis.png', dpi=300, bbox_inches='tight')
        print("\n✓ Visualization saved as 'hydropower_analysis.png'")

        plt.show()


def main():
    """Main function"""
    print("\n" + "="*80)
    print("HYDRO-POWER STATION COST ANALYSIS")
    print("="*80)

    # Create analyzer
    analyzer = HydroPowerCostAnalyzer()

    # Print results
    analyzer.print_results()

    # Create visualizations
    print("\nGenerating visualizations...")
    analyzer.create_visualizations()


if __name__ == "__main__":
    main()
