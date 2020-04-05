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



map = Map(nbRegions, AvgCities, StdCities, AvgQuartiers, StdQuartiers, AvgFamily, StdFamily, minFamilySize, maxFamilySize, regionHoppingProbas, citiesHoppingProbas, districtHoppingProbas,clusterHoppingProbas, supermaketBypeople, publicPlacesbypeople)