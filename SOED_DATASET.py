from numpy import *
from gurobipy import *
import math
import time
import random
############Design DataSet#####################
# normal distributions
def Platform_range(X,u,eta):
    r = 1 / sqrt(2 * pi * eta) * 1 / exp(-pow((X - u), 2) / (2 * pow(eta, 2)))
    return r

# Problem data
numGrids = 90
numPlatforms = 20
numStations = 10
numConflict = 0
m = numPlatforms
n = numGrids + numStations

# Add variables

weights = {}
d = {}  # the list number of sensors
c = {}  # the list number of sensors
powerPlatforms = {} #Total energy of the platform
powerStations = {} #Station carrying capacity
scope = {} # Observation capabilities of platforms

eta = 1
u = 0
q = 25.0
# Calculate Observation capabilities of platforms
for i in range(m):
    scope[i] = int(Platform_range(i / q, u, eta) * numGrids)
    powerPlatforms[i] = 3 * scope[i]
    powerStations[i] = 3 * scope[i]
distcen = 5;

f = open('data-20.txt', 'w') #清空文件内容再写
strstr = 'station:'
for i in range (numStations):
    sta[i] = 8*i
    strstr = strstr + str(sta[i]) + ','
f.write(strstr)
f.write('\n')
for i in range(m):
    f.writelines(['platform:',str(i), '  -->','\n']) #可写所有能迭代的类型，例如list
    f.write('grid:')
    for j in range(scope[i]):
        if (i*distcen + j) < n:
            f.writelines([str(i*distcen + j), ',']) #可写所有能迭代的类型，例如list
    f.write('\n')
f.close()

###the data of conflict###
##initialize all conflicting pairs##
conflict = [[0 for i in range(3)] for i in range (500)]
total_pair_sensor1 = [[0 for i in range(2)] for i in range (m * ( m - 1 ))]
total_pair_sensor = []
count1 = 0
for ii in range(50):
    for jj in range(ii + 1, 50):
        total_pair_sensor1[count1][0] = ii
        total_pair_sensor1[count1][1] = jj
        count1 = count1 + 1

total_number_conflicts = len(total_pair_sensor1)
#fliter#
for co in range (total_number_conflicts):
    if (total_pair_sensor1[co][1] * density - (total_pair_sensor1[co][0] * density + scope[total_pair_sensor1[co][0]]) > 0):
        continue
    else:
        total_pair_sensor.append(total_pair_sensor1[co])
count2 = 0
pair = [[0 for i in range(2)] for i in range (len(total_pair_sensor) * ( len(total_pair_sensor) - 1 ) )]

for ii in range(len(total_pair_sensor)):
     for jj in range(ii + 1, len(total_pair_sensor)):
         pair[count2][0] = ii
         pair[count2][1] = jj
         count2 = count2 + 1
for i in range(numConflict):
     s1 = random.randint(1, total_number_conflicts)
     while (total_pair_sensor[s1-1][1] * density - (total_pair_sensor[s1-1][0] * density + scope[total_pair_sensor[s1-1][0]]) > 0):
        s1 = random.randint(1, total_number_conflicts)
     start = total_pair_sensor[s1-1][1] * density
     end = total_pair_sensor[s1-1][0] * density + scope[total_pair_sensor[s1-1][0]]
     jj = start
     for ii in range( Total_count, end - start + Total_count ):
         conflict[ii][0] = jj
         conflict[ii][1] = total_pair_sensor[s1-1][0]
         conflict[ii][2] = total_pair_sensor[s1-1][1]
         f.writelines(['[',str(conflict[ii][1]),',',str(conflict[ii][2]),',',str(conflict[ii][0]),'] '])
         jj = jj + 1
     Total_count =  Total_count + end - start  
     f.write("\n\n")
f.close()

#############Constraint####################

#Degree Constraints
for i in range(m):
    M.addConstr(powerSum[i] >= quicksum(A[i, j + i * n] * a[i, j] * x[i, j] for j in range(n))
                + quicksum( A[i, j + i * n] * b1[i, j] * y[i, j] for j in range(n)))
for j in range(n):
    M.addConstr(powerStations[j] >= quicksum(B[j, j + i * n] * b2[i, j] * y[i, j] for i in range(m)))

for i in range(m):
    M.addConstr(quicksum(y[i, j] for j in range(n)) >= quicksum(x[i, j] for j in range(n)))
    
for j in range(n):
    M.addConstr(quicksum(x[i, j] for i in range(m)) >= 1)


# Continuity Constraint
for i in range(m):
    for j1 in range(n):
        for k in range(n):
            M.addConstr(quicksum(x[i, j] for j in range(n)) >=
                     (1-voidage)*(Num[j1]*x[i,j1]-Num[k]*x[i,k]))

# Constraint about Conflicts
M.addConstr(quicksum(c[j] for j in range(conflict_number)) <= 0)
for j in range(conflict_number):
     M.addConstr(
         1 - x[conflict[j][1], conflict[j][0]] - x[conflict[j][2], conflict[j][0]] + c[
             j] >= 0)
     M.addConstr(
         x[conflict[j][1], conflict[j][0]] + x[conflict[j][2], conflict[j][0]] - 2 * c[
             j] >= 0)
