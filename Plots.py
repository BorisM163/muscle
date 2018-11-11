import matplotlib.pyplot as plt
import numpy as np
import MATLAB
import DEFINES

def multiply_elemnt(arr,mul): #multiply each ellement by #mul times. 
    res=[]
    for x in arr:
        for i in range(mul):
            res.append(x)
    return res

def multiply_array(arr,mul): #cat the whole array to itself #mul times. (lenarray ---> mul*lenarray)
    res=[]
    for i in range(mul):
        res+=arr
    return res

def flat_arr(arr):
    res=[]
    for x in arr: res+=x
    return res

#plot mistakes graph- scatter\bars (can describe avg) 
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
    # print len(dx)
    # print len(dy)
    # print len(dz)
    # print len(xPos)
    # print len(yPos)
    # print len(zPos)
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
    dz = flat_arr(res["Z"])

    fig2 = plt.figure(g_ind+1)
    ax4 = fig2.add_subplot(111, projection='3d')
    ax4.scatter3D(xPos, yPos, dz, dz, cmap='Greens');
    ax4.set_xlabel('lines')
    ax4.set_ylabel(mis_name)
    ax4.set_zlabel('mistake - precent')
    ax4.set_title(mis_name)

def graphit(title, type_name, resultForGraph, max_strings, min_strings, mistkaes_inStr_max, mistkaes_inStr_min, indx):  #YAEL 18-10-18
    MATLAB.makeMATLAB(title, resultForGraph['Z'], min_strings, max_strings, mistkaes_inStr_min, mistkaes_inStr_max , "Number of strings", type_name+" in single string", "Error Probability")
    if not DEFINES.PYTHON_GRAPH and DEFINES.GRAPH_MID:
        MATLAB.run_MATLAB(title)
    if DEFINES.PYTHON_GRAPH and DEFINES.GRAPH_MID:
        num_of_mis = mistkaes_inStr_max + 1 - mistkaes_inStr_min
        py_plotAll(max_strings, min_strings, num_of_mis, resultForGraph, indx,False,False, title, True)
