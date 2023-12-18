import InputVariables
import numpy as np

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
        self.density = self.get_density()

    def tank_volume(self):
        volume_cylinder = np.pi * self.radius ** 2 * (self.length - 2*self.radius)
        volume_caps = 4/3 * np.pi * self.radius ** 3
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
    def get_density(self):
        for element in InputVariables.TankMaterial:
            if element["material"] == self.material:
                density = element["density"]
                break
        return density

class Loads:
    def __init__(self,pressure,launch_axial_loads):
        self.pressure = pressure
        self.launch_axial_loads = launch_axial_loads


#print(FuelTank(length=10,radius=0.3, t_1=5e-02, t_2=5e-02, material="Ti-6AI-4V").TotalVolume)