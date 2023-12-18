from scipy.optimize import shgo

import PropClass
from scipy.optimize import minimize
import InputVariables
import numpy as np
import ShellBuckling as sb
import ColumnBuckling as cb
import StressCalculator as sc

tank_variables = PropClass.FuelTank(10, 0.4, t_1=5 * 10 ** -3, t_2=5 * 10 ** -3, material="Ti-6AI-4V")
temperature = 273
volume_liquid = tank_variables.TotalVolume # m**3
initial_pressure =( InputVariables.gas_constant2 * temperature / ( volume_liquid*10**6 / InputVariables.n - InputVariables.b ) - InputVariables.a * InputVariables.get_alpha(temperature) / ( (volume_liquid*10**6 / InputVariables.n) ** 2 + 2 * InputVariables.b * volume_liquid *10**6/ InputVariables.n - InputVariables.b ** 2 ))*101325
loads = PropClass.Loads(pressure=initial_pressure, launch_axial_loads= 6 * 9.81)


variables2 = [temperature,
              tank_variables.radius,
              tank_variables.length,
              tank_variables.t_1,
              tank_variables.t_2]


def objective_function(variables):
    sampled_points.append(variables)
    mass = 1000 * tank_variables.density * (
            np.pi * 2 * variables[1] * variables[3] * (variables[2] - 2 * variables[1]) + 4 * np.pi * variables[
            1] ** 2 * variables[4])
    return mass


def constraint_equation_state(variables):
    alpha = InputVariables.get_alpha(variables[0])
    a = InputVariables.a
    b = InputVariables.b
    gas_const = InputVariables.gas_constant2
    n = InputVariables.n
    pressure = 101325*(gas_const * variables[0] / ( constraint_volume(variables)*10**6 / n - b ) - a * alpha / ( (constraint_volume(variables)*10**6 / n) ** 2 + 2 * b * constraint_volume(variables)*10**6 / n - b ** 2 ))
    # if abs(eqstate - variables[0]) > 0.1:
    #     print("eq_of_state violated", eqstate, variables[0])
    return pressure #eqstate - variables[0]
def constraint_shell_buckling(variables):
    poissoin_ratio = tank_variables.PoissonRatio
    youngs_modulus = tank_variables.YoungsModulus
    LaunchStress = sc.launch_stress_calculator(variables[1], InputVariables.total_mass_sc+objective_function(variables), variables[3])
    StressCrit = sb.calculate_shell_buckling(variables[2],variables[1],variables[3],poissoin_ratio,constraint_equation_state(variables),youngs_modulus)
    #  launch load - pressure_longitudinal <= critical stress from shell buckling
    if -LaunchStress + StressCrit < 0:
        print("violate shell buckle", LaunchStress, StressCrit)
    return -LaunchStress + StressCrit

def constraint_column_buckling(variables):
    youngs_modulus = tank_variables.YoungsModulus
    LaunchStress = sc.launch_stress_calculator(variables[1], InputVariables.total_mass_sc+objective_function(variables), variables[3])
    PressStress = (constraint_equation_state(variables) * variables[1]) / (variables[3] * 2)
    StressCrit = cb.calculate_column_buckling_stress(variables[2], variables[1], variables[3], youngs_modulus)
    # launch load - pressure_longitudinal <= critical stress column
    if -LaunchStress + PressStress + StressCrit < 0:
        print("column buckling no good", LaunchStress - PressStress, StressCrit)
    return -LaunchStress + PressStress + StressCrit
def constraint_volume(variables):
    calcvolume = np.pi *  variables[1]**2 * (variables[2] - 2 * variables[1]) + 4/3 * np.pi * variables[1] ** 3
    return calcvolume


def constraint_temp_upper(variables):
    # temperature <= 298.15
    if -variables[0] +298.15 < 0:
        print("temp constraint violated", variables[0])
    return -variables[0] + 298.15


def constraint_temp_lower(variables):
    # 263.15 <= temperature
    if -263.15 + variables[0] < 0:
        print("temp constraint violated2", variables[0])
    return -263.15 + variables[0]


def constraint_hoop_stress(variables):
    yield_stress = tank_variables.YieldStress*10**6
    #sigma_yield = (pressure*R)/t_1
    #Safety factor of 1.25
    if yield_stress - (constraint_equation_state(variables)*variables[1])/variables[3] < 0:
        print("hoop stress violated", yield_stress, (constraint_equation_state(variables)*variables[1])/variables[3])
    return yield_stress - (constraint_equation_state(variables)*variables[1])/variables[3]
def constraint_longitudinal_stress(variables):
    yield_stress = tank_variables.YieldStress*10**6
    #sigma_yield= (pressure*R)/(2*T_1)
    # Safety factor of 1.25
    if yield_stress - (constraint_equation_state(variables)*variables[1])/(variables[3]*2)< 0:
        print("longitudinal stress violated", yield_stress, (constraint_equation_state(variables)*variables[1])/(variables[3]*2))
    return yield_stress - (constraint_equation_state(variables)*variables[1])/(variables[3]*2)

def constraint_pressure(variables):
    if -constraint_equation_state(variables) + 25000000*1.375 < 0: #source: https://ui.adsabs.harvard.edu/abs/2004ESASP.555E..52R
        print("pressure constraint violated", constraint_equation_state(variables))
    return -constraint_equation_state(variables) + 2431800

def geometry(variables):
    if -2*variables[1] + variables[2] < 0:
        print("geometry constraint violated", 2*variables[1], variables[2])
    return variables[2] - 2 * variables[1]


constraints = [
    #{'type': 'eq', 'fun': constraint_equation_state, 'jac': lambda x: np.array([-100, -0.0013, -0.061001, 0, 0, 1])},
    {'type': 'ineq', 'fun': constraint_shell_buckling, 'jac': lambda x: np.array([0, 0.001, 0, 0.0005, 0])},
    {'type': 'ineq', 'fun': constraint_column_buckling, 'jac': lambda x: np.array([0, 0.001, -0.01, 0.0005, 0])},
    #{'type': 'eq', 'fun': constraint_volume, 'jac': lambda x: np.array([0, -0.01, -0.1, 0, 0, 0, 0])},
    {'type': 'ineq', 'fun': constraint_temp_lower, 'jac': lambda x: np.array([1, 0, 0, 0, 0])},
    {'type': 'ineq', 'fun': constraint_temp_upper, 'jac': lambda x: np.array([-1, 0, 0, 0, 0])},
    {'type': 'ineq', 'fun': constraint_hoop_stress, 'jac': lambda x: np.array([0, -0.001, 0, 0.0005, 0])},
    {'type': 'ineq', 'fun': constraint_longitudinal_stress, 'jac': lambda x: np.array([0, -0.001, 0, 0.0005, 0])},
    {'type': 'ineq', 'fun': constraint_pressure, 'jac': lambda x: np.array([-1, 0.0013, 0.06, 0, 0])},
    {'type': 'ineq', 'fun': geometry, 'jac': lambda x: np.array([0, -0.001, 0.005, 0, 0])},
]

# initial_guesses = [[],[],[]]
# for guess in initial_guesses:
#     result = minimize(objective_function, guess, constraints=constraints, method='SLSQP')
#     print(result)
bounds = [(263,300), (0.0001,9), (0.0001,18), (0.000001,1), (0.000001,1)] #, (263,300)] #, (0.0000001,100)]
#result = minimize(objective_function,bounds=bounds, constraints=constraints, method = "SLSQP", x0 = variables2, options = {'disp': True, 'maxiter': 1000}, callback=lambda variables: print(variables), jac= lambda variables: np.array([0,0.005,0.01,0.00005,0.00001])) #minimizer_kwargs={'method': 'SLSQP'})

# List to store sampled points
sampled_points = []
results = []

# Define a callback function to record sampled points
def callback_record_points(x):
    sampled_points.append(x)
    results.append([x, objective_function(x)])
result = shgo(objective_function, bounds=bounds, constraints=constraints, minimizer_kwargs={'method': 'SLSQP'}, options={'disp': True, 'jac': lambda variables: np.array([0,0.005,0.01,0.00005,0.00001]), 'maxiter': 1000}, callback=callback_record_points, sampling_method='sobol', n = 10000, iters=3)
print("result", result.message)
print([(constraint['fun'](result.x) <= 0) for constraint in constraints])
print([constraint['fun'](result.x) for constraint in constraints])
# print(result)
# for point in sampled_points:
#     print(point)

