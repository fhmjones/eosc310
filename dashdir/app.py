# file app.py

# bastardizing this model for now from: https://github.com/strawpants/daisyworld
# nice words about daisyworld at: http://www.jameslovelock.org/biological-homeostasis-of-the-global-environment-the-parable-of-daisyworld/


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go


import plotting as plot

# Dashboard preliminaries:
es = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=es)

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

# FIXME:
# This needs to be changed as a function of solar distance!
Fsnom = 3668  # nominal Flux in W/m^2


# Function calls for initializing figures:
constant_flux_temp = plot.constant_flux_temp(
    Fsnom,
    Albedo,
    rat,
    em_p,
    sig,
    ins_p,
    death,
    minarea,
    T_min,
    T_opt,
    areas,
)
constant_flux_area = plot.constant_flux_area(
    Fsnom,
    Albedo,
    rat,
    em_p,
    sig,
    ins_p,
    death,
    minarea,
    T_min,
    T_opt,
    areas,
)

varying_solar_flux_temp = plot.varying_solar_flux_temp(
    Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt
)

varying_solar_flux_area = plot.varying_solar_flux_area(
    Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt
)
xs = list(range(30))
ys = [10000 * 1.07 ** i for i in xs]
fig = go.Figure(data=go.Scatter(x=xs, y=ys))
fig.update_layout(xaxis_title="Years", yaxis_title="$")
##

app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Markdown(
                    """
            ### Welcome to Daisyworld!
            
            ----------  
            The biota have effected profound changes on the environment 
            of the surface of the earth. At the same time, that environment has 
            imposed constraints on the biota, so that life and the environment 
            may be considered as two parts of a coupled system. Unfortunately, the 
            system is too complex and too little known for us to model it adequately. 
            To investigate the properties which this close-coupling might confer on 
            the system, we chose to develop a model of an imaginary planet having 
            a very simple biosphere. It consisted of just two species of daisy of 
            different colours and was first described by Lovelock (1982). 
            The growth rate of the daisies depends on only one environmental 
            variable, temperature, which the daisies in turn modify because they 
            absorb different amounts of radiation. Regardless of the details of the 
            interaction, the effect of the daisies is to stabilize the temperature. 
            The result arises because of the peaked shape of the growth-temperature 
            curve and is independent of the mechanics by which the biota are assumed 
            to modify the temperature. We sketch out the elements of a biological 
            feedback system which might help regulate the temperature of the earth."
            - From [BIOLOGICAL HOMEOSTASIS OF THE GLOBAL ENVIRONMENT: THE PARABLE OF DAISYWORLD](http://www.jameslovelock.org/biological-homeostasis-of-the-global-environment-the-parable-of-daisyworld/)
            ___
            To add: 
            - Two sliders for initial daisy proportions
            - Slider for distance from Sun (0.5 AU to 1.5 AU)

            """
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
        # html.Div(
        #     [
        #         dcc.Graph(figure=albedo_plot),
        #     ],
        #     style={"width": "100%", "display": "inline-block"},
        # ),
        ###
        html.Div(
            [
                dcc.Markdown(
                    """
                ----------
                Make an interative plot: Adjust the sliders below to change the albedo of white and black daisies,
                and of the planetary surface. 
                """
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
        ### first column of sliders:
        html.Div(
            [
                dcc.Markdown(""" Initial white daisy area: """),
                dcc.Slider(
                    id="Sw0",
                    min=0.01,
                    max=0.5,
                    step=0.01,
                    value=areas["w"],
                    marks={0.01: "0.01", 0.5: "0.5"},
                    tooltip={"always_visible": True, "placement": "topLeft"},
                ),
                dcc.Markdown(""" Initial black daisy area:"""),
                dcc.Slider(
                    id="Sb0",
                    min=0.01,
                    max=0.5,
                    step=0.01,
                    value=areas["b"],
                    marks={0.01: "0.01", 0.5: "0.5"},
                    tooltip={"always_visible": True, "placement": "topLeft"},
                ),
                dcc.Markdown("""Distance from Sun (AU) **NOT IMPLEMENTED**"""),
                dcc.Slider(
                    id="r",
                    min=0,
                    max=1,
                    step=0.05,
                    value=1,  # CHANGE THIS
                    marks={0.5: "0.5", 1.5: "1.5"},
                    tooltip={"always_visible": True, "placement": "topRight"},
                ),
            ],
            style={
                "width": "37%",
                "display": "inline-block",
                "vertical-align": "top",
            },
        ),
        ### second column of sliders:
        html.Div(
            [
                dcc.Markdown(""" White daisy albedo:"""),
                dcc.Slider(
                    id="Aw",
                    min=0.5,
                    max=1,
                    step=0.05,
                    value=Albedo["w"],
                    marks={0.5: "0.5", 1: "1"},
                    tooltip={"always_visible": True, "placement": "topLeft"},
                ),
                dcc.Markdown(""" Black daisy albedo: """),
                dcc.Slider(
                    id="Ab",
                    min=0,
                    max=0.5,
                    step=0.05,
                    value=Albedo["b"],
                    marks={0: "0", 0.5: "0.5"},
                    tooltip={"always_visible": True, "placement": "topLeft"},
                ),
                dcc.Markdown(""" Background albedo:"""),
                dcc.Slider(
                    id="Ap",
                    min=0,
                    max=1,
                    step=0.05,
                    value=Albedo["none"],
                    marks={0: "0", 1: "1"},
                    tooltip={"always_visible": True, "placement": "topRight"},
                ),
            ],
            style={
                "width": "37%",
                "display": "inline-block",
                "vertical-align": "top",
            },
        ),
        html.Div(
            [
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
        html.Div(
            [
                dcc.Graph(figure=varying_solar_flux_temp),
            ],
            style={"width": "100%", "display": "inline-block"},
        ),
        html.Div(
            [
                dcc.Graph(figure=varying_solar_flux_area),
            ],
            style={"width": "100%", "display": "inline-block"},
        ),
        html.Div(
            [
                dcc.Markdown(
                    """
                #### Sources
                
                1. Methods from [DaisyWorld Jupyter Notebook](https://github.com/strawpants/daisyworld) by Roelof Rietbroek
                ----------
                """
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

# App callbacks to update figures with slider input:
@app.callback(
    Output(component_id="constant_flux_temp", component_property="figure"),
    Input(component_id="Aw", component_property="value"),
    Input(component_id="Ab", component_property="value"),
    Input(component_id="Ap", component_property="value"),
    Input(component_id="Sw0", component_property="value"),
    Input(component_id="Sb0", component_property="value"),
)
def update_constant_flux_temp(Aw, Ab, Ap, Sw0, Sb0):
    Albedo["w"] = Aw
    Albedo["b"] = Ab
    Albedo["none"] = Ap
    areas["w"] = Sw0
    areas["b"] = Sb0
    return plot.constant_flux_temp(
        Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt, areas
    )


@app.callback(
    Output(component_id="constant_flux_area", component_property="figure"),
    Input(component_id="Aw", component_property="value"),
    Input(component_id="Ab", component_property="value"),
    Input(component_id="Ap", component_property="value"),
    Input(component_id="Sw0", component_property="value"),
    Input(component_id="Sb0", component_property="value"),
)
def update_constant_flux_area(Aw, Ab, Ap, Sw0, Sb0):
    Albedo["w"] = Aw
    Albedo["b"] = Ab
    Albedo["none"] = Ap
    areas["w"] = Sw0
    areas["b"] = Sb0
    return plot.constant_flux_area(
        Fsnom, Albedo, rat, em_p, sig, ins_p, death, minarea, T_min, T_opt, areas
    )


if __name__ == "__main__":
    app.run_server(debug=True)
