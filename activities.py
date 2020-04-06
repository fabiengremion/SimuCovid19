import numpy as np
from scipy.stats import rv_discrete
activities = ['home', 'work', 'shopping', 'social']
#TODO:add visiting, differentiate work from school
typicalTimes = [12, 8, 8, 1, 4]
mobilityDegrees = {'home':[0,0,0,0], 'work':[0.05, 0.55, 0.3, 0.1],'shopping': [0.0,0.05,0.15,0.8], 'social': [0.01, 0.09, 0.8, 0.1]}
#idea: different levels: country-regions-cities-neighbourhood
#home has an assigned place

def sampleDistanceGenerator(activity):
    return rv_discrete(name='sampleDistanceGenerator', values=(np.arange(4), mobilityDegrees(activity)))