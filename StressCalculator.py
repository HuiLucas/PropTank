import PropClass
import InputVariables
import numpy as np

def launch_stress_calculator(FuelTank,mass,Loads):
    launch_force = Loads.launch_axial_loads * mass
    section_area = np.pi * ((FuelTank.radius+FuelTank.t_1)**2 - FuelTank.radius**2)
    launch_stress = launch_force/section_area
    return launch_stress

loads_debug = PropClass.Loads(0, 58.84)
mass1 = InputVariables.total_mass_sc
fuel_tank_1 = PropClass.FuelTank(length=2, radius=1, t_1=3 * 10 ** -3, t_2=4, material='Ti-6AI-4V')
print(launch_stress_calculator(fuel_tank_1,mass1,loads_debug))
