import streamlit as st

from forms.contact import contact_form

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

# --- HEAD SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/Profile Image.png", width=300)
with col2:
    st.title("Rizky Putra Laksmana", anchor=False)
    st.write(
        "Data Enthusiast, currently enhancing skills in data analysis, machine learning, and data visualization to drive data-driven decision-making in real-world applications."
    )
    if st.button("✉ Contact Me"):
        show_contact_form()

# ---------- CUSTOM CSS STYLING ----------
st.markdown("""
<style>
/* Base style for collapsible titles */
.details summary {
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 10px;
}
.details summary::marker {
  font-size: 20px;
}
.details {
  margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


# ---------- EXPERIENCE AND QUALIFICATIONS ----------
st.markdown("""
<details class="details">
<summary>Experience & Qualifications</summary>
<br>

- Gained hands-on experience in data wrangling, analysis, and visualization using Python and SQL<br>
- Performed exploratory data analysis (EDA) and statistical hypothesis testing on real-world datasets<br>
- Built interactive Power BI dashboards to communicate insights and business recommendations<br>
- Developed machine learning models for regression, classification and clustering tasks<br>
- Worked independently on end-to-end projects, including customer segmentation and A/B testing simulations<br>
- Strengthened problem-solving skills through weekly case studies and coding challenges<br>
</details>
""", unsafe_allow_html=True)


# ---------- SKILLS ----------
st.markdown("""
<details class="details">
<summary>Skills</summary>
<br>

<b>Soft Skills</b><br>
- Time Management<br>
- Analytical Thinking<br>
- Detail-Oriented<br>
- Independent Project Execution<br><br>

<b>Technical Skills</b><br>
- Programming & Analysis: Python (Pandas, NumPy, Scikit-learn, Seaborn, Matplotlib), SQL (DBeaver, SQLite)<br>
- Data Visualization: Power BI, Matplotlib, Seaborn<br>
- Data Handling: Data wrangling, EDA, hypothesis testing, A/B testing, machine learning<br>
- Productivity Tools: Microsoft Excel, Word, PowerPoint<br><br>

<b>Languages</b><br>
- English — C1 Advanced<br>
- Japanese — N5 Level<br>
</details>
""", unsafe_allow_html=True)