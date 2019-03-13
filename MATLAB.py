#testNIV
import DEFINES
import subprocess


def makeMATLAB(fileName,listList,minX,maxX, minY,maxY,xlabel,ylabel,zlabel):
    # this code make anylezation of the muscle tool using MATLAB
    #https://stackoverflow.com/questions/6657005/matlab-running-an-m-file-from-command-line
    f=open(DEFINES.MUSCLE_PATH + fileName + ".m", 'w')
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


def run_MATLAB(title):
    subprocess.call([r"C:\\Programs\MATLAB\R2017b\bin\matlab.exe", "-nodisplay", "-nosplash", "-nodesktop", "-r","\"run('" + DEFINES.MUSCLE_PATH + title + ".m')\""])


