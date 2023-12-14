import math
import PropClass

def calculate_column_buckling_stress(length, radius, t_1 , YoungsModulus ):
    # here the area considered is the area of the long section of the tank
    outer_radius = radius + t_1
    area = math.pi * (outer_radius ** 2 - radius ** 2)
    SecondMoment = math.pi * (outer_radius * 2) ** 3 * t_1 / 8
    CriticalStress = (YoungsModulus * math.pi ** 2 * SecondMoment * 10 ** 9) / (area * length ** 2)
    return CriticalStress

fuel_tank_1 = PropClass.FuelTank(length=2, radius=1, t_1=3 * 10 ** -3, t_2=4 * 10 ** -3, material='Ti-6AI-4V')
print(calculate_column_buckling_stress(10, 0.25, 1 * 10 ** -3, fuel_tank_1.YoungsModulus ))

