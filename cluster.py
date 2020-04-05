class Cluster:

    def __init__(self, listOfIndividuals, district, parameters):
        #list is a collection of individuals
        self.individuals = listOfIndividuals
        self.new = []
        self.parameters = parameters
            #proba d'y venir (0 si closed)
        
        self.district = district
        #position est un quartier qui appartient à une ville qui appartient à la Suisse.
        
        
        #Dans paramètres, ajouter un nombre moyen de personnes
        
    def update():
        
        #simule le spreading

        #demande à chaque individu s'il veut rester. Si oui rien change, sinon on l'enleve de la liste
        
        for el in self.individuals:
            el.update()
            #dans la méthode update éventuellement un individu sera mis dans la liste "new"
            
    def flush():
        
        self.individuals.append(self.new)
        for el in self.new:
            el.cluster = self
        self.new = empty()
        

class Family(Cluster):
    def __init__(self, listOfIndividuals, district, parameters):
        #utile pour restreindre les parametres
        super().__init__(listOfIndividuals, district, parameters)
        district.families.append(self)
        
    def addHomeIndividual(self, listOfIndividuals):
        self.individuals.append(listOfIndividuals)
        for el in listOfIndividuals:
            el.home = self
        
        
class Work(Cluster):
    def __init__(self, listOfIndividuals, district, parameters, size):
        #utile pour restreindre les parametres
        super().__init__(listOfIndividuals, district, parameters)
        district.work.append(self)
        self.size = size
        
    def addEmployees(self,emps):
        for el in emps:
            el.work = self
        
        
class SuperMarket(Cluster):
    def __init__(self, listOfIndividuals, district, parameters):
        #utile pour restreindre les parametres
        super().__init__(listOfIndividuals, district, parameters)
        district.superMarket.append(self)
        
class PublicPlaces(Cluster):
    def __init__(self, listOfIndividuals, district, parameters):
        #utile pour restreindre les parametres
        super().__init__(listOfIndividuals, district, parameters)
        district.publicPlaces.append(self)
        
        
class Alone(Cluster):
    def __init__(self, list, parameters):
        #utile pour restreindre les parametres
        super().__init__(list, parameters)