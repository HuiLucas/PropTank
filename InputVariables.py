import chemicals
import numpy as np

TankMaterial = [
    {'material': '316 Stainless Steel', 'Elastic Modulus': 190, 'density': 8070, 'thermal_expansion_coefficient': 18, 'ultimate_tensile_strength': 620, 'yield_stress': 170, 'resistance_factors': 'Excellent'},
    {'material': '18-8 SS', 'Elastic Modulus': 193, 'density': 7930, 'thermal_expansion_coefficient': 17.8, 'ultimate_tensile_strength': 620, 'yield_stress': 310, 'resistance_factors': 'Respectable but not for salty environments'},
    {'material': 'Carbon Steel', 'Elastic Modulus': 200, 'density': 7870, 'thermal_expansion_coefficient': 11.5, 'ultimate_tensile_strength': 540, 'yield_stress': 415, 'resistance_factors': 'Excellent'},
    {'material': 'Titanium (Grade 5)', 'Elastic Modulus': 113.8, 'density': 4430, 'thermal_expansion_coefficient': 8.6, 'ultimate_tensile_strength': 950, 'yield_stress': 880, 'resistance_factors': 'Excellent for corrosion but poor with wear', 'poisson_ratio': 0.33},
    {'material': 'Brass (Yellow)', 'Elastic Modulus': 76, 'density': 8740, 'thermal_expansion_coefficient': 21, 'ultimate_tensile_strength': 260, 'yield_stress': 90, 'resistance_factors': 'Good corrosion resistance', 'poisson_ratio': 0.33},
    {'material': 'Aluminium 7075', 'Elastic Modulus': 71.7, 'density': 2810, 'thermal_expansion_coefficient': 25.2, 'ultimate_tensile_strength': 572, 'yield_stress': 503, 'resistance_factors': 'Moderate', 'poisson_ratio': 0.33},
    {'material': '2014-T6', 'thermal_expansion_coefficient': 23, 'Elastic Modulus': 73.1 , 'yield_stress': 440 , 'poisson_ratio': 0.33 },
    {'material': '7075-T6', 'thermal_expansion_coefficient': 23.4, 'Elastic Modulus': 71.7, 'yield_stress': 462, 'poisson_ratio': 0.33},
    {'material': '4130 Steel', 'thermal_expansion_coefficient': 11.1, 'Elastic Modulus': 205, 'yield_stress': 1110, 'poisson_ratio': 0.33},
    {'material': '8630 Steel', 'thermal_expansion_coefficient': 11.3, 'Elastic Modulus': 200, 'yield_stress': 550, 'poisson_ratio': 0.33},
    {'material': '2024-T4', 'thermal_expansion_coefficient': 23.2, 'Elastic Modulus': 73.1, 'yield_stress': 260, 'poisson_ratio': 0.33},
    {'material': '356-T6 Aluminium', 'thermal_expansion_coefficient': 23.8, 'Elastic Modulus': 72.4, 'yield_stress': 152, 'poisson_ratio': 0.33},
    {'material': '2024-T3', 'thermal_expansion_coefficient': 21.6, 'Elastic Modulus': 73.1, 'yield_stress': 275},
    {'material': 'Ti-6AI-4V', 'Elastic Modulus': 113.8, 'yield_stress': 970, 'density': 4.43, 'poisson_ratio': 0.34},
    {'material': 'Al-Li 2195', 'Elastic Modulus': 69, 'yield_stress': 560, 'density': 2.71, 'poisson_ratio': 0.33},
    {'material': 'S2-glass/epoxy', 'Elastic Modulus': 20 , 'yield_stress': 457, 'density': 1.84, 'poisson_ratio': 0.23}
]

#### PROPELLANT PROPERTIES:
gas_constant = 8.314 #J/(mol*K)
gas_constant2 = 82.0573660809596 #cm^3*atm/(mol*K)
omega = chemicals.acentric.omega("60-34-4")
#print(omega)
kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega ** 2
T_critical = chemicals.critical.Tc("60-34-4")
p_critical = chemicals.critical.Pc("60-34-4")
p_critical_atm = p_critical / 101325
#print(T_critical, p_critical)
a = 0.45724 * gas_constant ** 2 * T_critical ** 2 / p_critical_atm

b = 0.07780 * gas_constant * T_critical / p_critical_atm
#print(a, b)
#alpha = ( 1 + kappa * ( 1 - np.sqrt(T_r) ) ) ** 2
def get_alpha(T):
    T_r = T / T_critical
    return ( 1 + kappa * ( 1 - np.sqrt(T_r) ) ) ** 2
molar_mass = chemicals.identifiers.MW("60-34-4")/1000 #kg/mol
#print(molar_mass)
propellant_mass = 97.57 #kg
n = (propellant_mass)/ molar_mass
total_mass_sc = 854.964 #kg
