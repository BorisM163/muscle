import DEFINES
import PATHS
import subprocess

def arr2FASTA(arr,form): #take an array and poot in fasta format
    #if form==1: it is DNA form.
    #if form==0 it is protain form
    fasta_file=open(PATHS.MUSCLE_PATH + PATHS.MUSCLE_IN_FILE,'w')
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



def muscleCall_and_Analyze(binarySourceString,arr):
    arr2FASTA(arr, 1)  # put arr in "in.txt" file
    #subprocess.call([r"/home/ubu/Yael/muscle3.8.31_i86linux64", "-in", PATHS.MUSCLE_PATH + PATHS.MUSCLE_IN_FILE, "-out", PATHS.MUSCLE_PATH + PATHS.MUSCLE_OUT_FILE])
    #subprocess.call([r"C:\\Users\moshab\Desktop\final project\muscle\muscle3.8.31_i86win32.exe", "-in", PATHS.MUSCLE_PATH + PATHS.MUSCLE_IN_FILE, "-out", PATHS.MUSCLE_PATH + PATHS.MUSCLE_OUT_FILE])
    subprocess.call([r"C:\Users\boris7\Desktop\final project\muscle\muscle3.8.31_i86win32.exe", "-in", PATHS.MUSCLE_PATH + PATHS.MUSCLE_IN_FILE, "-out", PATHS.MUSCLE_PATH + PATHS.MUSCLE_OUT_FILE])
   # subprocess.call([r"C:\Users\boris10\Desktop\projectCSE\muscle\muscle3.8.31_i86win32.exe", "-in", PATHS.MUSCLE_PATH + PATHS.MUSCLE_IN_FILE, "-out", PATHS.MUSCLE_PATH + PATHS.MUSCLE_OUT_FILE])

    fasta_file = open(PATHS.MUSCLE_PATH + PATHS.MUSCLE_OUT_FILE, 'r')  # read the output of mussle
    output_file = open(PATHS.MUSCLE_PATH + 'mussle_norm_output.txt', 'w')
    fasta_res = FASTA2arr(fasta_file, output_file)
    output_file.close()
    fasta_file.close()
    binaryAfterMajorityString = calc_str_majority(fasta_res)
    errorRate = statisticsFromMuscle(binarySourceString, binaryAfterMajorityString)
    return errorRate, binaryAfterMajorityString



def statisticsFromMuscle(binarySourceString, binaryAfterMajorityString):
    counter = {"Flips": 0, "Space": 0}
    sourceLen =len(binarySourceString)
    AfterMajorityLen= (binaryAfterMajorityString)
    if AfterMajorityLen!=sourceLen:
        assert("binarySourceString and binaryAfterMajorityString are in diffrent sizes")
    for s,m in zip(binarySourceString,binaryAfterMajorityString):
        if s!=m:
            if m =='-':
                if DEFINES.COUNT_SPACE_MISS:
                    counter['Space']+=1
            else: counter['Flips']+=1
    return ((1.0*(counter['Space']+counter['Flips']))/sourceLen) # resultForGraph['Z'].append((counter['Space']+counter['Flips'])/strLen)







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
