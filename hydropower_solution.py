"""
Hydro-Power Station Cost Analysis
Problem: Calculate generation cost in the form of A per kW plus B per kWh

Given:
- Capacity: 50,000 kW
- Capital cost: Rs. 1,200 per kW
- Annual charge on investment: 10%
- Royalty: Rs. 1 per kW per year + Rs. 0.01 per kWh
- Maximum demand: 40,000 kW
- Load factor: 80%
- Maintenance/Salaries: Rs. 6,50,000 (20% fixed, 80% variable)
"""


class HydroPowerCostAnalyzer:
    """Analyzes hydro-power station costs"""

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

        # Calculate all costs
        self.calculate()

    def calculate(self):
        """Perform all cost calculations"""

        # Step 1: Calculate total capital cost
        self.total_capital_cost = self.capacity_kw * self.capital_cost_per_kw

        # Step 2: Calculate annual investment charge (depreciation)
        self.annual_investment_charge = self.total_capital_cost * self.annual_charge_rate

        # Step 3: Calculate fixed royalty (based on maximum demand)
        self.fixed_royalty = self.royalty_per_kw * self.max_demand_kw

        # Step 4: Calculate fixed maintenance
        self.fixed_maintenance = self.fixed_maintenance_percent * self.total_maintenance

        # Step 5: Calculate total fixed charges
        self.total_fixed_charges = (
            self.annual_investment_charge +
            self.fixed_royalty +
            self.fixed_maintenance
        )

        # Step 6: Calculate fixed cost per kW (A)
        self.cost_per_kw = self.total_fixed_charges / self.max_demand_kw

        # Step 7: Calculate annual energy generated
        self.average_demand = self.load_factor * self.max_demand_kw
        self.annual_energy_kwh = self.average_demand * self.hours_per_year

        # Step 8: Calculate variable royalty
        self.variable_royalty = self.royalty_per_kwh * self.annual_energy_kwh

        # Step 9: Calculate variable maintenance
        self.variable_maintenance = (1 - self.fixed_maintenance_percent) * self.total_maintenance

        # Step 10: Calculate total variable charges
        self.total_variable_charges = self.variable_royalty + self.variable_maintenance

        # Step 11: Calculate variable cost per kWh (B)
        self.cost_per_kwh = self.total_variable_charges / self.annual_energy_kwh

    def print_detailed_report(self):
        """Print comprehensive cost analysis report"""

        print("\n" + "="*80)
        print(" "*20 + "HYDRO-POWER STATION COST ANALYSIS")
        print("="*80 + "\n")

        # Given Data Section
        print("┌" + "─"*78 + "┐")
        print("│" + " "*28 + "GIVEN DATA" + " "*40 + "│")
        print("├" + "─"*78 + "┤")
        print(f"│  Station Capacity              : {self.capacity_kw:>10,} kW" + " "*34 + "│")
        print(f"│  Capital Cost per kW           : Rs. {self.capital_cost_per_kw:>7,}" + " "*37 + "│")
        print(f"│  Total Capital Cost            : Rs. {self.total_capital_cost:>10,.0f}" + " "*29 + "│")
        print(f"│  Annual Charge Rate            : {self.annual_charge_rate*100:>10.0f}%" + " "*38 + "│")
        print(f"│  Maximum Demand                : {self.max_demand_kw:>10,} kW" + " "*34 + "│")
        print(f"│  Load Factor                   : {self.load_factor*100:>10.0f}%" + " "*38 + "│")
        print(f"│  Total Maintenance & Salaries  : Rs. {self.total_maintenance:>9,}" + " "*30 + "│")
        print(f"│  Fixed Maintenance Portion     : {self.fixed_maintenance_percent*100:>10.0f}%" + " "*38 + "│")
        print("└" + "─"*78 + "┘\n")

        # Fixed Charges Calculation
        print("┌" + "─"*78 + "┐")
        print("│" + " "*23 + "FIXED CHARGES CALCULATION" + " "*30 + "│")
        print("├" + "─"*78 + "┤")
        print("│                                                                              │")
        print("│  1. Annual Investment Charge (10% of Capital Cost):                          │")
        print(f"│     = 10% × Rs. {self.total_capital_cost:,.0f}" + " "*(73-len(f"     = 10% × Rs. {self.total_capital_cost:,.0f}")) + "│")
        print(f"│     = Rs. {self.annual_investment_charge:,.2f}" + " "*(73-len(f"     = Rs. {self.annual_investment_charge:,.2f}")) + "│")
        print("│                                                                              │")
        print("│  2. Fixed Royalty (Rs. 1 per kW on Maximum Demand):                          │")
        print(f"│     = {self.max_demand_kw:,} kW × Rs. 1" + " "*(73-len(f"     = {self.max_demand_kw:,} kW × Rs. 1")) + "│")
        print(f"│     = Rs. {self.fixed_royalty:,.2f}" + " "*(73-len(f"     = Rs. {self.fixed_royalty:,.2f}")) + "│")
        print("│                                                                              │")
        print("│  3. Fixed Maintenance (20% of Total Maintenance):                            │")
        print(f"│     = 20% × Rs. {self.total_maintenance:,}" + " "*(73-len(f"     = 20% × Rs. {self.total_maintenance:,}")) + "│")
        print(f"│     = Rs. {self.fixed_maintenance:,.2f}" + " "*(73-len(f"     = Rs. {self.fixed_maintenance:,.2f}")) + "│")
        print("│                                                                              │")
        print("│" + " "*5 + "─"*68 + " │")
        print(f"│     TOTAL FIXED CHARGES = Rs. {self.total_fixed_charges:,.2f}" + " "*(73-len(f"     TOTAL FIXED CHARGES = Rs. {self.total_fixed_charges:,.2f}")) + "│")
        print("│" + " "*5 + "─"*68 + " │")
        print("└" + "─"*78 + "┘\n")

        # Energy Generation
        print("┌" + "─"*78 + "┐")
        print("│" + " "*20 + "ENERGY GENERATION CALCULATION" + " "*29 + "│")
        print("├" + "─"*78 + "┤")
        print("│                                                                              │")
        print("│  Average Demand = Load Factor × Maximum Demand                              │")
        print(f"│                 = {self.load_factor} × {self.max_demand_kw:,} kW" + " "*(73-len(f"│                 = {self.load_factor} × {self.max_demand_kw:,} kW")) + "│")
        print(f"│                 = {self.average_demand:,.0f} kW" + " "*(73-len(f"│                 = {self.average_demand:,.0f} kW")) + "│")
        print("│                                                                              │")
        print("│  Annual Energy Generated = Average Demand × Hours per Year                  │")
        print(f"│                          = {self.average_demand:,.0f} kW × {self.hours_per_year:,} hours" + " "*(73-len(f"│                          = {self.average_demand:,.0f} kW × {self.hours_per_year:,} hours")) + "│")
        print(f"│                          = {self.annual_energy_kwh:,.0f} kWh" + " "*(73-len(f"│                          = {self.annual_energy_kwh:,.0f} kWh")) + "│")
        print("│                                                                              │")
        print("└" + "─"*78 + "┘\n")

        # Variable Charges Calculation
        print("┌" + "─"*78 + "┐")
        print("│" + " "*21 + "VARIABLE CHARGES CALCULATION" + " "*29 + "│")
        print("├" + "─"*78 + "┤")
        print("│                                                                              │")
        print("│  1. Variable Royalty (Rs. 0.01 per kWh Generated):                          │")
        print(f"│     = {self.annual_energy_kwh:,.0f} kWh × Rs. 0.01" + " "*(73-len(f"     = {self.annual_energy_kwh:,.0f} kWh × Rs. 0.01")) + "│")
        print(f"│     = Rs. {self.variable_royalty:,.2f}" + " "*(73-len(f"     = Rs. {self.variable_royalty:,.2f}")) + "│")
        print("│                                                                              │")
        print("│  2. Variable Maintenance (80% of Total Maintenance):                        │")
        print(f"│     = 80% × Rs. {self.total_maintenance:,}" + " "*(73-len(f"     = 80% × Rs. {self.total_maintenance:,}")) + "│")
        print(f"│     = Rs. {self.variable_maintenance:,.2f}" + " "*(73-len(f"     = Rs. {self.variable_maintenance:,.2f}")) + "│")
        print("│                                                                              │")
        print("│" + " "*5 + "─"*68 + " │")
        print(f"│     TOTAL VARIABLE CHARGES = Rs. {self.total_variable_charges:,.2f}" + " "*(73-len(f"     TOTAL VARIABLE CHARGES = Rs. {self.total_variable_charges:,.2f}")) + "│")
        print("│" + " "*5 + "─"*68 + " │")
        print("└" + "─"*78 + "┘\n")

        # Final Generation Cost
        print("╔" + "═"*78 + "╗")
        print("║" + " "*23 + "FINAL GENERATION COST" + " "*34 + "║")
        print("╠" + "═"*78 + "╣")
        print("║                                                                              ║")
        print("║  Cost per kW (A):                                                            ║")
        print("║      = Total Fixed Charges / Maximum Demand                                  ║")
        print(f"║      = Rs. {self.total_fixed_charges:,.2f} / {self.max_demand_kw:,} kW" + " "*(73-len(f"║      = Rs. {self.total_fixed_charges:,.2f} / {self.max_demand_kw:,} kW")) + "║")
        print(f"║      = Rs. {self.cost_per_kw:.4f} per kW" + " "*(73-len(f"║      = Rs. {self.cost_per_kw:.4f} per kW")) + "║")
        print("║                                                                              ║")
        print("║  Cost per kWh (B):                                                           ║")
        print("║      = Total Variable Charges / Annual Energy Generated                     ║")
        print(f"║      = Rs. {self.total_variable_charges:,.2f} / {self.annual_energy_kwh:,.0f} kWh" + " "*(73-len(f"║      = Rs. {self.total_variable_charges:,.2f} / {self.annual_energy_kwh:,.0f} kWh")) + "║")
        print(f"║      = Rs. {self.cost_per_kwh:.6f} per kWh" + " "*(73-len(f"║      = Rs. {self.cost_per_kwh:.6f} per kWh")) + "║")
        print("║                                                                              ║")
        print("╠" + "═"*78 + "╣")
        print("║" + " "*30 + "FINAL ANSWER" + " "*36 + "║")
        print("║                                                                              ║")
        answer = f"Generation Cost = Rs. {self.cost_per_kw:.2f} per kW + Rs. {self.cost_per_kwh:.4f} per kWh"
        padding = (78 - len(answer)) // 2
        print("║" + " "*padding + answer + " "*(78-padding-len(answer)) + "║")
        print("║                                                                              ║")
        print("╚" + "═"*78 + "╝\n")

        # Cost Breakdown Summary
        total_annual_cost = self.total_fixed_charges + self.total_variable_charges
        fixed_percent = (self.total_fixed_charges / total_annual_cost) * 100
        variable_percent = (self.total_variable_charges / total_annual_cost) * 100

        print("┌" + "─"*78 + "┐")
        print("│" + " "*24 + "COST BREAKDOWN SUMMARY" + " "*32 + "│")
        print("├" + "─"*78 + "┤")
        print("│                                                                              │")
        print(f"│  Total Annual Cost = Rs. {self.total_fixed_charges:,.2f} + Rs. {self.total_variable_charges:,.2f}" + " "*(73-len(f"│  Total Annual Cost = Rs. {self.total_fixed_charges:,.2f} + Rs. {self.total_variable_charges:,.2f}")) + "│")
        print(f"│                    = Rs. {total_annual_cost:,.2f}" + " "*(73-len(f"│                    = Rs. {total_annual_cost:,.2f}")) + "│")
        print("│                                                                              │")
        print(f"│  Fixed Cost Percentage     : {fixed_percent:>6.2f}%" + " "*(73-len(f"│  Fixed Cost Percentage     : {fixed_percent:>6.2f}%")) + "│")
        print(f"│  Variable Cost Percentage  : {variable_percent:>6.2f}%" + " "*(73-len(f"│  Variable Cost Percentage  : {variable_percent:>6.2f}%")) + "│")
        print("│                                                                              │")
        print("└" + "─"*78 + "┘\n")

        # Component Breakdown Bar Chart (ASCII)
        print("┌" + "─"*78 + "┐")
        print("│" + " "*26 + "COST COMPONENTS CHART" + " "*31 + "│")
        print("├" + "─"*78 + "┤")
        print("│                                                                              │")

        components = [
            ("Investment Charge", self.annual_investment_charge),
            ("Fixed Royalty", self.fixed_royalty),
            ("Fixed Maintenance", self.fixed_maintenance),
            ("Variable Royalty", self.variable_royalty),
            ("Variable Maintenance", self.variable_maintenance)
        ]

        max_value = max(c[1] for c in components)
        bar_width = 50

        for name, value in components:
            bar_length = int((value / max_value) * bar_width)
            percentage = (value / total_annual_cost) * 100
            bar = "█" * bar_length
            print(f"│  {name:.<22} {bar:<50}  │")
            print(f"│  {'':<22} Rs. {value:>10,.0f} ({percentage:>5.2f}%){'':<18}  │")

        print("│                                                                              │")
        print("└" + "─"*78 + "┘\n")

        print("="*80)
        print("\n")


def main():
    """Main execution function"""
    analyzer = HydroPowerCostAnalyzer()
    analyzer.print_detailed_report()

    # Print summary for quick reference
    print("\n" + "▶"*40)
    print("\n🔹 QUICK SUMMARY:")
    print(f"\n   A (Fixed Cost)     = Rs. {analyzer.cost_per_kw:.2f} per kW")
    print(f"   B (Variable Cost)  = Rs. {analyzer.cost_per_kwh:.4f} per kWh")
    print(f"\n   Generation Cost = Rs. {analyzer.cost_per_kw:.2f}/kW + Rs. {analyzer.cost_per_kwh:.4f}/kWh")
    print("\n" + "▶"*40 + "\n")


if __name__ == "__main__":
    main()
