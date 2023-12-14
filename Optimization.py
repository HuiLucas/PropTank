import scipy.optimize

import PropClass
from scipy.optimize import minimize
import InputVariables
import numpy as np
import ShellBuckling as sb
import ColumnBuckling as cb

tank_variables = PropClass.FuelTank(4,2, t_1 = 3*10**-3, t_2 = 3*10**-3, material= "Ti-6AI-4V")
temperature = 273
loads = PropClass.Loads(pressure=2.5 * 10 ** 6, launch_axial_loads= 6 * 9.81)
volume_liquid = 0.1 #m**3


variables2 = [tank_variables.density,
             tank_variables.radius ,
             tank_variables.length ,
             tank_variables.t_1 ,
             tank_variables.t_2,
             temperature,
             volume_liquid ,
             tank_variables.TotalVolume,
             loads.pressure]

def objective_function(variables):
    mass = variables[0] * (np.pi * 2 * variables[1] * variables[3] * (variables[2] - 2 * variables[1] ) + 4 * np.pi * variables[1] ** 2 * variables[4])
    return mass

def constraint_equation_state(variables):
    alpha = InputVariables.get_alpha(variables[5])
    a = InputVariables.a
    b = InputVariables.b
    gas_const = InputVariables.gas_constant
    n = InputVariables.n
    return gas_const * variables[5] / ( variables[6] / n - b ) - a * alpha / ( (variables[6] / n) ** 2 + 2 * b * variables[6] / n - b ** 2 ) - variables[8]

def constraint_shell_buckling(variables):
    poissoin_ratio = tank_variables.PoissonRatio
    youngs_modulus = tank_variables.YoungsModulus
    #  launch load - pressure_longitudinal <= critical stress from shell buckling
    return sb.calculate_shell_buckling(variables[2],variables[1],variables[3],poissoin_ratio,variables[8],youngs_modulus)

def constraint_column_buckling(variables):
    youngs_modulus = tank_variables.YoungsModulus
    # launch load - pressure_longitudinal <= critical stress column
    return cb.calculate_column_buckling_stress(variables[2],variables[1],variables[3],youngs_modulus)
def constraint_volume(variables):
    return variables[7] - variables[6]
def constraint_temp_upper(variables):
    # temperature <= 298.15
    return variables[5] - 298.15
def constraint_temp_lower(variables):
    # 263.15 <= temperature
    return 263.15 - variables[5]
def constraint_hoop_stress(variables):
    yield_stress = tank_variables.YieldStress
    #sigma_yield = (pressure*R)/t_1
    #Safety factor of 1.1
    return yield_stress * 1.1 - (variables[8]*variables[1])/variables[3]
def constraint_longitudinal_stress(variables):
    yield_stress = tank_variables.YieldStress
    #sigma_yield= (pressure*R)/(2*T_1)
    # Safety factor of 1.1
    return yield_stress * 1.1 - (variables[8]*variables[1])/(variables[3]*2)

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
print(result)