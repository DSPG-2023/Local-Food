import numpy as np
import matplotlib.pyplot as plt
import math

rnd = np.random
rnd.seed(15)

nc = 6 # number of counties
yc = {i:(rnd.rand(1)-.5)*100 for i in range(0,nc)}
xc = {i:(rnd.rand(1)-.5)*100 for i in range(0,nc)}

for i in range(0,nc):
    plt.scatter(float(xc[i]),float(yc[i]),c='r',marker='o')
    plt.annotate(i, (float(xc[i]-2.5),float(yc[i]-2.5)))


couple = [(i,j) for i in range(nc) for j in range(nc)]
single = [i for i in range(nc)]

c = {(i,j):np.hypot(xc[i]-xc[j],yc[i]-yc[j])[0] for i,j in couple}

D = {i:np.around(rnd.rand(1)*1000,2)[0] for i in range(nc)}
S = {i:np.around(rnd.rand(1)*1000,2)[0] for i in range(nc)}
P = {i:100+np.around(rnd.rand(1)*100,2)[0] for i in range(nc)}


from gurobipy import Model, GRB, quicksum

mdl = Model('LP')

x = mdl.addVars(couple, vtype=GRB.CONTINUOUS)
R = mdl.addVars(single, vtype=GRB.CONTINUOUS)

mdl.modelSense = GRB.MAXIMIZE

mdl.setObjective(quicksum(P[i]*R[i] for i in single) - quicksum(x[i,j]*c[i,j] for (i,j) in couple))

mdl.addConstrs(quicksum(x[i,j] for i in range(nc)) == R[j] for j in range(nc))
mdl.addConstrs(quicksum(x[i,j] for j in range(nc)) <= S[i] for i in range(nc))
mdl.addConstrs(R[j]  <= D[j] for j in range(nc))

mdl.optimize()

active_arcs = [a for a in couple if x[a].x > 0]

for i, j in active_arcs:
    if i !=j:
        plt.plot([xc[i][0], xc[j][0]], [yc[i][0], yc[j][0]], c='g', zorder=0)
        plt.arrow(xc[i][0], yc[i][0], 0.1*(xc[j][0]-xc[i][0]), 0.1*(yc[j][0]-yc[i][0]), width=0.4)
plt.show()

##

result = np.zeros([nc,nc])
for (i,j) in x.keys():
    result[i,j] = np.around(x[(i,j)].x,2)

import pandas as pd
results = pd.DataFrame(result)
results.to_csv("results.csv")