##
import numpy as np
import matplotlib.pyplot as plt
import math

rnd = np.random
rnd.seed(15)
##
import pandas as pd

data = pd.read_csv('Subset_data.csv')

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

#F-350 carrying 7,640 lbs carrying with mileage of 15 miles/gallon, and per gallon cost $3.5
c_conv = 3.5/15/(7640/2204.62)



##

from gurobipy import Model, GRB, quicksum

single_farmer_profit = list()

for single_farmer in single:

    mdl = Model()

    x = mdl.addVars(couple, vtype=GRB.CONTINUOUS)
    R = mdl.addVars(single, vtype=GRB.CONTINUOUS)

    mdl.modelSense = GRB.MAXIMIZE

    mdl.setObjective(quicksum(P_conv*P[j]*x[single_farmer,j] for j in single) - quicksum(c_conv*x[single_farmer,j]*c[single_farmer,j] for j in single))

    mdl.addConstrs(quicksum(x[i,j] for i in range(nc)) == R[j] for j in range(nc))
    mdl.addConstrs(quicksum(x[i,j] for j in range(nc)) <= S[i] for i in range(nc))
    mdl.addConstrs(R[j]  <= D[j] for j in range(nc))

    mdl.optimize()

    single_farmer_profit.append(mdl.objval)

##
from gurobipy import Model, GRB, quicksum

mdl = Model('LP')

x = mdl.addVars(couple, vtype=GRB.CONTINUOUS)
R = mdl.addVars(single, vtype=GRB.CONTINUOUS)

mdl.modelSense = GRB.MAXIMIZE

mdl.setObjective(quicksum(P_conv*P[i]*R[i] for i in single) - quicksum(c_conv*x[i,j]*c[i,j] for (i,j) in couple))

mdl.addConstrs(quicksum(x[i,j] for i in range(nc)) == R[j] for j in range(nc))
mdl.addConstrs(quicksum(x[i,j] for j in range(nc)) <= S[i] for i in range(nc))
mdl.addConstrs(R[j] <= D[j] for j in range(nc))

mdl.optimize()

combined_farmer_profit = list()

for single_farmer in single:
    combined_farmer_profit.append(sum(P_conv*P[i]*(x[single_farmer,i].x) for i in single) - sum(c_conv*(x[single_farmer,j].x)*c[single_farmer,j] for j in single))

##

single_farmer_profit = np.array(single_farmer_profit)
combined_farmer_profit = np.array(combined_farmer_profit)

# Logical check
single_farmer_profit >= combined_farmer_profit

profit_retained = (combined_farmer_profit/single_farmer_profit)*100