# analyzer.py
import re

# ================= SKILL CATEGORIES =================

SKILL_CATEGORIES = {
    "core_ai": [
        "machine learning", "deep learning", "neural networks",
        "tensorflow", "pytorch", "model evaluation"
    ],
    "data": [
        "pandas", "numpy", "data analysis",
        "data cleaning", "feature engineering"
    ],
    "programming": [
        "python", "r", "sql"
    ],
    "deployment": [
        "api", "flask", "fastapi", "docker"
    ],
    "specialized": [
        "natural language processing", "nlp",
        "computer vision", "cnn", "rnn",
        "reinforcement learning"
    ],
    "support": [
        "git", "matplotlib", "seaborn"
    ],
    "soft": [
        "communication", "teamwork", "problem solving"
    ]
}

SKILLS = [skill for category in SKILL_CATEGORIES.values() for skill in category]


# ================= CAREER PATHS =================

CAREER_PATHS = {
    "Data Scientist": ["python", "pandas", "numpy", "machine learning", "data analysis"],
    "Machine Learning Engineer": ["python", "machine learning", "tensorflow", "pytorch", "api"],
    "AI Engineer": ["python", "deep learning", "tensorflow", "pytorch", "api"],
    "NLP Engineer": ["python", "natural language processing", "nlp"],
    "Computer Vision Engineer": ["python", "computer vision", "cnn"]
}


# ================= SKILL ANALYSIS =================

def analyze_skills(text):
    text = text.lower()
    found_skills = {}

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        found_skills[skill] = len(re.findall(pattern, text))

    return found_skills


# ================= CATEGORY ANALYSIS =================

def analyze_categories(skill_data):
    return {
        category: sum(1 for s in skills if skill_data.get(s, 0) > 0)
        for category, skills in SKILL_CATEGORIES.items()
    }


# ================= READABILITY =================

def readability_score(text):
    sentences = [s for s in re.split(r'[.!?]', text) if s.strip()]
    words = text.split()
    if not sentences:
        return 0
    return round(len(words) / len(sentences), 2)


# ================= SMART SCORE =================

def calculate_score(skill_data, readability):
    categories = analyze_categories(skill_data)

    score = (
        categories["core_ai"] * 12 +
        categories["data"] * 8 +
        categories["programming"] * 6 +
        categories["deployment"] * 5 +
        categories["specialized"] * 8 +
        categories["soft"] * 3
    )

    score = min(score, 70)

    if readability <= 12:
        score += 30
    elif readability <= 18:
        score += 20
    else:
        score += 10

    return min(score, 100)


# ================= SKILLS GROUPING =================

def categorize_skills(skill_data):
    found = [s for s, c in skill_data.items() if c > 0]
    missing = [s for s, c in skill_data.items() if c == 0]
    return found, missing

# ================= AI SKILL COUNT (NEW) =================

def count_ai_skills(skill_data):
    ai_categories = ["core_ai", "data", "programming", "deployment", "specialized"]
    
    categories = analyze_categories(skill_data)
    
    return sum(categories[c] for c in ai_categories)


# ================= CAREER MATCH (IMPROVED %) =================

def suggest_careers(skill_data):
    results = []

    for career, required in CAREER_PATHS.items():
        match = sum(1 for s in required if skill_data.get(s, 0) > 0)
        total = len(required)

        percent = round((match / total) * 100)

        results.append((career, match, percent))

    return sorted(results, key=lambda x: x[2], reverse=True)


# ================= LEARNING PLAN =================

def recommend_learning(skill_data, career):
    required = CAREER_PATHS.get(career, [])
    return [s for s in required if skill_data.get(s, 0) == 0]


# ================= SMART INSIGHT (HUMAN-LIKE) =================

def generate_insight(skill_data):
    ai_total = sum(1 for v in skill_data.values() if v > 0 and v > 0)

    # better: directly rely on AI skill count logic externally
    ai_count = sum(
        skill_data.get(skill, 0)
        for category in ["core_ai", "data", "programming", "deployment", "specialized"]
        for skill in SKILL_CATEGORIES[category]
    )

    if ai_count == 0:
        return "No AI-related skills detected. This candidate is at the starting point of the AI learning path."

    elif ai_count <= 2:
        return "Beginner AI profile. Focus on Python, data analysis, and ML fundamentals."

    elif ai_count <= 5:
        return "Developing AI profile. You are building your foundation. Focus on core AI skills and small projects."

    elif ai_count <= 9:
        return "Intermediate AI profile. Strong foundations detected. Focus on real-world AI projects and specialization."

    else:
        return "Advanced AI profile. Ready for high-level AI engineering roles."

# ================= SMART SUGGESTIONS =================

def generate_suggestions(skill_data, readability):
    categories = analyze_categories(skill_data)

    suggestions = []

    if categories["core_ai"] == 0:
        suggestions.append("Start with machine learning fundamentals.")

    if categories["data"] == 0:
        suggestions.append("Learn pandas and numpy for data analysis.")

    if categories["deployment"] == 0:
        suggestions.append("Learn API development (Flask or FastAPI).")

    if readability > 18:
        suggestions.append("Use shorter sentences for better clarity.")

    if readability < 6:
        suggestions.append("Add more detailed project descriptions.")

    if not suggestions:
        suggestions.append("Excellent AI profile. Keep building advanced projects.")

    return suggestions


def compute_ai_maturity(skill_data):
    categories = analyze_categories(skill_data)

    score = (
        categories["core_ai"] * 25 +
        categories["data"] * 15 +
        categories["programming"] * 10 +
        categories["deployment"] * 15 +
        categories["specialized"] * 20 +
        categories["soft"] * 10
    )

    return min(score, 100)


def detect_skill_level(skill_data):
    score = compute_ai_maturity(skill_data)

    if score < 25:
        return "Beginner"
    elif score < 50:
        return "Developing"
    elif score < 70:
        return "Intermediate"
    elif score < 85:
        return "Advanced"
    else:
        return "Scholarship-Ready"


# HELPER
def skill_summary(skill_data):
    found = [s for s, c in skill_data.items() if c > 0]
    missing = [s for s, c in skill_data.items() if c == 0]

    return {
        "found": found,
        "missing": missing,
        "total_found": len(found)
    }

# ================= 💼 HIRABILITY ANALYSIS =================

def generate_hireability_statement(score, best_career, percent, level):

    # 🔥 NEW: handle non-AI candidates FIRST
    if level == "Non-AI Background":
        return (
            "This candidate does not yet meet the requirements for AI roles. "
            "A foundational learning path in programming, data analysis, and basic machine learning is required "
            "before becoming competitive in the AI job market."
        )

    # ================= EXISTING LOGIC =================

    if score >= 80:
        return f"This candidate is highly competitive for {best_career} roles and can contribute immediately."

    elif score >= 60:
        return f"This candidate shows strong potential for {best_career} roles with {percent}% alignment. With a few improvements, they can become highly competitive."

    else:
        return f"This candidate is in the early stage for {best_career} roles. A structured learning plan will significantly improve their profile."


# ================= 🚀 PROJECT RECOMMENDER =================

def recommend_projects(level, best_career):

    # 🔥 NEW: Handle complete beginners FIRST
    if level == "Non-AI Background":
        return [
            "Learn Python basics (variables, loops, functions)",
            "Build a simple calculator or number guessing game",
            "Practice basic data analysis using Excel or Python",
            "Create your first GitHub repository and upload a project"
        ]

    elif level in ["Beginner", "Developing"]:
        return [
            "Build a basic data analysis project using pandas",
            "Create a simple ML model (e.g., house price prediction)",
            "Do a Kaggle beginner project"
        ]

    elif level == "Intermediate":
        return [
            "Build an end-to-end ML project (data → model → evaluation)",
            "Create an API using Flask or FastAPI",
            "Deploy a simple ML app"
        ]

    elif level == "Advanced":
        return [
            "Deploy an ML model using Docker or cloud",
            "Build a deep learning project (CNN/NLP)",
            "Optimize model performance"
        ]

    elif level == "Scholarship-Ready":
        return [
            "Build production AI systems",
            "Contribute to open-source AI projects",
            "Publish a research-level AI project"
        ]

    # ✅ Safety fallback (never unrealistic)
    else:
        return [
            "Start learning programming fundamentals",
            "Build small beginner projects",
            "Explore data and basic problem solving"
        ]

# ================= 🎤 INTERVIEW READINESS =================

def interview_readiness(score):
    if score >= 80:
        return "Ready for AI job interviews."
    elif score >= 60:
        return "Almost ready. Focus on projects and interview practice."
    else:
        return "Not ready yet. Focus on building core AI skills first."


def next_step_action(level, match_percent):

    # 🔥 NEW: Handle non-AI background FIRST
    if level == "Non-AI Background":
        return "Start with Python basics, then move to data analysis and basic programming before learning machine learning."

    if level in ["Beginner", "Developing"]:
        return "Start learning Python, machine learning, and build your first 2 projects."

    elif level == "Intermediate":
        if match_percent >= 60:
            return "Build 2–3 strong AI projects and start applying for internships."
        else:
            return "Strengthen your core AI skills and complete guided projects."

    elif level == "Advanced":
        return "Focus on specialization and apply for internships or junior AI roles."

    else:
        return "Apply for AI roles and contribute to advanced projects."


def generate_profile_summary(level, best_career, best_percent, found_skills):
    top_skills = ", ".join(found_skills[:3]) if found_skills else "basic transferable skills"

    return (
        f"This candidate demonstrates an {level.lower()}-level AI profile with foundational strengths in {top_skills}, "
        f"and shows {best_percent}% alignment with {best_career} roles, indicating strong potential for growth."
    )


def competitiveness_level(score):
    if score >= 80:
        return "Highly Competitive (Top candidate level)"
    elif score >= 60:
        return "Moderately Competitive (Needs refinement)"
    elif score >= 40:
        return "Emerging Candidate (Developing stage)"
    else:
        return "Early-Stage Candidate (High growth potential)"


def action_plan(level, best_career, score=None, missing_skills=None, competitiveness=None):
    plan = {
        "Phase 1 (Foundation - 0 to 30 days)": [],
        "Phase 2 (Skill Building - 30 to 60 days)": [],
        "Phase 3 (Projects - 60 to 90 days)": [],
        "Phase 4 (Career Preparation - 90+ days)": [],
        "Priority Skills": [],
        "Final Recommendation": ""
    }

    # ================= BASE ROADMAP =================

    if level in ["Beginner", "Developing"]:
        plan["Phase 1 (Foundation - 0 to 30 days)"].extend([
            "Master Python basics (data types, loops, functions)",
            "Learn basic data analysis with pandas",
            "Understand basic statistics for AI"
        ])

        plan["Phase 2 (Skill Building - 30 to 60 days)"].extend([
            "Learn machine learning fundamentals",
            "Build first ML models (linear regression, classification)"
        ])

        plan["Phase 3 (Projects - 60 to 90 days)"].extend([
            "Build 2 beginner ML projects",
            "Start Kaggle competitions"
        ])

        plan["Phase 4 (Career Preparation - 90+ days)"].extend([
            "Create GitHub portfolio",
            "Apply for internships"
        ])

    elif level == "Intermediate":
        plan["Phase 1 (Foundation - 0 to 30 days)"].extend([
            "Strengthen ML fundamentals and data structures",
            f"Review key concepts for {best_career}"
        ])

        plan["Phase 2 (Skill Building - 30 to 60 days)"].extend([
            "Learn advanced ML techniques",
            "Improve model evaluation skills"
        ])

        plan["Phase 3 (Projects - 60 to 90 days)"].extend([
            f"Build 2 production-level projects for {best_career}",
            "Deploy a model using Flask or FastAPI"
        ])

        plan["Phase 4 (Career Preparation - 90+ days)"].extend([
            "Optimize GitHub portfolio",
            "Start applying for internships or junior roles"
        ])

    elif level == "Advanced":
        plan["Phase 1 (Foundation - 0 to 30 days)"].extend([
            f"Deep specialization in {best_career}",
            "Study advanced AI research papers"
        ])

        plan["Phase 2 (Skill Building - 30 to 60 days)"].extend([
            "Work on system design for AI applications",
            "Improve scalability and deployment skills"
        ])

        plan["Phase 3 (Projects - 60 to 90 days)"].extend([
            "Contribute to open-source AI projects",
            "Build advanced real-world AI system"
        ])

        plan["Phase 4 (Career Preparation - 90+ days)"].extend([
            "Apply for AI/ML Engineer roles",
            "Prepare for technical interviews"
        ])

    else:
        plan["Final Recommendation"] = "Apply for AI roles while continuously building real-world projects."

        plan["Scholarship Boost Strategy"] = [
        "Publish 1 research-style AI project (with documentation)",
        "Write a technical blog explaining your ML project",
        "Upload all projects to GitHub with README",
        "Practice explaining projects in interview format"
    ]

    # ================= PRIORITY SKILLS ENGINE =================

    if missing_skills:
        missing_skills = list(missing_skills)

        high_priority = missing_skills[:3]
        medium_priority = missing_skills[3:6] if len(missing_skills) > 3 else []

        plan["Priority Skills"] = {
            "High Priority": high_priority,
            "Medium Priority": medium_priority
        }

    # ================= SMART SCORING INSIGHT =================

    if score is not None:
        if score < 50:
            plan["Final Recommendation"] = "Focus on fundamentals before advanced AI topics."
        elif score < 70:
            plan["Final Recommendation"] = "You are close to job-ready — focus on projects and deployment."
        else:
            plan["Final Recommendation"] = "Strong profile — focus on specialization and job applications."

    # ================= CONTEXTUAL BOOST =================

    if competitiveness:
        plan["Final Recommendation"] += f" Current status: {competitiveness}."

    return plan


def scholarship_readiness(skill_data, score):
    categories = analyze_categories(skill_data)

    signals = []

    if categories["core_ai"] >= 2:
        signals.append("Strong AI foundation")

    if categories["deployment"] >= 1:
        signals.append("Industry-ready skills (deployment detected)")

    if categories["specialized"] >= 1:
        signals.append("Specialized AI knowledge")

    if score >= 75:
        signals.append("High academic competitiveness")

    return signals


def generate_final_admission_report(level, score, career, signals):
    signals_text = "\n- ".join(signals) if signals else "No strong signals yet"

    # 🔥 ADAPTIVE FINAL VERDICT
    if level == "Non-AI Background":
        final_message = (
            "You are at the beginning of your AI journey.\n"
            "Focus on learning Python, basic programming, and building simple projects "
            "before progressing to machine learning and AI."
        )

    elif level in ["Beginner", "Developing"]:
        final_message = (
            "You are building your AI foundation.\n"
            "Focus on core skills like data analysis, machine learning basics, "
            "and completing small to intermediate projects."
        )

    elif level == "Intermediate":
        final_message = (
            "You are close to being competitive.\n"
            "Focus on building strong end-to-end AI projects, deployment, and real-world applications."
        )

    else:  # Advanced / Scholarship-Ready
        final_message = (
            "You are a strong candidate for scholarships and AI roles.\n"
            "Focus on specialization, research projects, and high-impact contributions."
        )

    return (
        f"🎓 ADMISSION ANALYSIS REPORT\n\n"
        f"Level: {level}\n"
        f"AI Score: {score}/100\n"
        f"Target Path: {career}\n\n"
        f"Strength Signals:\n- {signals_text}\n\n"
        f"Final Verdict:\n"
        f"{final_message}"
    )


def count_soft_skills(skill_data):
    soft_skills = SKILL_CATEGORIES["soft"]
    return sum(1 for s in soft_skills if skill_data.get(s, 0) > 0)