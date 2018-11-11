import random

#this function build 2d-array with random number of deletions in each strings
def buildArraysRandomDeletions(binarySourceString, numberOfString, numOfGoodString=0,numberOfDeletionsInStr=0,numberOfFlipsInStr=0,numberOfStringsWithDeletions=None, MixedMistakesAddMoreFlips=0,MixedMistakesAddMoreDels=0):
    arr=[]
    #boris dont forget fix cheacking bugs
    for i in range(0,numberOfString):
        arr.append(binarySourceString)

    start_index = numOfGoodString
    end_index = numOfGoodString + numberOfStringsWithDeletions + MixedMistakesAddMoreDels
    for x in range(start_index, end_index):
        for j in range(random.randint(0,numberOfDeletionsInStr)):
            l=len(arr[x])
            i = random.randint(0, l-1)
            arr[x]=arr[x][:i]+arr[x][i+1:]

    start_index = numOfGoodString + numberOfStringsWithDeletions - MixedMistakesAddMoreFlips
    end_index = numberOfString
    arr = makeOfFlipsInStr(arr,start_index,end_index,numberOfFlipsInStr)
    return arr



#this function build the fight array (with the mistakes and the good string, forall modes)
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

#this function get a 2-dimentional array, and start+end rows to make random #numberOfDeletionsInStr del in each string
def makeDeletionsInStr(arr, start_index,end_index,numberOfDeletionsInStr):
    for x in range(start_index, end_index):
        for j in range(numberOfDeletionsInStr):
            l=len(arr[x])
            i = random.randint(0, l-1)
            arr[x]=arr[x][:i]+arr[x][i+1:]
    return arr

#this function get a 2-dimentional array, and start+end rows to make random #numberOfFlipsInStr flips in each string
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


