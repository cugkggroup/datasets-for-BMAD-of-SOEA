from numpy import *
import math
import time
import random

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

print scope