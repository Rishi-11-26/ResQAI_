import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

from data_store import (
    add_volunteer, get_volunteers,
    add_task, get_tasks,
    add_resource, get_resources,
)
from volunteer_matching import match_volunteers
from task_prediction import predict_task_priority
from gemini_ai import ai_recommendation, check_client
from disaster_map import show_map
from analytics_dashboard import generate_priority_chart, generate_availability_histogram

# Load environment variables
load_dotenv()

# Attempt to initialize Gemini check early
check_client()

# ================================
# Page Setup & Custom CSS
# ================================
st.set_page_config(page_title="ResQAI - AI Coordinator", layout="wide", page_icon="🚑")

st.markdown("""
<style>
    .hero-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
    }
    .hero-header h1 {
        margin: 0;
        font-weight: 800;
        font-family: 'Inter', sans-serif;
    }
    .hero-header p {
        margin: 5px 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    .stMetric {
        background-color: #f1f5f9;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #3b82f6;
    }
    [data-testid="stSidebar"] {
        background-color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-header">
    <h1>🚑 ResQAI</h1>
    <p>AI Powered Volunteer & Resource Coordination Platform</p>
</div>
""", unsafe_allow_html=True)

# (Session State for AI Assistant removed)

# ================================
# Navigation (Tabs instead of sidebar for main features)
# ================================
tabs = st.tabs([
    "📊 Dashboard", 
    "👥 Volunteers", 
    "📋 Tasks", 
    "📦 Resources", 
    "🤖 AI Matching"
])

# ================================
# Data Initialization
# ================================
volunteers_df = get_volunteers()
tasks_df = get_tasks()
resources_df = get_resources()


# ================================
# Tab 1: Dashboard
# ================================
with tabs[0]:
    st.subheader("Operations Dashboard")
    
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Volunteers", len(volunteers_df))
    c2.metric("Active Tasks", len(tasks_df))
    c3.metric("Resources Tracked", len(resources_df))
    high_priority_count = len(tasks_df[tasks_df['priority'] == 'High']) if not tasks_df.empty and 'priority' in tasks_df.columns else 0
    c4.metric("High Priority Tasks", high_priority_count)
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Geography")
        show_map(volunteers_df, tasks_df)
        
    with col2:
        st.markdown("### Metrics")
        chart1 = generate_priority_chart(tasks_df)
        if chart1: st.plotly_chart(chart1, use_container_width=True)
        chart2 = generate_availability_histogram(volunteers_df)
        if chart2: st.plotly_chart(chart2, use_container_width=True)

# ================================
# Tab 2: Volunteers
# ================================
with tabs[1]:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Register Volunteer")
        with st.form("volunteer_form", clear_on_submit=True):
            v_name = st.text_input("Name")
            v_loc = st.text_input("Location")
            v_skills = st.text_input("Skills (comma separated)")
            v_avail = st.number_input("Availability (hours/week)", 1, 40, 5)
            v_rel = st.slider("Reliability Score (Internal)", 0, 100, 80)
            submitted = st.form_submit_button("Register")
            if submitted and v_name:
                add_volunteer(v_name, v_loc, v_skills, v_avail, v_rel)
                st.success(f"{v_name} Registered successfully! Refreshing data...")
                st.rerun()

    with col2:
        st.subheader("Current Volunteers Directory")
        if not volunteers_df.empty:
            st.dataframe(volunteers_df, use_container_width=True, hide_index=True)
        else:
            st.info("No volunteers registered yet.")

# ================================
# Tab 3: Tasks
# ================================
with tabs[2]:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Create New Task")
        with st.form("task_form", clear_on_submit=True):
            t_name = st.text_input("Task Description / Name")
            t_loc = st.text_input("Location")
            t_skill = st.text_input("Required Core Skill")
            t_vol = st.number_input("Volunteers Needed", 1, 100, 5)
            t_sev = st.slider("Disaster Severity (1-10)", 1, 10, 5, help="Used by AI to predict priority")
            
            submitted = st.form_submit_button("Create & Analyze Task")
            
            if submitted and t_name:
                with st.spinner("AI is determining priority..."):
                    predicted_priority = predict_task_priority(t_name, t_skill, t_vol, t_sev)
                    add_task(t_name, t_loc, t_skill, t_vol, predicted_priority, t_sev, t_sev)
                st.success(f"Task created with predicted priority: **{predicted_priority}**")
                st.rerun()

    with col2:
        st.subheader("Active Tasks")
        if not tasks_df.empty:
            # Highlight high priority rows
            st.dataframe(tasks_df, use_container_width=True, hide_index=True)
        else:
            st.info("No active tasks.")

# ================================
# Tab 4: Resources
# ================================
with tabs[3]:
    st.subheader("Inventory Logistics")
    with st.expander("Add New Resource"):
        r_name = st.text_input("Resource Category (e.g. Med Kits, Food, Tents)")
        r_qty = st.number_input("Quantity", 1, 10000, 10)
        r_loc = st.text_input("Warehouse / Location")
        if st.button("Add Inventory"):
            if r_name:
                add_resource(r_name, r_qty, r_loc)
                st.success("Resource added.")
                st.rerun()

    if not resources_df.empty:
        st.dataframe(resources_df, use_container_width=True)
    else:
        st.info("No resources mapped.")

# ================================
# Tab 5: AI Matching Engine
# ================================
with tabs[4]:
    st.header("Intelligent Matching Engine")
    st.markdown("Our engine matches volunteers to tasks evaluating **Skills, Geography, Reliability, and Urgency**.")
    
    if volunteers_df.empty or tasks_df.empty:
        st.warning("Data required! Need at least 1 Volunteer and 1 Task.")
    else:
        # User selects a task to perform deeply matched analysis
        task_options = tasks_df['task_name'].tolist()
        selected_task = st.selectbox("Select Task to Match", task_options)
        
        if st.button("Run AI Matcher", type="primary"):
            with st.spinner("Running complex scoring matrix..."):
                top_matches = match_volunteers(volunteers_df, tasks_df[tasks_df['task_name'] == selected_task])
                
                if top_matches:
                    st.success(f"Found {len(top_matches)} candidates!")
                    st.dataframe(top_matches, use_container_width=True)
                    
                    # Gemini Explainability
                    with st.spinner("Generating AI Explanation..."):
                        explanation = ai_recommendation(selected_task, top_matches)
                        st.markdown("### 🤖 Coordinator's Rationale")
                        st.info(explanation)
                else:
                    st.error("No volunteers met the minimum scoring threshold for this task.")

# EOF
