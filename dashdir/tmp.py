#%%
import calculations as calc

# initial parameter values
sig = 5.670373e-8  # Stefan Boltzmann constant [W m^-2 K^-4]
ins_p = 0.2  # Insulation factor (0...1)
em_p = 1  # Emmissivity of the Planet (optional)
rat = 1 / 4  # ratio of cross section versus surface area of the Planet
Albedo = {
    "none": 0.5,
    "w": 0.75,
    "b": 0.25,
}  # Albedo vector [uninhabitated Planet , White daisies, Black daisies]

## growth optimum Temp of the white daisies
T_opt = {"w": 22.5 + 273.15}  # in Kelvin
T_min = {"w": 273.15 + 5}  # no growth below this temperature
death = {"w": 0.3}  # death rate of White daisies (fraction)

# assume the same growth curve for Black daisies (change if needed)
T_opt["b"] = T_opt["w"]
T_min["b"] = T_min["w"]
death["b"] = death["w"]
minarea = 0.01  # minimum area as a fraction occupied by each species
Fsnom = 3668  # nominal Flux in W/m^2


# %%
gw = []
gb = []
# amount of intervals to plot
nt = 20

t0 = 0
t1 = 45
dT = (t1 - t0) / nt
tempv = [t0 + i * dT for i in range(nt)]

for t in tempv:
    gw.append(calc.DaisyGrowth(t + 273.15, "w", T_min, T_opt))
    gb.append(calc.DaisyGrowth(t + 273.15, "b", T_min, T_opt))
# %%
