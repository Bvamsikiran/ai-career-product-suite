import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Career Product Suite", layout="centered")

st.title("AI Career Product Suite")
st.subheader("Tailored for Game Developers, VFX Artists & Designers")

# 1. Inputs from Streamlit UI
sample_resume = st.text_area("Paste Resume / Facts:", height=200)
sample_jd = st.text_area("Paste Target Job Description:", height=200)

# 2. Prompt Templates (Defined WITHOUT the 'f' prefix)
PROMPT_TEMPLATES = {
    "LinkedIn Summary": """You are an expert executive career coach specializing in the gaming and interactive media industry. Write a compelling LinkedIn "About" Summary for a veteran candidate with 12 years of industry experience across AI game development, game design, and VFX art. Position them strategically for the target Job Description.
STRICT RULES:
1. Combine the candidate's 12-year background in AI game dev, design, and VFX with facts, skills, and metrics explicitly stated in the RESUME. NO hallucinations.
2. Tone: Visionary, authoritative, and engaging. Maximum 3 short paragraphs highlighting technical depth and creative leadership.
RESUME: {sample_resume}
JOB DESCRIPTION: {sample_jd}""",

    "LinkedIn DM": """You are an executive career coach in gaming and tech. Write a highly concise LinkedIn Direct Message (under 75 words) from a veteran AI gaming developer, designer, and VFX artist (12 yrs exp) to a lead recruiter or director for the target Job Description.
STRICT RULES:
1. Frame the outreach around 12 years of specialized gaming experience, using ONLY facts from the RESUME. NO hallucinations.
2. Tone: Direct, respectful, and confident. Include a clear Call to Action (e.g., a brief 10-min chat).
RESUME: {sample_resume}
JOB DESCRIPTION: {sample_jd}""",

    "Cold Email": """You are an executive career coach. Write a targeted Cold Email from a 12-year veteran AI game developer, designer, and VFX artist to a hiring manager or studio director for the target Job Description.
STRICT RULES:
1. ONLY use facts from the RESUME. NO hallucinations.
2. Must include a high-impact, professional Subject Line highlighting high-level game dev/AI experience.
3. Tone: Executive-level, value-driven. Directly map 1–2 major technical or creative achievements from the resume to the studio's key requirements.
RESUME: {sample_resume}
JOB DESCRIPTION: {sample_jd}""",

    "Cover Letter": """You are an expert executive career coach in the games industry. Write a formal Cover Letter for a veteran candidate with 12 years of experience in AI game development, game design, and VFX art, applying for the target Job Description.
STRICT RULES:
1. Base all specific accomplishments strictly on the RESUME. NO hallucinations.
2. Structure: Formal greeting, impactful opening establishing 12 years of industry mastery across AI, design, and VFX, 2 body paragraphs demonstrating technical alignment and leadership value, and a confident closing.
RESUME: {sample_resume}
JOB DESCRIPTION: {sample_jd}"""
}

selected_option = st.selectbox("Select Asset to Generate:", list(PROMPT_TEMPLATES.keys()))

# 3. Execution Trigger
if st.button("Generate Asset"):
    if not sample_resume.strip() or not sample_jd.strip():
        st.warning("Please provide both the Resume and the Job Description before generating.")
    else:
        # Dynamically inject variables at runtime using .format()
        final_prompt = PROMPT_TEMPLATES[selected_option].format(
            sample_resume=sample_resume,
            sample_jd=sample_jd
        )
        
        with st.spinner("Generating content via Groq API..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": final_prompt}],
                    model="llama-3.3-70b-versatile",
                )
                
                st.success("Generation Complete!")
                st.markdown("### Generated Output")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error calling Groq API: {e}")
