import os
from google.colab import userdata
from groq import Groq

# Fetch secret key from Colab environment
api_key = userdata.get('GROQ_API_KEY')
client = Groq(api_key=api_key)

# Sample Inputs for Testing
sample_resume = """
John Doe - B.Tech Computer Science
Skills: Python, SQL, Basic HTML/CSS, Git, Pandas, Data Analysis.
Projects: Built a movie recommendation system in Python using Pandas.
Work Experience: Intern at Tech Corp (3 months) - Wrote SQL queries and cleaned datasets.
"""

sample_jd = """
Looking for a Junior AI/Data Developer.
Requirements: Python, Prompt Engineering, SQL, AWS, Docker, REST APIs.
Responsibilities: Build AI workflows, clean data, write backend queries.
"""

# We simulate the user selecting "Cold Email" from our UI
selected_output_type = "Cold Email"

PROMPTS = {
    "LinkedIn Summary": f"""You are an expert career coach. Write a compelling LinkedIn "About" Summary for the candidate, positioning them for the target Job Description.
STRICT RULES:
1. ONLY use facts, skills, and metrics explicitly stated in the RESUME. NO hallucinations.
2. Tone: Professional, forward-looking, and engaging. Maximum 3 short paragraphs.
RESUME: {sample_resume}
JOB DESCRIPTION: {sample_jd}""",

    "LinkedIn DM": f"""You are an expert career coach. Write a highly concise LinkedIn Direct Message (under 75 words) to a recruiter for the target Job Description.
STRICT RULES:
1. ONLY use facts from the RESUME. NO hallucinations.
2. Tone: Direct, polite, and confident. Include a clear Call to Action (e.g., a 10-min chat).
RESUME: {sample_resume}
JOB DESCRIPTION: {sample_jd}""",

    "Cold Email": f"""You are an expert career coach. Write a Cold Email to a hiring manager for the target Job Description.
STRICT RULES:
1. ONLY use facts from the RESUME. NO hallucinations.
2. Must include a catchy, professional Subject Line.
3. Tone: Professional, value-driven. Map 1-2 key resume achievements directly to the job requirements.
RESUME: {sample_resume}
JOB DESCRIPTION: {sample_jd}""",

    "Cover Letter": f"""You are an expert career coach. Write a formal Cover Letter for the target Job Description.
STRICT RULES:
1. ONLY use facts from the RESUME. NO hallucinations.
2. Structure: Formal greeting, engaging opening, 2 body paragraphs matching resume skills to JD needs, and a professional closing.
RESUME: {sample_resume}
JOB DESCRIPTION: {sample_jd}"""
}

system_prompt = PROMPTS[selected_output_type]

# Test Model Call
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": system_prompt}],
    temperature=0.3
)

print(f"--- GENERATED OUTPUT: {selected_output_type} ---")
print(response.choices[0].message.content)
