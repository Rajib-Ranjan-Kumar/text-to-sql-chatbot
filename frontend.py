import streamlit as st
from main import run

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="",
    layout="centered"
)

st.title("AI Data Analyst")
st.markdown("Ask questions about your data in natural language")

user_query = st.text_area(
    "Enter your question:",
    placeholder="e.g. Compare total clicks and applications for September 2026"
)

if st.button("Analyze"):

    if user_query.strip() == "":
        st.warning("Please enter a question to analyze")

    else:
        with st.spinner("Analyzing your query..."):

            answer = run(user_query)

        st.success("Analysis Completed!")

        st.markdown("### Analysis")

        st.dataframe(
            answer,
            use_container_width=True
        )