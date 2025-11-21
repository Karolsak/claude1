"""
Hydro-Power Station Cost Analysis with Professional Matplotlib Visualizations
Creates comprehensive charts and graphs for cost analysis
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np

class HydroPowerAnalyzer:
    def __init__(self):
        # Given data
        self.capacity_kw = 50000
        self.capital_cost_per_kw = 1200
        self.annual_charge_rate = 0.10
        self.royalty_per_kw = 1
        self.royalty_per_kwh = 0.01
        self.max_demand_kw = 40000
        self.load_factor = 0.80
        self.total_maintenance = 650000
        self.fixed_maintenance_percent = 0.20
        self.hours_per_year = 8760

        # Calculate
        self.calculate()

    def calculate(self):
        """Perform all cost calculations"""
        self.total_capital_cost = self.capacity_kw * self.capital_cost_per_kw
        self.annual_investment_charge = self.total_capital_cost * self.annual_charge_rate
        self.fixed_royalty = self.royalty_per_kw * self.max_demand_kw
        self.fixed_maintenance = self.fixed_maintenance_percent * self.total_maintenance
        self.total_fixed_charges = (self.annual_investment_charge +
                                   self.fixed_royalty + self.fixed_maintenance)
        self.cost_per_kw = self.total_fixed_charges / self.max_demand_kw

        self.average_demand = self.load_factor * self.max_demand_kw
        self.annual_energy_kwh = self.average_demand * self.hours_per_year
        self.variable_royalty = self.royalty_per_kwh * self.annual_energy_kwh
        self.variable_maintenance = (1 - self.fixed_maintenance_percent) * self.total_maintenance
        self.total_variable_charges = self.variable_royalty + self.variable_maintenance
        self.cost_per_kwh = self.total_variable_charges / self.annual_energy_kwh

    def print_summary(self):
        """Print calculation summary"""
        print("\n" + "="*80)
        print(" "*25 + "HYDRO-POWER COST ANALYSIS")
        print("="*80)
        print(f"\n{'CALCULATION RESULTS':^80}")
        print("-"*80)
        print(f"  Total Capital Cost:           Rs. {self.total_capital_cost:>15,.2f}")
        print(f"  Annual Investment Charge:     Rs. {self.annual_investment_charge:>15,.2f}")
        print(f"  Fixed Royalty:                Rs. {self.fixed_royalty:>15,.2f}")
        print(f"  Fixed Maintenance:            Rs. {self.fixed_maintenance:>15,.2f}")
        print(f"  {'─'*40:>60}")
        print(f"  Total Fixed Charges:          Rs. {self.total_fixed_charges:>15,.2f}")
        print()
        print(f"  Annual Energy Generated:          {self.annual_energy_kwh:>15,.0f} kWh")
        print(f"  Variable Royalty:             Rs. {self.variable_royalty:>15,.2f}")
        print(f"  Variable Maintenance:         Rs. {self.variable_maintenance:>15,.2f}")
        print(f"  {'─'*40:>60}")
        print(f"  Total Variable Charges:       Rs. {self.total_variable_charges:>15,.2f}")
        print("\n" + "="*80)
        print(f"{'FINAL ANSWER':^80}")
        print("="*80)
        print(f"\n  Fixed Cost (A):     Rs. {self.cost_per_kw:.2f} per kW")
        print(f"  Variable Cost (B):  Rs. {self.cost_per_kwh:.4f} per kWh")
        print(f"\n  {'Generation Cost = Rs. ' + f'{self.cost_per_kw:.2f}' + ' per kW + Rs. ' + f'{self.cost_per_kwh:.4f}' + ' per kWh':^80}")
        print("\n" + "="*80 + "\n")

    def create_visualizations(self):
        """Create comprehensive matplotlib visualizations"""

        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')

        # Create main figure
        fig = plt.figure(figsize=(20, 12))
        fig.suptitle('Hydro-Power Station Cost Analysis\nComprehensive Visualization',
                     fontsize=20, fontweight='bold', y=0.98)

        gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.35)

        # 1. Main Result Box (Top Center)
        ax_result = fig.add_subplot(gs[0, :])
        ax_result.axis('off')

        result_text = f"""
FINAL ANSWER

Generation Cost = Rs. {self.cost_per_kw:.2f} per kW + Rs. {self.cost_per_kwh:.4f} per kWh

Where:
    A (Fixed Cost) = Rs. {self.cost_per_kw:.2f} per kW
    B (Variable Cost) = Rs. {self.cost_per_kwh:.4f} per kWh
"""

        ax_result.text(0.5, 0.5, result_text,
                      transform=ax_result.transAxes,
                      fontsize=16, fontweight='bold',
                      verticalalignment='center',
                      horizontalalignment='center',
                      bbox=dict(boxstyle='round,pad=1', facecolor='lightgreen',
                               edgecolor='black', linewidth=3, alpha=0.8))

        # 2. Pie Chart - Fixed vs Variable
        ax1 = fig.add_subplot(gs[1, 0])
        sizes = [self.total_fixed_charges, self.total_variable_charges]
        labels = [f'Fixed Charges\nRs. {self.total_fixed_charges:,.0f}\n({100*self.total_fixed_charges/sum(sizes):.1f}%)',
                 f'Variable Charges\nRs. {self.total_variable_charges:,.0f}\n({100*self.total_variable_charges/sum(sizes):.1f}%)']
        colors = ['#ff9999', '#66b3ff']
        explode = (0.05, 0.05)

        wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels,
                                            colors=colors, autopct='%1.1f%%',
                                            shadow=True, startangle=90,
                                            textprops={'fontsize': 10, 'fontweight': 'bold'})
        ax1.set_title('Fixed vs Variable Cost\nDistribution',
                     fontsize=13, fontweight='bold', pad=15)

        # 3. Horizontal Bar - Cost Components
        ax2 = fig.add_subplot(gs[1, 1])
        components = ['Investment\nCharge', 'Fixed\nRoyalty', 'Fixed\nMaintenance',
                     'Variable\nRoyalty', 'Variable\nMaintenance']
        values = [self.annual_investment_charge, self.fixed_royalty,
                 self.fixed_maintenance, self.variable_royalty,
                 self.variable_maintenance]
        colors_bar = ['#ff6666', '#ff9999', '#ffcccc', '#6699ff', '#99ccff']

        y_pos = np.arange(len(components))
        bars = ax2.barh(y_pos, values, color=colors_bar, edgecolor='black', linewidth=1.5)

        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2.,
                    f' Rs. {width:,.0f}',
                    ha='left', va='center', fontsize=9, fontweight='bold')

        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(components, fontsize=10)
        ax2.set_xlabel('Cost (Rs.)', fontsize=11, fontweight='bold')
        ax2.set_title('Detailed Cost Components', fontsize=13, fontweight='bold', pad=15)
        ax2.grid(axis='x', alpha=0.3, linestyle='--')

        # 4. Stacked Bar - Fixed + Variable
        ax3 = fig.add_subplot(gs[1, 2])
        categories = ['Total\nAnnual\nCost']
        fixed = [self.total_fixed_charges]
        variable = [self.total_variable_charges]

        x = np.arange(len(categories))
        width = 0.5

        bars1 = ax3.bar(x, fixed, width, label='Fixed Charges',
                       color='#ff9999', edgecolor='black', linewidth=2)
        bars2 = ax3.bar(x, variable, width, bottom=fixed, label='Variable Charges',
                       color='#66b3ff', edgecolor='black', linewidth=2)

        ax3.text(0, fixed[0]/2, f'Rs. {fixed[0]:,.0f}',
                ha='center', va='center', fontsize=11, fontweight='bold')
        ax3.text(0, fixed[0] + variable[0]/2, f'Rs. {variable[0]:,.0f}',
                ha='center', va='center', fontsize=11, fontweight='bold')

        ax3.set_ylabel('Cost (Rs.)', fontsize=11, fontweight='bold')
        ax3.set_title('Stacked Cost View', fontsize=13, fontweight='bold', pad=15)
        ax3.set_xticks(x)
        ax3.set_xticklabels(categories, fontsize=10)
        ax3.legend(loc='upper right', fontsize=10)
        ax3.grid(axis='y', alpha=0.3, linestyle='--')

        # 5. Load Factor Sensitivity
        ax4 = fig.add_subplot(gs[2, 0])
        load_factors = np.linspace(0.5, 1.0, 11)
        variable_costs_per_kwh = []

        for lf in load_factors:
            avg_demand = lf * self.max_demand_kw
            annual_energy = avg_demand * self.hours_per_year
            var_royalty = self.royalty_per_kwh * annual_energy
            total_var_charges = var_royalty + self.variable_maintenance
            var_cost_per_kwh = total_var_charges / annual_energy
            variable_costs_per_kwh.append(var_cost_per_kwh)

        ax4.plot(load_factors * 100, variable_costs_per_kwh, 'b-o',
                linewidth=2.5, markersize=8, label='Variable Cost per kWh')
        ax4.axvline(x=self.load_factor * 100, color='r', linestyle='--',
                   linewidth=2.5, label=f'Current LF ({self.load_factor*100:.0f}%)')
        ax4.axhline(y=self.cost_per_kwh, color='g', linestyle='--',
                   linewidth=2, label=f'Current Cost\n(Rs. {self.cost_per_kwh:.4f}/kWh)')

        ax4.set_xlabel('Load Factor (%)', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Variable Cost per kWh (Rs.)', fontsize=11, fontweight='bold')
        ax4.set_title('Load Factor Impact on\nVariable Cost',
                     fontsize=13, fontweight='bold', pad=15)
        ax4.grid(True, alpha=0.3)
        ax4.legend(fontsize=9, loc='upper right')

        # 6. Component Percentage
        ax5 = fig.add_subplot(gs[2, 1])
        total_cost = self.total_fixed_charges + self.total_variable_charges

        components_pct = {
            'Investment\nCharge': self.annual_investment_charge/total_cost*100,
            'Fixed\nRoyalty': self.fixed_royalty/total_cost*100,
            'Fixed\nMaint.': self.fixed_maintenance/total_cost*100,
            'Variable\nRoyalty': self.variable_royalty/total_cost*100,
            'Variable\nMaint.': self.variable_maintenance/total_cost*100
        }

        labels_pct = list(components_pct.keys())
        values_pct = list(components_pct.values())
        colors_pct = ['#ff6666', '#ff9999', '#ffcccc', '#6699ff', '#99ccff']

        bars = ax5.bar(labels_pct, values_pct, color=colors_pct,
                      edgecolor='black', linewidth=1.5)

        for bar in bars:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax5.set_ylabel('Percentage of Total Cost (%)', fontsize=11, fontweight='bold')
        ax5.set_title('Cost Component\nPercentage Distribution',
                     fontsize=13, fontweight='bold', pad=15)
        ax5.grid(axis='y', alpha=0.3, linestyle='--')
        ax5.tick_params(axis='x', labelsize=9)

        # 7. Cost Comparison Table
        ax6 = fig.add_subplot(gs[2, 2])
        ax6.axis('tight')
        ax6.axis('off')

        demands = [10000, 20000, 30000, 40000]
        table_data = []

        for demand in demands:
            energy = demand * 0.80 * self.hours_per_year
            fixed_cost = self.cost_per_kw * demand
            variable_cost = self.cost_per_kwh * energy
            total = fixed_cost + variable_cost
            table_data.append([f'{demand:,}', f'{energy:,.0f}',
                              f'{fixed_cost:,.0f}', f'{variable_cost:,.0f}',
                              f'{total:,.0f}'])

        table = ax6.table(cellText=table_data,
                         colLabels=['Demand\n(kW)', 'Energy/Year\n(kWh)',
                                   'Fixed Cost\n(Rs.)', 'Variable Cost\n(Rs.)',
                                   'Total Cost\n(Rs.)'],
                         cellLoc='center',
                         loc='center',
                         bbox=[0, 0, 1, 1])

        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2.5)

        # Style header
        for i in range(5):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')

        # Alternate row colors
        for i in range(1, len(table_data) + 1):
            for j in range(5):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#f0f0f0')
                else:
                    table[(i, j)].set_facecolor('#ffffff')

        ax6.set_title('Cost Comparison at\nDifferent Load Levels',
                     fontsize=13, fontweight='bold', pad=15)

        # Save figure
        plt.savefig('hydropower_analysis_full.png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        print("\n✓ Comprehensive visualization saved as 'hydropower_analysis_full.png'")

        # Display
        plt.show()


def main():
    """Main execution"""
    print("\n" + "█"*80)
    print("█" + " "*20 + "HYDRO-POWER STATION COST ANALYSIS" + " "*27 + "█")
    print("█" + " "*25 + "WITH MATPLOTLIB VISUALIZATION" + " "*26 + "█")
    print("█"*80)

    analyzer = HydroPowerAnalyzer()
    analyzer.print_summary()

    print("\n" + "─"*80)
    print("Generating comprehensive visualizations...")
    print("─"*80)

    analyzer.create_visualizations()

    print("\n" + "✓"*80)
    print("\nVisualization complete! Check 'hydropower_analysis_full.png'")
    print("\n" + "✓"*80 + "\n")


if __name__ == "__main__":
    main()
