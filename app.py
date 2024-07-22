import streamlit as st
import folium
from streamlit_folium import st_folium


import os
import ast

import pandas as pd

# Function to load DataFrame from CSV
def load_data(file_path):
    return pd.read_csv(file_path)

# Path to the CSV file
csv_file_path = 'output.csv'  # Update this path to your CSV file

# Load the data
df = load_data(csv_file_path)
# Function to extract latitude and longitude from map_details
def extract_lat_long(map_details):
    try:
        # Convert string to tuple
        details = ast.literal_eval(map_details)
        # Check if latitude and longitude are valid
        lat, lon = details[1], details[2]
        if lat and lon:
            return lat, lon
        else:
            return None, None
    except:
        return None, None

# Apply function to DataFrame
df[['latitude', 'longitude']] = df['map_details'].apply(lambda x: pd.Series(extract_lat_long(x)))

# Filter out rows with missing latitude or longitude
df = df.dropna(subset=['latitude', 'longitude'])

# Rename youtube_video_link column to video_url
df = df.rename(columns={'youtube_video_link': 'video_url'})

# Drop the original map_details column
df = df.drop(columns=['map_details'])

print(df)
df.to_csv('refined_map.csv')

# Create a map centered at a specific location
map_center = [df['latitude'].mean(), df['longitude'].mean()]
mymap = folium.Map(location=map_center, zoom_start=6)

# Function to create an HTML iframe for the video popup
def create_video_popup(video_url):
    html = f'''
    <iframe width="560" height="315" src="{video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    '''
    return folium.Popup(html, max_width=560)

# Add markers to the map with video popups from the DataFrame
for _, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=create_video_popup(row['video_url'])
    ).add_to(mymap)

# Render the map in Streamlit
st_folium(mymap, width=800, height=600)