import openai
import streamlit as st
from config import env_vars

OPENAI_API_KEY = env_vars.OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

def generate_career_recommendation(o_level_results, post_secondary_pathway, qualification, qualification_grades, a_level_results, skills, career_goals, interests, country, max_tokens=1000):
    if not o_level_results or not post_secondary_pathway or not skills or not career_goals:
        return "❌ Please provide complete information: O-Level results, post-secondary pathway, qualification, skills, and career goals."

    if post_secondary_pathway == "Junior College (JC)" and not a_level_results:
        return "❌ Please provide your A-Level results for the Junior College pathway."

    prompt = (f"Based on the following academic results, skills, and interests, suggest suitable career paths, "
              f"relevant universities or institutions, and required certifications for a Singaporean student:\n"
              f"O-Level Results: {o_level_results}\n")

    if post_secondary_pathway == "Junior College (JC)":
        prompt += f"A-Level Results: {a_level_results}\n"
    else:
        prompt += f"Qualification: {qualification} (Grades: {qualification_grades})\n"

    prompt += (f"Post-Secondary Pathway: {post_secondary_pathway}\n"
               f"Skills: {skills}\n"
               f"Career Goals: {career_goals}\n"
               f"Interests: {interests}\n"
               f"Preferred Country: {country}\n"
               f"Include relevant details such as industries, potential job roles, and certifications to pursue in Singapore.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a career counselor for Singaporean students."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()

    except openai.OpenAIError as e:
        return f"⚠️ An OpenAI error occurred: {e}"
    except Exception as e:
        return f"⚠️ An error occurred: {e}"

def add_emojis_to_recommendation(recommendation):
    emojis = {
        "university": "🏛️ University",
        "certification": "📜 Certification",
        "industry": "🏢 Industry",
        "job roles": "💼 Job Roles",
        "career path": "🚀 Career Path",
        "skills": "🛠️ Skills",
        "experience": "📅 Experience",
        "internship": "💼 Internship",
        "degree": "🎓 Degree",
        "project": "📁 Project",
        "learning": "📘 Learning",
        "salary": "💰 Salary",
        "technology": "💻 Technology",
        "interview": "🤝 Interview",
        "qualification": "🎓 Qualification",
        "opportunities": "🚪 Opportunities",
    }
    for word, emoji in emojis.items():
        recommendation = recommendation.replace(word, emoji)
    return recommendation

def get_helpful_resources(career_goals):
    prompt = (f"Please suggest relevant and helpful online resources, such as online courses, articles, "
          f"certifications, and platforms, for someone looking to pursue a career in {career_goals}. "
          f"Include up-to-date websites with direct links, platforms, and certifications that can help them advance in this career. "
          f"Ensure all website URLs are correct and provide easy access. For example, you can refer to platforms like: "
          f"\n- [MySkillsFuture](https://www.myskillsfuture.gov.sg) "
          f"\n- [Coursera](https://www.coursera.org) "
          f"\n- [edX](https://www.edx.org) "
          f"Feel free to include any additional, relevant platforms or certifications.")


    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in education and career guidance."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        resources = response.choices[0].message['content'].strip().split("\n")
        return resources

    except openai.OpenAIError as e:
        return [f"⚠️ An OpenAI error occurred: {e}"]
    except Exception as e:
        return [f"⚠️ An error occurred: {e}"]

def local_css():
    st.markdown(
        f"""
        <style>
        body {{
            background-color: #e0f7e9;
            color: #333;
        }}
        .primary {{ color: #333; }}
        .recommendation-box {{
            background-color: #f9fdfc;
            color: #333;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #28a745;
            animation: fadeIn 1s ease-in;
            font-family: 'Trebuchet MS', sans-serif;
        }}
        .resources-box {{
            background-color: #f0f8ff;
            color: #333;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #4169e1;
            animation: resourceFadeIn 1.5s ease-in;
            font-family: 'Georgia', serif;
        }}
        .header {{
            color: #28a745;
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 30px;
            animation: slideIn 1s ease-in;
            font-family: 'Arial', sans-serif;
        }}
        .subheader {{
            color: #28a745;
            font-size: 24px;
            margin-top: 20px;
            margin-bottom: 10px;
            font-family: 'Arial', sans-serif;
        }}
        .stButton>button {{
            background-color: #28a745;
            color: #fff;
            border-radius: 10px;
            font-size: 16px;
            transition: background-color 0.3s ease;
            font-family: 'Verdana', sans-serif;
        }}
        .stButton>button:hover {{
            background-color: #a1dfc5;
        }}
        input[type="text"] {{
            background-color: #f1f9f7;
            border: 2px solid #28a745;
            border-radius: 5px;
            color: #333;
            font-size: 16px;
            font-weight: bold;
        }}
        input[type="text"]:focus {{
            border-color: #1f7a33;
            box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.2);
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        @keyframes slideIn {{
            from {{ transform: translateY(-50px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        @keyframes resourceFadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        .fade-in-text {{
            animation: textFadeIn 2s ease-in-out;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

local_css()

st.markdown('<div class="header fade-in-text">🎓PathFinder.2 by Studentpod 📖</div>', unsafe_allow_html=True)

o_level_results = st.text_input("**📝 O-Level Results** (e.g., Math: A1, English: A2, Science: B3)", "")
post_secondary_pathway = st.selectbox(
    "**📚 Post-Secondary Education Pathway**",
    ("Junior College (JC)", "Polytechnic", "Institute of Technical Education (ITE)")
)

a_level_results = None
qualification = None
qualification_grades = None

if post_secondary_pathway == "Junior College (JC)":
    a_level_results = st.text_input("**📝 A-Level Results** (e.g., Math: A, Physics: A, Chemistry: B)", "")
elif post_secondary_pathway == "Polytechnic":
    qualification = st.text_input("**🎓 Polytechnic Qualification** (e.g., Diploma in Engineering)", "")
    qualification_grades = st.text_input("**📈 Polytechnic Grade** (e.g., GPA 3.5/4)", "")
elif post_secondary_pathway == "Institute of Technical Education (ITE)":
    qualification = st.text_input("**🎓 ITE Qualification** (e.g., Higher Nitec in Electronics Engineering)", "")
    qualification_grades = st.text_input("**📈 ITE Grade** (e.g., GPA 3.5/4)", "")

skills = st.text_input("**🛠️ Skills** (e.g., Programming, Communication, Design)", "")
career_goals = st.text_input("**🚀 Career Goals** (e.g., Software Engineer, Entrepreneur)", "")
interests = st.text_input("**🎨 Interests** (e.g., Technology, Business, Arts)", "")
country = st.text_input("**🌍 Preferred Country to Study/Work** (e.g., Singapore, USA, UK)", "")

if st.button("💡 Get Career Recommendation"):
    recommendation = generate_career_recommendation(
        o_level_results, post_secondary_pathway, qualification, qualification_grades,
        a_level_results, skills, career_goals, interests, country
    )
    recommendation_with_emojis = add_emojis_to_recommendation(recommendation)
    st.markdown(f'<div class="recommendation-box fade-in-text">{recommendation_with_emojis}</div>', unsafe_allow_html=True)

    st.markdown('<div class="subheader fade-in-text">📚 Helpful Resources</div>', unsafe_allow_html=True)
    helpful_resources = get_helpful_resources(career_goals)
    st.markdown('<div class="resources-box fade-in-text">', unsafe_allow_html=True)
    for resource in helpful_resources:
        st.markdown(f"- {resource}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center;'><strong>Created with 💚 by Studentpod 💼</strong></p>", unsafe_allow_html=True)
