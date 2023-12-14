#Selection of the material
#import chemicals
import InputVariables
CompressiveLoad = 6*9.81*InputVariables.total_mass_sc
NBeams = 8
ActualLoad = CompressiveLoad/NBeams
MassTwoPreviousLugs = 79.05 * 10**(-3)


#trade_off
Ratio = (1371/2)/ActualLoad   #sqr(load of launch)/actualLoad

#Scale the lugs given the loads for the two lugs and then divide by two
MassNewLug = Ratio*(MassTwoPreviousLugs/2)
TotalMassLugs = MassNewLug * NBeams

print("Mass of the lug: ", MassNewLug)
print("Mass of the attachments: ", TotalMassLugs)