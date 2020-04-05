import activities

class Individual:

    __counter = 0 #counts the number of people
    
    def __init__(self, home, age, typeSocial, work, identity, idleTime, activity, typicalTimes):
        #list is a collection of individuals
        self.cluster = cluster
        
        type(self).__counter += 1
        
        self.age = age
        self.typeSocial = typeSocial #par exemple adulte, enfant, grand-parent
        
        self.home = home #NB:cluster home/family la mm chose
        self.work = work #a cluster
        self.identity = identity #a voir si c'est utile
        
        self.activies = typeSocial.activities 
            #ça nous permet de changer le comportement des individus
            #activities contient matrice de probas de passage d'une activité à une autre. Pour simplifier, on va commencer par des passages indépendants.
            #mm liste pour tout le  monde et proba diff.
        self.activitiesDurations = typicalTimes
        self.idleTime = idleTime #corresponds to the time (in units of update, before hopping)
        self.currentActivity = activity
    
    def __del__(self):
        type(self).__counter -= 1  
        
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
        #ici ça se corse...
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
    
    