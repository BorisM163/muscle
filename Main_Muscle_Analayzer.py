#!/usr/bin/env python
# from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

import random
import datetime
import PATHS
import MATLAB
import MuscleRunner
import ArraysBuilder
import DEFINES



def multiply_elemnt(arr,mul):
    res=[]
    for x in arr:
        for i in range(mul):
            res.append(x)
    return res
def multiply_array(arr,mul):
    res=[]
    for i in range(mul):
        res+=arr
    return res
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
def py_plotAll(NUMBER_OF_STRINGS_MAX,NUMBER_OF_STRINGS,num_of_mis,res,g_ind,mis_name,avg,scatter,hist):
    # plot preparetion: pos=data in x axis and in y axis. *BUT* not in z axis, data in Z axis is dz_flip
    # link-histogram: https://www.youtube.com/watch?v=W94Kv8-c_5g
    # link2: https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.htmlnum_of_lines=(NUMBER_OF_STRINGS_MAX-NUMBER_OF_STRINGS+1)    num_of_lines = (NUMBER_OF_STRINGS_MAX - NUMBER_OF_STRINGS + 1)

    num_of_lines=len(res["X"]) #NUMBER_OF_STRINGS_MAX+1-NUMBER_OF_STRINGS
    xPos = multiply_array(res["X"], num_of_mis)  # number of lines
    yPos = multiply_elemnt(range(0, num_of_mis), num_of_lines)  # number of flips per line
    zPos = np.zeros((num_of_mis) * num_of_lines)  # start position of the cherts is 0

    dx = 0.9*np.ones(num_of_lines * (num_of_mis))
    dy = 0.9*np.ones(num_of_lines * (num_of_mis))
    dz = flat_arr(res["Z"])
    print len(dx)
    print len(dy)
    print len(dz)
    print len(xPos)
    print len(yPos)
    print len(zPos)
    c=[]
    for z in dz:
        c.append(0.01*z)
    if avg:
        yPos_avg = range(0, num_of_mis)
        xPos_avg = np.zeros(len(yPos_avg))
        zPos_avg = np.zeros(len(yPos_avg))
        dx_avg = np.ones(len(yPos_avg))
        dy_avg = np.ones(len(yPos_avg))
        dz_avg = res['AVG']
    if hist:
        fig1 = plt.figure(g_ind)
        ax3 = fig1.add_subplot(111, projection='3d')
        colors = plt.cm.jet(c)
        ax3.bar3d(xPos, yPos, zPos, dx, dy, dz,color=colors)#'#00cc66')#cmap=cm.afmhot)
        if avg: ax3.bar3d(xPos_avg, yPos_avg, zPos_avg, dx_avg, dy_avg, dz_avg, color='#cc4466')
        ax3.set_xlabel('lines')
        ax3.set_ylabel(mis_name)
        ax3.set_zlabel('mistake - precent')
        ax3.set_title(mis_name)
    if scatter:
        fig2 = plt.figure(g_ind+1)
        ax4 = fig2.add_subplot(111, projection='3d')
        ax4.scatter3D(xPos, yPos, dz, dz, cmap='Greens');
        ax4.set_xlabel('lines')
        ax4.set_ylabel(mis_name)
        ax4.set_zlabel('mistake - precent')
        ax4.set_title(mis_name)

    return dz
def py_barPlot(xAxis_MAX,xAxis_min,num_of_mis,res,g_ind,mis_name):
    num_of_lines=xAxis_MAX+1-xAxis_min
    xPos = multiply_array(range(xAxis_min, xAxis_MAX + 1), num_of_mis)  # number of lines
    yPos = multiply_elemnt(range(0, num_of_mis), num_of_lines)  # number of flips per line
    zPos = np.zeros((num_of_mis) * num_of_lines)  # start position of the cherts is 0

    dx = 0.75*np.ones(num_of_lines * (num_of_mis))
    dy = 0.75*np.ones(num_of_lines * (num_of_mis))
    dz = flat_arr(res["Z"])

    # yPos_avg = range(0, num_of_mis)
    # xPos_avg = np.zeros(len(yPos_avg))
    # zPos_avg = np.zeros(len(yPos_avg))
    # dx_avg = np.ones(len(yPos_avg))
    # dy_avg = np.ones(len(yPos_avg))
    # dz_avg = res['AVG']

    fig1 = plt.figure(g_ind)
    ax3 = fig1.add_subplot(111, projection='3d')
    ax3.bar3d(xPos, yPos, zPos, dx, dy, dz, color='#770000cc')
    # ax3.bar3d(xPos_avg, yPos_avg, zPos_avg, dx_avg, dy_avg, dz_avg, color='#cc4466')
    ax3.set_xlabel('lines')
    ax3.set_ylabel(mis_name)
    ax3.set_zlabel('mistake - precent')
    ax3.set_title(mis_name)
def py_scatterPlot(xAxis_MAX,xAxis_min,num_of_mis,res,g_ind,mis_name):
    num_of_lines=xAxis_MAX+1-xAxis_min
    xPos = multiply_array(range(xAxis_min, xAxis_MAX + 1), num_of_mis)  # number of lines
    yPos = multiply_elemnt(range(0, num_of_mis), num_of_lines)  # number of flips per line
    zPos = np.zeros((num_of_mis) * num_of_lines)  # start position of the cherts is 0

    dx = np.ones(num_of_lines * (num_of_mis))
    dy = np.ones(num_of_lines * (num_of_mis))
    dz = flat_arr(res["Z"])

    fig2 = plt.figure(g_ind+1)
    ax4 = fig2.add_subplot(111, projection='3d')
    ax4.scatter3D(xPos, yPos, dz, dz, cmap='Greens');
    ax4.set_xlabel('lines')
    ax4.set_ylabel(mis_name)
    ax4.set_zlabel('mistake - precent')
    ax4.set_title(mis_name)
def write_arr2File(f,arr):#YAEL 18-10-18
    for x in arr:
        f.write(str(x)+" ")
    f.write("\n")




def graphit(title, type_name, resultForGraph, string_max, strings, mis_inStr_max, mis_inStr, indx):  #YAEL 18-10-18
    MATLAB.makeMATLAB(title, resultForGraph['Z'], DEFINES.NUMBER_OF_STRINGS, DEFINES.NUMBER_OF_STRINGS_MAX, DEFINES.NUMBER_OF_DELETIONS_IN_STR, DEFINES.NUMBER_OF_DELETIONS_IN_STR_MAX, "Number of strings", type_name+" in single string", "Error Probability")
    if not DEFINES.PYTHON_GRAPH and DEFINES.GRAPH:
        MATLAB.run_MATLAB(title)
    if DEFINES.PYTHON_GRAPH and DEFINES.GRAPH:
        num_of_mis = mis_inStr_max + 1 - mis_inStr
        py_plotAll(string_max, strings, num_of_mis, resultForGraph, indx, title, True)



def indexesOf_small2big(smallest,biggest,arr):
    start=-1; i=0; wird=-1;
    for x in arr:
        if x>=smallest and x<=biggest:
            if start==-1: start =i; wird=-1;
        elif x>biggest and start!=-1:
            return start,i
        elif x<smallest and start!=-1:
            wird+=1; #print "wird jump";
            if wird>=2:
                smallest=-1
        i+=1
    return start,i-1

def analayze_decoderStat(strLen,resultForGraph,f_write,num_of_mis):
    f_write.write("\n\n\n\n\n\t99%\t\t95%\t\t90%\n");   i = 0; j=0;
    tempRes = {"Z": [],"X":[]}; j+=1
    tempRes['X']=resultForGraph['X']
    for arr in resultForGraph["Z"]:
        tempRes["Z"].append([])
        for x in arr:
            if x <= 0.001: tempRes["Z"][-1].append(100)
            elif x <= 0.05 and x > 0.01: tempRes["Z"][-1].append(75)
            elif x > 0.05 and x <= 0.1: tempRes["Z"][-1].append(20)
            else: tempRes["Z"][-1].append(0)
    py_plotAll(DEFINES.NUMBER_OF_STRINGS_MAX, DEFINES.NUMBER_OF_STRINGS, num_of_mis, tempRes, strLen, "Del len:"+str(strLen), False,False,True)

#Maybe-YAEL will need
    # f_write.write(str(strLen) + "\n")
    # for num_of_mis in resultForGraph['Y']:
    #     s, t = indexesOf_small2big(0, 0.01, resultForGraph['Z'][i])
    #     f_write.write(str(num_of_mis) + "\t" + str(s) + "-" + str(0 + 1 * t))
    #     s, t = indexesOf_small2big(0.01, 0.05, resultForGraph['Z'][i])
    #     f_write.write("\t\t" + str(s) + "-" + str(0 + 1 * t))
    #     s, t = indexesOf_small2big(0.05, 0.1, resultForGraph['Z'][i])
    #     f_write.write("\t\t" + str(s) + "-" + str(0 + 1 * t) + "\n")
    #     i += 1





############################################ MAIM ############################################
binaryLongString ="00111101001011011000110001101110000011100110110101101101100011100100111100101110110011011010110001101110000011010100110111001100010001110000011000100111011101101100011011000111001101110010011001010110100001100110011011010111100001110010011010110110010101100011011101110110100101110100011100100111001101100111011011000111001000111101101111001011101111"
# binaryLongString ="01001011011000110001101110000011100011100100111100101110110011011010110001101110000011010"
# binarySourceString ="001111010010110110001100011011100000111001101101011011011000111001001111001011101100110110101100011011100000110101001101110011000100011100000110001001110111011011000110110001110011011100100110010101101000011001100110110101111000011100100110101101100101011000110111011101101001011101000111001001110011011001110110110001110010001111011011110010111011111"
# binarySourceString = "10101110001111000010100011001110000110001100100101110001100110010100011100011000011001011011010"

avgRes=open(PATHS.MUSCLE_PATH + PATHS.FILES_PATH + PATHS.AVG_RES_FILE,'w')
stat = open(PATHS.MUSCLE_PATH + PATHS.FILES_PATH + "statistics_MUSCLE.txt", 'w')

temp_end = 100
time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
while temp_end < len(binaryLongString) :
    #YAEL ------ loop statistics
    temp_end += 50
    binarySourceString=binaryLongString[:temp_end]

    DEFINES.NUMBER_OF_STRINGS = 2
    DEFINES.NUMBER_OF_STRINGS_MAX = 10
    # DEFINES.NUMBER_OF_STRINGS_MAX=100
    misMax = 0.1*len(binarySourceString)
    DEFINES.NUMBER_OF_DELETIONS_IN_STR_MAX= int(misMax)
    DEFINES.NUMBER_OF_FLIPS_IN_STR_MAX = int(misMax)
    DEFINES.NUMBER_OF_TOTAL_MISTAKES_MAX = int(misMax)


    if DEFINES.FLIP_MOD:
        numOfGoodString = DEFINES.NUMBER_OF_GOOD_STRINGS_FOR_FLIPS
        numberOfDeletionsInStr = DEFINES.NUMBER_OF_DELETIONS_IN_STR
        numberOfFlipsInStr = DEFINES.NUMBER_OF_FLIPS_IN_STR
        numberOfString = DEFINES.NUMBER_OF_STRINGS
        resultForGraphFlips={"X":[],"Y":[],"Z":[]} #x=number of strings, y=number of filps, z=error precent, AVG = the AVG of z
        while numberOfFlipsInStr <= DEFINES.NUMBER_OF_FLIPS_IN_STR_MAX:
            resultForGraphFlips['Z'].append([])
            while numberOfString <= DEFINES.NUMBER_OF_STRINGS_MAX:
                totalErrorRate=0
                for i in range(DEFINES.RAPEAT_TIMES):
                    numberOfStringsWithFlips = numberOfString - numOfGoodString
                    numberOfStringsWithDeletions,MixedMistakesAddMoreFlips,MixedMistakesAddMoreDels = 0,0,0
                    arr = ArraysBuilder.buildArrays(binarySourceString, numberOfString, numOfGoodString, numberOfDeletionsInStr, numberOfFlipsInStr, numberOfStringsWithDeletions, MixedMistakesAddMoreFlips, MixedMistakesAddMoreDels)
                    errorRate, binaryAfterMajorityString= MuscleRunner.muscleCall_and_Analyze(binarySourceString,arr)
                    totalErrorRate+=errorRate
                # end for
                totalErrorRate / DEFINES.RAPEAT_TIMES
                resultForGraphFlips['Z'][-1].append(totalErrorRate/DEFINES.RAPEAT_TIMES)
                if len(resultForGraphFlips['Z'])==1: resultForGraphFlips['X'].append(numberOfString)
                numberOfString += DEFINES.STRING_GAP
            resultForGraphFlips['Y'].append(numberOfFlipsInStr)
            numberOfFlipsInStr += DEFINES.FLIP_GAP
            numberOfString = DEFINES.NUMBER_OF_STRINGS

        graphit("FlipsGraph"+str(temp_end)+"_strGap"+str(DEFINES.STRING_GAP)+"_flipGap"+str(DEFINES.FLIP_GAP),
                "Flips", resultForGraphFlips, DEFINES.NUMBER_OF_STRINGS_MAX, DEFINES.NUMBER_OF_STRINGS, DEFINES.NUMBER_OF_FLIPS_IN_STR_MAX, DEFINES.NUMBER_OF_FLIPS_IN_STR, 1)
        dz_flip = flat_arr(resultForGraphFlips["Z"])
        avgRes.write(str(len(binarySourceString))+"\n")
        # write_arr2File(avgRes,resultForGraphFlips['AVG'])

    elif DEFINES.DELETE_MOD:
        numOfGoodString = DEFINES.NUMBER_OF_GOOD_STRINGS_FOR_DELETIONS
        numberOfDeletionsInStr = DEFINES.NUMBER_OF_DELETIONS_IN_STR
        numberOfFlipsInStr = DEFINES.NUMBER_OF_FLIPS_IN_STR
        numberOfString = DEFINES.NUMBER_OF_STRINGS
        resultForGraphDeletions={"X":[],"Y":[],"Z":[]} #x=number of strings, y=number of DELETIONSs, z=error precent, AVG = the AVG of z
          # x=number of strings, y=number of DELETIONSs, z=error precent, AVG = the AVG of z
        while numberOfDeletionsInStr <= DEFINES.NUMBER_OF_DELETIONS_IN_STR_MAX:
            resultForGraphDeletionsTemp = []
            resultForGraphDeletions['Z'].append([])
            while numberOfString <= DEFINES.NUMBER_OF_STRINGS_MAX:
                totalErrorRate = 0
                for i in range(DEFINES.RAPEAT_TIMES):
                    numberOfStringsWithDeletions = numberOfString - numOfGoodString
                    numberOfStringsWithFlips, MixedMistakesAddMoreFlips, MixedMistakesAddMoreDels = 0,0,0
                    arr = ArraysBuilder.buildArrays(binarySourceString, numberOfString + 1, numOfGoodString, numberOfDeletionsInStr, numberOfDeletionsInStr, numberOfStringsWithDeletions, MixedMistakesAddMoreFlips, MixedMistakesAddMoreDels)
                    errorRate, binaryAfterMajorityString = MuscleRunner.muscleCall_and_Analyze(binarySourceString, arr)
                    totalErrorRate += errorRate
                # end for
                totalErrorRate / DEFINES.RAPEAT_TIMES
                resultForGraphDeletions['Z'][-1].append(totalErrorRate/DEFINES.RAPEAT_TIMES)
                if len(resultForGraphDeletions['Z'])==1: resultForGraphDeletions['X'].append(numberOfString)
                numberOfString += DEFINES.STRING_GAP
                # end while
            resultForGraphDeletions['Y'].append(numberOfDeletionsInStr)
            numberOfDeletionsInStr += DEFINES.DEL_GAP
            numberOfString = DEFINES.NUMBER_OF_STRINGS
        # end while
        graphit("DeletionsGraph"+str(temp_end)+"_strGap"+str(DEFINES.STRING_GAP)+"_delGap"+str(DEFINES.DEL_GAP),
                "Deletions", resultForGraphDeletions, DEFINES.NUMBER_OF_STRINGS_MAX, DEFINES.NUMBER_OF_STRINGS, DEFINES.NUMBER_OF_DELETIONS_IN_STR_MAX, DEFINES.NUMBER_OF_DELETIONS_IN_STR, 3)
        dz_del = flat_arr(resultForGraphDeletions["Z"])
        # avgRes.write(str(len(binarySourceString))+"\n")
        # # write_arr2File(avgRes,resultForGraphDeletions['AVG'])
        # num_of_mis = DEFINES.NUMBER_OF_DELETIONS_IN_STR_MAX - DEFINES.NUMBER_OF_DELETIONS_IN_STR + 1
        # analayze_decoderStat(len(binarySourceString), resultForGraphDeletions, stat, num_of_mis)



    #THIS PART IS FOR FLIPS AND DELETIONS COMBINDED ANALYZIS
    elif DEFINES.MIXED:
        resultForGraphMixedMistakes = {"X":[],"Y": [], "Z": []}  # x=number of strings, y=number of MixedMistakes, z=error precent
        numberOfTotalMistakes = 0
        numOfGoodString = DEFINES.NUMBER_OF_GOOD_STRINGS_FOR_MIXED # = 0
        numberOfString = DEFINES.NUMBER_OF_STRINGS # = 2

        while numberOfTotalMistakes <= DEFINES.NUMBER_OF_TOTAL_MISTAKES_MAX:
            #numberOfTotalMistakes = numberOfDeletionsInStr + numberOfFlipsInStr
            numberOfDeletionsInStr = random.randint(0,  numberOfTotalMistakes)
            numberOfFlipsInStr = numberOfTotalMistakes-numberOfDeletionsInStr
            resultForGraphMixedMistakes['Z'].append([])
            while numberOfString <= DEFINES.NUMBER_OF_STRINGS_MAX:
                totalErrorRate = 0
                for i in range(DEFINES.RAPEAT_TIMES):
                    numberOfStringsWithDeletions = random.randint(0,numberOfString-numOfGoodString)
                    numberOfStringsWithFlips = numberOfString - numOfGoodString - numberOfStringsWithDeletions
                    MixedMistakesAddMoreFlips =(int)(numberOfStringsWithDeletions/2)
                    MixedMistakesAddMoreDels =  (int)(numberOfStringsWithFlips/2)
                    numberOfStringsWithFlips, MixedMistakesAddMoreFlips, MixedMistakesAddMoreDels = 0, 0, 0
                    arr = ArraysBuilder.buildArrays(binarySourceString, numberOfString, numOfGoodString,
                                                    numberOfDeletionsInStr, numberOfDeletionsInStr,
                                                    numberOfStringsWithDeletions, MixedMistakesAddMoreFlips,
                                                    MixedMistakesAddMoreDels)
                    errorRate,binaryAfterMajorityString = MuscleRunner.muscleCall_and_Analyze(binarySourceString, arr)
                totalErrorRate += errorRate
                # end for
                totalErrorRate / DEFINES.RAPEAT_TIMES
                resultForGraphMixedMistakes['Z'][-1].append(totalErrorRate / DEFINES.RAPEAT_TIMES)
                if len(resultForGraphMixedMistakes['Z'])==1: resultForGraphMixedMistakes['X'].append(numberOfString)
                numberOfString += DEFINES.STRING_GAP
                resultForGraphMixedMistakes['Y'].append(numberOfTotalMistakes)
            numberOfTotalMistakes += DEFINES.MIXED_GAP
            # resultForGraphMixedMistakes['AVG'].append(mean(resultForGraphMixedMistakes['Z'][-1]))
            numberOfString = DEFINES.NUMBER_OF_STRINGS

        graphit("MixedMistakes"+str(temp_end)+"_strGap"+str(DEFINES.STRING_GAP)+"_mstkGap"+str(DEFINES.MIXED_GAP),
                "MixedMistakes",resultForGraphMixedMistakes, DEFINES.NUMBER_OF_STRINGS_MAX, DEFINES.NUMBER_OF_STRINGS, DEFINES.NUMBER_OF_TOTAL_MISTAKES_MAX, DEFINES.NUMBER_OF_TOTAL_MISTAKES_MIN, 5)
        dz_mix = flat_arr(resultForGraphMixedMistakes["Z"])
        avgRes.write(str(len(binarySourceString))+"\n")
        # write_arr2File(avgRes,resultForGraphMixedMistakes['AVG'])

time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
print "start: " + time_start
print "end: " + time_end
x=1

print_before_and_after(binarySourceString, binaryAfterMajorityString) #only the last one, for debugging
avgRes.close()
avgRes = open(PATHS.MUSCLE_PATH + PATHS.FILES_PATH + PATHS.AVG_RES_FILE, 'r')
lines = avgRes.readlines()

#print results to file - avg and staff
stat.write("length\tmistakes_num with 0.05 total error" + "\t" + "precent\n")  # precent of "num of mistakes" that have p error (and less)
strLen_arr = [];
avg_arr = [];
i = 0;
while i < len(lines) - 1:
    countStat = 0
    avg_arr.append([])
    strLen_arr.append(int(lines[i]))
    lines[i + 1] = (lines[i + 1][:-1]).split(" ")
    for x in lines[i + 1][:-1]:
        avg_arr[-1].append(float(x))
        if float(x) < 0.055: countStat += 1
    i += 2
    stat.write(str(strLen_arr[-1]) + "\t\t       " + str(countStat) + "\t\t\t" + format((1.0 * countStat) / DEFINES.NUMBER_OF_DELETIONS_IN_STR_MAX, ".4f") + "\n")

num_of_mis = DEFINES.NUMBER_OF_DELETIONS_IN_STR_MAX - DEFINES.NUMBER_OF_DELETIONS_IN_STR + 1
stat.close(); avgRes.close();


if DEFINES.FLIP_MOD: print "mean: " + format(mean(dz_flip), ".4f")
if DEFINES.DELETE_MOD: print "mean: " + format(mean(dz_del), ".4f")
if DEFINES.MIXED: print "mean: " + format(mean(dz_mix), ".4f")
time_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
print "start: "+time_start
print "end: "+time_end

plt.show()
if DEFINES.PYTHON_GRAPH and DEFINES.GRAPH: plt.show()
