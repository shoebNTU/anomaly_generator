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
y = np.arange(0,200)
x1 = -7*np.ones_like(y)
x2 = 7*np.ones_like(y)
x_offset = np.sin(np.linspace(0,np.radians(360),len(y)))/2 

# Create a scatter trace for the railway track
trace1 = go.Scatter(
    x=x1,
    y=y,
    mode='lines',
    line=dict(color='black', width=4, dash='dot'), name = 'label1'
)

trace2 = go.Scatter(
    x=x2,
    y=y,
    mode='lines', name='label1',
    line=dict(color='black', width=4, dash='dot'), showlegend = False
)

trace3 = go.Scatter(
    x=x1+x_offset,
    y=y,
    mode='lines',
    line=dict(color='black', width=4), name = 'label2',
    customdata=-x_offset,
    hovertemplate='gauge: %{customdata:.2f} mm'
)

trace4 = go.Scatter(
    x=x2-x_offset,
    y=y,
    mode='lines', name='label2',
    line=dict(color='black', width=4), showlegend = False,
    customdata=-x_offset,
    hovertemplate='gauge: %{customdata:.2f} mm'
)

# Create a layout for the plot
layout = go.Layout(
    xaxis=dict(
        range=[-10, 10],
        showgrid=False,
        zeroline=False,
        showticklabels=False
    ),
    yaxis=dict(
        # range=[-1, 10],
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
fig.update_traces(hoverinfo="skip", hovertemplate=None, selector=dict(name='label1'))
# fig.update_traces(hoverinfo="skip", hovertemplate=None, selector=dict(name='trace2'))
fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

fig.add_annotation(
x=-7,  # arrows' head
y=100,  # arrows' head
ax=7,  # arrows' tail
ay=100,  # arrows' tail
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
x=7,  # arrows' head
y=100,  # arrows' head
ax=-7,  # arrows' tail
ay=100,  # arrows' tail
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
x=0,  # arrows' head
y=110,  # arrows' head
ax=-7,  # arrows' tail
ay=130,  # arrows' tail
xref='x',
yref='y',
axref='x',
ayref='y',
text='1435 mm (not to scale)',  # if you want only the arrow
showarrow=False,
arrowcolor='blue',font = dict(family="Arial", size=18)
)
# fig.update_annotations(font=dict(family="Arial", size=18, color="red"))

# Show the figure
st.plotly_chart(fig)