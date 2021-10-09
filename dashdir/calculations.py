import numpy as np


def UpdateAlbedo(x, Albedo):
    # define a function which updates the planetary albedo of the state vector (last entry)
    # Note that the state vector x is assumed to be a python dictionary
    # weighted sum of different planet cover
    x["Ap"] = Albedo["none"] * x["Su"] + Albedo["w"] * x["Sw"] + Albedo["b"] * x["Sb"]
    return x


def UpdateTemp(x, F, rat, em_p, sig, ins_p, Albedo):
    # function to update the state vector for the planetary temperature

    # outward flux of a planet with the average albedo (assume Black body)
    Fp = F * (1 - x["Ap"]) * rat / em_p

    # invert Stefan Boltzmann's law
    x["Tp"] = np.sqrt(np.sqrt((Fp / sig)))

    # now do the same for the regions with white and black daisies
    Fw = F * (1 - Albedo["w"]) * rat / em_p
    x["Tw"] = np.sqrt(np.sqrt((ins_p * (Fw - Fp) + Fp) / sig))

    # now do the same for the regions with white and black daisies
    Fb = F * (1 - Albedo["b"]) * rat / em_p
    x["Tb"] = np.sqrt(np.sqrt((ins_p * (Fb - Fp) + Fp) / sig))
    return x


def DaisyGrowth(T, bwtype, T_min, T_opt):
    Gw = 1 - ((T - T_opt[bwtype]) / (T_min[bwtype] - T_opt[bwtype])) ** 2
    # set negative values to 0
    if Gw < 0:
        return 0
    else:
        return Gw


# function to update areas based on growth rate and death rate
def UpdateAreas(x, death, minarea, T_min, T_opt):

    for Stype in ["w", "b"]:
        grwth = DaisyGrowth(x["T" + Stype], Stype, T_min, T_opt)
        ArType = "S" + Stype
        Ds = x[ArType] * (grwth * x["Su"] - death[Stype])
        # the following code applies 2 checks
        # (1) keep the area to zero if it has been
        # articifically set to exactly zero
        if x[ArType] > 0:
            x[ArType] += Ds
            # (2) apply the minimum area if the area comes below the threshold
            if x[ArType] < minarea:
                x[ArType] = minarea

    # update barren area (that what is left)
    x["Su"] = 1 - x["Sw"] - x["Sb"]


def NextState(x, F, rat, em_p, sig, ins_p, Albedo, death, minarea, T_min, T_opt):
    # make a copy of the previous statevector to work on
    xnew = x.copy()
    UpdateTemp(xnew, F, rat, em_p, sig, ins_p, Albedo)
    UpdateAreas(xnew, death, minarea, T_min, T_opt)
    UpdateAlbedo(xnew, Albedo)
    return xnew
