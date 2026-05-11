import pandas as pd
import streamlit as st


# Page title
st.title("LLM Evaluation Dashboard")


# Load CSV report
df = pd.read_csv("reports/evaluation_report.csv")


# Metrics
total_tests = len(df)

correct_tests = len(df[df["result"] == "CORRECT"])

accuracy = (correct_tests / total_tests) * 100

hallucination_rate = (
    df["hallucination_detected"].sum() / total_tests
) * 100

average_latency = df["latency_seconds"].mean()


# Display metrics
st.metric("Total Tests", total_tests)

st.metric("Accuracy", f"{accuracy:.2f}%")

st.metric(
    "Hallucination Rate",
    f"{hallucination_rate:.2f}%"
)

st.metric(
    "Average Latency",
    f"{average_latency:.2f} sec"
)


# Show evaluation table
st.subheader("Evaluation Results")

st.dataframe(df)