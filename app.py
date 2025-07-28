import streamlit as st
import pandas as pd
import os
import difflib
from dotenv import load_dotenv

from utils.data_summary import summarize_dataframe
from utils.genai_interface import query_llm
from utils.code_executor import execute_user_code
# from utils.report_generator import generate_report  # No longer needed

# Load environment variables
load_dotenv()

st.set_page_config(page_title="CSV AI Analyst", layout="wide")
st.title("📊 CSV AI Analyst")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

interactions = []

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Preview DataFrame
    st.write("### Preview of the data:")
    st.dataframe(df.head())

    # Data Summary
    st.write("### 📋 Data Summary:")
    summary = summarize_dataframe(df)

    st.subheader("🧾 Column Types")
    st.json(summary["dtypes"])

    st.subheader("⚠️ Missing Values")
    st.json(summary["missing_values"])

    st.subheader("📊 Summary Statistics")
    st.json(summary["summary_stats"])

    st.markdown("---")
    st.header("🔍 Ask a Question About Your Data")

    user_question = st.text_input("Ask a question (e.g., 'What is the average age?')")

    if user_question:
        available_columns = ", ".join(df.columns)
        base_prompt = f"""
You are a pandas expert. Convert the following user question into a valid pandas code snippet.
Assume the DataFrame is already loaded as `df`.

Available columns in df: {available_columns}

Question: {user_question}

Only return the Python code using df. Do not include explanations, comments, or markdown.
        """

        with st.spinner("Thinking..."):
            gen_code = query_llm(base_prompt.strip())

        st.code(gen_code, language="python")

        st.write("### 🧪 Execution Result")
        result = execute_user_code(df, gen_code)
        
        if result is None:
            st.success("✅ Code executed (no return value).")
        else:
            st.write(result)

        interactions.append({
            "question": user_question,
            "code": gen_code,
            "answer": str(result)
        })

    st.markdown("---")
    st.header("📈 Ask for a Chart")

    chart_question = st.text_input("Describe a chart to plot (e.g., 'bar chart of sales by region')")

    if chart_question:
        available_columns = list(df.columns)
        lower_columns = [col.lower() for col in available_columns]
        tokens = chart_question.lower().split()

        replacements = {}
        suggestions = []

        for token in tokens:
            matches = [col for col in lower_columns if token in col]
            if matches:
                matched_col = available_columns[lower_columns.index(matches[0])]
                replacements[token] = matched_col
            else:
                close = difflib.get_close_matches(token, lower_columns, n=1, cutoff=0.6)
                if close:
                    suggested_col = available_columns[lower_columns.index(close[0])]
                    suggestions.append(f"'{token}' → '{suggested_col}'")

        enhanced_question = chart_question
        for token, replacement in replacements.items():
            enhanced_question = enhanced_question.replace(token, replacement)

        if suggestions:
            st.warning("🔎 Possible column suggestions:\n" + "\n".join(suggestions))

        # Load chart prompt
        prompt_path = "prompts/chart_prompt.txt"
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as file:
                chart_prompt_template = file.read()
        else:
            chart_prompt_template = """
You are a data scientist.
Generate Python code using matplotlib or seaborn to plot the following chart using a DataFrame named `df`.

Instruction: {user_chart_prompt}
Available columns: {columns}

Only return Python code. No explanations.
"""

        final_chart_prompt = chart_prompt_template.format(
            user_chart_prompt=enhanced_question,
            columns=", ".join(available_columns)
        )

        with st.spinner("Generating chart code..."):
            chart_code = query_llm(final_chart_prompt.strip())

        st.code(chart_code, language="python")

        st.write("### 🖼️ Chart Output")
        result = execute_user_code(df, chart_code)

        if result is None:
            st.success("✅ Chart rendered below (if no errors).")
        else:
            st.write(result)

        interactions.append({
            "question": chart_question,
            "code": chart_code,
            "answer": str(result)
        })

    # 🔽 Commented out report generation and download
    # st.markdown("---")
    # st.header("📄 Download Summary Report")

    # if st.button("📥 Generate Report"):
    #     report_path = generate_report(interactions, summary)
    #     with open(report_path, "rb") as f:
    #         st.download_button(
    #             label="Download Markdown Report",
    #             data=f,
    #             file_name="csv_ai_report.md",
    #             mime="text/markdown"
    #         )
