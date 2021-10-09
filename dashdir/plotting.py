import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import calculations as calc


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
