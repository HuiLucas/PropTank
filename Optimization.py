from scipy.optimize import shgo

import PropClass
from scipy.optimize import minimize
import InputVariables
import numpy as np
import ShellBuckling as sb
import ColumnBuckling as cb
import StressCalculator as sc
import random
tank_variables = PropClass.FuelTank(3, 0.5, t_1=10 * 10 ** -3, t_2=5 * 10 ** -3, material="Ti-6AI-4V")
temperature = 263.15  # K
volume_liquid = tank_variables.TotalVolume  # m**3
initial_pressure = (InputVariables.gas_constant2 * temperature / (
            volume_liquid * 10 ** 6 / InputVariables.n - InputVariables.b) - InputVariables.a * InputVariables.get_alpha(
    temperature) / ((
                                volume_liquid * 10 ** 6 / InputVariables.n) ** 2 + 2 * InputVariables.b * volume_liquid * 10 ** 6 / InputVariables.n - InputVariables.b ** 2)) * 101325
loads = PropClass.Loads(pressure=initial_pressure, launch_axial_loads=6 * 9.81)

max_length = 1.75

variables2 = [tank_variables.t_2,
              tank_variables.radius,
              tank_variables.length,
              tank_variables.t_1,
              temperature]

num_guesses = 1000  # number of times the optimization runs
#### Optional max length make sure to change line in constraints dicitoinary
"""
def constraint_maxlength(variables):

    return max_length - variables[2]
"""
####


def objective_function(variables):
    mass = 1000 * tank_variables.density * (
            np.pi * 2 * variables[1] * variables[3] * (variables[2] - 2 * variables[1]) + 4 * np.pi * variables[
        1] ** 2 * variables[0])
    return mass


def constraint_equation_state(variables):
    alpha = InputVariables.get_alpha(variables[4])
    a = InputVariables.a
    b = InputVariables.b
    gas_const = InputVariables.gas_constant2
    n = InputVariables.n
    pressure = 101325 * (gas_const * variables[4] / (constraint_volume(variables) * 10 ** 6 / n - b) - a * alpha / (
                (constraint_volume(variables) * 10 ** 6 / n) ** 2 + 2 * b * constraint_volume(
            variables) * 10 ** 6 / n - b ** 2))
    return pressure  # eqstate - variables[4]


def constraint_shell_buckling(variables):
    poissoin_ratio = tank_variables.PoissonRatio
    youngs_modulus = tank_variables.YoungsModulus
    LaunchStress = sc.launch_stress_calculator(variables[1],
                                               InputVariables.total_mass_sc - 11.55 + objective_function(variables) ,
                                               variables[3])
    StressCrit = sb.calculate_shell_buckling(variables[2], variables[1], variables[3], poissoin_ratio,
                                             constraint_equation_state(variables), youngs_modulus)
    #  launch load - pressure_longitudinal <= critical stress from shell buckling
    #if -LaunchStress + StressCrit < 0:
        #print("violate shell buckle", LaunchStress, StressCrit)
    return -LaunchStress + StressCrit


def constraint_column_buckling(variables):
    youngs_modulus = tank_variables.YoungsModulus
    LaunchStress = sc.launch_stress_calculator(variables[1],
                                               InputVariables.total_mass_sc - 11.55 + objective_function(variables),
                                               variables[3])
    PressStress = (constraint_equation_state(variables) * variables[1]) / (variables[3] * 2)
    StressCrit = cb.calculate_column_buckling_stress(variables[2], variables[1], variables[3], youngs_modulus)
    # launch load - pressure_longitudinal <= critical stress column
    #if -LaunchStress + PressStress + StressCrit < 0:
        #print("column buckling no good", LaunchStress - PressStress, StressCrit)
    return -LaunchStress + PressStress + StressCrit


def constraint_volume(variables):

    calcvolume = np.pi * variables[1] ** 2 * (variables[2] - 2 * variables[1]) + 4 / 3 * np.pi * variables[1] ** 3
    return calcvolume


def constraint_temp_upper(variables):
    # variables[4] <= 298.15
    #if -variables[4] + 298.15 < 0:
        #print("temp constraint violated", variables[4])
    return -variables[4] + 298.15


def constraint_temp_lower(variables):
    # 263.15 <= variables[4]
    #if -263.15 + variables[4] < 0:
        #print("temp constraint violated2", variables[4])
    return -263.15 + variables[4]

def constraint_hoop_stress(variables):
    yield_stress = tank_variables.YieldStress * 10 ** 6
    # sigma_yield = (pressure*R)/t_1
    # Safety factor of 1.25
    #if yield_stress - (constraint_equation_state(variables) * variables[1]) / variables[3] < 0:
        #print("hoop stress violated", yield_stress,
              #(constraint_equation_state(variables) * variables[1]) / variables[3])
    return yield_stress - (constraint_equation_state(variables) * variables[1]) / variables[3]


def constraint_hoop_stress_ends(variables):
    yield_stress = tank_variables.YieldStress * 10 ** 6
    # sigma_yield = (pressure*R)/t_2
    # Safety factor of 1.25
    #if yield_stress - (constraint_equation_state(variables) * variables[1]) / variables[0] < 0:
        #print("hoop stress spherical ends violated", yield_stress,
              #(constraint_equation_state(variables) * variables[1]) / variables[0])
    return yield_stress - (constraint_equation_state(variables) * variables[1]) / variables[0]


def constraint_longitudinal_stress(variables):
    yield_stress = tank_variables.YieldStress * 10 ** 6
    # sigma_yield= (pressure*R)/(2*T_1)
    # Safety factor of 1.25
    #if yield_stress - (constraint_equation_state(variables) * variables[1]) / (variables[3] * 2) < 0:
        #print("longitudinal stress violated", yield_stress,
              #(constraint_equation_state(variables) * variables[1]) / (variables[3] * 2))
    return yield_stress - (constraint_equation_state(variables) * variables[1]) / (variables[3] * 2)


def upper_constraint_pressure(variables):
    #if -constraint_equation_state(
            #variables) + 2400000  < 0:  # source: https://www.space-propulsion.com/spacecraft-propulsion/bipropellant-thrusters/200n-bipropellant-thrusters.html
        #print("upper pressure constraint violated", constraint_equation_state(variables))
    return -constraint_equation_state(variables) + 2400000

def lower_constraint_pressure(variables):
    #if constraint_equation_state(
           # variables) - 1300000  < 0:  # source: https://www.space-propulsion.com/spacecraft-propulsion/bipropellant-thrusters/200n-bipropellant-thrusters.html
       # print("lower pressure constraint violated", constraint_equation_state(variables))
    return constraint_equation_state(variables) - 1300000


def geometry(variables):
    #if -2 * variables[1] + variables[2] < 0:
        #print("geometry constraint violated", 2 * variables[1], variables[2])
    return variables[2] - 2 * variables[1]


constraints = [
    # {'type': 'eq', 'fun': constraint_equation_state, 'jac': lambda x: np.array([-100, -0.0013, -0.061001, 0, 0, 1])},
    {'type': 'ineq', 'fun': constraint_shell_buckling},  # , 'jac': lambda x: np.array([0, 0.001, 0, 0.02])},
    {'type': 'ineq', 'fun': constraint_column_buckling},  # , 'jac': lambda x: np.array([0, 0.001, -0.01, 0.01])},
    # {'type': 'eq', 'fun': constraint_volume, 'jac': lambda x: np.array([0, -0.01, -0.1, 0, 0, 0, 0])},
    {'type': 'ineq', 'fun': constraint_temp_lower},  # , 'jac': lambda x: np.array([1, 0, 0, 0, 0])},
    {'type': 'ineq', 'fun': constraint_temp_upper},  # , 'jac': lambda x: np.array([-1, 0, 0, 0, 0])},
    {'type': 'ineq', 'fun': constraint_hoop_stress},  # , 'jac': lambda x: np.array([0, -0.001, 0, 0.0005])},
    {'type': 'ineq', 'fun': constraint_hoop_stress_ends},
    {'type': 'ineq', 'fun': constraint_longitudinal_stress},  # , 'jac': lambda x: np.array([0, -0.001, 0, 0.0005])},
    {'type': 'ineq', 'fun': upper_constraint_pressure},  # , 'jac': lambda x: np.array([0, 0.0013, 0.5, 0])},
    {'type': 'ineq', 'fun': lower_constraint_pressure},  # , 'jac': lambda x: np.array([0, 0.0013, 0.5, 0])},
    {'type': 'ineq', 'fun': geometry},  # , 'jac': lambda x: np.array([0, -0.001, 0.005, 0])},
    # Optional Max length{'type': 'ineq', 'fun': constraint_maxlength}
]

guesses= [variables2]

bounds = [(0.0001, 0.1), #t_2
          (0.1, 2), # radius
          (0.2, 2), #length
          (0.0001, 0.1), #t_1
          (263,300) #temp
          ] #, (0.0000001,100)]

guesses = [variables2]
# for loops to generate guesses:

for _ in range(num_guesses):
    guess = [random.uniform(low, high) for low, high in bounds]
    guesses.append(guess)

dictionary = []
for guess in guesses:
    result = minimize(objective_function,bounds=bounds, constraints=constraints, method = "SLSQP", x0 = guess, options = {'disp': True, 'maxiter': 1000}, callback=lambda variables: print(variables))  # , jac= lambda variables: np.array([0.00001,0.005,0.01,0.00003, 0])) #minimizer_kwargs={'method': 'SLSQP'})
    if result.success == True and 0.01 <= result.fun <=10000:
        dictionary.append([result.x, result.fun])

best_configuration = None
min_mass = float('inf')
# Iterate through the configurations
for config in dictionary:
    dimensions, mass = config
    if mass < min_mass:
        min_mass = mass
        best_configuration = config
print(best_configuration)

# Define a callback function to record sampled points


#result = shgo(objective_function, bounds=bounds, constraints=constraints, minimizer_kwargs={'method': 'SLSQP', 'constraints': constraints, 'bounds': bounds, 'options': {'maxiter': 1000}},
#              options={'disp': True, # 'jac': lambda variables: np.array([0.00001,0.005,0.01,0.00003, 0]),
#                       }, sampling_method='sobol', n=10000, iters=3)
"""print("result", result.message)
print([(constraint['fun'](result.x) <= 0) for constraint in constraints])
print([constraint['fun'](result.x) for constraint in constraints])
print(result)
# for point in sampled_points:
#     print(point)
print(result.x)
print("Pressure: ", constraint_equation_state(result.x), " pascal")
print(constraints[0]['fun'](result.x))
print(objective_function(result.x), "kg")
print(best_configuration)"""
#get mass of the tank for the Attachment Configuration and iterate

if best_configuration is not None:
    dimensions, mass = best_configuration
    print("Best Configuration:")
    print("t_2(mm):", dimensions[0] * 1000)
    print("t_1(mm):", dimensions[3] * 1000)
    print("radius(m):", dimensions[1])
    print("length(m):", dimensions[2])
    print("Mass(kg):", mass)
    print("Temperature:", dimensions[4])
    print("Pressure(atm):", constraint_equation_state(best_configuration[0])/101325)
    print("Volume(m^3): ", constraint_volume(best_configuration[0]))
else:
    print("No valid configuration found.")