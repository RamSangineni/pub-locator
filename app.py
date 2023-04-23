import streamlit as st
import pandas as pd
import numpy as np
import os
import folium
from streamlit_folium import folium_static
from sklearn.metrics.pairwise import euclidean_distances

def main():
    os.chdir('C:/Users/ramsa/Downloads/pubs locator streamlit/streamlitvenv')
    df = pd.read_csv('cleaned_df.csv')
    menu = ["Home", "Map", "Find_Nearest_Pubs"]
    choice = st.sidebar.selectbox("Select a page", menu)

    if choice == "Home":
        show_home_page(df)
    elif choice == "Map":
        Map(df)  # Pass the df DataFrame as an argument
    elif choice == "Find_Nearest_Pubs":
        Find_Nearest_Pubs(df)

# Rest of the code


def show_home_page(df):

    st.sidebar.title('General Information')
    st.title('Welcome to Club Locator(UK)')
    shape = df.shape
    total_LA = df['Local_Authority'].nunique()
    grouped = df.loc[:,['Name','Local_Authority']].groupby('Local_Authority')
    st.sidebar.header('Total Pubs: ')
    st.sidebar.write(str(int(shape[0])))
    st.sidebar.header('Total Local Authorities :')
    st.sidebar.write(str(total_LA))
    st.sidebar.header('Pubs grouped by Local Authority')
    st.sidebar.write(grouped.count())
    st.header('Head of the dataset')
    st.write(df.head(5))
    st.header('Columns present in the dataset')
    st.write(df.columns)

def Map(df):
    # Create a Streamlit app
    st.title("Pub Maps")

    # Display a selectbox to choose the search criteria (Postal Code or Local Authority)
    search_criteria = st.selectbox("Search Criteria", ["Postal Code", "Local Authority"])

    # Display a text input field for user to input the search term
    search_term = st.text_input("Enter Search Term")

    # Filter the data based on the search criteria and search term
    if search_criteria == "Postal Code":
        filtered_df = df[df['Postal Code'].str.contains(search_term, case=False)]
    else:
        filtered_df = df[df['Local_Authority'].str.contains(search_term, case=False)]

    # Display the filtered data
    if not filtered_df.empty:
        st.write(filtered_df)

        # Create folium map object centered at a specific latitude and longitude
        # You can choose any latitude and longitude as the initial center of the map
        latitude = filtered_df['Latitude'].mean()
        longitude = filtered_df['Longitude'].mean()
        m = folium.Map(location=[latitude, longitude], zoom_start=12)

        # Add markers to the map based on the latitude and longitude data
        for index, row in filtered_df.iterrows():
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"Name: {row['Name']}<br>Address: {row['Address']}<br>Postal Code: {row['Postal Code']}<br>Local Authority: {row['Local_Authority']}"
            ).add_to(m)

        # Display the map in Streamlit
        folium_static(m, height=400, width=800)
    else:
        st.write("No results found.")

    
    

def Find_Nearest_Pubs(df):
    st.title("Find the 5 Nearest Pubs")
    st.write("Enter your latitude and longitude below:")

    # Get user input for latitude and longitude
    user_latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, step=0.0001)
    user_longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, step=0.0001)

    # Calculate Euclidean distances from user's latitude and longitude to each pub's latitude and longitude
    df['Distance'] = euclidean_distances(df[['Latitude', 'Longitude']], [[user_latitude, user_longitude]])
    # Sort the pubs by distance and get the nearest 5 pubs
    nearest_pubs = df.sort_values('Distance').head(5)

    # Create folium map object centered at user's latitude and longitude
    m = folium.Map(location=[user_latitude, user_longitude], zoom_start=12)

    # Add markers to the map for the nearest pubs
    for index, row in nearest_pubs.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"Name: {row['Name']}<br>Address: {row['Address']}<br>Postal Code: {row['Postal Code']}<br>Local Authority: {row['Local_Authority']}"
        ).add_to(m)

    # Display the map in Streamlit
    folium_static(m, height=400, width=800)

    # Display the nearest pubs in a list below the map
    if not nearest_pubs.empty:
        st.write(nearest_pubs)
    else:
        st.write("No results found.")
    



if __name__=="__main__":
    main()

