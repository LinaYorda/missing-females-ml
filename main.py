import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

missing=pd.read_csv("data_csv/missing_famales_dropped_NaN.csv")

html_file_path="html/clusters_with_noise.html"



menu = ["Home", "KMeans Clustering"]
choice = st.sidebar.radio("Menu", menu)
st.sidebar.write("**About**: This project analyses data from missing Females in the USA, downloaded from [Kaggle](https://www.kaggle.com/datasets/ahmedemadeldin/missing-females-in-us/data).This dataset contains records of females reported missing across various states in the United States from the year 1944 to 2020. In addition, the author added MP cases across the globe.The study faces limitations due to the significant amount of missing data, which might have introduced bias in the analysis. The filtering out of cases with missing information may also have excluded relevant cases that could affect the generalizability of the findings. ")

if choice == "Home":
    st.title("Missing Female Data Analysis (1944-2020)")
    st.write("Welcome to the Home page! Use the sidebar to navigate through the app.")
    
    st.header("Spatial Clustering with noise")
    # Read the HTML file
    with open(html_file_path, 'r') as f:
        html_content = f.read()
    # Display the HTML file in the Streamlit app
    st.components.v1.html(html_content, width=800, height=600)
    
    st.header("Data Table")
    st.write("Here is the cleaned data table:")
    st.dataframe(missing)
    
    csv = missing.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download data as CSV", data=csv, file_name='data.csv', mime='text/csv')

elif choice == "KMeans Clustering":
    st.title("K-Means Clustering")
    st.write("Adjust the number of clusters:")
    n_clusters = st.slider("Number of clusters", 1, 10, 3)
    
    if 'latitude' in missing.columns and 'longitude' in missing.columns:
        kmeans = KMeans(n_clusters=n_clusters)
        missing['Cluster'] = kmeans.fit_predict(missing[['latitude', 'longitude']])
        
        st.write("Clustered Data:")
        st.dataframe(missing)
        
        # Scatter plot of the clusters
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=missing, x='longitude', y='latitude', hue='Cluster', palette='viridis', legend='full')
        plt.scatter(kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 0], s=100, c='red', label='Centroids')
        plt.legend()
        st.pyplot(plt)
    else:
        st.error("The data does not contain 'latitude' and 'longitude' columns required for clustering.")
