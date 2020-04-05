import numpy
from cluster import *
from individual import *

class Map:

    def __init__(self, nbRegions, AvgCities, StdCities, AvgQuartiers, StdQuartiers, AvgFamily, StdFamily, minFamilySize, maxFamilySize, regionHoppingProbas, citiesHoppingProbas, districtHoppingProbas, clusterHoppingProbas, supermaketBypeople, publicPlacesbypeople):
        
        self.nbRegions = nbRegions
        
        self.country = Country([], regionHoppingProbas)
        self.listOfPeople = []
        
        #create sub structure of the country
        regions  = [Region([],self.country, citiesHoppingProbas) for i in range(nbRegions)]
        for reg in regions:
            nbcities = int(round(abs(numpy.random.normal(AvgCities, StdCities))))
            citiesTemp = [City([],reg,districtHoppingProbas) for i in range(nbcities)]
            for cit in citiesTemp:
                nbdistricts = int(round(abs(numpy.random.normal(AvgQuartiers, StdQuartiers))))
                districtsTemp = [District([], [], [], [], cit, clusterHoppingProbas) for i in range(nbdistricts)]
                for dis in districtsTemp:
                    #add families cluster
                    nbfamilies = int(round(abs(numpy.random.normal(AvgFamily, StdFamily))))
                    FamilyTemp = [Family([],dis,[]) for i in range(nbfamilies)]
                    for fam in FamilyTemp:
                        nbpeople = numpy.random.randint(minFamilySize, maxFamilySize)
                        members = [Individual([], [], [], [], [], [], []) for i in range(nbpeople)]
                        fam.addHomeIndividual(members)
                        self.listOfPeople.append(members)
                    dis.addCluster(FamilyTemp)
                cit.addDistrict(districtsTemp)
            reg.addCity(citiesTemp)
        country.addRegion(regions)
        #TODO put family parameters
        #TODO, choose family size distribution
        #TODO, initialize people with datas
        #donner des ages aux personnes
        
        defineWorkingPlaces(self.country, workPlacesRatios, workPlacesSizes, workPlacesParameters)
        
        self.addPublics("SuperMarket", supermaketBypeople, SuperMarketParameters)
        self.addPublics("Public", supermaketBypeople, PublicPlacesParameters)

        
        
    def addPublics(self, type, density, PublicPlacesParameters):
        
        for reg in regions:
            for cit in citiesTemp:
                for dis in districtsTemp:
                    number = int(density*dis.getNumberOfPeople())
                    if type == "SuperMarket" :
                        SM = [SuperMarket([],dis,PublicPlacesParameters) for i in range(number)]
                    elif type == "PublicPlace":
                        PP = [PublicPlaces([],dis,PublicPlacesParameters) for i in range(number)]
                    
        
        
        
    def defineWorkingPlaces(country, ratios, sizes, parameters):
        #define 4 levels of working places, with different sizes (s1-s4)
        #with different ratio of population that can find a place in theses working places
        # level 1: r1 fraction of the population of the country have job here, the size is ~s1, check here how many of these we need. 
        # level 2: r2 fraction of the population of each region have job here, the size is ~s2, check here how many of these we need. 
        # level 3: r3 fraction of the population of each city have job here, the size is ~s3, check here how many of these we need. 
        # level 4: the size is ~s4, check here how many of these we need in each district to fill the working places
        
        nbPopulation = country.getPopulationSize()
        listOfPeopleTemp = self.listOfPeople
        remainingPlaces = nbPopulation #counter
        #1 
        N1 = int(round(nbPopulation*ratios.r1/sizes.s1)) #number of groups in category 1
        Size1 = int(round(nbPopulation*ratios.r1/N1))
        for i in range(N1):
            District = chooseDistrict()
            work = Work([],parameters, Size1)
            District.addCluster(work)
            emps, listOfPeopleTemp = chooseEmployee(work, Size1, listOfPeopleTemp)
            work.addEmployees(emps)
        remainingPlaces -= N1*S1
        
        #2
        N2 = int(round(nbPopulation*ratios.r2/sizes.s2)) #number of groups in category 2
        Size2 = int(round(nbPopulation*ratios.r2/N2))
        for i in range(N2):
            work = Work([],parameters, Size2)
            District.addCluster(work)
            emps, listOfPeopleTemp = chooseEmployee(work, Size2, listOfPeopleTemp)
            work.addEmployees(emps)
        remainingPlaces -= N2*S2
        
        #3
        N3 = int(round(nbPopulation*ratios.r3/sizes.s3)) #number of groups in category 3
        Size3 = int(round(nbPopulation*ratios.r3/N3))
        for i in range(N3):
            work = Work([],parameters, Size3)
            District.addCluster(work)
            emps, listOfPeopleTemp = chooseEmployee(work, Size3, listOfPeopleTemp)
            work.addEmployees(emps)
        remainingPlaces -= N3*S3
        
        #4
        remainingPlaces = nbPopulation-workingPlaces
        N4 = int(remainingPlaces/sizes.s4) #min number of groups in category 4
        for i in range(N4):
            work = Work([],parameters, Size4)
            District.addCluster(work)
            emps, listOfPeopleTemp = chooseEmployee(work, Size4, listOfPeopleTemp)
            work.addEmployees(emps)
        remainingPlaces -= N4*S4
        #for remainning nbpeople
        District = chooseDistrict()
        work = Work([],parameters, remainingPlaces)
        District.addCluster(work)
        emps, listOfPeopleTemp = chooseEmployee(work, remainingPlaces, listOfPeopleTemp)
        work.addEmployees(emps)
        
    
    def getClusterDistance(cluster1, cluster2):
        #distance is defined as the number of level we need to go up, same cluster : distance = 0
        
        if cluster1 == cluster2:
            distance =0
        elif cluster1.district == cluster2.district:
            distance = 1
        elif cluster1.district.city == cluster2.district.city:
            distance = 2
        elif cluster1.district.city.region == cluster2.district.city.region:
            distance = 3
        else:
            distance = 4
            
    def chooseEmployee(Work, N, ListOfCandidates):
        #Work: the working place
        #N: number of work
        distances = [getClusterDistance(Work, ListOfCandidates[i].home) for i in range(len(ListOfCandidates))]
        weights = numpy.divide(1.0,distances)
        probas = numpy.divide(weights, numpy.sum(weights))
        indexesDisponible = numpy.arange(len(ListOfCandidates))
        chosenIndexes = []
        
        for i in range(N):
            ind = numpy.random.choice(indexesDisponible,probas)
            chosenIndexes.append(ind)
            
            indexesDisponible.pop(ind)
            probas.pop(ind)
            probas = numpy.divide(probas, numpy.sum(probas))
        
        remainingCanditates = ListOfCandidates
        for index in sorted(chosenIndexes, reverse=True):
            del remainingCanditates[index]
            
        return ListOfCandidates[chosenIndexes], remainingCanditates
    

        
        
    def getPopulationSize():
        return Individual.__counter
        
    def chooseDistrict(self):
        #choose recursively a regions->city->district
        region = self.country.getaRegion()
        city = region.getaCity()
        district = city.getaDistrict()
        
        return district
        
    
        
    
    
    def update(self):
        self.country.update()
    
    

class Country:
    def __init__(self, regions, hopping_probas):
        self.regions = regions
        self.hopping_probas = hopping_probas
        
    def addRegion(self, listofRegion):
        self.regions.append(listofRegion)
        for el in listofRegion:
            el.country = self  
            
    def getRegions(self):
        return self.regions
        
    def getaRegion(self):
        nbRegions = len(self.regions)
        index = numpy.random.randint(0,nbRegions-1)
        return self.regions[index]
        
    def update(self):
        for el in self.regions:
            el.update()
    
    
class Region:
    def __init__(self, cities, country, hopping_probas):
        self.cities = cities
        self.country = country
        self.hopping_probas = hopping_probas
        
    def addCity(self, listofCities):
        self.cities.append(listofCities)
        for el in listofCities:
            el.region = self
            
    def getCities(self):
        return self.cities
        
    def getaCity(self):
        nbCities = len(self.cities)
        index = numpy.random.randint(0,nbCities-1)
        return self.cities[index]
    
    def update(self):
        for el in self.cities:
            el.update()
        
        
class City:
    def __init__(self, districts, region, hopping_probas):
        self.districts = districts
        self.region = region        
        self.hopping_probas = hopping_probas
    
    def addDistrict(self, listofDistricts):
        self.districts.append(listofDistricts)
        for el in listofDistricts:
            el.city = self
            
    def getDistricts(self):
        return self.districts
        
    def getaDistrict(self):
        nbdistricts = len(self.districts)
        index = numpy.random.randint(0,nbdistricts-1)
        return self.districts[index]
    
    def update(self):
        for el in self.districts:
            el.update()

        
class District:
    def __init__(self, family, work, superMarket, puplicPlaces, city, hopping_probas):
        self.family = family
        self.work = work
        self.superMarket = superMarket
        self.publicPlaces = puplicPlaces
        
        self.city = city
        self.hopping_probas = hopping_probas #est-ce vraiment utile ?

    def addCluster(self, listofClusters):
        self.clusters.append(listofClusters)
        for el in listofClusters:
            el.district = self
        
    def update(self):
        for el in self.clusters:
            el.update()

    def getNumberOfPeople(self):
        counter = 0
        for fam in self.family:
            counter += len(fam.individuals)
    
        
        
# s'imaginer à un output.      
