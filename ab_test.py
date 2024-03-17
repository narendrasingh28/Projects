import streamlit as st
import numpy as np
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt

def visualize_clicks_by_device(ab_test_data):
    device_clicks = ab_test_data.groupby('Device')['Clicks'].sum()
    fig, ax = plt.subplots()
    device_clicks.plot(kind='bar', ax=ax)
    ax.set_xlabel('Device')
    ax.set_ylabel('Total Clicks')
    ax.set_title('Total Clicks by Device')
    return fig, ax

def ab_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level):
    control_rate = control_conversions / control_visitors
    treatment_rate = treatment_conversions / treatment_visitors
    z_score = (treatment_rate - control_rate) / np.sqrt((control_rate * (1 - control_rate)) / control_visitors)
    alpha = 1 - (confidence_level / 100)
    z_critical = stats.norm.ppf(1 - alpha / 2)
    
    if z_score > z_critical:
        return "Experiment Group is Better"
    elif z_score < -z_critical:
        return "Control Group is Better"
    else:
        return "Indeterminate"

def main():
    st.title("A/B Test Hypothesis Testing App")

    st.subheader("Upload the A/B Testing Dataset")
    uploaded_file = st.file_uploader("Upload A/B Testing Dataset", type=["xlsx", "xls"])

    if uploaded_file is not None:
        ab_test_data = pd.read_excel(uploaded_file)
        st.write("Uploaded Data:")
        st.write(ab_test_data)

        st.subheader("Total Clicks by Device")
        fig, ax = visualize_clicks_by_device(ab_test_data)
        st.pyplot(fig)

        st.subheader("Hypothesis Testing")
        st.write("Enter the following inputs to perform the hypothesis test:")
        control_visitors = st.number_input("Control Group Visitors", value=5000)
        control_conversions = st.number_input("Control Group Conversions", value=400)
        treatment_visitors = st.number_input("Treatment Group Visitors", value=5000)
        treatment_conversions = st.number_input("Treatment Group Conversions", value=420)
        confidence_level = st.select_slider("Confidence Level", options=[90, 95, 99], value=95)

        if st.button("Run Hypothesis Test"):
            result = ab_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level)
            st.write("Result of Hypothesis Test:", result)

if __name__ == "__main__":
    main()
