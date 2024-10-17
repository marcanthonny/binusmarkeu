import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load CSV data from GitHub
url_c41 = 'https://raw.githubusercontent.com/marcanthonny/binusmarkeu/refs/heads/main/bin/cleaned_df/LC41.csv'
url_b41 = 'https://raw.githubusercontent.com/marcanthonny/binusmarkeu/refs/heads/main/bin/cleaned_df/LB41.csv'
url_a41 = 'https://raw.githubusercontent.com/marcanthonny/binusmarkeu/refs/heads/main/bin/cleaned_df/LA41.csv'

datalc41 = pd.read_csv(url_c41)
datalb41 = pd.read_csv(url_b41)
datala41 = pd.read_csv(url_a41)

# Data cleaning function
def clean_data(df):
    df['Final Profit'] = df['Final Profit'].replace('[\$,]', '', regex=True).astype(float)
    df['Percentage Delivered'] = df['Percentage Delivered'].replace('%', '', regex=True).astype(float)  # Updated line
    df['OTIF Percentage'] = df['OTIF Percentage'].replace('%', '', regex=True).astype(float)
    df['Quality Performance'] = df['Quality Performance'].replace('%', '', regex=True).astype(float)
    df['Flow Efficiency'] = df['Flow Efficiency'].replace('%', '', regex=True).astype(float)
    df['Resource Efficiency'] = df['Resource Efficiency'].replace('%', '', regex=True).astype(float)
    
    # Convert Throughout Time to minutes
    df['Throughout Time'] = pd.to_timedelta(df['Throughout Time']).dt.total_seconds() / 60
    return df

# Clean datasets
datalc41 = clean_data(datalc41)
datalb41 = clean_data(datalb41)
datala41 = clean_data(datala41)

# Split data into rounds
datalc41['Round'] = (datalc41.index // (len(datalc41) // 3)) + 1
datalb41['Round'] = (datalb41.index // (len(datalb41) // 3)) + 1
datala41['Round'] = (datala41.index // (len(datala41) // 3)) + 1

# Function to plot correlation matrix heatmap
def plot_correlation_heatmap(df, title):
    correlation_matrix = df.corr()
    plt.figure(figsize=(10, 8))
    plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
    plt.colorbar()
    plt.xticks(range(len(correlation_matrix)), correlation_matrix.columns, rotation=45)
    plt.yticks(range(len(correlation_matrix)), correlation_matrix.columns)
    plt.title(f'Correlation Matrix for {title}')
    st.pyplot(plt)  # Render the plot in Streamlit
    plt.clf()  # Clear the figure for the next plot

# Function to plot line charts
def plot_line_chart(df, title):
    plt.figure(figsize=(12, 6))
    
    for col in df.columns[1:-1]:  # Exclude 'Final Profit' and 'Round'
        plt.plot(df['Round'], df[col], marker='o', label=col)
    
    plt.title(title)
    plt.xlabel('Round')
    plt.ylabel('Performance')
    plt.xticks(np.arange(1, 4, 1))  # Show ticks for 3 rounds
    plt.legend()
    plt.grid()
    st.pyplot(plt)  # Render the plot in Streamlit
    plt.clf()  # Clear the figure for the next plot

# Display the plots
st.title('Performance Analysis Dashboard')
st.markdown("<h1 style='text-align: center; color: white; background-color: darkblue;'>Performance Analysis</h1>", unsafe_allow_html=True)

# Description for Correlation Matrix
st.markdown("""
Di ketiga dataset, terdapat beberapa pola yang konsisten:

Final Profit (Keuntungan Akhir) sangat dipengaruhi oleh metrik efisiensi seperti Flow Efficiency (Efisiensi Aliran), Percentage Delivered (Persentase Pengiriman), dan OTIF Percentage (Persentase Tepat Waktu dan Lengkap). Perusahaan yang ingin meningkatkan keuntungan harus fokus pada peningkatan ketepatan pengiriman, efisiensi aliran, dan meminimalkan tingkat stok.
Average Stock (Rata-rata Stok) secara konsisten berkorelasi negatif dengan keuntungan akhir, yang menyiratkan bahwa mengurangi tingkat inventaris secara signifikan dapat meningkatkan profitabilitas.
Throughout Time (Waktu Proses) cenderung memiliki korelasi negatif di seluruh data, yang menunjukkan bahwa pengurangan waktu proses atau lead time dapat meningkatkan berbagai metrik kinerja.
""")

# Correlation Matrices
st.subheader("Correlation Matrix for Dataset C41")
plot_correlation_heatmap(datalc41, "Dataset C41")

st.subheader("Correlation Matrix for Dataset B41")
plot_correlation_heatmap(datalb41, "Dataset B41")

st.subheader("Correlation Matrix for Dataset A41")
plot_correlation_heatmap(datala41, "Dataset A41")

# Description for Line Graphs
st.markdown("""
### Analisis:
**Dataset C41:**
Waktu Penyelesaian (coklat) menunjukkan penurunan signifikan dari putaran 1 ke putaran 3, dimulai di atas 350 dan turun mendekati 100.
Efisiensi Aliran (merah) dimulai rendah dan meningkat secara bertahap, menunjukkan peningkatan efisiensi aliran di setiap putaran.
Metrik lainnya menunjukkan peningkatan bertahap (Persentase Pengiriman, OTIF, Kinerja Kualitas) atau mempertahankan nilai yang stabil dengan sedikit variasi.

**Dataset B41:**
Waktu Penyelesaian (coklat) menunjukkan tren penurunan yang konsisten, mirip dengan C41 tetapi dimulai sekitar 300.
Metrik lain seperti Efisiensi Aliran dan Persentase Pengiriman menunjukkan peningkatan konsisten di setiap putaran, mirip dengan C41.
Kategori lainnya relatif stabil dengan perubahan kecil antara putaran.

**Dataset A41:**
Waktu Penyelesaian (coklat) memiliki pola paling dramatis: dimulai dari 200 di putaran 1, kemudian menunjukkan lonjakan tajam di atas 1000 pada putaran 3.
Metrik lainnya (Persentase Pengiriman, OTIF, Efisiensi Aliran, Kinerja Kualitas) hanya menunjukkan sedikit perubahan atau performa yang stabil di setiap putaran.

**Kesimpulan:**
Waktu Penyelesaian adalah metrik yang paling tidak stabil, menunjukkan fluktuasi besar di antara dataset dan putaran.

Efisiensi Aliran dan Persentase Pengiriman secara konsisten meningkat di semua dataset.

Dataset A41 menunjukkan lonjakan paling ekstrem pada Waktu Penyelesaian, sedangkan dataset lainnya, C41 dan B41, mengalami penurunan signifikan.

Secara keseluruhan, sebagian besar metrik tampaknya meningkat atau tetap stabil, kecuali Waktu Penyelesaian yang menunjukkan perilaku berbeda di setiap dataset.
""")

# Line Charts
st.subheader("Performance Comparison in Dataset C41")
plot_line_chart(datalc41, "Dataset C41 Performance")

st.subheader("Performance Comparison in Dataset B41")
plot_line_chart(datalb41, "Dataset B41 Performance")

st.subheader("Performance Comparison in Dataset A41")
plot_line_chart(datala41, "Dataset A41 Performance")
