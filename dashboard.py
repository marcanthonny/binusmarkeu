import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Load data from GitHub links
url1 = 'https://raw.githubusercontent.com/marcanthonny/binusmarkeu/refs/heads/main/bin/cleaned_df/LC41.csv'
url2 = 'https://raw.githubusercontent.com/marcanthonny/binusmarkeu/refs/heads/main/bin/cleaned_df/LB41.csv'
url3 = 'https://raw.githubusercontent.com/marcanthonny/binusmarkeu/refs/heads/main/bin/cleaned_df/LA41.csv'

# Data cleaning function
def clean_data(df):
    # Rename 'Delivered Percentage' to 'Percentage Delivered' if it exists
    if 'Delivered Percentage' in df.columns:
        df.rename(columns={'Delivered Percentage': 'Percentage Delivered'}, inplace=True)

    # Clean 'Final Profit'
    df['Final Profit'] = df['Final Profit'].replace('[\$,]', '', regex=True).astype(float)

    # Check if the column exists before replacing
    if 'Percentage Delivered' in df.columns:
        df['Percentage Delivered'] = df['Percentage Delivered'].replace('%', '', regex=True).astype(float)

    # Clean other percentage columns
    df['OTIF Percentage'] = df['OTIF Percentage'].replace('%', '', regex=True).astype(float)
    df['Quality Performance'] = df['Quality Performance'].replace('%', '', regex=True).astype(float)
    df['Flow Efficiency'] = df['Flow Efficiency'].replace('%', '', regex=True).astype(float)
    df['Resource Efficiency'] = df['Resource Efficiency'].replace('%', '', regex=True).astype(float)

    # Convert Throughout Time to minutes if it exists
    if 'Throughout Time' in df.columns:
        try:
            df['Throughout Time'] = pd.to_timedelta(df['Throughout Time'], errors='coerce').dt.total_seconds() / 60
        except Exception as e:
            st.error(f"Error converting 'Throughout Time': {e}")

    # Add 'Round' column
    df['Round'] = np.arange(1, len(df) + 1)  # Creates a sequential 'Round' column

    return df

# Load and clean datasets
datalc41 = clean_data(pd.read_csv(url1))
datalb41 = clean_data(pd.read_csv(url2))
datala41 = clean_data(pd.read_csv(url3))

# Title for the dashboard
st.title("Performance Analysis Dashboard")

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
st.dataframe(datalc41.head())  # Display first few rows of the cleaned LC41 dataset

st.write("#### Dataset B41")
st.dataframe(datalb41.head())  # Display first few rows of the cleaned LB41 dataset

st.write("#### Dataset A41")
st.dataframe(datala41.head())  # Display first few rows of the cleaned LA41 dataset

# Description for correlation matrix
st.write(""" 
Di ketiga dataset, terdapat beberapa pola yang konsisten:

Final Profit (Keuntungan Akhir) sangat dipengaruhi oleh metrik efisiensi seperti Flow Efficiency (Efisiensi Aliran), Percentage Delivered (Persentase Pengiriman), dan OTIF Percentage (Persentase Tepat Waktu dan Lengkap). Perusahaan yang ingin meningkatkan keuntungan harus fokus pada peningkatan ketepatan pengiriman, efisiensi aliran, dan meminimalkan tingkat stok.

Average Stock (Rata-rata Stok) secara konsisten berkorelasi negatif dengan keuntungan akhir, yang menyiratkan bahwa mengurangi tingkat inventaris secara signifikan dapat meningkatkan profitabilitas.

Throughout Time (Waktu Proses) cenderung memiliki korelasi negatif di seluruh data, yang menunjukkan bahwa pengurangan waktu proses atau lead time dapat meningkatkan berbagai metrik kinerja.
""")

# Function to plot the correlation matrix
def plot_correlation_heatmap(df, title):
    st.subheader(f'Correlation Matrix for {title}')
    correlation_matrix = df.corr()

    # Create a heatmap using matplotlib
    plt.figure(figsize=(10, 8))
    plt.imshow(correlation_matrix, cmap='Blues', aspect='auto')
    plt.colorbar()

    # Set ticks and labels
    plt.xticks(ticks=np.arange(len(correlation_matrix.columns)), labels=correlation_matrix.columns, rotation=45)
    plt.yticks(ticks=np.arange(len(correlation_matrix.columns)), labels=correlation_matrix.columns)

    # Show the plot
    st.pyplot(plt)

# Plot correlation matrices for each dataset
plot_correlation_heatmap(datalc41, "Dataset C41")
plot_correlation_heatmap(datalb41, "Dataset B41")
plot_correlation_heatmap(datala41, "Dataset A41")

# Line Graph for Performance Comparison
def plot_performance_comparison(df, title):
    st.subheader(f'Performance Comparison for {title}')

    # Melt the dataframe for easier plotting
    melted_df = df.melt(id_vars=['Round'], 
                        value_vars=['Throughout Time', 'Flow Efficiency', 'Percentage Delivered', 'OTIF Percentage', 'Quality Performance'])
    
    # Create the line plot
    plt.figure(figsize=(14, 8))
    for variable in melted_df['variable'].unique():
        subset = melted_df[melted_df['variable'] == variable]
        plt.plot(subset['Round'], subset['value'], marker='o', label=variable)

    plt.title(f'Performance Comparison in {title}')
    plt.xlabel('Round')
    plt.ylabel('Values')
    plt.legend()
    plt.grid()

    # Show the plot
    st.pyplot(plt)

# Plot performance comparison for each dataset
plot_performance_comparison(datalc41, "Dataset C41")
plot_performance_comparison(datalb41, "Dataset B41")
plot_performance_comparison(datala41, "Dataset A41")

# Final notes or conclusion if needed
st.write("""
### Kesimpulan:
Waktu Penyelesaian adalah metrik yang paling tidak stabil, menunjukkan fluktuasi besar di antara dataset dan putaran.

Efisiensi Aliran dan Persentase Pengiriman secara konsisten meningkat di semua dataset.

Dataset A41 menunjukkan lonjakan paling ekstrem pada Waktu Penyelesaian, sedangkan dataset lainnya, C41 dan B41, mengalami penurunan signifikan.

Secara keseluruhan, sebagian besar metrik tampaknya meningkat atau tetap stabil, kecuali Waktu Penyelesaian yang menunjukkan perilaku berbeda di setiap dataset.
""")
