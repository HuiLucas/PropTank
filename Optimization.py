import scipy.optimize

import PropClass
from scipy.optimize import minimize
import InputVariables
import numpy as np
import ShellBuckling as sb
import ColumnBuckling as cb

def objective_function(TankClass):
    mass = TankClass.density * (np.pi * 2 * TankClass.radius * TankClass.t_1 * (TankClass.length - 2 * TankClass.radius ) + 4 * np.pi * TankClass.radius ** 2 * TankClass.t_2)
    return mass

def constraint_equation_state(volume_liquid,temperature,Loads):
    alpha = InputVariables.get_alpha(temperature)
    a = InputVariables.a
    b = InputVariables.b
    gas_const = InputVariables.gas_constant
    n = InputVariables.n
    return gas_const * temperature / ( volume_liquid / n - b ) - a * alpha / ( (volume_liquid / n) ** 2 + 2 * b * volume_liquid / n - b ** 2 ) - Loads.pressure

def constraint_shell_buckling(TankClass, Loads):
    #  launch load - pressure_longitudinal <= critical stress from shell buckling
    return sb.calculate_shell_buckling(TankClass,Loads)

def constraint_column_buckling(TankClass,Loads):
    # launch load - pressure_longitudinal <= critical stress column
    return cb.calculate_column_buckling_stress(TankClass,Loads)

def constraint_volume(TankClass,volume_liquid):
    volume_tank = TankClass.TotalVolume
    return volume_tank - volume_liquid
def constraint_temp_upper(temperature):
    # temperature <= 298.15
    return temperature - 298.15
def constraint_temp_lower(temperature):
    # 263.15 <= temperature
    return 263.15 - temperature
def constraint_hoop_stress(TankClass, pressure):
    #sigma_yield = (pressure*R)/t_1
    #Safety factor of 1.1
    return TankClass.YieldStress * 1.1 - (pressure*TankClass.radius)/TankClass.t_1
def constraint_longitudinal_stress(TankClass, pressure):
    #sigma_yield= (pressure*R)/(2*T_1)
    # Safety factor of 1.1
    return TankClass.YieldStress * 1.1 - (pressure*TankClass.radius)/(TankClass.t_1 *2)
constraints = [
    {'type': 'eq', 'fun': constraint_equation_state},
    {'type': 'ineq', 'fun': constraint_shell_buckling},
    {'type': 'ineq', 'fun': constraint_column_buckling},
    {'type': 'ineq', 'fun': constraint_temp_lower},
    {'type': 'ineq', 'fun': constraint_temp_upper},
    {'type': 'eq', 'fun': constraint_hoop_stress},
    {'type': 'eq', 'fun': constraint_longitudinal_stress}
]

# initial_guesses = [[],[],[]]
# for guess in initial_guesses:
#     result = minimize(objective_function, guess, constraints=constraints, method='SLSQP')
#     print(result)

result = scipy.optimize.shgo(objective_function, constraints=constraints, method='SLSQP')
