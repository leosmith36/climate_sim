
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def findPoints(e,type,l,lat):
    S = 1367.6
    R = 2.912
    sig = 5.67e-8

    def s(x):
        if lat == "on":
            return 1.241 - 0.723*x**2
        else:
            return 1.0

    def a(x):
        return 0.5 - 0.2*np.tanh((x-265)/10)

    def da(x):
        return -0.02*(np.cosh((x-265)/10))**(-2)

    def findIntersection(f1,f2,x0):
        return fsolve(lambda x : f1(x,l) - f2(x,type),x0)

    def fun1(x,l,*args):
        return (0.25*(1-a(x))*S*x**0)*s(l)

    def fun2(x,type,*args):
        if type == "Stefan-Boltzmann":
            return (e*sig*x**4)
        else:
            return (203.3 + 2.09*(x-273.15))

    def fun(x):
        return fun1(x,l) - fun2(x,type)

    def dleft(x):
        return 0.25*(-1*da(x))*S*s(l)

    def dright(x,type):
        if type == "Stefan-Boltzmann":
            return 4*e*sig*x**3
        else:
            return 2.09*x**0

    def dfun(x):
        return dleft(x) - dright(x,type)


    def removeDuplicates(array):
        newArray = []
        tol = 1.0
        dup = False
        for i in array:
            if math.isclose(fun1(i,l)-fun2(i,type),0.0,abs_tol=1.0) and i >= 0.0:
                if len(newArray) == 0:
                    newArray.append(i)
                else:
                    dup = False
                    for j in newArray:
                        ulim = j + tol
                        llim = j - tol
                        if i < ulim and i > llim:
                            dup = True
                    if dup == False:
                        newArray.append(i)
        return newArray

    def createVert(array):
        newArray = []
        for i in array:
            newArray.append(fun2(i,type))
        return newArray



    def classifyPoints(array):
        s_pointsx = []
        u_pointsx = []
        s_pointsy = []
        u_pointsy = []
        ssi_pointsx = []
        ssi_pointsy = []
        ssd_pointsx = []
        ssd_pointsy = []
        text = "Equilibrium temperatures: \n"
        for i in array:
            bvr = str
            sign = dfun(i)
            left = fun(i-1)
            right = fun(i+1)
            if left > 0 and right > 0:
                bvr = "semi-stable (increasing)"
                ssi_pointsx.append(i)
                ssi_pointsy.append(fun1(i,l))
            elif left < 0 and right < 0:
                bvr = "semi-stable (decreasing)"
                ssd_pointsx.append(i)
                ssd_pointsy.append(fun1(i,l))
            elif sign > 0:
                bvr = "unstable"
                u_pointsx.append(i)
                u_pointsy.append(fun1(i,l))
            elif sign < 0:
                bvr = "stable"
                s_pointsx.append(i)
                s_pointsy.append(fun1(i,l))
            else:
                bvr = "unable to classify"
            tempK = round(i,1)
            tempC = round(i - 273.15,1)
            text += str(tempK) + " (" + str(tempC) + " \u00B0C), " + bvr + "\n"
        #print(text)
        return (s_pointsx,s_pointsy,u_pointsx,u_pointsy,text,ssi_pointsx,
                ssi_pointsy,ssd_pointsx,ssd_pointsy)


    range = np.arange(0.0,500.0,0.1)

    result = []
    for i in range:
        result.append(findIntersection(fun1,fun2,i)[0])

    resultx = removeDuplicates(result)
    resulty = createVert(resultx)

    x = np.linspace(200.0,350.0,100)

    cpoints = classifyPoints(resultx)

    fig,ax = plt.subplots()
    e_in, = ax.plot(x,fun1(x,l),'--y')
    e_out, = ax.plot(x,fun2(x,type),'c')
    stab = ax.scatter(cpoints[0],cpoints[1],marker="o",c="green")
    unstab = ax.scatter(cpoints[2],cpoints[3],marker="s",c="red")
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Rate of Change (K/year)")
    ax.set_title("Critical Temperatures")
    ax.legend(handles=[e_in,e_out,stab,unstab],
               labels=["Energy In","Energy Out","Stable","Unstable"])
    #plt.show()
    return (x,fun1(x,l),fun2(x,type),cpoints)



