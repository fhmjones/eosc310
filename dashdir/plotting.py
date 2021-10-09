import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import calculations as calc

from plotly.subplots import make_subplots


def initialize_albedo_plot(T_min, T_opt):
    # how does the growth curve of the Daisies look like?
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

    albedo_plot = go.Figure()
    albedo_plot.add_hrect(
        xref="paper",
        yref="paper",
        x0=1,
        x1=1.5,
        y0=-15,
        y1=100,
        line_width=0,
        fillcolor="white",
        opacity=1,
    )
    albedo_plot.update_xaxes(showgrid=True, zeroline=False)
    albedo_plot.update_yaxes(showgrid=True, zeroline=False)
    albedo_plot.add_trace(go.Scatter(x=tempv, y=gw, name="gw"))
    albedo_plot.add_trace(go.Scatter(x=tempv, y=gb, name="gb"))
    albedo_plot.update_layout(xaxis_title="tempv", yaxis_title="growth")

    albedo_plot.update_layout(xaxis_title="Temp [degC]", yaxis_title="Ratio")
    albedo_plot.update_xaxes(range=[0, t1])
    albedo_plot.update_yaxes(range=[0, 1])
    albedo_plot.layout.title = "Growth curve of daisies"

    return albedo_plot


def update_albedo_plot():
    pass


def constant_flux_temp(
    Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt
):
    # First experiment
    F = Fsnom * 1  # solar radiation

    # initial condition state vector
    x0 = {}
    x0["Sw"] = 0.01
    x0["Sb"] = 0.01
    x0["Su"] = 1 - x0["Sw"] - x0["Sb"]
    # note that we also need to initiate the planetary Albedo
    calc.UpdateAlbedo(x0, Albedo)
    # and the temperature
    calc.UpdateTemp(x0, F, rat, em_p, sig, ins_p, Albedo)

    # loop over generations
    ngen = 40

    xgens = []
    xgens.append(x0)
    for g in range(ngen - 1):
        xgens.append(
            calc.NextState(
                xgens[-1],
                F,
                rat,
                em_p,
                sig,
                ins_p,
                Albedo,
                death,
                minarea,
                T_min,
                T_opt,
            )
        )

    gens = [i for i in range(ngen)]

    # temperatures plot
    fig = go.Figure()
    fig.add_hrect(
        xref="paper",
        yref="paper",
        x0=1,
        x1=1.5,
        y0=-15,
        y1=100,
        line_width=0,
        fillcolor="white",
        opacity=1,
    )
    fig.update_xaxes(showgrid=True, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=False)
    fig.add_trace(
        go.Scatter(
            x=gens,
            y=[x["Tw"] - 273.15 for x in xgens],
            name="White daisies temperature",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=gens,
            y=[x["Tb"] - 273.15 for x in xgens],
            name="Black daisies temperature",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=gens, y=[x["Tp"] - 273.15 for x in xgens], name="Planet temperature"
        )
    )

    fig.update_layout(xaxis_title="Generation number", yaxis_title="Temperature [degC]")
    fig.update_xaxes(range=[0, ngen])
    fig.update_yaxes(range=[0, 50])
    fig.layout.title = "Constant flux temperature with daisy generation"

    #####
    # area plot:
    fig2 = go.Figure()
    fig2.add_hrect(
        xref="paper",
        yref="paper",
        x0=1,
        x1=1.5,
        y0=-15,
        y1=100,
        line_width=0,
        fillcolor="white",
        opacity=1,
    )
    fig2.update_xaxes(showgrid=True, zeroline=False)
    fig2.update_yaxes(showgrid=True, zeroline=False)
    fig2.add_trace(
        go.Scatter(
            x=gens,
            y=[x["Sw"] for x in xgens],
            name="White daisies area",
        )
    )
    fig2.add_trace(
        go.Scatter(
            x=gens,
            y=[x["Sb"] for x in xgens],
            name="Black daisies area",
        )
    )
    fig2.add_trace(
        go.Scatter(x=gens, y=[x["Su"] for x in xgens], name="Uninhabited area")
    )

    fig2.update_layout(xaxis_title="Generation number", yaxis_title="Fractional area")
    fig2.update_xaxes(range=[0, ngen])
    fig2.update_yaxes(range=[0, 1])
    fig2.layout.title = "Constant flux daisy coverage"

    return fig


def constant_flux_area(
    Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt
):
    # First experiment
    F = Fsnom * 1  # solar radiation

    # initial condition state vector
    x0 = {}
    x0["Sw"] = 0.01
    x0["Sb"] = 0.01
    x0["Su"] = 1 - x0["Sw"] - x0["Sb"]
    # note that we also need to initiate the planetary Albedo
    calc.UpdateAlbedo(x0, Albedo)
    # and the temperature
    calc.UpdateTemp(x0, F, rat, em_p, sig, ins_p, Albedo)

    # loop over generations
    ngen = 40

    xgens = []
    xgens.append(x0)
    for g in range(ngen - 1):
        xgens.append(
            calc.NextState(
                xgens[-1],
                F,
                rat,
                em_p,
                sig,
                ins_p,
                Albedo,
                death,
                minarea,
                T_min,
                T_opt,
            )
        )

    gens = [i for i in range(ngen)]

    #####
    # area plot:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_hrect(
        xref="paper",
        yref="paper",
        x0=1,
        x1=1.5,
        y0=-15,
        y1=100,
        line_width=0,
        fillcolor="white",
        opacity=1,
    )
    fig.update_xaxes(showgrid=True, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=False, secondary_y=True)
    fig.add_trace(
        go.Scatter(x=gens, y=[x["Sw"] for x in xgens], name="White daisies area"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=gens, y=[x["Sb"] for x in xgens], name="Black daisies area"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=gens, y=[x["Su"] for x in xgens], name="Uninhabited area"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=gens,
            y=[x["Ap"] for x in xgens],
            name="Combined albedo",
            line=dict(color="royalblue", dash="dot"),
        ),
        secondary_y=True,
    )
    # fig.update_layout(xaxis_title="Generation number", yaxis_title="Fractional area")
    fig.update_xaxes(title_text="Generation")
    fig.update_yaxes(title_text="Fractional area", secondary_y=False)
    fig.update_yaxes(title_text="Albedo", secondary_y=True)
    fig.update_xaxes(range=[0, ngen])
    fig.update_yaxes(range=[0, 1])
    fig.layout.title = "Constant flux daisy coverage"

    return fig
