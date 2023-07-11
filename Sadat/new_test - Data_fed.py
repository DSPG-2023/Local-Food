##
import numpy as np
import matplotlib.pyplot as plt
import math

rnd = np.random
rnd.seed(15)
##
import pandas as pd

data = pd.read_csv('Subset data.csv')

nc = len(data.index)
couple = [(i,j) for i in range(nc) for j in range(nc)]
single = [i for i in range(nc)]

yc = {i:data['Lattitude'][i] for i in range(0,nc)}
xc = {i:data['Longitude'][i] for i in range(0,nc)}

for i in range(0,nc):
    plt.scatter(float(xc[i]),float(yc[i]),c='r',marker='o')
    plt.annotate(data['County Name'][i], (float(xc[i]),float(yc[i])))
plt.show()

couple = [(i,j) for i in range(nc) for j in range(nc)]
single = [i for i in range(nc)]

lat_long_2_mile = 69

c = {(i,j):lat_long_2_mile*np.hypot(xc[i]-xc[j],yc[i]-yc[j]) for i,j in couple}

D = {i:data['Demand'][i] for i in range(0,nc)}
S = {i:data['Supply'][i] for i in range(0,nc)}
P = {i:data['Price'][i] for i in range(0,nc)}

P_conv = 2204.62

#10,000 lbs carrying volume, with mileage of 25miles/gallon, and per gallon cost $3.5
c_conv = 3.5/25/(10000/2204.62)



##
from gurobipy import Model, GRB, quicksum

mdl = Model('LP')

x = mdl.addVars(couple, vtype=GRB.CONTINUOUS)
R = mdl.addVars(single, vtype=GRB.CONTINUOUS)

mdl.modelSense = GRB.MAXIMIZE

mdl.setObjective(quicksum(P_conv*P[i]*R[i] for i in single) - quicksum(c_conv*x[i,j]*c[i,j] for (i,j) in couple))

mdl.addConstrs(quicksum(x[i,j] for i in range(nc)) == R[j] for j in range(nc))
mdl.addConstrs(quicksum(x[i,j] for j in range(nc)) <= S[i] for i in range(nc))
mdl.addConstrs(R[j]  <= D[j] for j in range(nc))


mdl.write('LP.lp')
mdl.optimize()

active_arcs = [a for a in couple if x[a].x > 0]

for i, j in active_arcs:
    if i !=j:
        plt.plot([xc[i], xc[j]], [yc[i], yc[j]], c='g', zorder=0)
        plt.arrow(xc[i], yc[i], 0.1*(xc[j]-xc[i]), 0.1*(yc[j]-yc[i]), width =0.01)
plt.show()

##

result = np.zeros([nc,nc])
power_bi_data = pd.DataFrame(columns=['From', 'To', 'Count', 'From Lat', 'From Long', 'To Lat', 'To Long'])

for (i,j) in x.keys():
    result[i,j] = np.around(x[(i,j)].x,2)
    if (result[i,j]!=0) and (i !=j) :
        new_row = {'From': data['County Name'][i] , 'To': data['County Name'][j], 'Count': result[i,j],
                   'From Lat': data['Lattitude'][i], 'From Long': data['Longitude'][i],
                   'To Lat': data['Lattitude'][j], 'To Long': data['Longitude'][j]}
        power_bi_data = power_bi_data._append(new_row, ignore_index=True)

results = pd.DataFrame(result)
results.to_csv("results.csv")

power_bi_data.to_csv("power_bi_data.csv", index=False)