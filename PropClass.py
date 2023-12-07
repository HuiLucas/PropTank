import InputVariables
class CylindricalFuelTank:
    def __init__(self, length, radius, t_1, t_2 , material):
        self.length = length
        self.radius = radius
        self.t_1 = t_1
        self.t_2 = t_2
        self.TotalVolume = self.TankVolume()
        self.material = material
        self.YoungsModulus = self.GetYoungsModulus()

    def TankVolume(self):
        volume_cylinder = 3.14159 * self.radius ** 2 * self.length
        volume_caps =  4/3 * 3.14159 * self.radius ** 3
        total_volume = volume_cylinder + volume_caps
        return total_volume
    def GetYoungsModulus(self):
        for element in InputVariables.TankMaterial:
            if element["material"] == self.material:
                YoungsModulus = element["Elastic Modulus"]
                break
        return YoungsModulus



fuel_tank = CylindricalFuelTank(length=1, radius=1, t_1=3, t_2=4, material="Aluminium 7075")
print(f"Total volume of the fuel tank: {fuel_tank.TotalVolume}")
print(f"Material stiffness of fuel tank: {fuel_tank.YoungsModulus} in GPa ")
print(f"Material of fuel tank: {fuel_tank.material}")