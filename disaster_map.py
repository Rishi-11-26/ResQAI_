import streamlit as st
import pandas as pd
import numpy as np

def show_map(volunteers_df, tasks_df=pd.DataFrame()):
    if volunteers_df.empty and tasks_df.empty:
        st.warning("No location data available for map.")
        return

    # Combine locations. For real apps, we'd geocode "location" string to lat/long.
    # Here we mock coordinates around a center point (e.g. Hyderabad, India roughly 17.38, 78.48)
    
    map_data = []

    # Mock Volunteers
    for idx, row in volunteers_df.iterrows():
        # Random variance for display purposes
        lat = 17.3850 + np.random.uniform(-0.05, 0.05)
        lon = 78.4867 + np.random.uniform(-0.05, 0.05)
        map_data.append({
            "lat": lat, 
            "lon": lon, 
            "name": row.get("name", "Volunteer"),
            "type": "Volunteer",
            "color": "#10b981", # Green
            "size": 15
        })

    # Mock Tasks
    for idx, row in tasks_df.iterrows():
        lat = 17.3850 + np.random.uniform(-0.05, 0.05)
        lon = 78.4867 + np.random.uniform(-0.05, 0.05)
        map_data.append({
            "lat": lat, 
            "lon": lon, 
            "name": row.get("task_name", "Task"),
            "type": "Task",
            "color": "#ef4444", # Red
            "size": 25
        })

    md_df = pd.DataFrame(map_data)
    
    if not md_df.empty:
        # Standard Streamlit map
        st.map(md_df, latitude="lat", longitude="lon", color="color", size="size")
