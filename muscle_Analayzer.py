#!/usr/bin/env python
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import random
import datetime
from matplotlib import cm
#python or matlab graph

#OPERETION MODS
PYTHON_GRAPH=True
GRAPH = False

FLIP_MOD=False
DELETE_MOD=True
MIXED=False

#count space as a mistake
COUNT_SPACE_MISS=False

#statistics
NUMBER_OF_STRINGS=20
# NUMBER_OF_STRINGS_MAX=10

NUMBER_OF_GOOD_STRINGS_FOR_FLIPS = 0
NUMBER_OF_GOOD_STRINGS_FOR_DELETIONS = 0
NUMBER_OF_GOOD_STRINGS_FOR_MIXED =0

NUMBER_OF_DELETIONS_IN_STR = 0
NUMBER_OF_DELETIONS_IN_STR_MAX=5
NUMBER_OF_FLIPS_IN_STR = 0
NUMBER_OF_FLIPS_IN_STR_MAX =5

NUMBER_OF_TOTAL_MISTAKES_MAX = 5
NUMBER_OF_TOTAL_MISTAKES_MIN = 0

STRING_GAP=20
DEL_GAP=1
FLIP_GAP=1
MIXED_GAP=1
RAPEAT_TIMES=10 #BORIS 25-10-18


#paths
MUSCLE_PATH ="/home/ubu/Yael/"#muscle3.8.31_i86linux64"   #Lab

FILES_PATH= "project/reasults/"#YAEL 18-10-18
AVG_RES_FILE="avg_muscle.txt"#YAEL 18-10-18

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


def buildArrays(binarySourceString, numberOfString, numOfGoodString=0,numberOfDeletionsInStr=0,numberOfFlipsInStr=0,numberOfStringsWithDeletions=None, MixedMistakesAddMoreFlips=0,MixedMistakesAddMoreDels=0):
    arr=[]
    #boris dont forget fix cheacking bugs
    for i in range(0,numberOfString):
        arr.append(binarySourceString)

    start_index = numOfGoodString
    end_index = numOfGoodString + numberOfStringsWithDeletions + MixedMistakesAddMoreDels
    arr = makeDeletionsInStr(arr,start_index,end_index, numberOfDeletionsInStr)

    start_index = numOfGoodString + numberOfStringsWithDeletions - MixedMistakesAddMoreFlips
    end_index = numberOfString
    arr = makeOfFlipsInStr(arr,start_index,end_index,numberOfFlipsInStr)

    return arr


def makeDeletionsInStr(arr, start_index,end_index,numberOfDeletionsInStr):
    for x in range(start_index, end_index):
        for j in range(numberOfDeletionsInStr):
            l=len(arr[x])
            i = random.randint(0, l-1)
            arr[x]=arr[x][:i]+arr[x][i+1:]
    return arr


def makeOfFlipsInStr(arr, start_index, end_index,numberOfFlipsInStr):
    for x in range(start_index ,end_index):
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




def graphit(title, tipe_name,resultForGraph,string_max,strings,mis_inStr_max, mis_inStr, indx):  #YAEL 18-10-18

    makeMATLAB(title, resultForGraph['Z'], NUMBER_OF_STRINGS, NUMBER_OF_STRINGS_MAX,
               NUMBER_OF_DELETIONS_IN_STR, NUMBER_OF_DELETIONS_IN_STR_MAX, "Number of strings", tipe_name+" in single string", "Error Probability")

    if not PYTHON_GRAPH and GRAPH:
        subprocess.call([r"C:\\Programs\MATLAB\R2017b\bin\matlab.exe", "-nodisplay", "-nosplash", "-nodesktop", "-r",
                         "\"run('" + MUSCLE_PATH + title+".m')\""])
        x = 1
    if PYTHON_GRAPH and GRAPH:
        num_of_mis = mis_inStr_max + 1 - mis_inStr
        py_plotAll(string_max, strings, num_of_mis, resultForGraph, indx, title,True)




def mucsleCall_and_analaize(arr,resultForGraph):   #YAEL 18-10-18
    arr2FASTA(arr, 1)  # put arr in "in.txt" file
    subprocess.call([r"/home/ubu/Yael/muscle3.8.31_i86linux64", "-in", MUSCLE_PATH + MUSCLE_IN_FILE, "-out", MUSCLE_PATH + MUSCLE_OUT_FILE])
    # subprocess.call([r"C:\\Users\moshab\Desktop\final project\muscle\muscle3.8.31_i86win32.exe", "-in", MUSCLE_PATH + MUSCLE_IN_FILE, "-out",MUSCLE_PATH + MUSCLE_OUT_FILE])
    fasta_file = open(MUSCLE_PATH + MUSCLE_OUT_FILE, 'r')  # read the output of mussle
    output_file = open(MUSCLE_PATH + 'mussle_norm_output.txt', 'w')
    fasta_res = FASTA2arr(fasta_file, output_file)
    output_file.close()
    fasta_file.close()
    binaryAfterMajorityString = calc_str_majority(fasta_res)
    resultForGraph = statisticsFromMuscle(binarySourceString, binaryAfterMajorityString,resultForGraph)
    return resultForGraph, binaryAfterMajorityString




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
    py_plotAll(NUMBER_OF_STRINGS_MAX, NUMBER_OF_STRINGS, num_of_mis, tempRes, strLen, "Del len:"+str(strLen), False,False,True)

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
avgRes=open(MUSCLE_PATH+FILES_PATH+AVG_RES_FILE,'w')
stat = open(MUSCLE_PATH + FILES_PATH + "statistics_MUSCLE.txt", 'w')

temp_end=0;
time_start=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
while(temp_end<len(binaryLongString)):
    #YAEL ------ loop statistics
    temp_end+=100
    binarySourceString=binaryLongString[:temp_end]

    NUMBER_OF_STRINGS = 20
    NUMBER_OF_STRINGS_MAX=len(binarySourceString)
    misMax=0.1*len(binarySourceString)
    NUMBER_OF_DELETIONS_IN_STR_MAX=int(misMax)
    NUMBER_OF_FLIPS_IN_STR_MAX =int(misMax)
    NUMBER_OF_TOTAL_MISTAKES_MAX =int(misMax)

    DEBUG = False #debug flags to all this program
    if DEBUG:
        counter=0

    if FLIP_MOD:
        numOfGoodString = NUMBER_OF_GOOD_STRINGS_FOR_FLIPS
        numberOfDeletionsInStr = NUMBER_OF_DELETIONS_IN_STR
        numberOfFlipsInStr = NUMBER_OF_FLIPS_IN_STR
        numberOfString = NUMBER_OF_STRINGS
        resultForGraphFlips={"X":[],"Y":[],"Z":[],"AVG":[]} #x=number of strings, y=number of filps, z=error precent, AVG = the AVG of z
        while numberOfFlipsInStr <=NUMBER_OF_FLIPS_IN_STR_MAX:
            resultForGraphFlips['Z'].append([])
            while numberOfString <= NUMBER_OF_STRINGS_MAX:
                numberOfStringsWithFlips = numberOfString - numOfGoodString
                numberOfStringsWithDeletions,MixedMistakesAddMoreFlips,MixedMistakesAddMoreDels = 0,0,0
                arr = buildArrays(binarySourceString, numberOfString, numOfGoodString, numberOfDeletionsInStr,numberOfFlipsInStr, numberOfStringsWithDeletions,MixedMistakesAddMoreFlips, MixedMistakesAddMoreDels)
                resultForGraphFlips,binaryAfterMajorityString= mucsleCall_and_analaize(arr, resultForGraphFlips)
                if len(resultForGraphFlips['Z'])==1: resultForGraphFlips['X'].append(numberOfString)
                numberOfString += STRING_GAP
            resultForGraphFlips['Y'].append(numberOfFlipsInStr)
            resultForGraphFlips['AVG'].append(mean(resultForGraphFlips['Z'][-1]))
            numberOfFlipsInStr+=FLIP_GAP
            numberOfString = NUMBER_OF_STRINGS

        graphit("FlipsGraph", "Flips", resultForGraphFlips, NUMBER_OF_STRINGS_MAX, NUMBER_OF_STRINGS, NUMBER_OF_FLIPS_IN_STR_MAX, NUMBER_OF_FLIPS_IN_STR, 1)
        dz_flip = flat_arr(resultForGraphFlips["Z"])
        avgRes.write(str(len(binarySourceString))+"\n")
        write_arr2File(avgRes,resultForGraphFlips['AVG'])

    elif DELETE_MOD:
        numOfGoodString = NUMBER_OF_GOOD_STRINGS_FOR_DELETIONS
        numberOfDeletionsInStr = NUMBER_OF_DELETIONS_IN_STR
        numberOfFlipsInStr = NUMBER_OF_FLIPS_IN_STR
        numberOfString = NUMBER_OF_STRINGS
        resultForGraphDeletions={"X":[],"Y":[],"Z":[],"AVG":[]} #x=number of strings, y=number of DELETIONSs, z=error precent, AVG = the AVG of z
        resultForGraphDeletionsTemp = {"X": [], "Y": [], "Z": [],"AVG": []}  # x=number of strings, y=number of DELETIONSs, z=error precent, AVG = the AVG of z

        while numberOfDeletionsInStr <= NUMBER_OF_DELETIONS_IN_STR_MAX:
            resultForGraphDeletions['Z'].append([])
            resultForGraphDeletionsTemp['Z'].append([])


            while numberOfString <= NUMBER_OF_STRINGS_MAX:
                for i in range(RAPEAT_TIMES):
                    numberOfStringsWithDeletions = numberOfString - numOfGoodString
                    numberOfStringsWithFlips, MixedMistakesAddMoreFlips, MixedMistakesAddMoreDels = 0,0,0
                    arr = buildArrays(binarySourceString, numberOfString+1, numOfGoodString, numberOfDeletionsInStr,numberOfDeletionsInStr, numberOfStringsWithDeletions,MixedMistakesAddMoreFlips, MixedMistakesAddMoreDels)

                    resultForGraphDeletionsTemp,binaryAfterMajorityString = mucsleCall_and_analaize(arr, resultForGraphDeletionsTemp)
                    if i==0:
                        resultForGraphDeletions['Z'][-1] = [x for x in resultForGraphDeletionsTemp['Z'][-1]]
                        # resultForGraphDeletions['Z'][-1][-1] = resultForGraphDeletionsTemp['Z'][-1][-1]
                    else:
                        # resultForGraphDeletions['Z'][-1][-1] = [a  + b for a, b in zip(resultForGraphDeletions['Z'][-1][-1], resultForGraphDeletionsTemp['Z'][-1][-1])]
                        resultForGraphDeletions['Z'][-1][-1] = resultForGraphDeletions['Z'][-1][-1] +resultForGraphDeletionsTemp['Z'][-1][-1]

                    resultForGraphDeletionsTemp['Z'][-1]
                # end for
                resultForGraphDeletions['Z'][-1] = [x/RAPEAT_TIMES for x in resultForGraphDeletions['Z'][-1]]
                if len(resultForGraphDeletions['Z'])==1: resultForGraphDeletions['X'].append(numberOfString)
                numberOfString += STRING_GAP
            # end while
            resultForGraphDeletions['Y'].append(numberOfDeletionsInStr)
            # resultForGraphDeletions['AVG'].append(mean(resultForGraphDeletions['Z'][-1]))
            numberOfDeletionsInStr += DEL_GAP
            numberOfString = NUMBER_OF_STRINGS
        # end while
        graphit("DeletionsGraph", "Deletions", resultForGraphDeletions, NUMBER_OF_STRINGS_MAX, NUMBER_OF_STRINGS, NUMBER_OF_DELETIONS_IN_STR_MAX, NUMBER_OF_DELETIONS_IN_STR, 3)
        dz_del = flat_arr(resultForGraphDeletions["Z"])
        avgRes.write(str(len(binarySourceString))+"\n")
        write_arr2File(avgRes,resultForGraphDeletions['AVG'])
        num_of_mis = NUMBER_OF_DELETIONS_IN_STR_MAX-NUMBER_OF_DELETIONS_IN_STR+1
        analayze_decoderStat(len(binarySourceString), resultForGraphDeletions, stat, num_of_mis)
    #THIS PART IS FOR FLIPS AND DELETIONS COMBINDED ANALYZIS
    elif MIXED:
        resultForGraphMixedMistakes = {"X":[],"Y": [], "Z": [],"AVG":[]}  # x=number of strings, y=number of MixedMistakes, z=error precent
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
                MixedMistakesAddMoreFlips =(int)(numberOfStringsWithDeletions/2)
                MixedMistakesAddMoreDels =  (int)(numberOfStringsWithFlips/2)
                arr = buildArrays(binarySourceString, numberOfString, numOfGoodString, numberOfDeletionsInStr,numberOfFlipsInStr, numberOfStringsWithDeletions, numberOfStringsWithFlips,MixedMistakesAddMoreFlips, MixedMistakesAddMoreDels)
                resultForGraphMixedMistakes,binaryAfterMajorityString= mucsleCall_and_analaize(arr, resultForGraphMixedMistakes)
                if len(resultForGraphMixedMistakes['Z'])==1: resultForGraphMixedMistakes['X'].append(numberOfString)
                numberOfString += STRING_GAP
                resultForGraphMixedMistakes['Y'].append(numberOfTotalMistakes)
            numberOfTotalMistakes += MIXED_GAP
            resultForGraphMixedMistakes['AVG'].append(mean(resultForGraphMixedMistakes['Z'][-1]))
            numberOfString = NUMBER_OF_STRINGS

        graphit("MixedMistakes", "Mixed-Mistakes", resultForGraphMixedMistakes, NUMBER_OF_STRINGS_MAX, NUMBER_OF_STRINGS, NUMBER_OF_TOTAL_MISTAKES_MAX, NUMBER_OF_TOTAL_MISTAKES_MIN, 5)
        dz_mix = flat_arr(resultForGraphMixedMistakes["Z"])
        avgRes.write(str(len(binarySourceString))+"\n")
        write_arr2File(avgRes,resultForGraphMixedMistakes['AVG'])


print_before_and_after(binarySourceString, binaryAfterMajorityString) #only the last one, for debugging
avgRes.close()
avgRes = open(MUSCLE_PATH + FILES_PATH + AVG_RES_FILE, 'r')
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
    stat.write(str(strLen_arr[-1]) + "\t\t       " + str(countStat) + "\t\t\t" + format((1.0 * countStat) / NUMBER_OF_DELETIONS_IN_STR_MAX, ".4f") + "\n")

num_of_mis = NUMBER_OF_DELETIONS_IN_STR_MAX - NUMBER_OF_DELETIONS_IN_STR + 1
stat.close(); avgRes.close();


if FLIP_MOD: print "mean: " + format(mean(dz_flip), ".4f")
if DELETE_MOD: print "mean: " + format(mean(dz_del), ".4f")
if MIXED: print "mean: " + format(mean(dz_mix), ".4f")
time_end=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
print "start: "+time_start
print "end: "+time_end

plt.show()
if PYTHON_GRAPH and GRAPH: plt.show()
