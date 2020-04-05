from geography import Map


nbRegions = 3
AvgCities = 4
StdCities = 1
AvgQuartiers = 5
StdQuartiers = 1
AvgFamily = 8
StdFamily = 3
minFamilySize = 1
maxFamilySize = 7
regionHoppingProbas = []
citiesHoppingProbas =[]
districtHoppingProbas = []
clusterHoppingProbas =[]
supermaketBypeople = 0.1
publicPlacesbypeople = 0.1
workingPlacesRatios = {"r1": 0.1, "r2": 0.2, "r3" : 0.3}
workingPlacesSizes = {"s1": 10, "s2": 8, "s3" : 5, "s4" : 3}
workPlacesParameters = []


map = Map(nbRegions, AvgCities, StdCities, AvgQuartiers, StdQuartiers, AvgFamily, StdFamily, minFamilySize, maxFamilySize, regionHoppingProbas, citiesHoppingProbas, districtHoppingProbas,clusterHoppingProbas, workingPlacesRatios, workingPlacesSizes, workPlacesParameters, supermaketBypeople, publicPlacesbypeople)