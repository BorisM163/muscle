#!/usr/bin/env python
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import random

#python or matlab graph

#OPERETION MODS
PYTHON_GRAPH=True

FLIP_MOD=False
DELETE_MOD=True
MIXED=False #15-10-18

#count space as a mistake
COUNT_SPACE_MISS=False

#statistics
NUMBER_OF_STRINGS=2
NUMBER_OF_STRINGS_MAX=70

NUMBER_OF_GOOD_STRINGS_FOR_FLIPS = 0
NUMBER_OF_GOOD_STRINGS_FOR_DELETIONS = 1
NUMBER_OF_GOOD_STRINGS_FOR_MIXED =0

NUMBER_OF_DELETIONS_IN_STR = 0
NUMBER_OF_DELETIONS_IN_STR_MAX=40
NUMBER_OF_FLIPS_IN_STR = 0
NUMBER_OF_FLIPS_IN_STR_MAX =30

NUMBER_OF_TOTAL_MISTAKES_MAX = 5 # for the mixed 15-10-18
NUMBER_OF_TOTAL_MISTAKES_MIN = 0 #for the mixed 15-10-18
MUSCLE_PATH ="/home/ubu/Yael/"#muscle3.8.31_i86linux64"   #Lab
#MUSCLE_PATH ="C:/Users/moshab/Desktop/final project/muscle/"  #Boris_comp
MUSCLE_IN_FILE = "in.txt"
MUSCLE_OUT_FILE = "out.txt"


def arr2FASTA(arr,form): #take an array and poot in fasta format
    #if form==1: it is DNA form.
    #if form==0 it is protain form
    fasta_file=open(MUSCLE_PATH+MUSCLE_IN_FILE,'w')
    if form == 1: str_form=">gi|"
    else: str_form =">AB"
    i=1
    for line in arr:
        fasta_file.write(str_form)
        fasta_file.write(str(i)+"\n")
        for x in line:
            if x=="0": fasta_file.write("E"+" ")
            if x=="1": fasta_file.write("A"+" ")
        fasta_file.write("\n"); i+=1
    fasta_file.close()

def FASTA2arr(fasta_file,output_file):#take fasta file, change it to an array and save the output on a file
    arr=[]
    lines=fasta_file.readlines()
    for line in lines:
        if line[0] != ">":
            for x in line:
                if x=="E": arr[-1].append("0")
                if x=="A": arr[-1].append("1")
                if x=='-': arr[-1].append("-")
        else:
            if line[0]==">":
                arr.append([])

    for line in arr:#write to file
        for x in line:
            output_file.write(str(x)+" ")
        output_file.write("\n")
    return arr

def calc_str_majority(arr):
    length=[]; res=[]; i=-1
    for line in arr: length.append(len(line))
    while(i<max(length)-1):
        count1=0; count0=0; i+=1; countSpace=0;
        for line in arr:
            if i<len(line):
                if line[i]=="1": count1+=1
                elif line[i]=="0": count0+=1
                elif line[i]=="-": countSpace+=1
        if countSpace>max(count0,count1): res.append("-")
        elif count1>max(count0,countSpace): res.append("1")
        else: res.append("0")
    return res

def buildArrays(binarySourceString, numberOfString, numOfGoodString=0,numberOfDeletionsInStr=0,numberOfFlipsInStr=0,numberOfStringsWithDeletions=None, numberOfStringsWithFlips=None, numberOfStringsWithMixedMistakes=None):
    arr=[]
    #boris dont forget fix this
    # if (numberOfStringsWithDeletions is None) and (numberOfStringsWithFlips is None):
    #     numberOfStringsWithDeletions = numberOfString - numOfGoodString
    #     numberOfStringsWithFlips = numberOfString - numOfGoodString
    #
    # if (numberOfStringsWithDeletions + numberOfStringsWithFlips  + numOfGoodString) != numberOfString:
    #     assert("string array building calculation has problem, cheack yourself")

    for i in range(0,numberOfString):
        arr.append(binarySourceString)
    if numberOfDeletionsInStr!=0:
        arr=makeDeletionsInStr(arr,numberOfString,numOfGoodString,numberOfDeletionsInStr, numberOfStringsWithDeletions, numberOfStringsWithFlips,numberOfStringsWithMixedMistakes)
    if numberOfFlipsInStr!=0:
        arr=makeOfFlipsInStr(arr,numberOfString,numOfGoodString,numberOfFlipsInStr, numberOfStringsWithDeletions, numberOfStringsWithFlips,numberOfStringsWithMixedMistakes)
    return arr

def makeDeletionsInStr(arr, numberOfString, numOfGoodString,numberOfDeletionsInStr, numberOfStringsWithDeletions, numberOfStringsWithFlips,numberOfStringsWithMixedMistakes):
    for x in range(numOfGoodString, numOfGoodString + numberOfStringsWithDeletions): #17-10-18 night
        for j in range(numberOfDeletionsInStr):
            l=len(arr[x])
            i = random.randint(0, l-1)
            arr[x]=arr[x][:i]+arr[x][i+1:]
    return arr

def makeOfFlipsInStr(arr, numberOfString, numOfGoodString,numberOfFlipsInStr, numberOfStringsWithDeletions, numberOfStringsWithFlips,numberOfStringsWithMixedMistakes):
    for x in range(numOfGoodString + numberOfStringsWithDeletions - numberOfStringsWithMixedMistakes ,numberOfString):
        for j in range(numberOfFlipsInStr):
            l=len(arr[x])
            i = random.randint(0, l-1)
            if arr[x][i]=='1':
                arr[x]=arr[x][:i]+'0'+arr[x][i+1:]
            else:
                arr[x] = arr[x][:i] + '1' + arr[x][i+1:]
    return arr

def statisticsFromMuscle(binarySourceString, binaryAfterMajorityString,resultForGraph):
    counter = {"Flips": 0, "Space": 0}
    sourceLen =len(binarySourceString)
    AfterMajorityLen= (binaryAfterMajorityString)
    if AfterMajorityLen!=sourceLen:
        assert("binarySourceString and binaryAfterMajorityString are in diffrent sizes")
    for s,m in zip(binarySourceString,binaryAfterMajorityString):
        if s!=m:
            if m =='-':
                if COUNT_SPACE_MISS:
                    counter['Space']+=1
            else: counter['Flips']+=1
    resultForGraph['Z'][-1].append((1.0*(counter['Space']+counter['Flips']))/sourceLen) # resultForGraph['Z'].append((counter['Space']+counter['Flips'])/strLen)
    return resultForGraph

def makeMATLAB(fileName,listList,minX,maxX, minY,maxY,xlabel,ylabel,zlabel):
    # this code make anylezation of the muscle tool using MATLAB
    #https://stackoverflow.com/questions/6657005/matlab-running-an-m-file-from-command-line
    f=open(MUSCLE_PATH+fileName+".m",'w')
    f.write("[X,Y] = meshgrid("+str(minX)+":"+str(maxX)+","+str(minY) +":"+str(maxY)+");\n")
    f.write("Z=[")
    for list in listList:
        f.write(str(list))
        f.write(";")
    f.write("];\n")
    f.write("mesh(X,Y,Z);\n")
    f.write("xlabel('"+xlabel+"');\n")
    f.write("ylabel('"+ylabel+"');\n")
    f.write("zlabel('"+zlabel+"');\n")
    f.write("savefig('"+fileName+"Lines')\n")

    #https://stackoverflow.com/questions/28991376/how-to-set-x-and-y-values-when-using-bar3-in-matlab
    f.write("figure\n")
    f.write("x=["+str(minX)+":"+str(maxX)+"];\n")
    f.write("y=["+str(minY)+":"+str(maxY)+"];\n")
    f.write("h=bar3(y, Z);\n")
    f.write("Xdat=get(h,'XData');\n")
    f.write("axis tight\n")
    f.write("for ii=1:length(Xdat)\n"
            "    Xdat{ii}=Xdat{ii}+(min(x(:))-1)*ones(size(Xdat{ii}));\n"
            "    set(h(ii),'XData',Xdat{ii});\n"
            "end\n")
    f.write("xlabel('"+xlabel+"');\n")
    f.write("ylabel('"+ylabel+"');\n")
    f.write("zlabel('"+zlabel+"');\n")
    f.write("savefig('"+fileName+"Bars')\n")
    f.close()

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
    print "source: " + str(len(binarySourceString)) + "bits", "\tres: " + str(len(binaryAfterMajorityString)) + "bits"
    print binarySourceString
    print ''.join(binaryAfterMajorityString)
def py_plot(NUMBER_OF_STRINGS_MAX,NUMBER_OF_STRINGS,num_of_mis,res,g_ind,mis_name):
    # plot preparetion: pos=data in x axis and in y axis. *BUT* not in z axis, data in Z axis is dz_flip
    # link-histogram: https://www.youtube.com/watch?v=W94Kv8-c_5g
    # link2: https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.htmlnum_of_lines=(NUMBER_OF_STRINGS_MAX-NUMBER_OF_STRINGS+1)    num_of_lines = (NUMBER_OF_STRINGS_MAX - NUMBER_OF_STRINGS + 1)
    num_of_lines=NUMBER_OF_STRINGS_MAX+1-NUMBER_OF_STRINGS
    xPos = multiply_array(range(NUMBER_OF_STRINGS, NUMBER_OF_STRINGS_MAX + 1), num_of_mis)  # number of lines
    yPos = multiply_elemnt(range(0, num_of_mis), num_of_lines)  # number of flips per line
    zPos = np.zeros((num_of_mis) * num_of_lines)  # start position of the cherts is 0

    dx = np.ones(num_of_lines * (num_of_mis))
    dy = np.ones(num_of_lines * (num_of_mis))
    dz = flat_arr(res["Z"])

    yPos_avg = range(0, num_of_mis)
    xPos_avg = np.zeros(len(yPos_avg))
    zPos_avg = np.zeros(len(yPos_avg))
    dx_avg = np.ones(len(yPos_avg))
    dy_avg = np.ones(len(yPos_avg))
    dz_avg = res['AVG']

    fig1 = plt.figure(g_ind)
    ax3 = fig1.add_subplot(111, projection='3d')
    ax3.bar3d(xPos, yPos, zPos, dx, dy, dz, color='#00ceaa')
    ax3.bar3d(xPos_avg, yPos_avg, zPos_avg, dx_avg, dy_avg, dz_avg, color='#cc4466')
    ax3.set_xlabel('lines')
    ax3.set_ylabel('mis_name')
    ax3.set_zlabel('mistake - precent')
    ax3.set_title('mis_name')

    fig2 = plt.figure(g_ind+1)
    ax4 = fig2.add_subplot(111, projection='3d')
    ax4.scatter3D(xPos, yPos, dz, dz, cmap='Greens');
    ax4.set_xlabel('lines')
    ax4.set_ylabel('mis_name')
    ax4.set_zlabel('mistake - precent')
    ax4.set_title('mis_name')

    return dz

############################################ MAIM ############################################
binarySourceString ="01110100101101100011000110111000001110011011010110110110001110010011110010111011001101101011000110111000001101010011011100110001000111000001100010011101110110110001101100011100"
#"01001011011000110001101110000011100011100100111100101110110011011010110001101110000011010"
#"10101110001111000010100011001110000110001100100101110001100110010100011100011000011001011011010"
DEBUG = False #debug flags to all this program

if DEBUG:
    counter=0

if FLIP_MOD:
    numOfGoodString = NUMBER_OF_GOOD_STRINGS_FOR_FLIPS
    numberOfDeletionsInStr = NUMBER_OF_DELETIONS_IN_STR
    numberOfFlipsInStr = NUMBER_OF_FLIPS_IN_STR
    numberOfString = NUMBER_OF_STRINGS
    #resultForGraphFlips={"Y":[],"Z":[]} #x=number of strings, y=number of filps, z=error precent
    resultForGraphFlips={"Y":[],"Z":[],"AVG":[]} #x=number of strings, y=number of filps, z=error precent
    while numberOfFlipsInStr <=NUMBER_OF_FLIPS_IN_STR_MAX:
        resultForGraphFlips['Z'].append([])
        while numberOfString <= NUMBER_OF_STRINGS_MAX:
            # 17-10-18 night fix
            numberOfStringsWithDeletions = 0
            numberOfStringsWithFlips = numberOfString - numOfGoodString
            numberOfStringsWithMixedMistakes = 0
            arr = buildArrays(binarySourceString, numberOfString, numOfGoodString, numberOfDeletionsInStr, numberOfFlipsInStr,numberOfStringsWithDeletions,numberOfStringsWithFlips, numberOfStringsWithMixedMistakes)
            arr2FASTA(arr, 0)  # put arr in "in.txt" file
            subprocess.call([r"/home/ubu/Yael/muscle3.8.31_i86linux64", "-in", MUSCLE_PATH + MUSCLE_IN_FILE, "-out", MUSCLE_PATH + MUSCLE_OUT_FILE]);
            #subprocess.call([r"C:\\Users\moshab\Desktop\final project\muscle\muscle3.8.31_i86win32.exe", "-in", MUSCLE_PATH + MUSCLE_IN_FILE, "-out",MUSCLE_PATH + MUSCLE_OUT_FILE])
            fasta_file = open(MUSCLE_PATH + MUSCLE_OUT_FILE, 'r')  # read the output of mussle
            output_file = open(MUSCLE_PATH+'mussle_norm_output.txt', 'w')
            fasta_res = FASTA2arr(fasta_file, output_file)
            output_file.close()
            fasta_file.close()
            binaryAfterMajorityString = calc_str_majority(fasta_res)
            resultForGraphFlips=statisticsFromMuscle(binarySourceString, binaryAfterMajorityString, resultForGraphFlips)
            numberOfString += 1
        resultForGraphFlips['Y'].append(numberOfFlipsInStr)
        resultForGraphFlips['AVG'].append(mean(resultForGraphFlips['Z'][-1]))
        numberOfFlipsInStr+=1
        numberOfString = NUMBER_OF_STRINGS

    #------------------------------------BORIS------------------------------------------------------------------------------------------------------------

    makeMATLAB("FlipsGraph", resultForGraphFlips['Z'], NUMBER_OF_STRINGS, NUMBER_OF_STRINGS_MAX, NUMBER_OF_FLIPS_IN_STR,
               NUMBER_OF_FLIPS_IN_STR_MAX, "Number of strings", "Flips in single string", "Error Probability")
    if not PYTHON_GRAPH:
        subprocess.call([r"C:\\Programs\MATLAB\R2017b\bin\matlab.exe","-nodisplay", "-nosplash", "-nodesktop", "-r","\"run('"+MUSCLE_PATH + "FlipsGraph.m')\""])
        x = 1
    if PYTHON_GRAPH:
        num_of_flip = NUMBER_OF_FLIPS_IN_STR_MAX + 1 - NUMBER_OF_FLIPS_IN_STR
        dz_flip = py_plot(NUMBER_OF_STRINGS_MAX, NUMBER_OF_STRINGS, num_of_flip, resultForGraphFlips, 1,"Flips")

if DELETE_MOD:
    numOfGoodString = NUMBER_OF_GOOD_STRINGS_FOR_DELETIONS
    numberOfDeletionsInStr = NUMBER_OF_DELETIONS_IN_STR
    numberOfFlipsInStr = NUMBER_OF_FLIPS_IN_STR
    numberOfString = NUMBER_OF_STRINGS
    #resultForGraphDeletions={"Y":[],"Z":[]} #x=number of strings, y=number of DELETIONSs, z=error precent
    resultForGraphDeletions={"Y":[],"Z":[],"AVG":[]} #x=number of strings, y=number of DELETIONSs, z=error precent
    while numberOfDeletionsInStr <=NUMBER_OF_DELETIONS_IN_STR_MAX:
        resultForGraphDeletions['Z'].append([])
        while numberOfString <= NUMBER_OF_STRINGS_MAX:
            numberOfStringsWithDeletions = numberOfString - numOfGoodString
            numberOfStringsWithFlips = 0
            numberOfStringsWithMixedMistakes = 0
            arr = buildArrays(binarySourceString, numberOfString, numOfGoodString, numberOfDeletionsInStr, numberOfFlipsInStr,numberOfStringsWithDeletions,numberOfStringsWithFlips, numberOfStringsWithMixedMistakes)
            arr2FASTA(arr, 1)  # put arr in "in.txt" file
            subprocess.call([r"/home/ubu/Yael/muscle3.8.31_i86linux64", "-in", MUSCLE_PATH + MUSCLE_IN_FILE, "-out",MUSCLE_PATH + MUSCLE_OUT_FILE])
            #subprocess.call([r"C:\\Users\moshab\Desktop\final project\muscle\muscle3.8.31_i86win32.exe", "-in", MUSCLE_PATH + MUSCLE_IN_FILE, "-out",MUSCLE_PATH + MUSCLE_OUT_FILE])
            fasta_file = open(MUSCLE_PATH + MUSCLE_OUT_FILE, 'r')  # read the output of mussle
            output_file = open(MUSCLE_PATH+'mussle_norm_output.txt', 'w')
            fasta_res = FASTA2arr(fasta_file, output_file)
            output_file.close()
            fasta_file.close()
            binaryAfterMajorityString = calc_str_majority(fasta_res)
            resultForGraphDeletions=statisticsFromMuscle(binarySourceString, binaryAfterMajorityString, resultForGraphDeletions)
            numberOfString+=1
        resultForGraphDeletions['Y'].append(numberOfDeletionsInStr)
        resultForGraphDeletions['AVG'].append(mean(resultForGraphDeletions['Z'][-1]))
        numberOfDeletionsInStr+=1
        numberOfString = NUMBER_OF_STRINGS


    #------------------------------------BORIS------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    makeMATLAB("DeletionsGraph", resultForGraphDeletions['Z'], NUMBER_OF_STRINGS, NUMBER_OF_STRINGS_MAX,
               NUMBER_OF_DELETIONS_IN_STR, NUMBER_OF_DELETIONS_IN_STR_MAX, "Number of strings",
               "Delitions in single string", "Error Probability")
    if not PYTHON_GRAPH:
        subprocess.call([r"C:\\Programs\MATLAB\R2017b\bin\matlab.exe","-nodisplay", "-nosplash", "-nodesktop", "-r","\"run('"+MUSCLE_PATH + "DeletionsGraph.m')\""])
        x = 1

    if PYTHON_GRAPH:
        num_of_del=NUMBER_OF_DELETIONS_IN_STR_MAX + 1- NUMBER_OF_DELETIONS_IN_STR
        dz_del= py_plot(NUMBER_OF_STRINGS_MAX, NUMBER_OF_STRINGS, num_of_del, resultForGraphDeletions,3, "Deleteions")


#THIS PART IS FOR FLIPS AND DELETIONS COMBINDED ANALYZIS
if MIXED:
    #resultForGraphMixedMistakes = {"Y": [], "Z": []}  # x=number of strings, y=number of MixedMistakes, z=error precent
    resultForGraphMixedMistakes = {"Y": [], "Z": [],"AVG":[]}  # x=number of strings, y=number of MixedMistakes, z=error precent

    numberOfTotalMistakes = 0
    numOfGoodString = NUMBER_OF_GOOD_STRINGS_FOR_MIXED
    numberOfString = NUMBER_OF_STRINGS

    while numberOfTotalMistakes <= NUMBER_OF_TOTAL_MISTAKES_MAX:
        numberOfDeletionsInStr = random.randint(0,  numberOfTotalMistakes)
        numberOfFlipsInStr = numberOfTotalMistakes-numberOfDeletionsInStr
        resultForGraphMixedMistakes['Z'].append([]) #17-10-18 night
        while numberOfString <= NUMBER_OF_STRINGS_MAX:
            numberOfStringsWithDeletions = random.randint(0,numberOfString-numOfGoodString)
            numberOfStringsWithFlips = numberOfString - numOfGoodString - numberOfStringsWithDeletions
            numberOfStringsWithMixedMistakes = (int)((numberOfString - numOfGoodString)/2)
            arr = buildArrays(binarySourceString, numberOfString, numOfGoodString, numberOfDeletionsInStr, numberOfFlipsInStr, numberOfStringsWithDeletions, numberOfStringsWithFlips , numberOfStringsWithMixedMistakes)
            arr2FASTA(arr, 1)  # put arr in "in.txt" file
            subprocess.call([r"/home/ubu/Yael/muscle3.8.31_i86linux64", "-in", MUSCLE_PATH + MUSCLE_IN_FILE, "-out",MUSCLE_PATH + MUSCLE_OUT_FILE])
            #subprocess.call([r"C:\\Users\moshab\Desktop\final project\muscle\muscle3.8.31_i86win32.exe", "-in",
             #                MUSCLE_PATH + MUSCLE_IN_FILE, "-out", MUSCLE_PATH + MUSCLE_OUT_FILE])
            fasta_file = open(MUSCLE_PATH + MUSCLE_OUT_FILE, 'r')  # read the output of mussle
            output_file = open(MUSCLE_PATH + 'mussle_norm_output.txt', 'w')
            fasta_res = FASTA2arr(fasta_file, output_file)
            output_file.close()
            fasta_file.close()
            binaryAfterMajorityString = calc_str_majority(fasta_res)
            statisticsFromMuscle(binarySourceString, binaryAfterMajorityString, resultForGraphMixedMistakes)
            numberOfString += 1
            resultForGraphMixedMistakes['Y'].append(numberOfTotalMistakes)
        numberOfTotalMistakes += 1
        resultForGraphMixedMistakes['AVG'].append(mean(resultForGraphMixedMistakes['Z'][-1]))
        numberOfString = NUMBER_OF_STRINGS

    #------------------------------------BORIS------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    makeMATLAB("MixedMistakes", resultForGraphMixedMistakes['Z'], NUMBER_OF_STRINGS, NUMBER_OF_STRINGS_MAX,
               NUMBER_OF_TOTAL_MISTAKES_MIN, NUMBER_OF_TOTAL_MISTAKES_MAX, "Number of strings", "Mixed Mistakes",
               "Error Probability")

    if not PYTHON_GRAPH:
        subprocess.call([r"C:\\Programs\MATLAB\R2017b\bin\matlab.exe","-nodisplay", "-nosplash", "-nodesktop", "-r","\"run('"+MUSCLE_PATH + "MixedMistakes.m')\""])
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        x=1
    if PYTHON_GRAPH:
        num_of_mis=NUMBER_OF_TOTAL_MISTAKES_MAX + 1- NUMBER_OF_TOTAL_MISTAKES_MIN
        dz_mix= py_plot(NUMBER_OF_STRINGS_MAX, NUMBER_OF_STRINGS, num_of_mis, resultForGraphMixedMistakes,5, "Mixed-Mistakes")


if PYTHON_GRAPH:
    if FLIP_MOD: print "mean: " + format(mean(dz_flip),".4f")
    if DELETE_MOD: print "mean: "+format(mean(dz_del),".4f")
    if MIXED: print "mean: "+format(mean(dz_mix),".4f")
    print_before_and_after(binarySourceString, binaryAfterMajorityString) #only the last one, for debugging
    x = 1
    plt.show()
    x=1

