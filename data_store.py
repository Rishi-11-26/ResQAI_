import os
import json
import pandas as pd
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase
if not firebase_admin._apps:
    use_mock = True
    try:
        # Check Streamlit secrets
        if "firebase" in st.secrets:
            firebase_creds = dict(st.secrets["firebase"])
            # Format the private key properly if it was parsed as string with literal \n
            if "private_key" in firebase_creds and r"\n" in firebase_creds["private_key"]:
                firebase_creds["private_key"] = firebase_creds["private_key"].replace(r"\n", "\n")
            cred = credentials.Certificate(firebase_creds)
            firebase_admin.initialize_app(cred)
            use_mock = False
        # Else check local file
        elif os.path.exists("firebase_credentials.json"):
            cred = credentials.Certificate("firebase_credentials.json")
            firebase_admin.initialize_app(cred)
            use_mock = False
    except Exception as e:
        print(f"Failed to initialize Firebase, falling back to mock: {e}")

if not use_mock:
    db = firestore.client()
else:
    db = None

# Mock storages
_mock_volunteers = []
_mock_tasks = []
_mock_resources = []

# ================================
# VOLUNTEERS
# ================================

def add_volunteer(name, location, skills, availability, reliability_score=80):
    data = {
        "name": name,
        "location": location,
        "skills": skills,
        "availability": availability,
        "reliability_score": reliability_score,
        "added_at": datetime.now().isoformat()
    }
    if use_mock:
        data["id"] = f"vol_{len(_mock_volunteers)+1}"
        _mock_volunteers.append(data)
    else:
        db.collection("volunteers").add(data)

def get_volunteers():
    if use_mock:
        return pd.DataFrame(_mock_volunteers)
    else:
        docs = db.collection("volunteers").stream()
        data = [doc.to_dict() for doc in docs]
        return pd.DataFrame(data)

# ================================
# TASKS
# ================================

def add_task(task_name, location, skill_required, volunteers_needed, priority="Medium", urgency=5, severity=5):
    data = {
        "task_name": task_name,
        "location": location,
        "skill_required": skill_required,
        "volunteers_needed": volunteers_needed,
        "priority": priority, # High, Medium, Low
        "urgency_level": urgency, # 1-10
        "disaster_severity": severity, # 1-10
        "status": "Active",
        "added_at": datetime.now().isoformat()
    }
    if use_mock:
        data["id"] = f"task_{len(_mock_tasks)+1}"
        _mock_tasks.append(data)
    else:
        db.collection("tasks").add(data)

def get_tasks():
    if use_mock:
        return pd.DataFrame(_mock_tasks)
    else:
        docs = db.collection("tasks").stream()
        data = [doc.to_dict() for doc in docs]
        return pd.DataFrame(data)

# ================================
# RESOURCES
# ================================

def add_resource(resource_name, quantity, location):
    data = {
        "resource_name": resource_name,
        "quantity": quantity,
        "location": location,
        "status": "Available",
        "added_at": datetime.now().isoformat()
    }
    if use_mock:
        data["id"] = f"res_{len(_mock_resources)+1}"
        _mock_resources.append(data)
    else:
        db.collection("resources").add(data)

def get_resources():
    if use_mock:
        return pd.DataFrame(_mock_resources)
    else:
        docs = db.collection("resources").stream()
        data = [doc.to_dict() for doc in docs]
        return pd.DataFrame(data)
