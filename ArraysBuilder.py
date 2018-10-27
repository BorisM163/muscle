import random

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