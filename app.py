import streamlit as st
from agent import generate_scrum_report

# Function to wrap report generation
def get_commits_by_author(repo_url: str, author: str) -> dict:
    # You can modify this function to pass repo_url and author to actual logic
    return {
        'scrum_report': generate_scrum_report()['scrum_report']
    }

# Set page config
st.set_page_config(page_title="Scrum Report Generator", layout="centered")

# Title and description
st.title("GitSnap: Automated Scrum Report")
st.markdown("Enter a GitHub repository and author name to generate a detailed, styled Scrum Report.")

# Initialize session state
if "scrum_data" not in st.session_state:
    st.session_state.scrum_data = None

# Input Form
with st.form("scrum_form"):
    repo_url = st.text_input("🔗 GitHub Repository URL", value="https://github.com/inamurahman/GitSnap")
    author = st.text_input("👤 Author Name", value="inamurahman")
    # repo_name = st.text_input("Repository Name", value="GitSnap")
    # author = ""
    submitted = st.form_submit_button("Generate Report")

    if submitted:
        if not repo_url or not author:
            st.warning("Please enter both the repository URL and author name.")
        else:
            with st.spinner("🔍 Fetching commits and generating scrum report..."):
                st.session_state.scrum_data = get_commits_by_author(repo_url, author)

# Display Scrum Report
if st.session_state.scrum_data:
    st.markdown("---")
    st.success("✅ Scrum report generated!")
    st.markdown(st.session_state.scrum_data["scrum_report"], unsafe_allow_html=True)
