# Enhanced Streamlit Dashboard for LLM Evaluation Platform


import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="LLM Evaluation Dashboard",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------
# Load Data
# --------------------------------

df = pd.read_csv("reports/evaluation_report.csv")


# --------------------------------
# Data Cleaning
# --------------------------------

if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])


# --------------------------------
# Metrics Calculation
# --------------------------------


total_tests = len(df)

correct_tests = len(
    df[df["result"] == "CORRECT"]
)

incorrect_tests = len(
    df[df["result"] == "INCORRECT"]
)

accuracy = (
    correct_tests / total_tests
) * 100

hallucination_rate = (
    df["hallucination_detected"].sum()
    / total_tests
) * 100

average_latency = (
    df["latency_seconds"].mean()
)


# --------------------------------
# Sidebar
# --------------------------------

st.sidebar.title("⚙️ Dashboard Controls")

selected_result = st.sidebar.multiselect(
    "Filter Results",
    options=df["result"].unique(),
    default=df["result"].unique()
)

filtered_df = df[
    df["result"].isin(selected_result)
]


# --------------------------------
# Dashboard Header
# --------------------------------

st.title("🤖 LLM Evaluation Dashboard")

st.markdown(
    """
    Monitor AI system quality, hallucinations,
    latency, and evaluation performance.
    """
)

st.divider()


# --------------------------------
# KPI Cards
# --------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Total Tests",
        total_tests
    )

with col2:
    st.metric(
        "✅ Accuracy",
        f"{accuracy:.2f}%"
    )

with col3:
    st.metric(
        "⚠️ Hallucination Rate",
        f"{hallucination_rate:.2f}%"
    )

with col4:
    st.metric(
        "⏱️ Avg Latency",
        f"{average_latency:.2f} sec"
    )


st.divider()


# --------------------------------
# Charts Row 1
# --------------------------------

chart_col1, chart_col2 = st.columns(2)


# Pie Chart
with chart_col1:

    pie_data = pd.DataFrame({
        "Result": ["CORRECT", "INCORRECT"],
        "Count": [correct_tests, incorrect_tests]
    })

    pie_chart = px.pie(
        pie_data,
        names="Result",
        values="Count",
        title="📌 Evaluation Result Distribution",
        hole=0.4
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )


# Hallucination Chart
with chart_col2:

    hallucination_chart = px.bar(
        filtered_df,
        x="question",
        y="hallucination_detected",
        title="🚨 Hallucination Detection",
        text="hallucination_detected"
    )

    st.plotly_chart(
        hallucination_chart,
        use_container_width=True
    )


st.divider()


# --------------------------------
# Charts Row 2
# --------------------------------

chart_col3, chart_col4 = st.columns(2)


# Latency Chart
with chart_col3:

    latency_chart = px.bar(
        filtered_df,
        x="question",
        y="latency_seconds",
        title="⚡ Latency Per Question",
        text="latency_seconds"
    )

    st.plotly_chart(
        latency_chart,
        use_container_width=True
    )


# Similarity Score Chart
with chart_col4:

    similarity_chart = px.line(
        filtered_df,
        x="question",
        y="similarity_score",
        markers=True,
        title="📈 Similarity Score Trend"
    )

    st.plotly_chart(
        similarity_chart,
        use_container_width=True
    )


st.divider()


# --------------------------------
# Gauge Chart
# --------------------------------

st.subheader("🎯 Overall Accuracy Gauge")

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=accuracy,
    title={'text': "Accuracy %"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "green"},
        'steps': [
            {'range': [0, 50], 'color': "lightcoral"},
            {'range': [50, 80], 'color': "khaki"},
            {'range': [80, 100], 'color': "lightgreen"}
        ]
    }
))

st.plotly_chart(
    fig,
    use_container_width=True
)


st.divider()


# --------------------------------
# Evaluation Results Table
# --------------------------------

st.subheader("📋 Detailed Evaluation Results")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# --------------------------------
# Download CSV
# --------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Evaluation Report",
    data=csv,
    file_name="evaluation_report.csv",
    mime="text/csv"
)


# --------------------------------
# Footer
# --------------------------------

st.markdown("---")

st.caption(
    "Built using FastAPI, Groq, Streamlit, Plotly, and GitHub Actions"
)


