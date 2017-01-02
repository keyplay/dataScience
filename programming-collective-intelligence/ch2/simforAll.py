#! python2.7
# -*- coding: utf-8 -*-
# simforAll.py - calculate similarity of all users and store the result 

from math import sqrt

def sim_distance(prefs, person1, person2):
    si = {}
    
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
            
    if len(si) == 0:
        return 0
        
    sum_of_square = sum([pow(prefs[person1][item]-prefs[person2][item], 2) for item in si])
    
    return 1/(1+sqrt(sum_of_square))

# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs, person, n=5, similarity=sim_distance):

    scores=[(similarity(prefs, person, other), other) for other in prefs if other!=person]

    scores.sort()
    scores.reverse()

    return scores[0:n]

# calculate similarity of all users and store the result    
def topMatchesForAll(prefs, n=5, similarity=sim_distance):
    sim_dict = {}
    
    for person in prefs:
        sim_dict[person] = topMatches(prefs, person, n, similarity)
        
    return sim_dict

# calculate similarity of all users and store the result in a fast way    
def topMatchesForAllFast(prefs, n=-1, similarity=sim_distance):
    sim_dict = {}
    
    for person in prefs:
        scores = {}   # store the similarity of one person with others
        for other in prefs:
            if other!= person:
                # if the similarity has been calculated, just query it
                if other in sim_dict:
                    scores[other] = sim_dict[other][person]
                else:
                    scores[other] = similarity(prefs, person, other)
        sim_dict[person] = scores
    
    # sort items of sim_dict by value
    import operator
    for person in sim_dict:
        sim_dict[person] = sorted(sim_dict[person].items(), key=operator.itemgetter(1), reverse=True)
        sim_dict[person] = sim_dict[person][0:n]
    return sim_dict

    
# test   
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

print topMatchesForAll(critics)
print topMatchesForAllFast(critics)
