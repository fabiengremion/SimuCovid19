import numpy
from cluster import *
from individual import *
from scipy.stats import rv_discrete


class Map:

    def __init__(self, nbRegions, AvgCities, StdCities, AvgQuartiers, StdQuartiers, AvgFamily, StdFamily, minFamilySize, maxFamilySize, regionHoppingProbas, citiesHoppingProbas, districtHoppingProbas, clusterHoppingProbas,workingPlacesRatios, workingPlacesSizes, workPlacesParameters, supermaketBypeople, publicPlacesbypeople, mobilityDegrees):
        
        self.nbRegions = nbRegions
        
        self.country = Country([], regionHoppingProbas)
        self.listOfPeople = []
        self.familySizeGenerator = familySizeGenerator()
        self.adultAgeCategoryGenerator, self.adultAgeCategoryBoundaries = adultAgeCategoryGenerator()
        
        #create sub structure of the country
        regionsTemp  = [Region([], self.country, citiesHoppingProbas) for i in range(nbRegions)]
        for reg in regionsTemp:
            nbcities = int(round(abs(numpy.random.normal(AvgCities, StdCities))))
            citiesTemp = [City([] ,reg , districtHoppingProbas) for i in range(nbcities)]
            for cit in citiesTemp:
                nbdistricts = int(round(abs(numpy.random.normal(AvgQuartiers, StdQuartiers))))
                districtsTemp = [District([], [], [], [], cit, clusterHoppingProbas) for i in range(nbdistricts)]
                for dis in districtsTemp:
                    #add families cluster
                    nbfamilies = int(round(abs(numpy.random.normal(AvgFamily, StdFamily))))
                    FamilyTemp = [Family([],dis,[]) for i in range(nbfamilies)]
                    for fam in FamilyTemp:
                        #nbpeople = numpy.random.randint(minFamilySize, maxFamilySize)
                        nbpeople = int(self.familySizeGenerator.rvs(size=1))
                        members = [Individual(fam, None, None, fam, [], [], age = None) for i in range(nbpeople)] # give a family and set at home
                        #TODO:mettre d'abord des adultes et compléter avec des enfants
                        fam.addHomeIndividual(members)
                        countmember = 1
                        for mem in members:
                            if countmember<3:
                                ageCategory = int(self.adultAgeCategoryGenerator.rvs(size=1))
                                mem.age = numpy.random.randint(*self.adultAgeCategoryBoundaries[ageCategory]) #the little star unpacks the tuple
                            if countmember>=3:
                                mem.age = numpy.random.randint(1, 19)
                            self.listOfPeople.append(mem)
                            countmember = countmember + 1

                    dis.addFamily(FamilyTemp)
                cit.addDistrict(districtsTemp)
            reg.addCity(citiesTemp)
        self.country.addRegion(regionsTemp)

        #TODO put family parameters
        #TODO, choose family size distribution
        #TODO, initialize people with datas
        #TODO, donner des ages aux personnes https://www.bfs.admin.ch/bfs/fr/home/statistiques/population/effectif-evolution/age-etat-civil-nationalite.html
        
        '''self.defineWorkingPlaces(self.country, workingPlacesRatios, workingPlacesSizes, workPlacesParameters, mobilityDegrees)'''
        
        '''self.addPublics("SuperMarket", supermaketBypeople, SuperMarketParameters)
        self.addPublics("Public", supermaketBypeople, PublicPlacesParameters)'''

        
        
    def addPublics(self, type, density, PublicPlacesParameters):
        
        for reg in regions:
            for cit in citiesTemp:
                for dis in districtsTemp:
                    number = int(density*dis.getNumberOfPeople())
                    if type == "SuperMarket" :
                        SM = [SuperMarket([] ,dis ,PublicPlacesParameters) for i in range(number)]
                    elif type == "PublicPlace":
                        PP = [PublicPlaces([] ,dis ,PublicPlacesParameters) for i in range(number)]
                    
        
        
        
    def defineWorkingPlaces(self, country, ratios, sizes, parameters, mobilityDegrees):
        #define 4 levels of working places, with different sizes (s1-s4)
        #with different ratio of population that can find a place in theses working places
        # level 1: r1 fraction of the population of the country have job here, the size is ~s1, check here how many of these we need. 
        # level 2: r2 fraction of the population of each region have job here, the size is ~s2, check here how many of these we need. 
        # level 3: r3 fraction of the population of each city have job here, the size is ~s3, check here how many of these we need. 
        # level 4: the size is ~s4, check here how many of these we need in each district to fill the working places
        
        nbPopulation = Individual.counter
        listOfPeopleTemp = self.listOfPeople
        remainingPlaces = nbPopulation #counter
        workMobilityDegrees = mobilityDegrees['work']
        #1 
        N1 = int(round(nbPopulation*ratios['r1']/sizes['s1'])) #number of groups in category 1
        Size1 = int(round(nbPopulation*ratios['r1']/N1))
        for i in range(N1):
            District = self.chooseDistrict()
            work = Work([],District,parameters, Size1)
            emps, listOfPeopleTemp = self.chooseEmployee(work, Size1, listOfPeopleTemp,workMobilityDegrees)
            work.addEmployees(emps)
        remainingPlaces -= N1*S1
        
        #2
        N2 = int(round(nbPopulation*ratios['r2']/sizes['s2'])) #number of groups in category 2
        Size2 = int(round(nbPopulation*ratios['r2']/N2))
        for i in range(N2):
            work = Work([],District,parameters, Size2)
            District.addCluster(work)
            emps, listOfPeopleTemp = self.chooseEmployee(work, Size2, listOfPeopleTemp,workMobilityDegrees)
            work.addEmployees(emps)
        remainingPlaces -= N2*S2
        
        #3
        N3 = int(round(nbPopulation*ratios['r3']/sizes['s1'])) #number of groups in category 3
        Size3 = int(round(nbPopulation*ratios['r3']/N3))
        for i in range(N3):
            work = Work([],District,parameters, Size3)
            District.addCluster(work)
            emps, listOfPeopleTemp = self.chooseEmployee(work, Size3, listOfPeopleTemp,workMobilityDegrees)
            work.addEmployees(emps)
        remainingPlaces -= N3*S3
        
        #4
        remainingPlaces = nbPopulation-workingPlaces
        N4 = int(remainingPlaces/sizes.s4) #min number of groups in category 4
        for i in range(N4):
            work = Work([],District,parameters, Size4)
            District.addCluster(work)
            emps, listOfPeopleTemp = self.chooseEmployee(work, Size4, listOfPeopleTemp,workMobilityDegrees)
            work.addEmployees(emps)
        remainingPlaces -= N4*S4
        #for remainning nbpeople
        District = chooseDistrict()
        work = Work([],District,parameters, remainingPlaces)
        District.addCluster(work)
        emps, listOfPeopleTemp = self.chooseEmployee(work, remainingPlaces, listOfPeopleTemp,workMobilityDegrees)
        work.addEmployees(emps)
        
    
    def getClusterDistance(self,cluster1, cluster2):
        #distance is defined as the number of level we need to go up, same cluster : distance = 0
        
        if cluster1 == cluster2:
            return 0
        elif cluster1.district == cluster2.district:
            return 1
        elif cluster1.district.city == cluster2.district.city:
            return 2
        elif cluster1.district.city.region == cluster2.district.city.region:
            return 3
        else:
            return 4
            
            
    def chooseEmployee(self, Work, N, ListOfCandidates):
        #Work: the working place
        #N: number of work
        distances = [self.getClusterDistance(Work, ListOfCandidates[i].home) for i in range(len(ListOfCandidates))]
        weights = numpy.divide(1.0,distances)
        probas = numpy.divide(weights, numpy.sum(weights))#to change
        indexesDisponible = numpy.arange(len(ListOfCandidates))
        chosenIndexes = []
        
        for i in range(N):
            for j in range(len(ListOfCandidates)):
                ind = numpy.random.choice(indexesDisponible,probas)
                chosenIndexes.append(ind)
                
                indexesDisponible.pop(ind)
                probas.pop(ind)
                probas = numpy.divide(probas, numpy.sum(probas))
        
        remainingCanditates = ListOfCandidates
        for index in sorted(chosenIndexes, reverse=True):
            del remainingCanditates[index]
            
        return ListOfCandidates[chosenIndexes], remainingCanditates
    

        
        
        
    def chooseDistrict(self):
        #choose recursively a regions->city->district
        region = self.country.getaRegion()
        city = region.getaCity()
        district = city.getaDistrict()
        
        return district
        
    
        
    
    
    def update(self):
        self.country.update()
        
    def PlotMap(self):
        strSpace = ' '*9
        
        iReg, iCit, iDist, iCL = 1,1,1,1
        print("Country:")
        for reg in self.country.regions:
            print(strSpace + "R" + str(iReg) + ":")
            for cit in reg.cities:
                print(strSpace*2 + "C" + str(iCit) + ":")
                for dist in cit.districts:
                    print(strSpace*3 + "D" + str(iDist) + ":")
                    iCL = 0
                    for house in dist.families:
                        print(strSpace*4 + "F" + str(iCL) + ": " + str(house.getMembersNumber()) )
                        iCL += 1
                    iCL = 0
                    for work in dist.work:
                        print(strSpace*4 + "W" + str(iCL) + ": " + str(work.getMembersNumber()) )
                        iCL += 1
                    iCL = 0
                    for sM in dist.superMarkets:
                        print(strSpace*4 + "SM" + str(iCL) + ": " + str(sM.getMembersNumber()) )
                        iCL += 1
                    iCL = 0
                    for pP in dist.publicPlaces:
                        print(strSpace*4 + "PP" + str(iCL) + ": " + str(pP.getMembersNumber()) )
                        iCL += 1
                    
                    iDist +=1
                iCit +=1
            iReg +=1
    

class Country:
    def __init__(self, regions, hopping_probas):
        self.regions = regions
        self.hopping_probas = hopping_probas
        
    def addRegion(self, listofRegion):
        for el in listofRegion:
            self.regions.append(el)
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
        for el in listofCities:
            self.cities.append(el)
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
        for el in listofDistricts:
            self.districts.append(el)
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
    def __init__(self, families, work, superMarkets, puplicPlaces, city, hopping_probas):
        self.families = families
        self.work = work
        self.superMarkets = superMarkets
        self.publicPlaces = puplicPlaces
        
        self.city = city
        self.hopping_probas = hopping_probas #est-ce vraiment utile ?

    def addFamily(self, listOfFamilies):
        for el in listOfFamilies:
            self.families.append(el)
            el.district = self

        
    def update(self):
        for el in self.clusters:
            el.update()

    def getNumberOfPeople(self):
        counter = 0
        for fam in self.family:
            counter += len(fam.individuals)
    

def familySizeGenerator():
    # from https: // www.bfs.admin.ch / bfs / fr / home / statistiques / population / effectif - evolution / menages.html
    # We imagine that families are either composed of one adult or 2 adults or 2 adults + 3 kids. We ignore bigger families and adults flatsharing
    familySize = numpy.arange(6)
    familySizeProba = numpy.array([0, 0.35, 0.33, 0.13, 0.13, 0.06])
    familySizeGenerator = rv_discrete(name='familySizeGenerator', values=(familySize, familySizeProba))

    return familySizeGenerator



def adultAgeCategoryGenerator():
    # from https://www.bfs.admin.ch/bfs/fr/home/statistiques/population/effectif-evolution/age-etat-civil-nationalite.html# We imagine that families are either composed of one adult or 2 adults or 2 adults + 3 kids. We ignore bigger families and adults flatsharing
    ageCategory = numpy.arange(4) #corresponds to 20-39, 40-64, 65-79, 80-100
    categoryBoundaries = [(20, 39), (40, 64), (65, 79), (80, 100)]
    ageCategoryProba = numpy.array([23.5, 34.6, 15.7, 6.3])
    ageCategoryProba = ageCategoryProba * 1/ageCategoryProba.sum()
    ageCategoryGenerator = rv_discrete(name='ageCategoryGenerator', values=(ageCategory, ageCategoryProba))

    return ageCategoryGenerator, categoryBoundaries

# s'imaginer à un output