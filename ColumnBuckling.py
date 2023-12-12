import math
import PropClass

def calculate_column_buckling_stress(FuelTank):
    # here the area considered is the area of the long section of the tank
    outer_radius = FuelTank.radius + FuelTank.t_1
    area = math.pi * (outer_radius ** 2 - FuelTank.radius ** 2)
    SecondMoment = math.pi * (outer_radius * 2) ** 3 * FuelTank.t_1 / 8
    CriticalStress = (FuelTank.YoungsModulus * math.pi ** 2 * SecondMoment * 10 ** 9) / (area * FuelTank.length ** 2)
    return CriticalStress / 10 ** 6

debug_fuel_tank = PropClass.FuelTank(length=20, radius=1, t_1 = 1 * 10 ** -3, t_2=4, material='Ti-6AI-4V')

print(calculate_column_buckling_stress(FuelTank=debug_fuel_tank))



