import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# Set page title and favicon
st.set_page_config(page_title="Chainage Readings Forecast", page_icon=":tram:")
st.title("Chainage Readings Forecast")
st.info(""" This app presents sample readings and forecast readings. Forecast readings have been calculated based on the following -  \n
    - Linear degradation assumption  \n
    - User-defined parameters in the sidebar """)

st.set_option('deprecation.showPyplotGlobalUse', False)

no_of_years = st.sidebar.number_input("Number of years to forecast", min_value=1, max_value=5, value=3, step=1)
degradation_factor  = st.sidebar.slider("Degradation Factor (in mm/year)", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

# reading gauge file
gauge = pd.read_csv('gauge.csv',usecols=['gauge'])
representative_distance = 7 #half-width of rail

# Define the x and y coordinates of the railway track
x = np.arange(0,len(gauge))
y1 = -7*np.ones_like(x)
y2 = 7*np.ones_like(x)
y_offset = gauge['gauge'].values/2 
y_offset_degradation =  y_offset + no_of_years*degradation_factor/2 #his will be changed based on feedback from Ngee Hung

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

# forecasts
trace5 = go.Scatter(
    x=x,
    y=y1+y_offset_degradation,
    opacity=0.8,
    mode='lines',
    line=dict(color='orange', width=2), name = 'forecast',
    customdata=-y_offset_degradation,
    hovertemplate='gauge: %{customdata:.2f} mm'
)

trace6 = go.Scatter(
    x=x,
    y=y2-y_offset_degradation,
    opacity=0.8,
    mode='lines', name='forecast',
    line=dict(color='orange', width=2), showlegend = False,
    customdata=-y_offset_degradation,
    hovertemplate='gauge: %{customdata:.2f} mm'
)

# Create a layout for the plot
layout = go.Layout(
    xaxis=dict(
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
    height=500
)

# Create a figure object and add the trace to it
fig = go.Figure(data=[trace1,trace2,trace3,trace4,trace5,trace6], layout=layout)
fig.update_traces(hoverinfo="skip", hovertemplate=None, selector=dict(name='baseline'))
fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

st.plotly_chart(fig)