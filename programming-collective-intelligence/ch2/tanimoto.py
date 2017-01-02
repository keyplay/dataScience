#! python2.7
# -*- coding: utf-8 -*-
# tanimoto.py - get the Tanimoto value of two point to measure the similarity.

def sim_tanimoto(prefs, person1, person2):
    si = {}     # store shared items of person1 and person2
    
    # get shared items
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    
    # if there is no shared items, return 0        
    if len(si) == 0:
        return 0
    
    # calculate the similarity    
    sum1 = sum([prefs[person1][item] * prefs[person2][item] for item in si])
    sum21 = sum([pow(prefs[person1][item], 2) for item in si])
    sum22 = sum([pow(prefs[person2][item], 2) for item in si])
    
    return sum1/(sum21+sum22-sum1)

# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_tanimoto):

  scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]

  scores.sort()
  scores.reverse()

  return scores[0:n]

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
  
print topMatches(critics, 'Toby', n=6, similarity=sim_tanimoto)
