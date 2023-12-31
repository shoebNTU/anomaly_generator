import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Set page title and favicon
st.set_page_config(page_title="Sample chainage readings", page_icon=":lower_left_paintbrush:")
st.title("Sample chainage readings")
st.info(""" This app presents a demo of a chainage comprising of 200 representative gauge readings. Please hover over the gauge to read the corresponding gauge readings.""")
# length = st.sidebar.slider("Gauge Length", min_value=12.0, max_value=15.0, value=(14.0), step=0.1)
st.set_option('deprecation.showPyplotGlobalUse', False)

# Define the x and y coordinates of the railway track
x = np.arange(0,200)
y1 = -7*np.ones_like(x)
y2 = 7*np.ones_like(x)
y_offset = np.sin(np.linspace(0,np.radians(360),len(x)))/2 

# Create a scatter trace for the railway track
trace1 = go.Scatter(
    x=x,
    y=y1,
    mode='lines',
    line=dict(color='black', width=4, dash='dot'), name = 'baseline'
)

trace2 = go.Scatter(
    x=x,
    y=y2,
    mode='lines', name='baseline',
    line=dict(color='black', width=4, dash='dot'), showlegend = False
)

trace3 = go.Scatter(
    x=x,
    y=y1+y_offset,
    mode='lines',
    line=dict(color='blue', width=2), name = 'measured',
    customdata=-y_offset,
    hovertemplate='gauge: %{customdata:.2f} mm'
)

trace4 = go.Scatter(
    x=x,
    y=y2-y_offset,
    mode='lines', name='measured',
    line=dict(color='blue', width=2), showlegend = False,
    customdata=-y_offset,
    hovertemplate='gauge: %{customdata:.2f} mm'
)

# Create a layout for the plot
layout = go.Layout(
    xaxis=dict(
        # range=[-10, 10],
        showgrid=False,
        zeroline=False,
        showticklabels=False
    ),
    yaxis=dict(
        range=[-10, 10],
        showgrid=False,
        zeroline=False,
        showticklabels=False
    ),
    width=800,
    height=500,
    # margin=dict(l=10, r=10, t=10, b=10)
)


# Create a figure object and add the trace to it
fig = go.Figure(data=[trace1,trace2,trace3,trace4], layout=layout)
fig.update_traces(hoverinfo="skip", hovertemplate=None, selector=dict(name='baseline'))
# fig.update_traces(hoverinfo="skip", hovertemplate=None, selector=dict(name='trace2'))
fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

fig.add_annotation(
y=-7,  # arrows' head
x=100,  # arrows' head
ay=7,  # arrows' tail
ax=100,  # arrows' tail
xref='x',
yref='y',
axref='x',
ayref='y',
text='',  # if you want only the arrow
showarrow=True,
arrowhead=2,
arrowsize=1,
arrowwidth=4,
arrowcolor='blue'
)

fig.add_annotation(
y=7,  # arrows' head
x=100,  # arrows' head
ay=-7,  # arrows' tail
ax=100,  # arrows' tail
xref='x',
yref='y',
axref='x',
ayref='y',
text='',  # if you want only the arrow
showarrow=True,
arrowhead=2,
arrowsize=1,
arrowwidth=4,
arrowcolor='blue'
)

fig.add_annotation(
y=0,  # arrows' head
x=110,  # arrows' head
ax=-7,  # arrows' tail
ay=130,  # arrows' tail
xref='x',
yref='y',
axref='x',
ayref='y',
text='1435 mm (not to scale)',  # if you want only the arrow
showarrow=False,
arrowcolor='blue',font = dict(family="Arial", size=18),
textangle=-90
)
# fig.update_annotations(font=dict(family="Arial", size=18, color="red"))

# Show the figure
st.plotly_chart(fig)