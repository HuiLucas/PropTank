import PropClass
import InputVariables
import numpy as np

def launch_stress_calculator(Radius,mass,t_1):
    launch_force = 6 * 9.80665 * mass
    print(launch_force)
    section_area = np.pi * ((Radius + t_1)**2 - Radius**2)
    launch_stress = launch_force/section_area
    return launch_stress

mass1 = InputVariables.total_mass_sc
fuel_tank_1 = PropClass.FuelTank(length=2, radius=1, t_1=1 * 10 ** -3, t_2=4 * 10 ** -3, material='Ti-6AI-4V')
print(launch_stress_calculator(fuel_tank_1.radius,mass1,fuel_tank_1.t_1))
#print((2026500*fuel_tank_1.radius)/(fuel_tank_1.t_1*2) * 10 ** -6)
