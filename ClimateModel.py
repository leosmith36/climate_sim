
import math
import numpy as np
import matplotlib.pyplot as plt

def getModel(e,de,T0,scen,typ,l,lat,tim):

    S = 1367.6
    R = 2.912
    sig = 5.67e-8
    nl0 = math.sin((54.4*math.pi)/180.0)

    def s(x):
        if lat == "on":
            return 1.241 - 0.723*x**2
        else:
            return 1.0

    #def nu(T,t):
    #    return t*g(t)*(T-285)+math.sin((55*math.pi)/180)

    def nlf(T,t):
        return g(t)*(T-263.15)

    def g(t):
        if scen == "Constant":
            return e*t**0
        elif scen == "Linear":
            return de*t + e
        elif scen == "Logarithmic":
            return de*np.log(t+1.0) + e
        elif scen == "Exponential":
            return e*np.exp(de*t)

    def a(x,l,nl):
        if lat == "on":
            if l < nl:
                return 0.32
            elif l > nl:
                return 0.62
            else:
                return 0.5*(0.32+0.62)
        else:
            return 0.5 - 0.2*np.tanh((x-265)/10)

    def f(x,t,typ,l,nl):
        if typ == "Stefan-Boltzmann":
            return (s(l)*0.25*(1-a(x,l,nl))*S*x**0 - g(t)*sig*x**4)/R
        else:
            return (s(l)*0.25*(1-a(x,l,nl))*S*x**0 - (203.3 + 2.09*(x-273.15)))/R

    h = 0.1
    
    time = tim


    def rk4(h,T0,time,nl0):
        n = int(time/h)
        T = T0
        T_data = np.array([T0])
        t_data = np.arange(0,time,h)
        nl_data = np.array([nl0])
        nl = nl0

        for i in range(n-1):
            t = i * h
            if lat == "on":
                nk1 = nlf(T,t)
                k1 = f(T,t,typ,l,nl)

                nk2 = nlf(T+(0.5*h*k1),t+0.5*h)
                k2 = f(T+(0.5*h*k1),t+0.5*h,typ,l,nl+(0.5*h*nk1))

                nk3 = nlf(T+(0.5*h*k2),t+0.5*h)
                k3 = f(T+(0.5*h*k2),t+0.5*h,typ,l,nl+(0.5*h*nk2))

                nk4 = nlf(T+h*k3,t+h)
                k4 = f(T+h*k3,t+h,typ,l,nl+h*nk3)

                T += (h/6)*(k1+2*k2+2*k3+k4)
                T_data = np.append(T_data,[T])
                nl += (h/6)*(nk1+2*nk2+2*nk3+nk4)
                if nl > 1:
                    nl = 1
                elif nl < 0:
                    nl = 0
                nl_data = np.append(nl_data,[nl])

            else:
                
                k1 = f(T,t,typ,l,nl)
                k2 = f(T+(0.5*h*k1),t+0.5*h,typ,l,nl)
                k3 = f(T+(0.5*h*k2),t+0.5*h,typ,l,nl)
                k4 = f(T+h*k3,t+h,typ,l,nl)
                T += (h/6)*(k1+2*k2+2*k3+k4)
                T_data = np.append(T_data,[T])

        time_range = np.arange(0,time,h)
        e_data = g(time_range)
        return (t_data,T_data,time_range,e_data,T)

    data = rk4(h,T0,time,nl0)

    fig,ax = plt.subplots()
    ax.plot(data[0],data[1],'-r')
    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Temperature (K)")
    ax.set_title("Global Average Surface Temperature Projection")
    #plt.show()

    return data
