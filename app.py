import os
import json
import streamlit as st
from google.colab import userdata
from groq import Groq

# Initialize Groq Client
# (When migrating to Streamlit Cloud, replace `userdata.get()` with `st.secrets["GROQ_API_KEY"]`)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.environ.get('GROQ_API_KEY')

client = Groq(api_key=api_key)

# ---------------------------------------------------------
# Dynamic Prompt Generators
# ---------------------------------------------------------

def get_career_prompt(output_type: str, resume: str, jd: str) -> str:
    prompts = {
        "LinkedIn Summary": f"""You are an expert career coach. Write a compelling LinkedIn "About" Summary for the candidate, positioning them for the target Job Description.
STRICT RULES:
1. ONLY use facts, skills, and metrics explicitly stated in the RESUME. NO hallucinations.
2. Tone: Professional, forward-looking, and engaging. Maximum 3 short paragraphs.
RESUME: {resume}
JOB DESCRIPTION: {jd}""",

        "LinkedIn DM": f"""You are an expert career coach. Write a highly concise LinkedIn Direct Message (under 75 words) to a recruiter for the target Job Description.
STRICT RULES:
1. ONLY use facts from the RESUME. NO hallucinations.
2. Tone: Direct, polite, and confident. Include a clear Call to Action (e.g., a 10-min chat).
RESUME: {resume}
JOB DESCRIPTION: {jd}""",

        "Cold Email": f"""You are an expert career coach. Write a Cold Email to a hiring manager for the target Job Description.
STRICT RULES:
1. ONLY use facts from the RESUME. NO hallucinations.
2. Must include a catchy, professional Subject Line.
3. Tone: Professional, value-driven. Map 1-2 key resume achievements directly to the job requirements.
RESUME: {resume}
JOB DESCRIPTION: {jd}""",

        "Cover Letter": f"""You are an expert career coach. Write a formal Cover Letter for the target Job Description.
STRICT RULES:
1. ONLY use facts from the RESUME. NO hallucinations.
2. Structure: Formal greeting, engaging opening, 2 body paragraphs matching resume skills to JD needs, and a professional closing.
RESUME: {resume}
JOB DESCRIPTION: {jd}"""
    }
    return prompts[output_type]


def get_hackathon_prompt(raw_idea: str) -> str:
    return f"""You are a Senior Product Manager helping a student team scope a 24-hour hackathon project.

RAW IDEA: {raw_idea}
AVAILABLE TECH STACK: Python, Streamlit, Gemini API, Supabase, HTML.

INSTRUCTIONS:
1. Identify the core problem.
2. Define 2-3 MVP features using ONLY the available tech stack.
3. Respond strictly in JSON format using this exact schema:
{{
  "project_title": "string",
  "core_problem": "string",
  "mvp_features": ["feature 1", "feature 2"],
  "recommended_stack": "string"
}}
"""

# ---------------------------------------------------------
# Streamlit Interface
# ---------------------------------------------------------

st.set_page_config(page_title="AI Career & Hackathon Assistant", page_icon="🚀", layout="wide")
st.title("🤖 AI Career & Hackathon Assistant")

tab1, tab2 = st.tabs(["💼 Career Content Generator", "💡 Hackathon Scoper"])

# --- TAB 1: Career Content Generator ---
with tab1:
    st.header("Generate Tailored Application Materials")
    
    col1, col2 = st.columns(2)
    with col1:
        sample_resume_default = """John Doe - B.Tech Computer Science
Skills: Python, SQL, Basic HTML/CSS, Git, Pandas, Data Analysis.
Projects: Built a movie recommendation system in Python using Pandas.
Work Experience: Intern at Tech Corp (3 months) - Wrote SQL queries and cleaned datasets."""
        resume_input = st.text_area("Paste Resume", value=sample_resume_default, height=200)

    with col2:
        sample_jd_default = """Looking for a Junior AI/Data Developer.
Requirements: Python, Prompt Engineering, SQL, AWS, Docker, REST APIs.
Responsibilities: Build AI workflows, clean data, write backend queries."""
        jd_input = st.text_area("Paste Job Description", value=sample_jd_default, height=200)

    selected_output_type = st.selectbox(
        "Select Content Type",
        ["Cold Email", "LinkedIn Summary", "LinkedIn DM", "Cover Letter"]
    )

    if st.button("Generate Career Content"):
        if not resume_input or not jd_input:
            st.warning("Please provide both a resume and a job description.")
        else:
            prompt = get_career_prompt(selected_output_type, resume_input, jd_input)
            with st.spinner("Generating response..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3
                    )
                    st.subheader(f"Generated Output: {selected_output_type}")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error calling LLM: {e}")

# --- TAB 2: Hackathon Scoper ---
with tab2:
    st.header("Scope Your 24-Hour Hackathon MVP")
    
    raw_idea = st.text_area(
        "Enter Raw Project Idea",
        placeholder="e.g., An AI tool that helps students quickly parse lecture notes into flashcards and quizzes."
    )

    if st.button("Scope MVP"):
        if not raw_idea:
            st.warning("Please enter a raw project idea.")
        else:
            prompt = get_hackathon_prompt(raw_idea)
            with st.spinner("Scoping MVP..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3,
                        response_format={"type": "json_object"}  # Forces valid JSON output
                    )
                    
                    raw_content = response.choices[0].message.content
                    parsed_json = json.loads(raw_content)

                    # Display formatted JSON results
                    st.success("Project Scope Generated!")
                    st.subheader(f"📌 Project: {parsed_json.get('project_title', 'Untitled')}")
                    st.write(f"**Core Problem:** {parsed_json.get('core_problem', '')}")
                    
                    st.write("**MVP Features:**")
                    for feat in parsed_json.get("mvp_features", []):
                        st.markdown(f"- {feat}")
                        
                    st.write(f"**Recommended Stack:** `{parsed_json.get('recommended_stack', '')}`")

                    # Collapsible raw JSON view
                    with st.expander("View Raw JSON"):
                        st.json(parsed_json)

                except Exception as e:
                    st.error(f"Error processing project scope: {e}")
