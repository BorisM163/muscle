#!/usr/bin/env python
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

import random
import datetime
import MuscleRunner
import ArraysBuilder
import DEFINES
import Plots

#shalom any yael lustig yim y2

def flat_arr(arr):
    res=[]
    for x in arr:
        res+=x
    return res
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
def print_before_and_after(binarySourceString,binaryAfterMajorityString):
    # type: (object, object) -> object
    print "source: " + str(len(binarySourceString)) + "bits", "\tres: " + str(len(binaryAfterMajorityString)) + "bits"
    print binarySourceString
    print ''.join(binaryAfterMajorityString)
def write_arr2File(f,arr):#YAEL 18-10-18
    for x in arr:
        f.write(str(x)+" ")
    f.write("\n")
def analayze_decoderStat(NUMBER_OF_STRINGS_MAX,NUMBER_OF_STRINGS_MIN, strLen,resultForGraph,num_of_mis):
    i = 0; j=0;
    tempRes = {"Z": [],"X":[]}; j+=1
    tempRes['X']=resultForGraph['X']
    for arr in resultForGraph["Z"]:
        tempRes["Z"].append([])
        for x in arr:
            if x <= 0.001: tempRes["Z"][-1].append(100)
            elif x <= 0.05 and x > 0.01: tempRes["Z"][-1].append(75)
            elif x > 0.05 and x <= 0.1: tempRes["Z"][-1].append(20)
            else: tempRes["Z"][-1].append(0)
    Plots.py_plotAll(NUMBER_OF_STRINGS_MAX, NUMBER_OF_STRINGS_MIN, num_of_mis, tempRes, strLen, "Del len:"+str(strLen), False,False,True)


############################################ MAIM ############################################
binaryLongString ="110001101111111010011100111000011001110111111100111100001110101011011111111001110111111011011100111111001111100011100011111000011010101101100110100011000101101101110010011000011101000111100111101101101001111010111001011101101110101111100111110011110010011100111101100110010011001011100010110010111100111101110110111011011101100111111000011001011110011110010011011101110100111001011100101110110111100111100111110101110100111100001111001111011111000011110100111000011001101101111110010111011001110100110100011100101101111111011111010001100110110010111110001101100111011111001001111001111001111101101110011111000011101111101100110"
y=len(binaryLongString)
x=1
temp_end = 200
time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

while temp_end < len(binaryLongString) :
    temp_end += 100
    binarySourceString = binaryLongString[:temp_end]

    NUMBER_OF_STRINGS_MIN = 20
    NUMBER_OF_STRINGS_MAX = int(0.75*len(binarySourceString))
    misMax = 0.1*len(binarySourceString)
    NUMBER_OF_DELETIONS_IN_STR_MIN= 0
    NUMBER_OF_DELETIONS_IN_STR_MAX= 5 #int(misMax)
    NUMBER_OF_RANDOM_DELETIONS_IN_STR_MIN = 0
    NUMBER_OF_RANDOM_DELETIONS_IN_STR_MAX = int(misMax)
    NUMBER_OF_FLIPS_IN_STR_MIN=0
    NUMBER_OF_FLIPS_IN_STR_MAX = 5#int(misMax)
    NUMBER_OF_TOTAL_MISTAKES_MIN = 0
    NUMBER_OF_TOTAL_MISTAKES_MAX = int(misMax)

    STRING_GAP = 20
    DEL_GAP = 1
    FLIP_GAP = 1
    MIXED_GAP = 1
    RAPEAT_TIMES = 5

    if DEFINES.FLIP_MOD:
        numberOfString = NUMBER_OF_STRINGS_MIN
        numberOfFlipsInStr=NUMBER_OF_FLIPS_IN_STR_MIN
        resultForGraphFlips={"X":[],"Y":[],"Z":[]} #x=number of strings, y=number of filps, z=error precent, AVG = the AVG of z
        while numberOfFlipsInStr <= NUMBER_OF_FLIPS_IN_STR_MAX:
            resultForGraphFlips['Z'].append([])
            while numberOfString <= NUMBER_OF_STRINGS_MAX:
                totalErrorRate=0
                for i in range(RAPEAT_TIMES):
                    arr = ArraysBuilder.buildArrays(binarySourceString=binarySourceString,
                                                    numberOfString=numberOfString,
                                                    numOfGoodString=0,
                                                    numberOfDeletionsInStr=0,
                                                    numberOfFlipsInStr=0,
                                                    numberOfStringsWithDeletions=0,
                                                    MixedMistakesAddMoreFlips=0,
                                                    MixedMistakesAddMoreDels=0)
                    errorRate, binaryAfterMajorityString = MuscleRunner.muscleCall_and_Analyze(binarySourceString, arr)
                    totalErrorRate+=errorRate
                # end for
                totalErrorRate / RAPEAT_TIMES
                resultForGraphFlips['Z'][-1].append(totalErrorRate/RAPEAT_TIMES)
                if len(resultForGraphFlips['Z'])==1: resultForGraphFlips['X'].append(numberOfString)
                numberOfString += STRING_GAP
            resultForGraphFlips['Y'].append(numberOfFlipsInStr)
            numberOfFlipsInStr += FLIP_GAP
            numberOfString = NUMBER_OF_STRINGS_MIN

        Plots.graphit(title="FlipsGraph"+str(temp_end)+"_strGap"+str(STRING_GAP)+"_flipGap"+str(FLIP_GAP),
                type_name="Flips",
                resultForGraph=resultForGraphFlips,
                max_strings=NUMBER_OF_STRINGS_MAX,
                min_strings=NUMBER_OF_STRINGS_MIN,
                mistkaes_inStr_max=NUMBER_OF_FLIPS_IN_STR_MAX,
                mistkaes_inStr_min=NUMBER_OF_FLIPS_IN_STR_MIN,
                indx=1)
        dz_flip = flat_arr(resultForGraphFlips["Z"])
        num_of_mis = NUMBER_OF_FLIPS_IN_STR_MAX - NUMBER_OF_FLIPS_IN_STR_MIN + 1
        analayze_decoderStat(NUMBER_OF_STRINGS_MAX,NUMBER_OF_STRINGS_MIN,len(binarySourceString), resultForGraphFlips, num_of_mis)

    elif DEFINES.DELETE_MOD:
        numberOfDeletionsInStr = 0
        numberOfString = NUMBER_OF_STRINGS_MIN
        resultForGraphDeletions={"X":[],"Y":[],"Z":[]} #x=number of strings, y=number of DELETIONSs, z=error precent
        while numberOfDeletionsInStr <= NUMBER_OF_DELETIONS_IN_STR_MAX:
            resultForGraphDeletions['Z'].append([])
            while numberOfString <= NUMBER_OF_STRINGS_MAX:
                totalErrorRate = 0
                for i in range(RAPEAT_TIMES):
                    arr = ArraysBuilder.buildArrays(binarySourceString=binarySourceString,
                                                    numberOfString=numberOfString+1,
                                                    numOfGoodString=0,
                                                    numberOfDeletionsInStr=numberOfDeletionsInStr,
                                                    numberOfFlipsInStr=numberOfDeletionsInStr,
                                                    numberOfStringsWithDeletions=numberOfString - 0, # numberOfString - numOfGoodString
                                                    MixedMistakesAddMoreFlips=0,
                                                    MixedMistakesAddMoreDels=0)
                    errorRate, binaryAfterMajorityString = MuscleRunner.muscleCall_and_Analyze(binarySourceString, arr)
                    totalErrorRate += errorRate
                totalErrorRate / RAPEAT_TIMES
                resultForGraphDeletions['Z'][-1].append(totalErrorRate/RAPEAT_TIMES)
                if len(resultForGraphDeletions['Z'])==1: resultForGraphDeletions['X'].append(numberOfString)
                numberOfString += STRING_GAP
            resultForGraphDeletions['Y'].append(numberOfDeletionsInStr)
            numberOfDeletionsInStr += DEL_GAP
            numberOfString = NUMBER_OF_STRINGS_MIN
        Plots.graphit(title="DeletionsGraph"+str(temp_end)+"_strGap"+str(STRING_GAP)+"_delGap"+str(DEL_GAP),
                type_name ="Deletions",
                resultForGraph = resultForGraphDeletions,
                max_strings = NUMBER_OF_STRINGS_MAX,
                min_strings = NUMBER_OF_STRINGS_MIN,
                mistkaes_inStr_max = NUMBER_OF_DELETIONS_IN_STR_MAX,
                mistkaes_inStr_min = NUMBER_OF_DELETIONS_IN_STR_MIN,
                indx = 3)
        dz_del = flat_arr(resultForGraphDeletions["Z"])
        num_of_mis = NUMBER_OF_DELETIONS_IN_STR_MAX - NUMBER_OF_DELETIONS_IN_STR_MIN + 1
        analayze_decoderStat(NUMBER_OF_STRINGS_MAX,NUMBER_OF_STRINGS_MIN,len(binarySourceString), resultForGraphDeletions, num_of_mis)

    # DiffrentDeletionsGraph
    elif DEFINES.RANDOM_DELETIONS:
        numberOfRandomDeletionsInStr = NUMBER_OF_RANDOM_DELETIONS_IN_STR_MIN
        numberOfString = NUMBER_OF_STRINGS_MIN
        resultForGraphRandomDeletions = {"X": [], "Y": [],"Z": []}  # x=number of strings, y=number of DELETIONSs, z=error precent
        while numberOfRandomDeletionsInStr <= NUMBER_OF_RANDOM_DELETIONS_IN_STR_MAX:
            resultForGraphRandomDeletions['Z'].append([])
            while numberOfString <= NUMBER_OF_STRINGS_MAX:
                totalErrorRate = 0
                for i in range(RAPEAT_TIMES):
                    arr = ArraysBuilder.buildArraysRandomDeletions(binarySourceString=binarySourceString,
                                                    numberOfString=numberOfString + 1,
                                                    numOfGoodString=0,
                                                    numberOfDeletionsInStr=numberOfRandomDeletionsInStr,
                                                    numberOfFlipsInStr=numberOfRandomDeletionsInStr,
                                                    numberOfStringsWithDeletions=numberOfString - 0,# numberOfString - numOfGoodString
                                                    MixedMistakesAddMoreFlips=0,
                                                    MixedMistakesAddMoreDels=0)
                    errorRate, binaryAfterMajorityString = MuscleRunner.muscleCall_and_Analyze(binarySourceString, arr)
                    totalErrorRate += errorRate
                totalErrorRate / RAPEAT_TIMES
                resultForGraphRandomDeletions['Z'][-1].append(totalErrorRate / RAPEAT_TIMES)
                if len(resultForGraphRandomDeletions['Z']) == 1: resultForGraphRandomDeletions['X'].append(numberOfString)
                numberOfString += STRING_GAP
                resultForGraphRandomDeletions['Y'].append(numberOfRandomDeletionsInStr)
            numberOfRandomDeletionsInStr += DEL_GAP
            numberOfString = NUMBER_OF_STRINGS_MIN
        Plots.graphit(title="RandomDeletionsGraph" + str(temp_end) + "_strGap" + str(STRING_GAP) + "_delGap" + str(DEL_GAP),
                type_name="RandomDeletions",
                resultForGraph=resultForGraphRandomDeletions,
                max_strings=NUMBER_OF_STRINGS_MAX,
                min_strings=NUMBER_OF_STRINGS_MIN,
                mistkaes_inStr_max = NUMBER_OF_RANDOM_DELETIONS_IN_STR_MAX,
                mistkaes_inStr_min = NUMBER_OF_RANDOM_DELETIONS_IN_STR_MIN,
                indx=3)
        dz_rand_del = flat_arr(resultForGraphRandomDeletions["Z"])
        num_of_mis = NUMBER_OF_RANDOM_DELETIONS_IN_STR_MAX - NUMBER_OF_RANDOM_DELETIONS_IN_STR_MIN + 1
        analayze_decoderStat(NUMBER_OF_STRINGS_MAX,NUMBER_OF_STRINGS_MIN,len(binarySourceString), resultForGraphRandomDeletions, num_of_mis)

    #THIS PART IS FOR FLIPS AND DELETIONS COMBINDED ANALYZIS
    elif DEFINES.MIXED:
        resultForGraphMixedMistakes = {"X":[],"Y": [], "Z": []}  # x=number of strings, y=number of MixedMistakes, z=error precent
        numberOfTotalMistakes = NUMBER_OF_TOTAL_MISTAKES_MIN
        numberOfString = NUMBER_OF_STRINGS_MIN # = 2
        while numberOfTotalMistakes <= DEFINES.NUMBER_OF_TOTAL_MISTAKES_MAX:
            #numberOfTotalMistakes = numberOfDeletionsInStr + numberOfFlipsInStr
            numberOfDeletionsInStr = random.randint(0,  numberOfTotalMistakes)
            numberOfFlipsInStr = numberOfTotalMistakes-numberOfDeletionsInStr
            resultForGraphMixedMistakes['Z'].append([])
            while numberOfString <= NUMBER_OF_STRINGS_MAX:
                totalErrorRate = 0
                for i in range(DEFINES.RAPEAT_TIMES):
                    numOfGoodString=0
                    numberOfStringsWithDeletions = random.randint(0, numberOfString - numOfGoodString)
                    numberOfStringsWithFlips = numberOfString - numOfGoodString - numberOfStringsWithDeletions
                    MixedMistakesAddMoreFlips = (int)(numberOfStringsWithDeletions / 2)
                    MixedMistakesAddMoreDels = (int)(numberOfStringsWithFlips / 2)
                    arr = ArraysBuilder.buildArrays(binarySourceString=binarySourceString,
                                                    numberOfString=numberOfString,
                                                    numOfGoodString=numOfGoodString,
                                                    numberOfDeletionsInStr=numberOfDeletionsInStr,
                                                    numberOfFlipsInStr=numberOfDeletionsInStr,
                                                    numberOfStringsWithDeletions=numberOfStringsWithDeletions,
                                                    MixedMistakesAddMoreFlips=MixedMistakesAddMoreFlips,
                                                    MixedMistakesAddMoreDels=MixedMistakesAddMoreDels)
                    errorRate, binaryAfterMajorityString = MuscleRunner.muscleCall_and_Analyze(binarySourceString, arr)
                    totalErrorRate += errorRate
                # end for
                resultForGraphMixedMistakes['Z'][-1].append(totalErrorRate / DEFINES.RAPEAT_TIMES)
                if len(resultForGraphMixedMistakes['Z'])==1: resultForGraphMixedMistakes['X'].append(numberOfString)
                numberOfString += STRING_GAP
                resultForGraphMixedMistakes['Y'].append(numberOfTotalMistakes)
            numberOfTotalMistakes += MIXED_GAP
            numberOfString = NUMBER_OF_STRINGS_MIN

        Plots.graphit(title="MixedMistakes"+str(temp_end)+"_strGap"+str(STRING_GAP)+"_mstkGap"+str(MIXED_GAP),
                      type_name = "MixedMistakes",
                      resultForGraph=resultForGraphMixedMistakes,
                      max_strings=NUMBER_OF_STRINGS_MAX,
                      min_strings=NUMBER_OF_STRINGS_MIN,
                      mistkaes_inStr_max=NUMBER_OF_TOTAL_MISTAKES_MAX,
                      mistkaes_inStr_min=NUMBER_OF_TOTAL_MISTAKES_MIN,
                      indx=5)
        dz_mix = flat_arr(resultForGraphMixedMistakes["Z"])
    num_of_mis = NUMBER_OF_TOTAL_MISTAKES_MAX - NUMBER_OF_TOTAL_MISTAKES_MIN + 1
    analayze_decoderStat(NUMBER_OF_STRINGS_MAX, NUMBER_OF_STRINGS_MIN, len(binarySourceString), resultForGraphMixedMistakes, num_of_mis)



print_before_and_after(binarySourceString, binaryAfterMajorityString) #only the last one, for debugging

if DEFINES.FLIP_MOD: print "mean: " + format(mean(dz_flip), ".4f")
if DEFINES.DELETE_MOD: print "mean: " + format(mean(dz_del), ".4f")
# if DEFINES.MIXED: print "mean: " + format(mean(dz_mix), ".4f")
if DEFINES.RANDOM_DELETIONS: print "mean: " + format(mean(dz_rand_del), ".4f")

time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
print "start: " + time_start
print "end: " + time_end
x=1

plt.show()
if DEFINES.PYTHON_GRAPH and DEFINES.GRAPH_MID: plt.show()
