import numpy as np
from matplotlib import pyplot as plt

altitude_params = [
    # alt   g       press   density
    [0000, 9.807, 10.13, 1.225],
    [1000, 9.804, 8.988, 1.112],
    [2000, 9.801, 7.950, 1.007],
    [3000, 9.797, 7.012, 0.909],
    [4000, 9.794, 6.166, 0.819],
    [5000, 9.791, 5.405, 0.736],
    [6000, 9.788, 4.722, 0.660],
    [7000, 9.785, 4.111, 0.590],
    [8000, 9.782, 3.565, 0.526],
    [9000, 9.779, 3.080, 0.467],
    [10000, 9.776, 2.650, 0.413],
    [15000, 9.761, 1.211, 0.194],
    [20000, 9.745, 0.553, 0.089],
    [25000, 9.730, 0.255, 0.040],
    [30000, 9.715, 0.120, 0.018],
    [40000, 9.684, 0.029, 0.004],
    [50000, 9.654, 0.008, 0.001],
    [60000, 9.624, 0.002, 0.000],
    [70000, 9.594, 0.000, 0.000],
    [80000, 9.564, 0.000, 0.000],
]


class AltParams:
    altitude = 0
    g = 9.8
    pressure = 10.13
    density = 1.225

    def __init__(self, a, g, p, d) -> None:
        self.altitude = a
        self.g = g
        self.pressure = p
        self.density = d

    def __str__(self):
        return f"Altitude: {self.altitude}, g: {self.g}, Pressure: {self.pressure}, Density: {self.density}"


def get_parameters(params_list, arr):
    for i in arr:
        for j in range(4):
            params_list[j].append(i[j])


def alt_grav(alt):
    return alt * (-3.00000000e-06) + 9.804


def alt_pressure(alt):
    return pressure[0] * np.exp(-0.00014786 * (alt))


def alt_density(alt):
    return dens[0] * np.exp(-1.00653010e-04 * (alt))


def alt_data(arr):
    return arr[0] * (-3.00000000e-06) + 9.804, pressure[0] * np.exp(-0.00014786 * (arr[0])), \
           dens[0] * np.exp(-1.00653010e-04 * (arr[0]))


alt, g, pressure, dens = [], [], [], []
params_list = (alt, g, pressure, dens)
get_parameters(params_list, altitude_params)

g = params_list[1]
pressure = params_list[2]
density = params_list[3]

altitude = 0
thrust = 37770000
thrustV = 39600000
startingMass = 2900000
fuelMass = 2077000
mass = startingMass
burnTime = 177
time = 0
startTime = 9
velocity = 0
timeStep = 0.1
acceleration = 0
altitudeData = []
altitudeData_air = []
altitudeData_press = []
altitudeData_grav = []
altitudeData_all = []
altitudeData_vac = []
grav = 9.8

fuelConsumption = (fuelMass / burnTime) * timeStep

while time < burnTime:
    if time > startTime:
        altitude += velocity * timeStep
        velocity += acceleration * timeStep
    mass -= fuelConsumption
    acceleration = thrustV / mass - grav
    time += timeStep
    altitudeData.append(altitude)

velocity = 0
time = 0
mass = startingMass
acceleration = 0
altitude = 0

while time < burnTime:
    if time > startTime:
        altitude += velocity * timeStep
        velocity += acceleration * timeStep
    mass -= fuelConsumption
    acceleration = -alt_grav(altitude) + thrustV / mass - alt_density(altitude) * 55 * velocity ** 2 / (2 * mass)\
                   - velocity * (fuelMass / burnTime) / mass
    time += timeStep
    altitudeData_vac.append(altitude)

velocity = 0
time = 0
mass = startingMass
acceleration = 0
altitude = 0

while time < burnTime:
    if time > startTime:
        altitude += velocity * timeStep
        velocity += acceleration * timeStep
    mass -= fuelConsumption
    acceleration = -alt_grav(altitude) + (thrust - thrustV) / (10.13 * mass) * alt_pressure(
        altitude) + thrustV / mass - velocity * (fuelMass / burnTime) / mass
    time += timeStep
    altitudeData_air.append(altitude)

velocity = 0
time = 0
mass = startingMass
acceleration = 0
altitude = 0

while time < burnTime:
    if time > startTime:
        altitude += velocity * timeStep
        velocity += acceleration * timeStep
    mass -= fuelConsumption
    acceleration = -alt_grav(altitude) + (thrust - thrustV) / (10.13 * mass) * alt_pressure(
        altitude) + thrustV / mass - alt_density(altitude) * 55 * velocity ** 2 / (2 * mass) - velocity * (
                           fuelMass / burnTime) / mass
    time += timeStep
    altitudeData_all.append(altitude)


plt.plot(np.arange(0, burnTime + timeStep, timeStep), altitudeData_all, label="Real")
plt.plot(np.arange(0, burnTime + timeStep, timeStep), altitudeData, linestyle='dashed', label="Model")
plt.plot(np.arange(0, burnTime + timeStep, timeStep), altitudeData_air, linestyle='-.', label="No air res")
plt.plot(np.arange(0, burnTime + timeStep, timeStep), altitudeData_vac, linestyle=':', label="Vacuum")

plt.ylabel('Altitude')
plt.xlabel('Time')
plt.legend()
plt.show()
