html.Div(
    [
        dcc.Markdown("""Label"""),
        dcc.Slider(
            id="id",
            min=0,
            max=1,
            step=0.05,
            value=[],
            marks={0: "0", 1: "1"},
            tooltip={"always_visible": True, "placement": "topLeft"},
        ),
    ],
    style={"width": "37%", "display": "inline-block", "vertical-align": "top"},
),
