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

def constraint_shell_buckling(TankClass,Loads):
    #  launch load - pressure_longitudinal < critical stress from shell buckling
    return sb.calculate_shell_buckling(TankClass,Loads)

def constraint_column_buckling(TankClass,Loads):
    # launch load - pressure_longitudinal < critical stress column
    return cb.calculate_column_buckling_stress(TankClass,Loads)

def constraint_volume(TankClass,volume_liquid):
    volume_tank = TankClass.TotalVolume
    return volume_tank - volume_liquid


constraints = [
    {'type': 'eq', 'fun': constraint_equation_state},
    {'type': 'ineq', 'fun': constraint_shell_buckling},
    {'type': 'ineq', 'fun': constraint_column_buckling},
    {'type': 'eq', 'fun': constraint_volume},
]


result = minimize(objective_function, initial_design, constraints=constraints, method='SLSQP')
