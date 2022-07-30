from tkinter import *
from tkinter import ttk
import ClimatePoints as points
import ClimateModel as model
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
											   NavigationToolbar2Tk)
import numpy as np
import math

window = Tk()
window.title("Climate Simulation")
window.state("zoomed")

main = ttk.Frame(window,padding="5 5 5 5")
main.grid(column=0,row=0,sticky=(N,W,E,S))

main2 = ttk.Frame(window,padding="5 5 5 5")
main2.grid(column=1,row=0,sticky=(N,W,E,S))

main3 = ttk.Frame(window,padding="5 5 5 5")
main3.grid(column=2,row=0,sticky=(N,W,E,S))

ge_const = StringVar(value = 0.616)
temp = StringVar(value=287.7)
dge_const = StringVar(value=-0.001)
#dge_const2 = StringVar(value = 0.0)
emission_type = StringVar()
mod_type = StringVar()
latitude = StringVar(value=0.0)
lat_state = StringVar(value="off")
real_type = StringVar()
time = StringVar(value = 50.0)

ge_entry = ttk.Entry(main,width=7,textvariable=ge_const)
ge_entry.grid(column=1,row=0,sticky=(N,W,E,S),padx="5",pady="5")

ge_text = ttk.Label(main,text="Emissivity, \u03F5")
ge_text.grid(column=0,row=0,sticky=E,padx="5",pady="5")

ge_change = ttk.Entry(main,width=7,textvariable=dge_const)
ge_change.grid(column=1,row=3,sticky=(N,W,E,S),padx="5",pady="5")

change_text = ttk.Label(main,text="")
change_text.grid(column=0,row=3,sticky=E,padx="5",pady="5")

#ge_change2 = ttk.Entry(main,width=7,textvariable=dge_const2)
#ge_change2.grid(column=1,row=4,sticky=(N,W,E,S),padx="5",pady="5")

temp_entry = ttk.Entry(main,width=7,textvariable=temp)
temp_entry.grid(column=1,row=1,sticky=(N,W,E,S),padx="5",pady="5")

temp_text = ttk.Label(main,text="Initial Temperature (K)")
temp_text.grid(column=0,row=1,sticky=E,padx="5",pady="5")

points_text = ttk.Label(main3,text = "")
points_text.grid(column=1,row=1,sticky=(W,N),padx="5",pady="5")

num_label = ttk.Label(main2,text = "Numerical Solution")
num_label.grid(column=0,row=0,padx="1",pady="1")

pts_label = ttk.Label(main3,text = "Equilibrium Temperatures")
pts_label.grid(column=0,row=0,padx="1",pady="1")

equation_label = ttk.Label(main,text="")
equation_label.grid(column=0,row=5,sticky=E,padx="5",pady="5")

type_label = ttk.Label(main,text="Model Type")
type_label.grid(column=0,row=7,sticky=E,padx="5",pady="5")

lat_entry = ttk.Entry(main,width=7,textvariable=latitude)
lat_entry.grid(column=1,row=8,sticky=(N,W,E,S),padx="5",pady="5")

lat_label = ttk.Label(main,text = "Latitude (\u00B0)")
lat_label.grid(column=0,row=8,sticky=E,padx="5",pady="5")

time_entry = ttk.Entry(main,width=7,textvariable=time)
time_entry.grid(column=1,row=2,sticky=(N,W,E,S),padx="5",pady="5")

time_label = ttk.Label(main,text="Number of Years")
time_label.grid(column=0,row=2,sticky=E,padx="5",pady="5")

real_label = ttk.Label(main,text="Emissions Projection")
real_label.grid(column=0,row=10,sticky=E,padx="5",pady="5")

result_label = ttk.Label(main3,text = "")
result_label.grid(column=1,row=1,sticky=W,padx="5",pady="5")

def lat_change(*args):
	if str(lat_state.get()) == "on":
		lat_entry.configure(state="enabled")
		latitude.set(value=0.0)
	else:
		latitude.set(value=0.0)
		lat_entry.configure(state="disabled")

lat_change()

lat_check = ttk.Checkbutton(main,text = "Latitude Dependence",
							 variable=lat_state,command=lat_change,
							 onvalue="on",offvalue="off")
lat_check.grid(column=1,row=9,sticky=(N,W,E,S),padx="5",pady="5")

def change_label(*args):
	scen = str(emission_type.get())
	if scen == "Constant":
		dge_const.set(value=0.0)
		ge_change.configure(state = "disabled")
		change_text.configure(text = "")
		equation_label.configure(text="\u03F5(t) = \u03F5\u2080")
	elif scen == "Linear":
		ge_change.configure(state = "enabled")
		change_text.configure(text = "C (\u0394\u03F5, per year)")
		equation_label.configure(text="\u03F5(t) = C*t + \u03F5\u2080")
	elif scen == "Logarithmic":
		ge_change.configure(state = "enabled")
		change_text.configure(text = "C (scale)")
		equation_label.configure(text="\u03F5(t) = C*ln(t - 1) + \u03F5\u2080")
	elif scen == "Exponential":
		ge_change.configure(state = "enabled")
		change_text.configure(text = "C (rate)")
		equation_label.configure(text="\u03F5(t) = \u03F5\u2080*exp(C*t)")

def set_real(conc):
	chng = (-0.008/140.0)
	chng2 = (conc-481.0)/85
	dghg = round(chng*chng2,10)
	return dghg

def change_real(*args):
	real = str(real_type.get())
	if real == "Custom":
		scenario.configure(state="enabled")
		time_entry.configure(state="enabled")
		ge_entry.configure(state="enabled")
		ge_change.configure(state="enabled")
	elif real == "No Action":
		emission_type.set(value="Linear")
		change_label()
		scenario.configure(state="disabled")
		ge_entry.configure(state="disabled")
		ge_change.configure(state="disabled")
		time_entry.configure(state="disabled")
		ge_const.set(value = 0.616)
		dge_const.set(value = set_real(1060.0))
		time.set(value=85.0)
	elif real == "Current Pledges":
		emission_type.set(value="Linear")
		change_label()
		scenario.configure(state="disabled")
		ge_entry.configure(state="disabled")
		ge_change.configure(state="disabled")
		time_entry.configure(state="disabled")
		ge_const.set(value = 0.616)
		dge_const.set(value = set_real(855.0))
		time.set(value=85.0)
	elif real == "2\u00B0C Pathway":
		emission_type.set(value="Linear")
		change_label()
		scenario.configure(state="disabled")
		ge_entry.configure(state="disabled")
		ge_change.configure(state="disabled")
		time_entry.configure(state="disabled")
		ge_const.set(value = 0.616)
		dge_const.set(value = set_real(485.0))
		time.set(value=85.0)
	

scenarios = ["Constant","Linear","Logarithmic","Exponential"]
scenario = ttk.OptionMenu(main,emission_type,scenarios[0],
							*scenarios,command=change_label)
scenario.grid(column=1,row=5,sticky=(N,W,E,S),padx="5",pady="5")

mod_types = ["Stefan-Boltzmann","North-Coakley"]
mod_menu = ttk.OptionMenu(main,mod_type,mod_types[0],*mod_types)
mod_menu.grid(column=1,row=7,sticky=(N,W,E,S),padx="5",pady="5")

real_types = ["Custom","No Action","Current Pledges","2\u00B0C Pathway"]
real_menu = ttk.OptionMenu(main,real_type,real_types[0],*real_types,command=change_real)
real_menu.grid(column=1,row=10,sticky=(N,W,E,S),padx="5",pady="5")

def run(*args):
	ghg = float(ge_const.get())
	if ghg <= 1 and ghg >= 0:
		lat_on = str(lat_state.get())
		mod_type1 = str(mod_type.get())
		lat = math.sin((float(latitude.get())*math.pi)/180)
		pts = points.findPoints(ghg,mod_type1,lat,lat_on)
		x = pts[0]
		f1 = pts[1]
		f2 = pts[2]
		cpoints = pts[3]
		pts_text = cpoints[4]
		gr.clear()
		plot1 = gr.add_subplot(111)
		plot1.set_xlabel("Temperature (K)")
		plot1.set_ylabel("Energy (W)")
		plot1.set_title("Critical Temperatures")
		e_in, = plot1.plot(x,f1,'--y')
		e_out, = plot1.plot(x,f2,'c')
		stab = plot1.scatter(cpoints[0],cpoints[1],marker="o",c="green")
		unstab = plot1.scatter(cpoints[2],cpoints[3],marker="s",c="red")
		ssi = plot1.scatter(cpoints[5],cpoints[6],marker=">",c="blue")
		ssd = plot1.scatter(cpoints[7],cpoints[8],marker="<",c="blue")
		plot1.legend(handles=[e_in,e_out,stab,unstab,ssi,ssd],
					 labels=["Energy In","Energy Out","Stable","Unstable",
			  "Semi-Stable (inc.)","Semi-Stable (dec.)"],prop={'size' : 7})
		canvas.draw_idle()
		points_text.configure(text=pts_text)

		gr3.clear()
		plot3 = gr3.add_subplot(111)
		xrange = np.linspace(0,1,200)
		yrange = np.linspace(0,500,200)
		vert = np.full(200,ghg,dtype=float)
		x,y = np.meshgrid(xrange,yrange)
		if mod_type1 == "Stefan-Boltzmann":
			equation = 0.25*(1-a(y))*1367.6 - x*5.67e-8*y**4
		else:
			equation = 0.25*(1-a(y))*1367.6 - (203.3 + 2.09*(y-273.15))
		plot3.contour(x,y,equation,[0])
		plot3.set_ylabel("Temperature (K)")
		plot3.set_xlabel("Emissivity, \u03F5")
		plot3.set_title("Bifurcation Diagram")
		plot3.plot(vert,y)
		canvas3.draw_idle()


def run2(*args):
	mod_type1 = str(mod_type.get())
	lat = math.sin((float(latitude.get())*math.pi)/180)
	lat_on = str(lat_state.get())
	ghg = float(ge_const.get())
	dghg = float(dge_const.get())
	#dghg2 = float(dge_const2.get())
	t = float(temp.get())
	scen = str(emission_type.get())
	tim = float(time.get())
	if ghg <= 1 and ghg >= 0:
		mod = model.getModel(ghg,dghg,t,scen,mod_type1,lat,lat_on,tim)
		x = mod[0]
		y = mod[1]
		gr2.clear()
		plot2 = gr2.add_subplot(111)
		plot2.set_xlabel("Time (years)")
		plot2.set_ylabel("Temperature (K)")
		plot2.set_title("Temperature Projection",pad=15)
		mod_plot = plot2.plot(x,y,'-r')
		canvas2.draw_idle()

		time_range = mod[2]
		e_data = mod[3]
		gr4.clear()
		plot4 = gr4.add_subplot(111)
		plot4.set_ylabel("Emissivity, \u03F5")
		plot4.set_xlabel("Time (years)")
		plot4.set_title("Emissivity Trend")
		e_plot = plot4.plot(time_range,e_data)
		canvas4.draw_idle()

		final_T = str(round(mod[4],1))
		change_T = str(round(mod[4]-float(temp.get()),1))
		years = str(int(tim))
		result_label.configure(text="Temperature after "+years+" years: "+final_T+
						 "\u00B0C\nChange: "+change_T+"\u00B0C")


def run3(*args):
	run()
	run2()

def a(x):
	return 0.5 - 0.2*np.tanh((x-265)/10)

run_button = ttk.Button(main,command=run,text="Plot Right Graphs")
run_button.grid(column=1,row=11,sticky=(N,W,E,S),padx="5",pady="5")

run2_button = ttk.Button(main,command=run2,text="Plot Left Graphs")
run2_button.grid(column=1,row=12,sticky=(N,W,E,S),padx="5",pady="5")

run3_button = ttk.Button(main,command=run3,text="Plot All")
run3_button.grid(column=1,row=13,sticky=(N,W,E,S),padx="5",pady="5")

gr = Figure(figsize=(3.5,3),dpi=100, tight_layout=True)
canvas = FigureCanvasTkAgg(gr,main3)  
canvas.get_tk_widget().grid(column=0,row=1, 
	sticky=(N,S,E,W),padx="5",pady="5")
plot1 = gr.add_subplot(111)
plot1.plot()

gr2 = Figure(figsize=(3.5,3),dpi=100, tight_layout=True)
canvas2 = FigureCanvasTkAgg(gr2,main2)  
canvas2.get_tk_widget().grid(column=0,row=1, 
	sticky=(N,S,E,W),padx="5",pady="5")
plot2 = gr2.add_subplot(111)
plot2.plot()

gr3 = Figure(figsize=(3.5,3),dpi=100, tight_layout=True)
canvas3 = FigureCanvasTkAgg(gr3,main3)  
canvas3.get_tk_widget().grid(column=0,row=2, 
	sticky=(N,S,E,W),padx="5",pady="5")
plot3 = gr3.add_subplot(111)
plot3.plot()

gr4 = Figure(figsize=(3.5,3),dpi=100, tight_layout=True)
canvas4 = FigureCanvasTkAgg(gr4,main2)  
canvas4.get_tk_widget().grid(column=0,row=2, 
	sticky=(N,S,E,W),padx="5",pady="5")
plot4 = gr4.add_subplot(111)
plot4.plot()


def close():
	window.destroy()
	sys.exit(0)

change_label()
window.protocol("WM_DELETE_WINDOW",close)
#photo = PhotoImage(file = "earth.png")
#window.iconphoto(False,photo)
window.mainloop()