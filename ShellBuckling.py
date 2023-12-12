import numpy as np
import PropClass

def calculate_shell_buckling(FuelTank,Loads):
    MinLambda = np.sqrt((12/np.pi ** 4) * (FuelTank.length ** 4 / (FuelTank.radius ** 2 * FuelTank.t_1 ** 2)) * (1 - FuelTank.PoissonRatio ** 2))
    MinK = 2 * MinLambda
    queue = (Loads.pressure / (FuelTank.YoungsModulus * 10 ** 9)) * (FuelTank.radius/FuelTank.t_1) ** 2
    CriticalStress = (1.983-0.983 * np.exp(-23.14 * queue)) * MinK * ((np.pi ** 2 * FuelTank.YoungsModulus * 10 **9)/(12 * (1 - FuelTank.PoissonRatio ** 2))*(FuelTank.t_1/FuelTank.length) ** 2)
    return CriticalStress / 10 ** 6

loads_debug = PropClass.Loads(-100000,0)
fuel_tank_1 = PropClass.FuelTank(length=2, radius=1, t_1=3 * 10 ** -3, t_2=4, material='Ti-6AI-4V')

print(calculate_shell_buckling(fuel_tank_1,loads_debug))