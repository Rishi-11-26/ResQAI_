import pandas as pd
from volunteer_scoring import calculate_score

def match_volunteers(volunteers_df, tasks_df):
    matches = []
    
    if volunteers_df.empty or tasks_df.empty:
        return matches

    for _, task in tasks_df.iterrows():
        scored_volunteers = []
        for _, volunteer in volunteers_df.iterrows():
            score = calculate_score(volunteer, task)
            # Retain a threshold minimum score to be considered a match
            if score > 20: 
                scored_volunteers.append({
                    "task": task.get("task_name", "Unknown Task"),
                    "volunteer": volunteer.get("name", "Unknown Volunteer"),
                    "score": round(score, 1),
                    "reason_data": {
                        "v_skills": volunteer.get("skills", ""),
                        "t_skills": task.get("skill_required", ""),
                        "v_loc": volunteer.get("location", ""),
                        "t_loc": task.get("location", ""),
                        "v_avail": volunteer.get("availability", 0)
                    }
                })

        # Sort dynamically scored volunteers highest to lowest
        scored_volunteers.sort(key=lambda x: x["score"], reverse=True)
        
        # Pick top N based on task needs (safeguard missing values with default 5)
        needed = int(task.get("volunteers_needed", 5))
        top_candidates = scored_volunteers[:needed]
        matches.extend(top_candidates)

    return matches
