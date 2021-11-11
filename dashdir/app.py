# file app.py

# based on this model for now from: https://github.com/strawpants/daisyworld
# nice words about daisyworld at: http://www.jameslovelock.org/biological-homeostasis-of-the-global-environment-the-parable-of-daisyworld/


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
import copy


import plotting as plot
import calculations as calc

# Dashboard preliminaries:
es = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=es)

instructions = open("instructions.md", "r")
instructions_markdown = instructions.read()

attributions = open("attributions.md", "r")
attributions_markdown = attributions.read()


# Daisyworld preliminaries:
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
areas = {"w": 0.01, "b": 0.01}

## growth optimum Temp of the white daisies
T_opt = {"w": 22.5 + 273.15}  # in Kelvin
T_min = {"w": 273.15 + 5}  # no growth below this temperature
death = {"w": 0.3}  # death rate of White daisies (fraction)

# assume the same growth curve for Black daisies (change if needed)
T_opt["b"] = T_opt["w"]
T_min["b"] = T_min["w"]
death["b"] = death["w"]
minarea = 0.01  # minimum area as a fraction occupied by each species

solar_distance = calc.fromAU(1)
Fsnom = calc.update_solar_constant(solar_distance)

init_vars = dict(
    Fsnom=Fsnom,
    Albedo=Albedo,
    rat=rat,
    em_p=em_p,
    sig=sig,
    ins_p=ins_p,
    death=death,
    minarea=minarea,
    T_min=T_min,
    T_opt=T_opt,
)

# deepcopy of init_vars for callbacks:
live_vars = copy.deepcopy(init_vars)

# Function calls for initializing figures:
constant_flux_temp = plot.constant_flux_temp(
    **init_vars,
    areas=areas,
)
constant_flux_area = plot.constant_flux_area(
    **init_vars,
    areas=areas,
)

varying_solar_flux_temp = plot.varying_solar_flux_temp(**init_vars)
varying_solar_flux_area = plot.varying_solar_flux_area(**init_vars)


slider_style = {
    "width": "20%",
    "display": "inline-block",
    "horizontal-align": "top",
}

app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Markdown(
                    """
            ### Welcome to Daisyworld!
                 """
                ),
                html.Img(src=app.get_asset_url("Daisyworld_pict.jpeg")),
                dcc.Markdown(
                    # using the instructions markdown file that was loaded in above
                    children=instructions_markdown
                ),
            ],
            style={
                "width": "100%",
                "display": "inline-block",
                "padding": "0 20",
                "vertical-align": "middle",
                "margin-bottom": 30,
                "margin-right": 50,
                "margin-left": 20,
            },
        ),
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Constant solar flux",
                    children=[
                        html.Div(
                            [
                                ###
                                html.Div(
                                    [
                                        dcc.Markdown(""" White daisy albedo:"""),
                                        dcc.Slider(
                                            id="Aw_1",
                                            min=0.5,
                                            max=1,
                                            step=0.05,
                                            value=Albedo["w"],
                                            marks={0.5: "0.5", 1: "1"},
                                            tooltip={
                                                "always_visible": True,
                                                "placement": "topLeft",
                                            },
                                        ),
                                    ],
                                    style=slider_style,
                                ),
                                html.Div(
                                    [
                                        dcc.Markdown(""" Black daisy albedo: """),
                                        dcc.Slider(
                                            id="Ab_1",
                                            min=0,
                                            max=0.5,
                                            step=0.05,
                                            value=Albedo["b"],
                                            marks={0: "0", 0.5: "0.5"},
                                            tooltip={
                                                "always_visible": True,
                                                "placement": "topLeft",
                                            },
                                        ),
                                    ],
                                    style=slider_style,
                                ),
                                html.Div(
                                    [
                                        dcc.Markdown(""" Soil albedo """),
                                        dcc.Slider(
                                            id="Ap_1",
                                            min=0.3,
                                            max=0.7,
                                            step=0.01,
                                            value=Albedo["none"],
                                            marks={0.3: "0.3", 0.7: "0.7"},
                                            tooltip={
                                                "always_visible": True,
                                                "placement": "topLeft",
                                            },
                                        ),
                                    ],
                                    style=slider_style,
                                ),
                                html.Div(
                                    [
                                        dcc.Markdown("""Insulation factor"""),
                                        dcc.Slider(
                                            id="ins_1",
                                            min=0,
                                            max=1,
                                            step=0.05,
                                            value=ins_p,
                                            marks={0: "0", 1: "1"},
                                            tooltip={
                                                "always_visible": True,
                                                "placement": "topRight",
                                            },
                                        ),
                                    ],
                                    style=slider_style,
                                ),
                                html.Div(
                                    [
                                        ##
                                        dcc.Markdown("""Distance from Sun (AU)"""),
                                        dcc.Slider(
                                            id="distance",
                                            min=0.8,
                                            max=1.2,
                                            step=0.01,
                                            value=calc.toAU(solar_distance),
                                            marks={0.8: "0.8", 1.2: "1.2"},
                                            tooltip={
                                                "always_visible": True,
                                                "placement": "topRight",
                                            },
                                        ),
                                    ],
                                    style=slider_style,
                                ),
                                ###
                                html.Button("Reset", id="reset_button", n_clicks=0),
                                ###
                                dcc.Graph(id="constant_flux_area"),
                            ],
                            style={"width": "100%", "display": "inline-block"},
                        ),
                        html.Div(
                            [
                                dcc.Graph(id="constant_flux_temp"),
                            ],
                            style={"width": "100%", "display": "inline-block"},
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Varying solar flux",
                    children=[
                        html.Div(
                            [
                                ###
                                ###
                                html.Div(
                                    [
                                        dcc.Markdown(""" White daisy albedo:"""),
                                        dcc.Slider(
                                            id="Aw_2",
                                            min=0.5,
                                            max=1,
                                            step=0.05,
                                            value=Albedo["w"],
                                            marks={0.5: "0.5", 1: "1"},
                                            tooltip={
                                                "always_visible": True,
                                                "placement": "topLeft",
                                            },
                                        ),
                                    ],
                                    style=slider_style,
                                ),
                                html.Div(
                                    [
                                        dcc.Markdown(""" Black daisy albedo: """),
                                        dcc.Slider(
                                            id="Ab_2",
                                            min=0,
                                            max=0.5,
                                            step=0.05,
                                            value=Albedo["b"],
                                            marks={0: "0", 0.5: "0.5"},
                                            tooltip={
                                                "always_visible": True,
                                                "placement": "topLeft",
                                            },
                                        ),
                                    ],
                                    style=slider_style,
                                ),
                                html.Div(
                                    [
                                        dcc.Markdown(""" Soil albedo """),
                                        dcc.Slider(
                                            id="Ap_2",
                                            min=0.3,
                                            max=0.7,
                                            step=0.01,
                                            value=Albedo["none"],
                                            marks={0.03: "0.03", 0.7: "0.7"},
                                            tooltip={
                                                "always_visible": True,
                                                "placement": "topLeft",
                                            },
                                        ),
                                    ],
                                    style=slider_style,
                                ),
                                html.Div(
                                    [
                                        dcc.Markdown("""Insulation factor"""),
                                        dcc.Slider(
                                            id="ins_2",
                                            min=0,
                                            max=1,
                                            step=0.05,
                                            value=ins_p,
                                            marks={0: "0", 1: "1"},
                                            tooltip={
                                                "always_visible": True,
                                                "placement": "topRight",
                                            },
                                        ),
                                    ],
                                    style=slider_style,
                                ),
                                ###
                                html.Button("Reset", id="reset_button_2", n_clicks=0),
                                dcc.Graph(id="varying_solar_flux_temp"),
                                dcc.Graph(id="varying_solar_flux_area"),
                            ],
                            style={"width": "100%", "display": "inline-block"},
                        ),
                    ],
                ),
            ]
        ),
        html.Div(
            [
                dcc.Markdown(
                    # the markdown from the attributions file loaded in above.
                    children=attributions_markdown
                ),
            ],
            style={
                "width": "100%",
                "display": "inline-block",
                "padding": "0 20",
                "vertical-align": "middle",
                "margin-bottom": 30,
                "margin-right": 50,
                "margin-left": 20,
            },
        ),
    ],
    style={"width": "1000px"},
)


# pair of callback functions to reset sliders to initial values
# saved in init_vars dictionary:
# TAB 1:
@app.callback(
    Output("Aw_1", "value"),
    Output("Ab_1", "value"),
    Output("Ap_1", "value"),
    Output("ins_1", "value"),
    Output("distance", "value"),
    Input("reset_button", "n_clicks"),
)
def reset_tab1(reset_button):
    return (
        init_vars["Albedo"]["w"],
        init_vars["Albedo"]["b"],
        init_vars["Albedo"]["none"],
        init_vars["ins_p"],
        1,
    )


# TAB 2:
@app.callback(
    Output("Aw_2", "value"),
    Output("Ab_2", "value"),
    Output("Ap_2", "value"),
    Output("ins_2", "value"),
    Input("reset_button_2", "n_clicks"),
)
def reset_tab2(reset_button_2):
    return (
        init_vars["Albedo"]["w"],
        init_vars["Albedo"]["b"],
        init_vars["Albedo"]["none"],
        init_vars["ins_p"],
    )


# TAB 1:
# callback to update figures for constant flux sliders:
@app.callback(
    Output(component_id="constant_flux_temp", component_property="figure"),
    Output(component_id="constant_flux_area", component_property="figure"),
    Input(component_id="Aw_1", component_property="value"),
    Input(component_id="Ab_1", component_property="value"),
    Input(component_id="Ap_1", component_property="value"),
    Input(component_id="ins_1", component_property="value"),
    # Input(component_id="Sw0", component_property="value"),
    # Input(component_id="Sb0", component_property="value"),
    Input(component_id="distance", component_property="value"),
)
def update_constant_flux_figures(Aw_1, Ab_1, Ap_1, ins_1, distance):
    return plot.update_constant_flux_temp(
        live_vars, Aw_1, Ab_1, Ap_1, ins_1, distance, areas
    ), plot.update_constant_flux_area(
        live_vars, Aw_1, Ab_1, Ap_1, ins_1, distance, areas
    )


# TAB 2:
# callback to update figures for varying flux sliders:
@app.callback(
    Output(component_id="varying_solar_flux_temp", component_property="figure"),
    Output(component_id="varying_solar_flux_area", component_property="figure"),
    Input(component_id="Aw_2", component_property="value"),
    Input(component_id="Ab_2", component_property="value"),
    Input(component_id="Ap_2", component_property="value"),
    Input(component_id="ins_2", component_property="value"),
    # Input(component_id="Sw0", component_property="value"),
    # Input(component_id="Sb0", component_property="value"),
)
def update_varying_flux_figures(Aw_2, Ab_2, Ap_2, ins_2):
    return plot.update_varying_flux_temp(
        live_vars, Aw_2, Ab_2, Ap_2, ins_2
    ), plot.update_varying_flux_area(live_vars, Aw_2, Ab_2, Ap_2, ins_2)


if __name__ == "__main__":
    app.run_server(debug=True)
