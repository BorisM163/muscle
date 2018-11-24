import DEFINES
import subprocess


def makeMATLAB(fileName,listList,minX,maxX, minY,maxY,xlabel,ylabel,zlabel, gap):
    # type: (string, list, integer, integer, integer, integer, string, string, string, string) -> None
    """
        this function creates an mathlab file from the results collected via the muscle anylzer
        plots 4 bar graphs
    :param fileName: the name of the file would be saved in mathlab format
    :param listList:  the data base of the muscle result (Z axi)
    :param minX:  the min X axi value
    :param maxX: the max X axi value
    :param minY: the min Y axi value
    :param maxY: the min y axi value
    :param xlabel: xlabel
    :param ylabel: ylabel
    :param zlabel: zlabel
    :param gap: yael step in X axi
    """
    # this code make anylezation of the muscle tool using MATLAB
    #https://stackoverflow.com/questions/6657005/matlab-running-an-m-file-from-command-line
    f=open(DEFINES.MUSCLE_PATH + fileName + ".m", 'w')
    f.write("Z=[")
    for list in listList:
        f.write(str(list))
        f.write(";")
    f.write("];\n")
    f.write("figure\n")
    f.write("y=["+str(minY)+":"+str(maxY)+"];\n")
    f.write("h1=bar3(y, Z);\n")
    f.write("set(gca,'XTick',[1:1:"+str(maxX)+"],'XTickLabel',["+str(minX)+":"+gap+":"+str(maxX)+"],'fontsize',3);\n")
    f.write("axis tight\n")
    f.write("xlabel('"+xlabel+"');\n")
    f.write("ylabel('"+ylabel+"');\n")
    f.write("zlabel('error "+zlabel+"');\n")
    f.write("savefig('"+fileName+"_errorP_notFullX')\n")



    f.write("figure\n")
    f.write("ZZ = (1. - Z);\n")
    f.write("ZZ = ZZ. * 100;\n")
    f.write("ZZ(ZZ >= 95) = 100;\n")
    f.write("ZZ(ZZ < 95 & ZZ >= 90) = 50;\n")
    f.write("ZZ(ZZ < 90) = 0;\n")
    f.write("h2=bar3(y, ZZ);\n")
    f.write("set(gca,'XTick',[1:1:"+str(maxX)+"],'XTickLabel',["+str(minX)+":"+gap+":"+str(maxX)+"],'fontsize',3);\n")
    f.write("axis tight\n")
    f.write("xlabel('"+xlabel+"');\n")
    f.write("ylabel('"+ylabel+"');\n")
    f.write("zlabel('succs "+zlabel+"');\n")
    f.write("savefig('"+fileName+"_succsP_notFullX')\n")

    f.write("figure\n")
    f.write("O = zeros("+str(maxY+1)+","+str(maxX)+");\n")
    f.write("j = 0;\n")
    f.write("for i="+str(minX)+ ":" + gap + ":" + str(maxX) +"\n")
    f.write("   j = j + 1;\n")
    f.write("   O(:, i)=Z(:, j);\n")
    f.write("end\n")
    f.write("h3=bar3(y, O);\n")
    #f.write("set(gca,'XTick',[1:1:" + str(maxX) + "],'XTickLabel',[" + str(minX) + ":" + gap + ":" + str(maxX) + "],'fontsize',3);\n")
    f.write("axis tight\n")
    f.write("xlabel('" + xlabel + "');\n")
    f.write("ylabel('" + ylabel + "');\n")
    f.write("zlabel('error " + zlabel + "');\n")
    f.write("savefig('" + fileName + "_errorP_yesFullX')\n")

    f.write("figure\n")
    f.write("O = zeros("+str(maxY+1)+","+str(maxX)+");\n")
    f.write("j = 0;\n")
    f.write("for i="+str(minX)+ ":" + gap + ":" + str(maxX) +"\n")
    f.write("   j = j + 1;\n")
    f.write("   O(:, i)=ZZ(:, j);\n")
    f.write("end\n")
    f.write("h3=bar3(y, O);\n")
    #f.write("set(gca,'XTick',[1:1:" + str(maxX) + "],'XTickLabel',[" + str(minX) + ":" + gap + ":" + str(maxX) + "],'fontsize',3);\n")
    f.write("axis tight\n")
    f.write("xlabel('" + xlabel + "');\n")
    f.write("ylabel('" + ylabel + "');\n")
    f.write("zlabel('succs" + zlabel + "');\n")
    f.write("savefig('" + fileName + "_succsP_yesFullX')\n")
    f.close()




def run_MATLAB(title):
    subprocess.call([r"C:\\Programs\MATLAB\R2017b\bin\matlab.exe", "-nodisplay", "-nosplash", "-nodesktop", "-r","\"run('" + DEFINES.MUSCLE_PATH + title + ".m')\""])


