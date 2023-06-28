import streamlit as st
import pysketcher as ps
import matplotlib.pyplot as plt
from pysketcher.backend.matplotlib import MatplotlibBackend

# Set page title and favicon
st.set_page_config(page_title="Sketch Generator", page_icon=":bar_chart:")
st.title("Parametric sketch generator")
st.sidebar.info(""" This app helps you sketch gauges of different lengths.""")
length = st.sidebar.slider("Gauge Length", min_value=12.0, max_value=15.0, value=(14.0), step=0.1)
st.set_option('deprecation.showPyplotGlobalUse', False)

if st.sidebar.button("Generate sketch"):
    # figure = plt.figure(figsize=(8, 6))
    figure = ps.Figure(0.0, 1.0, 0.0, 1.0, MatplotlibBackend) # assuming this is 20x20
    
    left_point_x = (10 - length/2)/20
    right_point_x = (10 + length/2)/20
    a = ps.Point(left_point_x, 0.0)
    b = ps.Point(left_point_x, 1.0)
    line_1 = ps.Line(a, b)

    a = ps.Point(right_point_x, 0.0)
    b = ps.Point(right_point_x, 1.0)
    line_2 = ps.Line(a,b)

    text1 = ps.Text(length, ps.Point(0.5,0.51))
    text1.style.line_color = ps.TextStyle.Color.BLUE
    dim1 = ps.DoubleArrow(ps.Point(left_point_x, 0.5), ps.Point(right_point_x, 0.50)) # ps.LinearDimension('\n', ps.Point(left_point_x, 0.0), ps.Point(right_point_x, 0.0))
    dim1.style.line_color = ps.Style.Color.BLUE
     #style.line_color = ps.Style.Color.BLUE
    dim1.offset_style = ps.LinearDimension.OffsetStyle.HORIZONTAL
    # dim1.offset_style = ps.LinearDimension.OffsetStyle.HORIZONTAL
    # double_arrow = ps.DoubleArrow(
    # ps.Point(left_point_x, 0.5),
    # ps.Point(right_point_x, 0.5))
 

    figure.add(line_1)
    figure.add(line_2)
    figure.add(dim1)
    figure.add(text1)
    st.pyplot(figure.show())


