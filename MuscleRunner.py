import DEFINES
import subprocess

def arr2FASTA(arr,form): #take an array and poot in fasta format
    #if form==1: it is DNA form.
    #if form==0 it is protain form
    fasta_file=open(DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_IN_FILE,'w')
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


#call muscle and decide about the final string (with majority algorithm), and the error rate
def muscleCall_and_Analyze(binarySourceString, arr):
    arr2FASTA(arr, 1)  # put arr in "in.txt" file
    subprocess.call([r"/home/ubu/Yael/muscle3.8.31_i86linux64", "-in", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_IN_FILE, "-out", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_OUT_FILE])
    #subprocess.call([r"C:\\Users\moshab\Desktop\final project\muscle\muscle3.8.31_i86win32.exe", "-in", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_IN_FILE, "-out", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_OUT_FILE])
    # subprocess.call([r"C:\Users\boris7\Desktop\final project\muscle\muscle3.8.31_i86win32.exe", "-in", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_IN_FILE, "-out", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_OUT_FILE])
   # subprocess.call([r"C:\Users\boris10\Desktop\projectCSE\muscle\muscle3.8.31_i86win32.exe", "-in", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_IN_FILE, "-out", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_OUT_FILE])

    fasta_file = open(DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_OUT_FILE, 'r')  # read the output of mussle
    output_file = open(DEFINES.MUSCLE_PATH + 'mussle_norm_output.txt', 'w')
    fasta_res = FASTA2arr(fasta_file, output_file)
    output_file.close()
    fasta_file.close()
    binaryAfterMajorityString = calc_str_majority(fasta_res)
    if DEFINES.OVERCOME_SPACE:
        errorRate = statisticsFromMuscle_GapSpace(binarySourceString, binaryAfterMajorityString)
    else:
        errorRate = statisticsFromMuscle(binarySourceString, binaryAfterMajorityString)

    return errorRate, binaryAfterMajorityString


#return the error preecent. #COUNT_SPACE_MISS=True -> calc "-" as an error
def statisticsFromMuscle(binarySourceString, binaryAfterMajorityString):
    counter = {"Flips": 0, "Space": 0}
    sourceLen =len(binarySourceString)
    AfterMajorityLen= (binaryAfterMajorityString)
    if AfterMajorityLen!=sourceLen:
        assert("binarySourceString and binaryAfterMajorityString are in diffrent sizes")
        print("binarySourceString and binaryAfterMajorityString are in diffrent sizes")
        #return
    for s,m in zip(binarySourceString,binaryAfterMajorityString):
        if s!=m:
            if m =='-':
                if DEFINES.COUNT_SPACE_MISS:
                    counter['Space']+=1
            else: counter['Flips']+=1
    return ((1.0*(counter['Space']+counter['Flips']))/sourceLen) # resultForGraph['Z'].append((counter['Space']+counter['Flips'])/strLen)


#return the error preecent. 
#this function supose to be smarter and caculate the possible error probebility
def statisticsFromMuscle_GapSpace(binarySourceString, binaryAfterMajorityString):
    counter = {"Flips": 0, "Space": 0}
    sourceLen =len(binarySourceString)
    AfterMajorityLen= (binaryAfterMajorityString)
    if AfterMajorityLen!=sourceLen:
        print("binarySourceString and binaryAfterMajorityString are in diffrent sizes")
    j=0; k=0;c=0;
    for i in range(len(binaryAfterMajorityString)):
        if j<(len(binarySourceString)-1) and k< (len(binaryAfterMajorityString)-1):
            if binaryAfterMajorityString[k]!=binarySourceString[j]:
                if binaryAfterMajorityString[k] =="-":
                    c+=1
                    if(flip_counter(binarySourceString[j:],(binaryAfterMajorityString[k+1:]))<flip_counter(binarySourceString[j:],binaryAfterMajorityString[k:])):
                          j-=1
                          k-=1
                          binaryAfterMajorityString=binaryAfterMajorityString[:k]+binaryAfterMajorityString[k+1:]
                          print "without: "+str(k)
                          print str(binarySourceString[j+1:(j+1 + 30)])
                          st = ''.join(binaryAfterMajorityString[k:(k + 30)])
                          print st
                    else:
                        print "good: " +str(k)
                        print str(binarySourceString[j:(j+30)])
                        st=''.join(binaryAfterMajorityString[k:(k+30)])
                        print st
                else:
                    counter['Flips']+=1
        j+=1; k+=1
    print "after stat - overcome space reasults:"
    st=''.join(binaryAfterMajorityString)
    print binarySourceString
    print st
    return ((1.0*(counter['Space']+counter['Flips']))/sourceLen) # resultForGraph['Z'].append((counter['Space']+counter['Flips'])/strLen)

#count only the flips between 2 string, until there is "-" (after some "0101...")
# this function is used in statisticsFromMuscle_GapSpace
def flip_counter(binarySourceString,binaryAfterMajorityString):
    flips=0; first=True
    for s,m in zip(binarySourceString,binaryAfterMajorityString):
        if m=="-":
            if not first: return flips
        else: first=False
        if (m=="0" and s=="1") or (s=="0" and m=="1"):
            flips+=1
    return flips


def calc_str_majority(arr):#calc the final out of the majority of the samples
    length=[]; res=[]; i=-1
    for line in arr: length.append(len(line))
    while(i<max(length)-1):
        count1=0; count0=0; i+=1; countSpace=0;
        for line in arr:
            if i<len(line):
                if line[i]=="1": count1+=1
                elif line[i]=="0": count0+=1
                elif line[i]=="-": countSpace+=1

        if countSpace>max(count0,count1):
            res.append("-")
            print str(countSpace) +" : "+str(i)+" (1: "+str(count1)+",0:"+str(count0)+")"
        elif count1> max(count0,countSpace): res.append("1")
        elif count0>= max(count1,countSpace): res.append("0")
    return res
