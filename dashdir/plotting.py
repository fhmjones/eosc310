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


def constant_flux_temp(
    Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt, areas
):
    # solve the constant flux problem:
    xgens, gens = calc.update_constant_flux(
        Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt, areas
    )

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
            line=dict(color="khaki", width=8),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=gens,
            y=[x["Tb"] - 273.15 for x in xgens],
            name="Black daisies temperature",
            line=dict(color="black", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=gens,
            y=[x["Tp"] - 273.15 for x in xgens],
            name="Planet temperature",
            line=dict(color="seagreen", width=4),
        )
    )

    fig.update_layout(xaxis_title="Generation number", yaxis_title="Temperature [degC]")
    fig.update_xaxes(range=[0, len(gens)])
    fig.update_yaxes(range=[10, 40])
    fig.layout.title = "Constant flux temperature with daisy generation"
    fig.update_layout(plot_bgcolor="lightgray")
    return fig


def constant_flux_area(
    Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt, areas
):
    # solve the constant flux problem:
    xgens, gens = calc.update_constant_flux(
        Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt, areas
    )

    # make the figure:
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
        go.Scatter(
            x=gens,
            y=[x["Sw"] for x in xgens],
            name="White daisies area",
            line=dict(color="khaki", width=8),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=gens,
            y=[x["Sb"] for x in xgens],
            name="Black daisies area",
            line=dict(color="black", width=3),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=gens,
            y=[x["Su"] for x in xgens],
            name="Uninhabited area",
            line=dict(color="saddlebrown", width=4),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=gens,
            y=[x["Ap"] for x in xgens],
            name="Combined albedo",
            line=dict(color="royalblue", dash="dash"),
        ),
        secondary_y=True,
    )
    # fig.update_layout(xaxis_title="Generation number", yaxis_title="Fractional area")
    fig.update_xaxes(title_text="Generation")
    fig.update_yaxes(title_text="Fractional area", secondary_y=False)
    fig.update_yaxes(title_text="Albedo", secondary_y=True)
    fig.update_xaxes(range=[0, len(gens)])
    fig.update_yaxes(range=[0, 1])
    fig.layout.title = "Constant flux daisy coverage"
    # fig.update_layout(paper_bgcolor="black")
    fig.update_layout(plot_bgcolor="lightgray")

    return fig


def varying_solar_flux_temp(
    Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt
):
    xeq, xeqbar, _, F = calc.update_equi_flux(
        Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt
    )
    # fig = go.Figure(data=go.Scatter(x=F, y=[x["Tw"] - 273.15 for x in xeq]))
    ##
    # # fig = make_subplots(rows=1, cols=2, subplot_titles=("Plot1", "Plot2"))
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
    # # subplot 1
    fig.update_xaxes(showgrid=True, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=False)
    fig.add_trace(
        go.Scatter(
            x=F,
            y=[x["Tw"] - 273.15 for x in xeq],
            name="White daisies temperature",
            line=dict(color="khaki", width=7),
        ),
    )
    # fig.add_trace(
    #     go.Scatter(
    #         x=F,
    #         y=[x["Tw"] - 273.15 for x in xeqinv],
    #         name="White daisies temperature (backwards)",
    #         line=dict(color="lightskyblue", dash="dot", width=5),
    #     ),
    # )
    fig.add_trace(
        go.Scatter(
            x=F,
            y=[x["Tb"] - 273.15 for x in xeq],
            name="Black daisies temperature",
            line=dict(color="black", width=3),
        ),
    )
    # fig.add_trace(
    #     go.Scatter(
    #         x=F,
    #         y=[x["Tb"] - 273.15 for x in xeqinv],
    #         name="Black daisies temperature (backwards)",
    #         line=dict(color="darkslategray", dash="dot", width=3),
    #     ),
    # )
    fig.add_trace(
        go.Scatter(
            x=F,
            y=[x["Tp"] - 273.15 for x in xeq],
            name="Planet temperature",
            line=dict(color="seagreen", width=3),
        ),
    )
    # fig.add_trace(
    #     go.Scatter(
    #         x=F,
    #         y=[x["Tp"] - 273.15 for x in xeqinv],
    #         name="Planet temperature (backwards)",
    #         line=dict(color="sienna", dash="dot", width=3),
    #     ),
    # )
    fig.add_trace(
        go.Scatter(
            x=F,
            y=[x["Tp"] - 273.15 for x in xeqbar],
            name="Planet temperature (without life)",
            line=dict(color="gray", dash="dash", width=3),
        ),
    )

    fig.update_xaxes(title="Solar Flux", range=[0.6, F[-1]])
    fig.update_yaxes(title="Temperature [degC]", range=[-20, 80])
    fig.update_layout(title_text="Equilibrium temperature vs solar flux")
    fig.update_layout(plot_bgcolor="lightgray")

    return fig


def varying_solar_flux_area(
    Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt
):
    xeq, _, _, F = calc.update_equi_flux(
        Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt
    )
    # fig = go.Figure(data=go.Scatter(x=F, y=[x["Tw"] - 273.15 for x in xeq]))
    ##
    # # fig = make_subplots(rows=1, cols=2, subplot_titles=("Plot1", "Plot2"))
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
    # # subplot 1
    fig.update_xaxes(showgrid=True, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=False)
    fig.add_trace(
        go.Scatter(
            x=F,
            y=[x["Sw"] for x in xeq],
            name="White daisies area",
            line=dict(color="khaki", width=7),
        ),
    )
    # fig.add_trace(
    #     go.Scatter(
    #         x=F,
    #         y=[x["Sw"] for x in xeqinv],
    #         name="White daisies area (backwards)",
    #         line=dict(color="lightskyblue", dash="dot", width=5),
    #     ),
    # )
    fig.add_trace(
        go.Scatter(
            x=F,
            y=[x["Sb"] for x in xeq],
            name="Black daisies area",
            line=dict(color="black", width=3),
        ),
    )
    # fig.add_trace(
    #     go.Scatter(
    #         x=F,
    #         y=[x["Sb"] for x in xeqinv],
    #         name="Black daisies area (backwards)",
    #         line=dict(color="darkslategray", dash="dot", width=3),
    #     ),
    # )
    fig.add_trace(
        go.Scatter(
            x=F,
            y=[x["Su"] for x in xeq],
            name="Uninhabited area",
            line=dict(color="saddlebrown", width=3),
        ),
    )
    # fig.add_trace(
    #     go.Scatter(
    #         x=F,
    #         y=[x["Su"] for x in xeqinv],
    #         name="Uninhabited area (backwards)",
    #         line=dict(color="sienna", dash="dot", width=3),
    #     ),
    # )

    fig.update_xaxes(title="Solar Flux", range=[0.6, F[-1]])
    fig.update_yaxes(title="Fractional area", range=[0, 1])
    fig.update_layout(title_text="Equilibrium area vs solar flux")
    fig.update_layout(plot_bgcolor="lightgray")
    return fig


# def update_constant_flux_temp(Aw, Ab, Ap, Sw0, Sb0, solar_distance):  # with initial conditions
def update_constant_flux_temp(live_vars, Aw, Ab, Ap, ins, distance, areas):
    live_vars["Albedo"]["w"] = Aw
    live_vars["Albedo"]["b"] = Ab
    live_vars["Albedo"]["none"] = Ap
    live_vars["ins_p"] = ins
    # areas["w"] = Sw0
    # areas["b"] = Sb0
    live_vars["Fsnom"] = calc.update_solar_constant(calc.fromAU(distance))
    return constant_flux_temp(**live_vars, areas=areas)


def update_constant_flux_area(live_vars, Aw, Ab, Ap, ins, distance, areas):
    live_vars["Albedo"]["w"] = Aw
    live_vars["Albedo"]["b"] = Ab
    live_vars["Albedo"]["none"] = Ap
    live_vars["ins_p"] = ins
    # areas["w"] = Sw0
    # areas["b"] = Sb0
    live_vars["Fsnom"] = calc.update_solar_constant(calc.fromAU(distance))
    return constant_flux_area(**live_vars, areas=areas)


def update_varying_flux_temp(live_vars, Aw, Ab, Ap, ins):
    live_vars["Albedo"]["w"] = Aw
    live_vars["Albedo"]["b"] = Ab
    live_vars["Albedo"]["none"] = Ap
    live_vars["ins_p"] = ins
    # areas["w"] = Sw0
    # areas["b"] = Sb0
    # return plot.constant_flux_temp(
    #     Fsnom, Albedo, rat, em_p, sig, ins, death, minarea, T_min, T_opt, areas
    return varying_solar_flux_temp(**live_vars)


def update_varying_flux_area(live_vars, Aw, Ab, Ap, ins):
    live_vars["Albedo"]["w"] = Aw
    live_vars["Albedo"]["b"] = Ab
    live_vars["Albedo"]["none"] = Ap
    live_vars["ins_p"] = ins
    # areas["w"] = Sw0
    # areas["b"] = Sb0
    # Fsnom = calc.update_solar_constant(calc.fromAU(solar_distance))
    return varying_solar_flux_area(**live_vars)
