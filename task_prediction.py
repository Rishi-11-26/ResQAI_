import os
from gemini_ai import client, check_client

def predict_task_priority(task_name, skill_required, volunteers_needed, severity=5):
    """
    Uses Gemini to analyze the task details and predict priority (Low, Medium, High).
    """
    check_client()
    if not client:
        # Fallback simplistic logic if no AI
        if int(volunteers_needed) >= 10 or severity >= 8:
            return "High"
        elif int(volunteers_needed) >= 5 or severity >= 5:
            return "Medium"
        return "Low"

    prompt = f"""
Analyze the following disaster response task and categorize its priority strictly as one of the following words: High, Medium, Low.

Task Details:
Name: {task_name}
Requirements: {skill_required}
Volunteers Needed: {volunteers_needed}
Reported Disaster Severity (1-10): {severity}

Return ONLY the word High, Medium, or Low.
"""
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        prediction = response.text.strip().replace(".", "")
        if prediction in ["High", "Medium", "Low"]:
            return prediction
        else:
            return "Medium"
    except:
        return "Medium"
