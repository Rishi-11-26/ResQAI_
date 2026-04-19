def calculate_distance(loc1, loc2):
    # Mocking a static distance calculation based on strings
    # In a full production app, you might use geopy.distance combined with geopy.geocoders
    if loc1.lower() == loc2.lower():
        return 0 # 0 miles away
    return 15 # mock 15 miles distance for different locations

def calculate_score(volunteer, task):
    """
    Upgraded matching algorithm utilizing:
    - Skill match percentage
    - Geographic distance
    - Volunteer reliability score
    - Volunteer availability
    - Task urgency level
    """
    score = 0
    
    # 1. Skill Match (Max 40 points)
    v_skills = [s.strip().lower() for s in volunteer.get("skills", "").split(",")]
    t_skill = task.get("skill_required", "").lower()
    
    skill_score = 0
    # If explicit required skill is exactly in volunteer's skills
    if t_skill in v_skills:
        skill_score += 40
    else:
        # Partial match if any string overlaps
        for vs in v_skills:
            if t_skill in vs or vs in t_skill:
                skill_score += 20
                break
                
    # CRITICAL: Prevent unskilled volunteers from being mobilized by failing them entirely
    if skill_score == 0:
        return 0
        
    score += skill_score
    
    # 2. Location Distance Match (Max 25 points)
    dist = calculate_distance(volunteer.get("location", ""), task.get("location", ""))
    if dist < 5:
        score += 25
    elif dist < 20:
        score += 15
    else:
        score += 5

    # 3. Availability against Expected Needs (Max 20 points)
    # E.g. volunteer has X hours, task has an urgency context
    v_avail = volunteer.get("availability", 0)
    urgency = float(task.get("urgency_level", 5)) # 1-10
    
    # Needs more hours if urgency is high
    if v_avail >= 8:
        score += 20
    elif v_avail >= 4:
        score += 10
    else:
        score += 5
        
    # 4. Volunteer Reliability Score (Max 15 points)
    # Assume historical reliability out of 100
    reliability = float(volunteer.get("reliability_score", 80))
    score += (reliability / 100) * 15

    # Cap score at 100
    return min(score, 100)
