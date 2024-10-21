import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Load data from GitHub links
url1 = 'https://raw.githubusercontent.com/marcanthonny/binusmarkeu//refs/heads/main/bin/cleaned_df/LC41.csv'
url2 = 'https://raw.githubusercontent.com/marcanthonny/binusmarkeu/refs/heads/main/bin/cleaned_df/LB41.csv'
url3 = 'https://raw.githubusercontent.com/marcanthonny/binusmarkeu/refs/heads/main/bin/cleaned_df/LA41.csv'

# Data cleaning function
def clean_data(df):
    if 'Delivered Percentage' in df.columns:
        df.rename(columns={'Delivered Percentage': 'Percentage Delivered'}, inplace=True)
    df['Final Profit'] = df['Final Profit'].replace('[\$,]', '', regex=True).astype(float)

    if 'Percentage Delivered' in df.columns:
        df['Percentage Delivered'] = df['Percentage Delivered'].replace('%', '', regex=True).astype(float)
    df['OTIF Percentage'] = df['OTIF Percentage'].replace('%', '', regex=True).astype(float)
    df['Quality Performance'] = df['Quality Performance'].replace('%', '', regex=True).astype(float)
    df['Flow Efficiency'] = df['Flow Efficiency'].replace('%', '', regex=True).astype(float)
    df['Resource Efficiency'] = df['Resource Efficiency'].replace('%', '', regex=True).astype(float)

    if 'Throughout Time' in df.columns:
        df['Throughout Time'] = pd.to_timedelta(df['Throughout Time'], errors='coerce').dt.total_seconds() / 60

    df['Round'] = np.arange(1, len(df) + 1)
    return df

# Load and clean datasets
datalc41 = clean_data(pd.read_csv(url1))
datalb41 = clean_data(pd.read_csv(url2))
datala41 = clean_data(pd.read_csv(url3))

# Title for the dashboard
st.markdown("<h1 style='text-align: center; color: white;'>Performance Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<div style='background-color: darkblue; padding: 10px;'>"
            "<h3 style='color: white;'>Name: Marc Anthony Samuel</h3>"
            "<h3 style='color: white;'>NIM: 2602193982</h3>"
            "<h3 style='color: white;'>Class: LC41</h3>"
            "</div>", unsafe_allow_html=True)

# Show the cleaned data for exploration
st.markdown("### Data Exploration")
st.write("#### Dataset C41")
st.dataframe(datalc41.head())

st.write("#### Dataset B41")
st.dataframe(datalb41.head())

st.write("#### Dataset A41")
st.dataframe(datala41.head())

st.write(""" 
Di ketiga dataset, terdapat beberapa pola yang konsisten:
- Final Profit sangat dipengaruhi oleh metrik efisiensi seperti Flow Efficiency, Percentage Delivered, dan OTIF Percentage.
- Average Stock berkorelasi negatif dengan keuntungan akhir.
- Throughout Time cenderung memiliki korelasi negatif di seluruh data.
""")

# Function to plot the interactive correlation heatmap
def plot_correlation_heatmap(df, title):
    st.subheader(f'Interactive Correlation Matrix for {title}')
    correlation_matrix = df.corr()

    # Create a heatmap using Plotly
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='Blues',
        zmin=-1, zmax=1,
        hoverongaps=False
    ))
    fig.update_layout(title=title, xaxis_nticks=36)
    st.plotly_chart(fig)

# Plot correlation matrices for each dataset
plot_correlation_heatmap(datalc41, "Dataset C41")
plot_correlation_heatmap(datalb41, "Dataset B41")
plot_correlation_heatmap(datala41, "Dataset A41")

# Line Graph for Performance Comparison (Interactive)
def plot_performance_comparison(df, title):
    st.subheader(f'Interactive Performance Comparison for {title}')
    fig = px.line(df, x='Round', 
                  y=['Throughout Time', 'Flow Efficiency', 'Percentage Delivered', 'OTIF Percentage', 'Quality Performance'],
                  labels={'value': 'Performance Metrics', 'variable': 'Metric'}, 
                  title=f'Performance Comparison in {title}')
    st.plotly_chart(fig)

# Plot performance comparison for each dataset
plot_performance_comparison(datalc41, "Dataset C41")
plot_performance_comparison(datalb41, "Dataset B41")
plot_performance_comparison(datala41, "Dataset A41")

# Final notes or conclusion
st.write("""
### Kesimpulan:
- Waktu Penyelesaian adalah metrik yang paling tidak stabil.
- Efisiensi Aliran dan Persentase Pengiriman secara konsisten meningkat.
- Dataset A41 menunjukkan lonjakan paling ekstrem pada Waktu Penyelesaian.
""")