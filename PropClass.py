import InputVariables

class FuelTank:
    def __init__(self, length, radius, t_1, t_2 , material):
        self.length = length
        self.radius = radius
        self.t_1 = t_1
        self.t_2 = t_2
        self.TotalVolume = self.tank_volume()
        self.material = material
        self.YoungsModulus = self.get_youngs_modulus()
        self.YieldStress = self.get_yield_stress()
        self.PoissonRatio = self.get_poisson_ratio()
        self.material_cost = self.get_material_cost()
        self.design_cost = self.get_design_cost()

    def tank_volume(self):
        volume_cylinder = 3.14159 * self.radius ** 2 * (self.length - 2*self.radius)
        volume_caps = 4/3 * 3.14159 * self.radius ** 3
        total_volume = volume_cylinder + volume_caps
        return total_volume
    def get_youngs_modulus(self):
        for element in InputVariables.TankMaterial:
            if element["material"] == self.material:
                YoungsModulus = element["Elastic Modulus"]
                break
        return YoungsModulus
    def get_yield_stress(self):
        for element in InputVariables.TankMaterial:
            if element["material"] == self.material:
                yield_stress = element["yield_stress"]
                break
        return yield_stress
    def get_poisson_ratio(self):
        for element in InputVariables.TankMaterial:
            if element["material"] == self.material:
                poisson_ratio = element["poisson_ratio"]
                break
        return poisson_ratio
    def get_material_cost(self):
        for element in InputVariables.TankMaterial:
            if element["material"] == self.material:
                material_cost = element["material_cost"]
                break
        return material_cost
    def get_design_cost(self):
        return self.TotalVolume * self.material_cost



fuel_tank = FuelTank(length=1, radius=1, t_1=3, t_2=4, material="Aluminium 7075")
print(f"Total volume of the fuel tank: {fuel_tank.TotalVolume}")
print(f"Material stiffness of fuel tank: {fuel_tank.YoungsModulus} in GPa ")
print(f"Material of fuel tank: {fuel_tank.material}")

class Loads:
    def __init__(self,pressure):
        self.pressure = pressure

