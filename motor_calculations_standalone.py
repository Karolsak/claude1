"""
Standalone induction motor calculations (no GUI dependencies)
Solves the specific problem and demonstrates all calculations
"""

import math


class MotorParameters:
    """Motor parameters data structure"""
    def __init__(self):
        self.poles = 4
        self.voltage_ll = 460.0  # Line-to-line voltage (V)
        self.frequency = 50.0  # Hz
        self.current = 25.0  # A
        self.power_factor = 0.85

        # Losses
        self.stator_loss = 1000.0  # W
        self.rotor_loss = 500.0  # W
        self.rotational_loss = 250.0  # W
        self.core_loss = 800.0  # W
        self.stray_loss = 200.0  # W


class InductionMotorAnalyzer:
    """Static analysis of induction motor"""

    def __init__(self, params):
        self.params = params
        self.results = {}

    def calculate_all(self):
        """Calculate all motor parameters"""
        # (a) Input power
        sqrt3 = math.sqrt(3)
        p_in = sqrt3 * self.params.voltage_ll * self.params.current * self.params.power_factor
        self.results['p_in'] = p_in

        # (a) Electromagnetic (air gap) power
        p_elm = p_in - self.params.stator_loss - self.params.core_loss - self.params.stray_loss
        self.results['p_elm'] = p_elm

        # (b) Mechanical power
        p_m = p_elm - self.params.rotor_loss
        self.results['p_m'] = p_m

        # (c) Output power
        p_out = p_m - self.params.rotational_loss
        self.results['p_out'] = p_out

        # (d) Efficiency
        efficiency = (p_out / p_in) * 100 if p_in > 0 else 0
        self.results['efficiency'] = efficiency

        # (e) Slip and operating speed
        slip = self.params.rotor_loss / p_elm if p_elm > 0 else 0
        self.results['slip'] = slip

        # Synchronous speed
        n_s = (120 * self.params.frequency) / self.params.poles  # rpm
        self.results['n_s'] = n_s

        # Operating speed
        n = n_s * (1 - slip)
        self.results['n'] = n

        # Angular velocities (rad/s)
        omega_s = (2 * math.pi * self.params.frequency) * 2 / self.params.poles
        omega_m = omega_s * (1 - slip)
        self.results['omega_s'] = omega_s
        self.results['omega_m'] = omega_m

        # (f) Electromagnetic torque
        t_elm = p_elm / omega_s if omega_s > 0 else 0
        self.results['t_elm'] = t_elm

        # (g) Shaft (output) torque
        t_out = p_out / omega_m if omega_m > 0 else 0
        self.results['t_out'] = t_out

        return self.results


def main():
    print("=" * 80)
    print(" INDUCTION MOTOR PROBLEM SOLUTION")
    print("=" * 80)
    print()

    # Create motor parameters with the problem data
    params = MotorParameters()

    print("GIVEN DATA:")
    print("-" * 80)
    print(f"Number of poles:                    {params.poles}")
    print(f"Line-to-line voltage:               {params.voltage_ll} V")
    print(f"Frequency:                          {params.frequency} Hz")
    print(f"Current:                            {params.current} A")
    print(f"Power factor:                       {params.power_factor} (lagging)")
    print(f"Stator winding loss (P_1w):         {params.stator_loss} W")
    print(f"Rotor winding loss (P_2w):          {params.rotor_loss} W")
    print(f"Rotational losses (P_rot):          {params.rotational_loss} W")
    print(f"Core loss (P_Fe):                   {params.core_loss} W")
    print(f"Stray load loss (P_str):            {params.stray_loss} W")
    print()

    # Create analyzer and calculate
    analyzer = InductionMotorAnalyzer(params)
    results = analyzer.calculate_all()

    print("DETAILED CALCULATIONS:")
    print("-" * 80)
    print()

    # Input power
    sqrt3 = math.sqrt(3)
    p_in = sqrt3 * params.voltage_ll * params.current * params.power_factor
    print(f"Input Power:")
    print(f"  P_in = √3 × V_LL × I × cos(φ)")
    print(f"  P_in = √3 × {params.voltage_ll} × {params.current} × {params.power_factor}")
    print(f"  P_in = {p_in:.2f} W")
    print()

    # (a) Electromagnetic power
    p_elm = p_in - params.stator_loss - params.core_loss - params.stray_loss
    print(f"(a) Electromagnetic (Air Gap) Power:")
    print(f"  P_elm = P_in - P_1w - P_Fe - P_str")
    print(f"  P_elm = {p_in:.2f} - {params.stator_loss} - {params.core_loss} - {params.stray_loss}")
    print(f"  P_elm = {p_elm:.2f} W")
    print()

    # (b) Mechanical power
    p_m = p_elm - params.rotor_loss
    print(f"(b) Mechanical Power:")
    print(f"  P_m = P_elm - P_2w")
    print(f"  P_m = {p_elm:.2f} - {params.rotor_loss}")
    print(f"  P_m = {p_m:.2f} W")
    print()

    # (c) Output power
    p_out = p_m - params.rotational_loss
    print(f"(c) Output Power:")
    print(f"  P_out = P_m - P_rot")
    print(f"  P_out = {p_m:.2f} - {params.rotational_loss}")
    print(f"  P_out = {p_out:.2f} W")
    print()

    # (d) Efficiency
    efficiency = (p_out / p_in) * 100
    print(f"(d) Efficiency:")
    print(f"  η = (P_out / P_in) × 100%")
    print(f"  η = ({p_out:.2f} / {p_in:.2f}) × 100%")
    print(f"  η = {efficiency:.2f}%")
    print()

    # (e) Slip and operating speed
    slip = params.rotor_loss / p_elm
    n_s = (120 * params.frequency) / params.poles
    n = n_s * (1 - slip)
    print(f"(e) Slip and Operating Speed:")
    print(f"  Slip: s = P_2w / P_elm")
    print(f"  s = {params.rotor_loss} / {p_elm:.2f}")
    print(f"  s = {slip:.4f} ({slip*100:.2f}%)")
    print()
    print(f"  Synchronous Speed: n_s = 120 × f / p")
    print(f"  n_s = 120 × {params.frequency} / {params.poles}")
    print(f"  n_s = {n_s:.2f} rpm")
    print()
    print(f"  Operating Speed: n = n_s × (1 - s)")
    print(f"  n = {n_s:.2f} × (1 - {slip:.4f})")
    print(f"  n = {n:.2f} rpm")
    print()

    # (f) Electromagnetic torque
    omega_s = (2 * math.pi * params.frequency) * 2 / params.poles
    t_elm = p_elm / omega_s
    print(f"(f) Electromagnetic Torque:")
    print(f"  ω_s = 4π × f / p = {omega_s:.2f} rad/s")
    print(f"  T_elm = P_elm / ω_s")
    print(f"  T_elm = {p_elm:.2f} / {omega_s:.2f}")
    print(f"  T_elm = {t_elm:.2f} N·m")
    print()

    # (g) Shaft torque
    omega_m = omega_s * (1 - slip)
    t_out = p_out / omega_m
    print(f"(g) Shaft (Output) Torque:")
    print(f"  ω_m = ω_s × (1 - s) = {omega_m:.2f} rad/s")
    print(f"  T_out = P_out / ω_m")
    print(f"  T_out = {p_out:.2f} / {omega_m:.2f}")
    print(f"  T_out = {t_out:.2f} N·m")
    print()

    print("=" * 80)
    print(" SUMMARY OF RESULTS")
    print("=" * 80)
    print()
    print(f"(a) Electromagnetic Power (P_elm):     {p_elm:10.2f} W")
    print(f"(b) Mechanical Power (P_m):            {p_m:10.2f} W")
    print(f"(c) Output Power (P_out):              {p_out:10.2f} W")
    print(f"(d) Efficiency (η):                    {efficiency:10.2f} %")
    print(f"(e) Slip (s):                          {slip:10.4f} ({slip*100:.2f}%)")
    print(f"    Operating Speed (n):               {n:10.2f} rpm")
    print(f"(f) Electromagnetic Torque (T_elm):    {t_elm:10.2f} N·m")
    print(f"(g) Shaft Torque (T_out):              {t_out:10.2f} N·m")
    print()
    print("=" * 80)
    print()

    print("POWER FLOW DIAGRAM:")
    print("-" * 80)
    print(f"Input Power ({p_in:.0f} W)")
    print("  │")
    print(f"  ├─→ Stator Loss ({params.stator_loss:.0f} W)")
    print(f"  ├─→ Core Loss ({params.core_loss:.0f} W)")
    print(f"  ├─→ Stray Loss ({params.stray_loss:.0f} W)")
    print("  │")
    print(f"  ↓ Electromagnetic Power ({p_elm:.0f} W)")
    print("  │")
    print(f"  ├─→ Rotor Loss ({params.rotor_loss:.0f} W)")
    print("  │")
    print(f"  ↓ Mechanical Power ({p_m:.0f} W)")
    print("  │")
    print(f"  ├─→ Rotational Loss ({params.rotational_loss:.0f} W)")
    print("  │")
    print(f"  ↓ Output Power ({p_out:.0f} W)")
    print()

    total_loss = (params.stator_loss + params.rotor_loss + params.core_loss +
                  params.rotational_loss + params.stray_loss)
    print(f"Total Losses: {total_loss:.0f} W ({total_loss/p_in*100:.2f}% of input)")
    print()

    print("=" * 80)
    print(" ADDITIONAL ANALYSIS")
    print("=" * 80)
    print()

    # Power factor analysis
    apparent_power = sqrt3 * params.voltage_ll * params.current
    reactive_power = math.sqrt(apparent_power**2 - p_in**2)
    print(f"Apparent Power (S):                {apparent_power:.2f} VA")
    print(f"Active Power (P):                  {p_in:.2f} W")
    print(f"Reactive Power (Q):                {reactive_power:.2f} VAR")
    print()

    # Performance metrics
    torque_per_amp = t_out / params.current
    power_per_amp = p_out / params.current
    print(f"Torque per Ampere:                 {torque_per_amp:.2f} N·m/A")
    print(f"Power per Ampere:                  {power_per_amp:.2f} W/A")
    print()

    # Loss breakdown percentage
    print("LOSS BREAKDOWN (% of input power):")
    print("-" * 80)
    print(f"Stator Winding Loss:               {params.stator_loss/p_in*100:6.2f} %")
    print(f"Rotor Winding Loss:                {params.rotor_loss/p_in*100:6.2f} %")
    print(f"Core Loss:                         {params.core_loss/p_in*100:6.2f} %")
    print(f"Rotational Loss:                   {params.rotational_loss/p_in*100:6.2f} %")
    print(f"Stray Load Loss:                   {params.stray_loss/p_in*100:6.2f} %")
    print(f"Total Losses:                      {total_loss/p_in*100:6.2f} %")
    print(f"Output Power:                      {p_out/p_in*100:6.2f} %")
    print()

    print("=" * 80)
    print(" CALCULATIONS COMPLETE")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
