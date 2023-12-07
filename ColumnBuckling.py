import math
import PropClass

def buckling_stress_check(FuelTank,Loads):
    # here the area considered is the area of the long section of the tank
    outer_radius = FuelTank.radius + FuelTank.t_1
    area = math.pi * (outer_radius ** 2 - FuelTank.radius ** 2)
    SecondMoment = 0.5 * math.pi * (outer_radius ** 4 - FuelTank ** 4)
    CriticalStress = (FuelTank.YoungsModulus * math.pi ** 2 * 10 ** 3 * SecondMoment ) / (area * FuelTank.length ** 2)
    if CriticalStress > FuelTank.yieldstress:
        return False , CriticalStress
    else:
        return True



