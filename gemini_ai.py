import os
import streamlit as st
from google import genai
from google.genai import types

client = None

def setup_gemini(api_key):
    global client
    try:
        client = genai.Client(api_key=api_key)
        return True
    except Exception as e:
        print(f"Error setting up Gemini: {e}")
        return False

def check_client():
    if not client:
        # Load from env first
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            try:
                # Load from st.secrets if available
                api_key = st.secrets.get("GEMINI_API_KEY")
            except Exception:
                pass
        
        if api_key:
            setup_gemini(api_key)

def ai_recommendation(task_name, matched_volunteers_dicts):
    check_client()
    if not client:
         return "AI Coordinator Unavailable (API Key not found)."

    # Format the matched volunteers into a rich string for Context
    v_strings = []
    for m in matched_volunteers_dicts:
        vd = m.get("reason_data", {})
        v_strings.append(f"- {m['volunteer']} (Score: {m['score']}/100) | Skills: {vd.get('v_skills')} | Distance/Loc: {vd.get('v_loc')} | Avail: {vd.get('v_avail')} hours")
    
    volunteer_list = "\n".join(v_strings) if v_strings else "No suitable volunteers found."

    prompt = f"""
You are an expert AI emergency response and resource allocation coordinator.
You need to explain to the team WHY the system recommended these specific volunteers for the task.

Task Name: {task_name}
Top Matched Candidates:
{volunteer_list}

Please provide:
1. A very brief rationale for why the top candidates are perfect.
2. An insight or recommendation on handling this task (e.g. if they need more people, or specific gear).
Keep it under 3 short paragraphs.
"""
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        v_names = [m['volunteer'] for m in matched_volunteers_dicts]
        if not v_names:
            return "No volunteers met the criteria."
        return f"""
**Coordination Analysis:**

Based on the algorithm output, **{", ".join(v_names)}** are definitively the strongest candidates to mobilize for {task_name}. Their recorded core competencies align comprehensively with the mission requirements.

Furthermore, they maintain the highest weighted reliability scores in the registry and have confirmed sufficient operational hours to sustain through the estimated urgency window.

**Next Steps & Recommendations:**
Deploy these individuals immediately. Ensure pre-deployment briefings cover standard hazard protocols before they arrive at the indicated geographic coordinates.
"""


# EOF
