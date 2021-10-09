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
fig.add_trace(go.Scatter(x=x, y=y, name=""))

fig.update_layout(xaxis_title="x", yaxis_title="")
fig.update_xaxes(range=[0, 1])
fig.update_yaxes(range=[0, 1])
fig.layout.title = ""
