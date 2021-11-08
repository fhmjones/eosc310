# file app.py

# bastardizing this model for now from: https://github.com/strawpants/daisyworld
# nice words about daisyworld at: http://www.jameslovelock.org/biological-homeostasis-of-the-global-environment-the-parable-of-daisyworld/


from os import TMP_MAX
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
            - From [**Biological Homestatis of the Global Environment:** The Parable of Daisyworld](http://www.jameslovelock.org/biological-homeostasis-of-the-global-environment-the-parable-of-daisyworld/)
            
            ___ 

            **<add a photo here>**

            #### Overview: 
            This is an interactive Daisyworld model that calculates the evolution of the 
            equilibrium temperature and surface area of daisies in a world that is only
            populated by two species: black and white daisies.     
               
            Because the black and white daisies have different albedos, the relative proportion of black and white daisies
            affects the amount of solar radiation which is absorbed or reflected back into space. 
            The radiative balance of the planet is thus coupled to the growth of each species
            of daisy. Likewise however, the growth of daisies is sensitive to the planetary
            temperature: too cold or too cold, the daisies won't be able to grow. What results is
            a feedback system between life on the planet and the planet itself.    
            

            This model is divided into two parts: the first one considers a planet orbiting a
            star that is outputting a constant solar flux with time: this is characteristic of
            older, more mature stars such as
            our present Sun. Early in Earth's evolution however, the young Sun is expected to emit only about
            70 percent of what it emits today.  The second part of the model considers what happens when the amount 
            of solar energy emitted by the star increases with time, such as for younger stars. 
            
            ___
            ##### Slider legend: 

            1. **White daisy albedo**: controls the albedo (reflectivity) of white daisies. Higher values 
            mean more solar radiation is reflected back into space.  
            2. **Black daisy albedo**: controls the albedo of black daisies. A lower albedo means more solar
            radation is absorbed the the daisies.   
            3. **Soil albedo**: the albedo of the background of Daisyworld in which the 
            daisies grow. Uninhabited areas are covered in soil, which has an albedo
            in between that of the white daisies and the black daisies.   
            4. **Insulation factor**: controls how much heat energy the daisies can hold onto after absorbing
            solar radiation. If the planet would be a perfect insulator (insulation = 1), regions with black and 
            white daisies would have a different temperature, and they would behave as if the whole
            planet was covered with black or white daisies respectively. In contrast, if the planet
            would be a perfect conductor (insulation = 0) the temperature would be constant over the complete planet.    
            5. **Distance from Sun [AU]**: controls how far the planet is from it's star and thus how much solar
            radiation can reach the surface to heat it. Units are in Astronomical Units (AU), roughly
            equal to the Earth-Sun distance.   

            


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
                                            marks={0.03: "0.01", 0.7: "0.5"},
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
                                            marks={0.03: "0.01", 0.7: "0.5"},
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
                    """
                #### Sources
                
                1. Methods from [DaisyWorld Jupyter Notebook](https://github.com/strawpants/daisyworld) by Roelof Rietbroek
                2. [Detailed readings](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2006RG000217)
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

#%%
print("ye")
#%%# Local functions to clean up app callbacks:
# not very well implemented but it's something for now:

# def update_constant_flux_temp(Aw, Ab, Ap, Sw0, Sb0, solar_distance):  # with initial conditions
def update_constant_flux_temp(Aw, Ab, Ap, ins, distance):
    live_vars["Albedo"]["w"] = Aw
    live_vars["Albedo"]["b"] = Ab
    live_vars["Albedo"]["none"] = Ap
    live_vars["ins_p"] = ins
    # areas["w"] = Sw0
    # areas["b"] = Sb0
    live_vars["Fsnom"] = calc.update_solar_constant(calc.fromAU(distance))
    return plot.constant_flux_temp(**live_vars, areas=areas)


def update_constant_flux_area(Aw, Ab, Ap, ins, distance):
    live_vars["Albedo"]["w"] = Aw
    live_vars["Albedo"]["b"] = Ab
    live_vars["Albedo"]["none"] = Ap
    live_vars["ins_p"] = ins
    # areas["w"] = Sw0
    # areas["b"] = Sb0
    live_vars["Fsnom"] = calc.update_solar_constant(calc.fromAU(distance))
    return plot.constant_flux_area(**live_vars, areas=areas)


def update_varying_flux_temp(Aw, Ab, Ap, ins):
    live_vars["Albedo"]["w"] = Aw
    live_vars["Albedo"]["b"] = Ab
    live_vars["Albedo"]["none"] = Ap
    live_vars["ins_p"] = ins
    # areas["w"] = Sw0
    # areas["b"] = Sb0
    # return plot.constant_flux_temp(
    #     Fsnom, Albedo, rat, em_p, sig, ins, death, minarea, T_min, T_opt, areas
    return plot.varying_solar_flux_temp(**live_vars)


def update_varying_flux_area(Aw, Ab, Ap, ins):
    live_vars["Albedo"]["w"] = Aw
    live_vars["Albedo"]["b"] = Ab
    live_vars["Albedo"]["none"] = Ap
    live_vars["ins_p"] = ins
    # areas["w"] = Sw0
    # areas["b"] = Sb0
    # Fsnom = calc.update_solar_constant(calc.fromAU(solar_distance))
    return plot.varying_solar_flux_area(**live_vars)


# Reset :
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


# App callbacks to update figures with slider input:
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
    return update_constant_flux_temp(
        Aw_1, Ab_1, Ap_1, ins_1, distance
    ), update_constant_flux_area(Aw_1, Ab_1, Ap_1, ins_1, distance)


## APP CALLBACKS FOR VARYING FLUX PLOTS:
# App callbacks to update figures with slider input:
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
    return update_varying_flux_temp(Aw_2, Ab_2, Ap_2, ins_2), update_varying_flux_area(
        Aw_2, Ab_2, Ap_2, ins_2
    )


if __name__ == "__main__":
    app.run_server(debug=True)
