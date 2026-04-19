import plotly.express as px
import pandas as pd

def generate_priority_chart(tasks_df):
    if tasks_df.empty:
        return None
    priority_counts = tasks_df["priority"].value_counts().reset_index()
    priority_counts.columns = ["Priority", "Count"]
    
    # Use distinct colors for Low, Medium, High
    color_map = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}
    
    fig = px.pie(
        priority_counts, 
        names="Priority", 
        values="Count", 
        title="Task Priority Distribution",
        color="Priority",
        color_discrete_map=color_map,
        hole=0.4
    )
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    return fig

def generate_availability_histogram(volunteers_df):
    if volunteers_df.empty:
        return None
    
    fig = px.histogram(
        volunteers_df, 
        x="availability", 
        nbins=10, 
        title="Volunteer Availability Breakdown",
        labels={"availability": "Hours Available"}
    )
    fig.update_layout(bargap=0.1, margin=dict(t=40, b=0, l=0, r=0))
    # Streamlit friendly dark theme style
    fig.update_traces(marker_color='#3b82f6')
    return fig
