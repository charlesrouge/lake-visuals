import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from numpy.polynomial import Polynomial as P
import numpy as np

# Define attractors
class lakeAttractorList:
    def __init__(self):
        self.Oligo = []  # oligotrophic attractors
        self.Unst = []  # unstable attractors
        self.Eutro = []  # eutrophic attractors
        self.first = np.zeros(3) # first input for which attractor type exists

# Polynomial for root search
def lakePoly(b, q, l):
    lp = np.zeros(q+2)
    lp[q+1] = -b
    lp[q] = l+1
    lp[1] = lp[1]-b
    lp[0] = l
    return lp

# Computing all lake attractors for all values of Ph input l
def lakeAttractors(b,q,lmax):
    eqList = lakeAttractorList()
    l = np.arange(0,lmax,0.001)
    for i in range(len(l)):
        lp = P(lakePoly(b,q,l[i]))
        r = lp.roots()
        rpr = [] # real, positive roots
        for j in range(len(r)):
            if r[j].imag==0 and r[j].real>=0:
                rpr.append(r[j].real) # root is real and positive
        rpr = sorted(rpr)
        if len(eqList.Eutro)==0 and len(rpr)>1:
            eqList.first[2] = l[i] # mark first point with eutrophic attractor
        if len(eqList.Unst)==0 and len(rpr)==3:
            eqList.first[1] = l[i] # mark first point with unstable attractor
        if len(rpr)==3:
            eqList.Oligo.append(rpr[0])
            eqList.Unst.append(rpr[1])
            eqList.Eutro.append(rpr[2])
        elif len(rpr)==1:
            if len(eqList.Unst) == 0:
                eqList.Oligo.append(rpr[0])
            else:
                eqList.Eutro.append(rpr[0])
        else:
            eqList.Oligo.append(rpr[0])
            eqList.Eutro.append(rpr[1])
    return eqList

# Plotting attractors for a set of parameters (building block for the 2 routines below)
def lakeAttBasic(b,q,lmax,dl,color):
    eqList = lakeAttractors(b, q, lmax)
    lakeAttBase(eqList,dl,color)
    return eqList

def lakeAttBase(eqList,dl,color):
    l1 = np.arange(eqList.first[0], eqList.first[0] + len(eqList.Oligo) * dl, dl)
    l2 = np.arange(eqList.first[1], eqList.first[1] + len(eqList.Unst) * dl - 1E-10, dl)
    l3 = np.arange(eqList.first[2], eqList.first[2] + len(eqList.Eutro) * dl - 1E-10, dl)
    plt.plot(l1, eqList.Oligo, color=color)
    plt.plot(l2, eqList.Unst, linestyle='--', color=color)
    plt.plot(l3, eqList.Eutro, color=color)
    return None

# Plot for attractors with a given set of parameters and input level
def lakeAttPlot(b,q,lmax,dl,show):
    plt.figure()
    unstable = mlines.Line2D([], [], color='k', linestyle='--', label='Unstable')
    stable = mlines.Line2D([], [], color='k', label='Stable')
    eqList = lakeAttBasic(b,q,lmax,dl,'k')
    l_end = min(lmax, len(eqList.Oligo) * dl + .25)
    plt.xlabel('Total average phosphorus input')
    plt.ylabel('Phosphorus concentration')
    axes=plt.gca()
    axes.set_xlim([0,l_end])
    if len(eqList.Eutro)>0:
        axes.set_ylim([0,np.max(eqList.Eutro[1:int(l_end/dl)])+.1])
    else:
        axes.set_ylim([0,np.max(eqList.Oligo[1:int(l_end/dl)])+.1])
    plt.title('Attractors for b='+str(b)+', q='+str(q))
    plt.legend(handles=[stable, unstable], loc=4)
    if show == 1:
        plt.show()
    return None

# Plot for attractors in a range. b, q and l are [min,max] vectors. q INTEGER
def lakeAttRange(b,q,l,lmax,dl,show):
    plt.figure()
    lakeAttBasic(b[0],q[0],lmax,dl,'c')
    lakeAttBasic(b[0],q[1],lmax,dl,'g')
    lakeAttBasic(b[1], q[0], lmax,dl,'b')
    lakeAttBasic(b[1], q[1], lmax,dl,'y')
    plt.plot(np.ones(11)*l[0],np.arange(0,5.1,.5),':k')
    plt.plot(np.ones(11) * l[1], np.arange(0, 5.1, .5), ':k')
    plt.xlabel('Total average phosphorus input L')
    plt.ylabel('Phosphorus concentration')
    axes = plt.gca()
    axes.set_xlim([0, lmax])
    axes.set_ylim([0, 4])
    plt.title(r'Attractors for b $\in$ [' + str(b[0]) + ',' + str(b[1]) + '], q $\in$ [' + str(q[0]) + ',' + str(q[1]) + ']',\
              usetex=True)
    cyan_l = mlines.Line2D([], [], color='c', label='b='+str(b[0])+', q='+str(q[0]))
    green_l = mlines.Line2D([], [], color='g', label='b='+str(b[0])+', q='+str(q[1]))
    blue_l = mlines.Line2D([], [], color='b', label='b='+str(b[1])+', q='+str(q[0]))
    yellow_l = mlines.Line2D([], [], color='y', label='b='+str(b[1])+', q='+str(q[1]))
    unstable = mlines.Line2D([], [], color='k', linestyle='--', label = 'Unstable')
    stable = mlines.Line2D([], [], color='k', label='Stable')
    l_range = mlines.Line2D([], [], color='r', linestyle=':', label = 'Range for L')
    plt.legend(handles=[l_range,stable, unstable, cyan_l, green_l, blue_l, \
                        yellow_l], loc=4)
    if show==1:
        plt.show()
    return None