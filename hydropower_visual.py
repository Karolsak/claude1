"""
Hydro-Power Station Cost Analysis with ASCII Visualization
Enhanced version with detailed visual representation
"""


class HydroPowerVisualAnalyzer:
    """Enhanced analyzer with visual ASCII charts"""

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
        self.variable_maintenance = ((1 - self.fixed_maintenance_percent) *
                                    self.total_maintenance)
        self.total_variable_charges = self.variable_royalty + self.variable_maintenance
        self.cost_per_kwh = self.total_variable_charges / self.annual_energy_kwh

    def draw_pie_chart(self, title, data, width=60):
        """Draw an ASCII pie chart"""
        total = sum(d[1] for d in data)
        print("\n" + "┌" + "─" * (width + 2) + "┐")
        title_padding = (width - len(title)) // 2
        print("│ " + " " * title_padding + title + " " * (width - title_padding - len(title)) + " │")
        print("├" + "─" * (width + 2) + "┤")

        for label, value in data:
            percentage = (value / total) * 100
            bar_length = int((percentage / 100) * (width - 30))
            bar = "█" * bar_length
            print(f"│ {label:<25} {bar:<{width-30}} {percentage:5.1f}% │")
            print(f"│ {'':25} Rs. {value:>12,.0f}{'':>{width-43}} │")

        print("│" + " " * (width + 2) + "│")
        print(f"│ {'TOTAL:':<25} Rs. {total:>12,.0f}{'':>{width-43}} │")
        print("└" + "─" * (width + 2) + "┘")

    def draw_horizontal_bar(self, title, data, width=70):
        """Draw horizontal bar chart"""
        max_value = max(d[1] for d in data)
        print("\n" + "┌" + "─" * (width + 2) + "┐")
        title_padding = (width - len(title)) // 2
        print("│ " + " " * title_padding + title + " " * (width - title_padding - len(title)) + " │")
        print("├" + "─" * (width + 2) + "┤")

        for label, value in data:
            bar_length = int((value / max_value) * 40)
            bar = "▓" * bar_length
            percentage = (value / sum(d[1] for d in data)) * 100
            print(f"│ {label:<25} {bar:<40} │")
            print(f"│ {'':25} Rs. {value:>10,.0f} ({percentage:>5.2f}%) │")

        print("└" + "─" * (width + 2) + "┘")

    def draw_load_factor_analysis(self):
        """Draw load factor impact analysis"""
        print("\n" + "┌" + "─" * 78 + "┐")
        print("│" + " " * 20 + "LOAD FACTOR IMPACT ANALYSIS" + " " * 31 + "│")
        print("├" + "─" * 78 + "┤")
        print("│                                                                              │")
        print("│  Load Factor Impact on Variable Cost per kWh:                               │")
        print("│                                                                              │")

        load_factors = [0.50, 0.60, 0.70, 0.80, 0.90, 1.00]

        for lf in load_factors:
            avg_demand = lf * self.max_demand_kw
            annual_energy = avg_demand * self.hours_per_year
            var_royalty = self.royalty_per_kwh * annual_energy
            total_var = var_royalty + self.variable_maintenance
            cost_kwh = total_var / annual_energy

            bar_length = int(cost_kwh * 2000)
            bar = "█" * bar_length
            marker = " <-- Current" if abs(lf - self.load_factor) < 0.01 else ""

            print(f"│  {lf*100:>5.0f}%  Rs. {cost_kwh:.6f}/kWh  {bar:<30}{marker:<12}  │")

        print("│                                                                              │")
        print("└" + "─" * 78 + "┘")

    def draw_cost_formula(self):
        """Draw the cost formula visualization"""
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + " " * 20 + "COST FORMULA BREAKDOWN" + " " * 35 + "║")
        print("╠" + "═" * 78 + "╣")
        print("║                                                                              ║")
        print("║  Generation Cost = A per kW + B per kWh                                     ║")
        print("║                                                                              ║")
        print("║  Where:                                                                      ║")
        print(f"║      A = Rs. {self.cost_per_kw:.2f} per kW (Fixed Cost Component)                      ║")
        print(f"║      B = Rs. {self.cost_per_kwh:.6f} per kWh (Variable Cost Component)              ║")
        print("║                                                                              ║")
        print("║  ┌────────────────────────────────────────────────────────────────────────┐ ║")
        print("║  │                                                                        │ ║")
        print(f"║  │   ANSWER: Rs. {self.cost_per_kw:.2f}/kW + Rs. {self.cost_per_kwh:.4f}/kWh                     │ ║")
        print("║  │                                                                        │ ║")
        print("║  └────────────────────────────────────────────────────────────────────────┘ ║")
        print("║                                                                              ║")
        print("║  For a customer using P kW demand and E kWh energy:                         ║")
        print(f"║      Total Cost = {self.cost_per_kw:.2f} × P + {self.cost_per_kwh:.4f} × E                           ║")
        print("║                                                                              ║")
        print("║  Example: If P = 1000 kW and E = 100,000 kWh:                               ║")
        example_p = 1000
        example_e = 100000
        example_cost = self.cost_per_kw * example_p + self.cost_per_kwh * example_e
        print(f"║      Total Cost = {self.cost_per_kw:.2f} × {example_p} + {self.cost_per_kwh:.4f} × {example_e}                     ║")
        print(f"║                 = Rs. {self.cost_per_kw * example_p:,.2f} + Rs. {self.cost_per_kwh * example_e:,.2f}                           ║")
        print(f"║                 = Rs. {example_cost:,.2f}                                              ║")
        print("║                                                                              ║")
        print("╚" + "═" * 78 + "╝")

    def draw_comparison_table(self):
        """Draw comparison table for different scenarios"""
        print("\n" + "┌" + "─" * 78 + "┐")
        print("│" + " " * 18 + "COST COMPARISON AT DIFFERENT LOADS" + " " * 26 + "│")
        print("├" + "─" * 78 + "┤")
        print("│                                                                              │")
        print("│  Demand  │  Energy/Year    │  Fixed Cost  │ Variable Cost │  Total Cost    │")
        print("│  (kW)    │  (kWh)          │  (Rs.)       │ (Rs.)         │  (Rs.)         │")
        print("│" + "─" * 76 + "│")

        demands = [10000, 20000, 30000, 40000]
        for demand in demands:
            # Assume 80% load factor for each
            energy = demand * 0.80 * self.hours_per_year
            fixed_cost = self.cost_per_kw * demand
            variable_cost = self.cost_per_kwh * energy
            total_cost = fixed_cost + variable_cost

            print(f"│  {demand:>6,} │ {energy:>15,.0f} │ {fixed_cost:>12,.2f} │ {variable_cost:>13,.2f} │ {total_cost:>14,.2f} │")

        print("│                                                                              │")
        print("└" + "─" * 78 + "┘")

    def display_all(self):
        """Display complete analysis with visualizations"""
        print("\n" + "█" * 80)
        print("█" + " " * 15 + "HYDRO-POWER STATION COST ANALYSIS" + " " * 32 + "█")
        print("█" + " " * 25 + "WITH VISUALIZATION" + " " * 37 + "█")
        print("█" * 80)

        # 1. Main calculation results
        print("\n" + "▼" * 40 + " CALCULATION RESULTS " + "▼" * 39)

        self.draw_cost_formula()

        # 2. Fixed vs Variable breakdown
        print("\n" + "▼" * 40 + " COST BREAKDOWN " + "▼" * 44)

        fixed_variable_data = [
            ("Fixed Charges", self.total_fixed_charges),
            ("Variable Charges", self.total_variable_charges)
        ]
        self.draw_pie_chart("FIXED vs VARIABLE COST DISTRIBUTION", fixed_variable_data)

        # 3. Detailed components
        components_data = [
            ("Investment Charge", self.annual_investment_charge),
            ("Fixed Royalty", self.fixed_royalty),
            ("Fixed Maintenance", self.fixed_maintenance),
            ("Variable Royalty", self.variable_royalty),
            ("Variable Maintenance", self.variable_maintenance)
        ]
        self.draw_horizontal_bar("DETAILED COST COMPONENTS", components_data)

        # 4. Load factor analysis
        print("\n" + "▼" * 40 + " SENSITIVITY ANALYSIS " + "▼" * 38)
        self.draw_load_factor_analysis()

        # 5. Comparison table
        print("\n" + "▼" * 40 + " PRACTICAL EXAMPLES " + "▼" * 40)
        self.draw_comparison_table()

        # 6. Summary box
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + " " * 32 + "KEY FINDINGS" + " " * 34 + "║")
        print("╠" + "═" * 78 + "╣")
        print("║                                                                              ║")
        print(f"║  • Fixed charges dominate at {(self.total_fixed_charges/(self.total_fixed_charges+self.total_variable_charges))*100:.1f}% of total annual cost              ║")
        print(f"║  • Investment charge is the largest component at {(self.annual_investment_charge/(self.total_fixed_charges+self.total_variable_charges))*100:.1f}%             ║")
        print(f"║  • At current {self.load_factor*100:.0f}% load factor, generating {self.annual_energy_kwh:,.0f} kWh/year     ║")
        print(f"║  • Total annual operating cost: Rs. {self.total_fixed_charges + self.total_variable_charges:,.2f}                         ║")
        print(f"║  • Average cost per kWh (if all costs averaged): Rs. {(self.total_fixed_charges + self.total_variable_charges)/self.annual_energy_kwh:.4f}/kWh        ║")
        print("║                                                                              ║")
        print("╚" + "═" * 78 + "╝")

        print("\n" + "█" * 80)
        print("█" + " " * 78 + "█")
        print("█" + " " * 10 + "✓ Analysis Complete - Generation Cost Determined" + " " * 19 + "█")
        print("█" + " " * 78 + "█")
        print("█" * 80 + "\n")


def main():
    """Main execution"""
    analyzer = HydroPowerVisualAnalyzer()
    analyzer.display_all()

    # Print final answer prominently
    print("\n" + "┏" + "━" * 78 + "┓")
    print("┃" + " " * 20 + "🎯 FINAL ANSWER TO THE PROBLEM 🎯" + " " * 25 + "┃")
    print("┣" + "━" * 78 + "┫")
    print("┃" + " " * 78 + "┃")
    answer = f"Generation Cost = Rs. {analyzer.cost_per_kw:.2f} per kW + Rs. {analyzer.cost_per_kwh:.4f} per kWh"
    padding = (78 - len(answer)) // 2
    print("┃" + " " * padding + answer + " " * (78 - padding - len(answer)) + "┃")
    print("┃" + " " * 78 + "┃")
    print("┃" + " " * 30 + "Where:" + " " * 43 + "┃")
    print(f"┃" + " " * 25 + f"A = Rs. {analyzer.cost_per_kw:.2f} per kW" + " " * (78 - 25 - len(f"A = Rs. {analyzer.cost_per_kw:.2f} per kW")) + "┃")
    print(f"┃" + " " * 25 + f"B = Rs. {analyzer.cost_per_kwh:.4f} per kWh" + " " * (78 - 25 - len(f"B = Rs. {analyzer.cost_per_kwh:.4f} per kWh")) + "┃")
    print("┃" + " " * 78 + "┃")
    print("┗" + "━" * 78 + "┛\n")


if __name__ == "__main__":
    main()
