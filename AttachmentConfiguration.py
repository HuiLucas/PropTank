#Selection of the material

CompressiveLoad = #calculated
NBeams = 8
ActualLoad = CompressiveLoad/NBeams
MassTwoPreviousLugs = 79.05 * 10^(-3)


#trade_off
Ratio = (1371/2)/ActualLoad   #sqr(load of launch)/actualLoad

#Scale the lugs given the loads for the two lugs and then divide by two
MassNewLug = Ratio*(MassTwoPreviousLugs/2)
TotalMassLugs = MassNewLug * NBeams