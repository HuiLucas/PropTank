import math
import PropClass

def buckling_stress_check(FuelTank):
    # here the area considered is the area of the long section of the tank
    outer_radius = FuelTank.radius + FuelTank.t_1
    area = math.pi * (outer_radius ** 2 - FuelTank.radius ** 2)
    SecondMoment = math.pi * (outer_radius * 2) ** 3 * FuelTank.t_1 / 8
    CriticalStress = (FuelTank.YoungsModulus * math.pi ** 2 * SecondMoment * 10 ** 9) / (area * FuelTank.length ** 2)
    if CriticalStress > FuelTank.YieldStress * 10 ** 6:
        return "Column Buckling", False, f"The critical stress is {CriticalStress / 10 ** 6} MPa"
    else:
        return "Column Buckling", True, f"The critical stress is {CriticalStress / 10 ** 6} MPa"

debug_fuel_tank = PropClass.FuelTank(length=2, radius=1, t_1 = 1 * 10 ** -3, t_2=4, material="Aluminium 7075")

print(buckling_stress_check(debug_fuel_tank))


