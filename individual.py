import activities

class Individual:

    counter = 0 #counts the number of people (global)
    
    def __init__(self, home, work, idleTime, currentActivity, activities, typicalTimes, age):
        #list is a collection of individuals
        
        Individual.counter += 1
        

        
        self.home = home #NB:cluster home/family la mm chose
        self.work = work #a cluster
        
        self.activies = activities 
            #ça nous permet de changer le comportement des individus
            #activities contient matrice de probas de passage d'une activité à une autre. Pour simplifier, on va commencer par des passages indépendants.
            #mm liste pour tout le  monde et proba diff.
        self.activitiesDurations = typicalTimes
        self.idleTime = idleTime #corresponds to the time (in units of update, before hopping)
        self.currentActivity = currentActivity
        self.age = age
    
    def __del__(self):
        Individual.counter -= 1  
        
    def update():
        
        #controle si dois rester
        idleTime = idleTime-1
        if idleTime == 0:
            activity, time = self.chooseActivity()
            self.currentActivity = activity 
            self.idleTime = time #dangereux ?
            self.choseCluster(activity)

        
        #si un individu doit changer d'activité, choisir l'activité en fonction de la matrice activities.
        # l'activité determine ou non le cluster où on va aller.
        # tirer au sort le temps qu'il y restera.
        # appelle méthode add du cluster, modifie le paramètre cluster de l'individu, et le temps qu'il y reste.

    def setCurrentActivity(self, act):
        self.currentActivity = act
    
    def chooseActivity():
        nextActivitiesProba = self.activities[currentActivity]
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_discrete.html
        ActivityIndices = np.arange(nextActivitiesProba.size())
        custm = stats.rv_discrete(name='custm', values=(ActivityIndices, nextActivitiesProba))
        activity = custm.rvs(size=1) #random integer representing the activity
        time = self.times[activity] #on s'imagine que chaque personne passe un temps diff. sur les activités ou pas?
            # TO DO: ajouter de la variabilité par rapport au temps typique ? Nécessaire ?
        return activity, time
        
    def chooseCluster(activity):

        if activity == family:
            cluster = self.home
            
        elif activity == work:
            cluster = self.work
        
        else:
            cluster = movingRadius(activity)
        
        cluster.new = self
        self.cluster = cluster
    
    def choseInstance(activity, starting_cluster):
        #retrouver le pays et voilà tout le monde est content.
        pass


    #liste d'activités: home, work, school / shopping, visiting?, social
    
    