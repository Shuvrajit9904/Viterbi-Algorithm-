import sys
import numpy as np
import math
prob1 = sys.argv[1]
prob = open(prob1)

probDict = {}
for items in prob:    
    split1 = items.split()
    ky = " ".join([split1[0],split1[1]])
    probDict[ky] = float(split1[-1])

sent1 = sys.argv[2]
sent = open(sent1)

pos = open('possiblePoS.txt')
possiblePoS = []

for line in pos:
    line.strip('\n')
    possiblePoS.append(line.strip('\n'))

dictPoS = {}
for i in range(len(possiblePoS)):
    dictPoS[i] = possiblePoS[i]
    
for line in sent:
    print "PROCESSING SENTENCE:", line
    split2 = line.split()
    l1 = len(split2)
    l2 = len(possiblePoS)
    viterbi = np.ones((l2, l1))
    forward = np.ones((l2, l1))
    backpointer = np.zeros((l2, l1-1))
    for wrd in range(l1):
        for state in range(l2):
            if wrd == 0:
                #backpointer[state,wrd] = 0
                transition = " ".join([possiblePoS[state].lower(),'phi'])
                emission = " ".join([split2[wrd],possiblePoS[state]])                            
                if emission and transition in probDict:
                    viterbi[state,wrd] = probDict[transition]*probDict[emission]
                    forward[state,wrd] = probDict[transition]*probDict[emission]
                elif emission in probDict and transition not in probDict:                    
                    viterbi[state,wrd] = math.pow(10,-4)*probDict[emission]
                    forward[state,wrd] = math.pow(10,-4)*probDict[emission]
                elif transition in probDict and emission not in probDict:                    
                    viterbi[state,wrd] = math.pow(10,-4)*probDict[transition]
                    forward[state,wrd] = math.pow(10,-4)*probDict[transition]
                else:
                    viterbi[state,wrd] = math.pow(10,-8)
                    forward[state,wrd] = math.pow(10,-8)
            else:                
                emission = " ".join([split2[wrd].lower(),possiblePoS[state].lower()])                
                maintainarray = []
                i = 0
                for st in viterbi[:,wrd-1]:
                    transition = " ".join([possiblePoS[state], dictPoS[i]])
                    if transition in probDict:                            
                        maintainarray.append(st * probDict[transition])
                    else:
                        maintainarray.append(st * 0.0001)
                    i += 1
                if emission in probDict:                    
                    viterbi[state,wrd] = max(maintainarray)*probDict[emission]
                    backpointer[state,wrd-1] = maintainarray.index(max(maintainarray))                    
                    forward[state,wrd] = probDict[emission] * sum(maintainarray)
                else:
                    viterbi[state,wrd] = max(maintainarray)*math.pow(10,-4)
                    backpointer[state,wrd-1] = maintainarray.index(max(maintainarray))
                    forward[state,wrd] = math.pow(10,-4) * sum(maintainarray)

    v = np.log2(viterbi)
    print "FINAL VITERBI NETWORK"
    for i in range(len(v[0,:])):
        for j in range(len(v[:,0])):
            #print j,len(v[0,:])
            print "P({} = {}) = {}".format(split2[i], dictPoS[j], round(v[j,i],4))
    print '\n'        
    #print backpointer
    print "FINAL BACKPOINTER NETWORK"
    for i in range(len(backpointer[0,:])):
        for j in range(len(backpointer[:,0])):            
            print "Backptr({} = {}) = {}".format(split2[i], dictPoS[j], dictPoS[backpointer[j,i]])
    print '\n'
    print "BEST TAG SEQUENCE HAS LOG PROBABILITY = {}".format(round(max(v[:,-1]),4))
    for i in range(len(v[0,:])):
        l = len(v[0,:])-1
        word = len(v[0,:])-1-i
        mx = -1
        for j in range(len(v[:,word])):
            if viterbi[j,word] >= mx:
                mx = viterbi[j,word]
                ind = j
        print "{} -> {}".format(split2[word],possiblePoS[ind])
    print '\n'
    print "FORWARD ALGORITHM RESULTS"
    #print forward
    for i in range(len(forward[0,:])):
        tot = 0
        for j in range(len(forward[:,0])):
            tot = tot + forward[j,i]
        for j in range(len(forward[:,0])):            
            print "P({} = {}) = {}".format(split2[i], dictPoS[j], round(forward[j,i]/tot,4))
    print '\n'            
