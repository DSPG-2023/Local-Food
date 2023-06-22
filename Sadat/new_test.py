import numpy as np
import matplotlib.pyplot as plt
import math

rnd = np.random
rnd.seed(15)

nc = 12 # number of counties
xc = {i:(rnd.rand(1)-.5)*100 for i in range(0,nc)}
yc = {i:(rnd.rand(1)-.5)*100 for i in range(0,nc)}

for i in range(0,nc):
    plt.scatter(float(xc[i]),float(yc[i]),c='r',marker='o')


A = [(i,j) for i in range(nc) for j in range(nc)]
c = {(i,j):np.hypot(xc[i]-xc[j],yc[i]-yc[j])[0] for i,j in A}

D = {i:np.around(rnd.rand(1)*1000,2)[0] for i in range(nc)}
S = {i:np.around(rnd.rand(1)*1200,2)[0] for i in range(nc)}

while(sum(S.values())<sum(D.values())):
    S = {i: np.around(rnd.rand(1) * 1200, 2)[0] for i in range(nc)}

from gurobipy import Model, GRB, quicksum

mdl = Model('LP')

x = mdl.addVars(A, vtype=GRB.CONTINUOUS)

mdl.modelSense = GRB.MINIMIZE

mdl.setObjective(quicksum(x[i,j]*c[i,j] for (i,j) in A))
mdl.addConstrs(quicksum(x[i,j] for i in range(nc)) >= D[j] for j in range(nc))
mdl.addConstrs(quicksum(x[i,j] for j in range(nc)) <= S[i] for i in range(nc))

mdl.write('LP.lp')
mdl.optimize()

active_arcs = [a for a in A if x[a].x > 0]

for i, j in active_arcs:
    if i !=j:
        plt.plot([xc[i][0], xc[j][0]], [yc[i][0], yc[j][0]], c='g', zorder=0)
        plt.arrow(xc[i][0], yc[i][0], 0.1*(xc[j][0]-xc[i][0]), 0.1*(yc[j][0]-yc[i][0]), width=0.4)
plt.show()

##

result = np.zeros([nc,nc])
for (i,j) in x.keys():
    result[i,j] = np.around(x[(i,j)].x,2)