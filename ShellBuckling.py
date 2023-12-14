import numpy as np
import PropClass

# variables = [FuelTank.length,
#               FuelTank.radius ,
#               FuelTank.t_1 ,
#               FuelTank.PoissonRatio,
#               Loads.pressure,
#               FuelTank.YoungsModulus,
#               ]

def calculate_shell_buckling(length, radius, t_1 , PoissonRatio , pressure , YoungsModulus ):
    MinLambda = np.sqrt((12/np.pi ** 4) * (length ** 4 / (radius ** 2 * t_1 ** 2)) * (1 - PoissonRatio ** 2))
    MinK = 2 * MinLambda
    queue = (pressure / (YoungsModulus * 10 ** 9)) * (radius/t_1) ** 2
    CriticalStress = (1.983-0.983 * np.exp(-23.14 * queue)) * MinK * ((np.pi ** 2 * YoungsModulus * 10 **9)/(12 * (1 - PoissonRatio ** 2))*(t_1/length) ** 2)
    return CriticalStress

fuel_tank_1 = PropClass.FuelTank(length=2, radius=1, t_1=3 * 10 ** -3, t_2=4 * 10 ** -3, material='Ti-6AI-4V')
print(calculate_shell_buckling(100, 0.5, 1 * 10 ** -3, fuel_tank_1.PoissonRatio, 2026500, fuel_tank_1.YoungsModulus))