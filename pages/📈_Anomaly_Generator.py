import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

# Set page title and favicon
st.set_page_config(page_title="Anomaly Dataset Generator", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title("Anomaly Dataset Generator")
st.info(""" This app enables you to create custom dummy data with following controls - 
- Measurement attribute name
- Number of samples
- Percentage of anomalies
- Threshold interval (acceptable range of values)  \n
Finally, you can visualize and download the generated dataset in the form of a csv file. 
""")

# Define user input fields

name = st.sidebar.text_input('Enter measurement attribute', value='Gauge', placeholder='unnamed')
num_samples = st.sidebar.number_input("Number of samples", min_value=1, max_value=10000, value=100, step=1)
num_features = 1
# num_features = st.sidebar.number_input("Number of features", min_value=1, max_value=10, value=2, step=1)
contamination = st.sidebar.slider("Percentage of anomalies", min_value=0.0, max_value=100.0, value=(10.0), step=1.0)
feature_range = st.sidebar.slider("Threshold interval", min_value=0.0, max_value=10.0, value=(4.0,6.0), step=0.1)

# Generate anomaly dataset
if st.sidebar.button("Generate dataset"):
    start = feature_range[0]
    end = feature_range[1]
    np.random.seed(123)
    time_series = np.random.uniform(start, end, num_samples)
    # now randomly select integers in the range of n
    np.random.seed(123)
    anomalous_size = round(contamination*num_samples/100.0)
    anomalous_size_upper = anomalous_size//2
    anomalous_size_lower = anomalous_size - anomalous_size_upper
    anomalous_indices = np.random.choice(num_samples, size = anomalous_size, replace=False) 
    outliers = np.concatenate((np.random.uniform(start-1,start, anomalous_size_upper), 
                        np.random.uniform(end+0.1,end+1, anomalous_size_lower)))
    outliers_categorical = np.zeros_like(time_series)
    outliers_categorical[anomalous_indices] = 1
    time_series[anomalous_indices] = outliers
    df = pd.DataFrame({'values':list(time_series.reshape(-1,)),'anomaly':outliers_categorical})
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['values'],x=df.index, mode='lines', name='Inliers'))
    fig.add_trace(go.Scatter(y=outliers, x=anomalous_indices, mode='markers', name='Outliers',marker=dict(color='red')))
    # Add two horizontal dotted lines
    fig.add_hline(y=start, line=dict(color='red', width=2, dash='dot'))
    fig.add_hline(y=end, line=dict(color='orange', width=2, dash='dot'))
    fig.update_layout(xaxis_title='Sample number', yaxis_title='Measurement value', title=f'Generated data for {name}')
    # Add a grid to the x and y axes
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    st.plotly_chart(fig, use_container_width=True)   

    # Convert the dataframe to CSV and create a download button
    csv = convert_df(df)
    if len(name) == 0:
        name = 'unnamed'
    st.download_button(label='Download dataset', data=csv, file_name=f'{name}.csv', mime='text/csv')

