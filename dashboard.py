import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

# Set page config
st.set_page_config(page_title="Performance Dashboard", layout="wide")

# Load data from GitHub CSV links
@st.cache_data
def load_data():
    datalc41 = pd.read_csv('https://raw.githubusercontent.com/your_username/your_repo/main/datalc41.csv')
    datalb41 = pd.read_csv('https://raw.githubusercontent.com/your_username/your_repo/main/datalb41.csv')
    datala41 = pd.read_csv('https://raw.githubusercontent.com/your_username/your_repo/main/datala41.csv')
    return datalc41, datalb41, datala41

datalc41, datalb41, datala41 = load_data()

# Function to clean the dataset
def clean_data(df):
    df['Final Profit'] = df['Final Profit'].replace('[\$,]', '', regex=True).astype(float)
    df['Percentage Delivered'] = df['Percentage Delivered'].replace('%', '', regex=True).astype(float)
    df['OTIF Percentage'] = df['OTIF Percentage'].replace('%', '', regex=True).astype(float)
    df['Quality Performance'] = df['Quality Performance'].replace('%', '', regex=True).astype(float)
    df['Flow Efficiency'] = df['Flow Efficiency'].replace('%', '', regex=True).astype(float)
    df['Resource Efficiency'] = df['Resource Efficiency'].replace('%', '', regex=True).astype(float)

    # Convert Throughout Time to minutes
    def convert_to_minutes(time_str):
        match = re.match(r'(\d+):(\d+)\.(\d+)', time_str)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = int(match.group(3))
            total_minutes = hours * 60 + minutes + seconds / 60
            return total_minutes
        else:
            return None  # Return None if the format doesn't match
    
    df['Throughout Time'] = df['Throughout Time'].apply(convert_to_minutes)
    return df

# Clean each dataset
datalc41 = clean_data(datalc41)
datalb41 = clean_data(datalb41)
datala41 = clean_data(datala41)

# Add round column
for df in [datalc41, datalb41, datala41]:
    df['Round'] = (df.index // (len(df) // 3)) + 1  # Assign round based on row index

# Create correlation matrices
correlation_matrix_c41 = datalc41.corr()
correlation_matrix_b41 = datalb41.corr()
correlation_matrix_a41 = datala41.corr()

# Function to plot correlation heatmap
def plot_correlation_heatmap(correlation_matrix, title):
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt=".2f", linewidths=0.5)
    plt.title(title)
    st.pyplot(plt)

# Plot heatmaps for each dataset
st.sidebar.header("Correlation Heatmaps")
st.subheader("Correlation Heatmap for Dataset C41")
plot_correlation_heatmap(correlation_matrix_c41, "Correlation Matrix Heatmap for datalc41")
st.subheader("Correlation Heatmap for Dataset B41")
plot_correlation_heatmap(correlation_matrix_b41, "Correlation Matrix Heatmap for datalb41")
st.subheader("Correlation Heatmap for Dataset A41")
plot_correlation_heatmap(correlation_matrix_a41, "Correlation Matrix Heatmap for datala41")

# Prepare data for line plots
def prepare_line_plot_data(df):
    return pd.melt(df, id_vars='Round', value_vars=[
        'Percentage Delivered', 'OTIF Percentage', 'Quality Performance', 
        'Flow Efficiency', 'Resource Efficiency', 'Throughout Time'
    ])

# Melt dataframes to long format for line plots
melted_c41 = prepare_line_plot_data(datalc41)
melted_b41 = prepare_line_plot_data(datalb41)
melted_a41 = prepare_line_plot_data(datala41)

# Line plots
st.subheader("Performance Comparison Across Rounds")
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Plot for each dataset
for ax, melted, title in zip(axes, [melted_c41, melted_b41, melted_a41], 
                              ['Dataset C41', 'Dataset B41', 'Dataset A41']):
    sns.lineplot(data=melted, x='Round', y='value', hue='variable', marker='o', ax=ax)
    ax.set_title(f'Performance Comparison in {title}')
    ax.set_xlabel('Round')
    ax.set_ylabel('Value')
    ax.set_xticks([1, 2, 3])
    ax.legend(title='Categories', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
st.pyplot(fig)
