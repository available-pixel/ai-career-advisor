# app.py
import streamlit as st
from utils import extract_text_from_pdf
from streamlit_pdf_viewer import pdf_viewer
import os
from analyzer import (
    analyze_skills,
    readability_score,
    calculate_score,
    categorize_skills,
    suggest_careers,
    generate_insight,
    detect_skill_level,
    generate_hireability_statement,
    recommend_projects,
    next_step_action,
    competitiveness_level,
    action_plan,
    scholarship_readiness,
    generate_final_admission_report,
    count_ai_skills,
    count_soft_skills
)

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Career Advisor Pro",
    page_icon="🧠",
    layout="wide"
)

st.markdown(
    """
    <style>

    /* MAIN BACKGROUND (SOFT GREY GRADIENT) */
    .stApp {
        background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
        color: #111827;
    }

    /* SIDEBAR (LIGHT GREY) */
    section[data-testid="stSidebar"] {
        background: #e5e7eb;
        color: #111827;
    }

    /* HEADINGS */
    h1 {
        color: #111827;
    }

    h2, h3 {
        color: #374151;
    }

    /* METRICS (CARDS STYLE) */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #d1d5db;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    /* BUTTONS */
    .stButton>button {
        background: linear-gradient(90deg, #6b7280, #9ca3af);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 8px 16px;
    }

    /* ALERT BOXES (INFO / SUCCESS / WARNING) */
    .stAlert {
        border-radius: 10px;
        border: 1px solid #d1d5db;
        background-color: #ffffff;
        color: #111827;
    }

    /* PROGRESS BAR */
    div[data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #9ca3af, #6b7280);
    }

    /* INPUT BOXES */
    input, textarea {
        background-color: #ffffff !important;
        color: #111827 !important;
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ================= SIDEBAR =================
st.sidebar.title("🧠 AI Career Advisor")
page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "🧩 Skills Analysis",
        "🎯 Career Path",
        "🚀 Learning Roadmap",
        "🎓 Scholarship Report"
    ]
)

# ================= SIDEBAR INPUT =================
uploaded_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])

# ================= DEMO CV =================
st.sidebar.markdown("## ⚡ Try Demo CV")

demo_choice = st.sidebar.radio(
    "Select Demo Resume",
    ["None", "🧠 Strong AI Profile", "📈 Beginner AI Profile"]
)

# ================= DEMO FILE MAPPING =================
demo_file = None

if demo_choice == "🧠 Strong AI Profile":
    demo_file = "demo_cvs/expert_cv.pdf"

elif demo_choice == "📈 Beginner AI Profile":
    demo_file = "demo_cvs/beginner_cv.pdf"

# ================= FILE SELECTION =================
file_to_use = None

if uploaded_file:
    file_to_use = uploaded_file
elif demo_file:
    file_to_use = demo_file

if demo_choice != "None":
    st.sidebar.success("Demo CV Loaded ✅")

# ================= PROCESS FILE ONCE =================
if file_to_use:
    if isinstance(file_to_use, str):
        text = extract_text_from_pdf(file_to_use)
    else:
        file_to_use.seek(0)
        text = extract_text_from_pdf(file_to_use)

    skills = analyze_skills(text)
    ai_skill_count = count_ai_skills(skills)
    soft_skill_count = count_soft_skills(skills)
    readability = readability_score(text)
    score = calculate_score(skills, readability)
    found_skills, missing_skills = categorize_skills(skills)

    level = detect_skill_level(skills)

    career_matches = suggest_careers(skills)
    if career_matches:
        best_career, _, best_percent = career_matches[0]
    else:
        best_career, best_percent = "No Match", 0

    # SMART FIX
    if ai_skill_count == 0:
        best_career = "No AI Career Match Yet"
        best_percent = 0
        level = "Non-AI Background"

    # ================= DASHBOARD =================
    if page == "📊 Dashboard":
        st.title("📊 Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("AI Score", f"{score}/100")
        col2.metric("Skill Level", level)
        col3.metric("Best Match", best_career)
        col4.metric("Match %", f"{best_percent}%")

        st.progress(score / 100)

        st.subheader("AI Insight")
        st.success(generate_insight(skills))

        st.subheader("📄 Resume Preview")

        if isinstance(file_to_use, str):  # demo file
            with open(file_to_use, "rb") as f:
                pdf_bytes = f.read()
        else:  # uploaded file
            file_to_use.seek(0)  # 🔥 RESET POINTER (VERY IMPORTANT)
            pdf_bytes = file_to_use.read()

        pdf_viewer(pdf_bytes)

    # ================= SKILLS =================
    elif page == "🧩 Skills Analysis":
        st.title("🧩 Skills Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✔ Strengths")
            for s in found_skills[:8]:
                st.success(s)

        with col2:
            st.subheader("❌ Skill Gaps")

            if ai_skill_count == 0:
                starter_skills = ["python", "data analysis", "statistics"]
                for s in starter_skills:
                    st.warning(s)
            else:
                for s in missing_skills[:5]:
                    st.warning(s)

    # ================= CAREER =================
    elif page == "🎯 Career Path":
        st.title("🎯 Career Path")

        st.success(f"{best_career}")
        st.info(f"Match Score: {best_percent}%")

        st.write(generate_hireability_statement(score, best_career, best_percent, level))
        st.warning(next_step_action(level, best_percent))
        st.success(competitiveness_level(score))

    # ================= ROADMAP =================
    elif page == "🚀 Learning Roadmap":
        st.title("🚀 Learning Roadmap")

        plan = action_plan(level, best_career, score, missing_skills, competitiveness_level(score))

        for phase, tasks in plan.items():
            st.subheader(phase)

            if isinstance(tasks, list):
                for t in tasks:
                    st.write("•", t)

            elif isinstance(tasks, dict):
                for k, v in tasks.items():
                    st.write(f"**{k}:** {', '.join(v)}")

        st.subheader("Recommended Projects")

        for p in recommend_projects(level, best_career):
            st.write("•", p)

    # ================= SCHOLARSHIP =================
    elif page == "🎓 Scholarship Report":
        st.title("🎓 Scholarship Report")

        signals = scholarship_readiness(skills, score)

        if not signals and level == "Non-AI Background":
            st.warning(
                "Start with Python, basic programming, and simple projects before AI specialization."
            )
        elif not signals:
            st.warning("Focus on building projects and core AI skills.")
        else:
            for s in signals:
                st.success(s)

        st.subheader("Final Admission Report")
        st.code(generate_final_admission_report(level, score, best_career, signals))

else:
    st.title("🧠 AI Career Advisor Pro")
    st.info("Upload a resume from the sidebar to begin analysis.")