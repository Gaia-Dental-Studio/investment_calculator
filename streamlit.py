# streamlit.py

import streamlit as st
import requests
import pandas as pd

# Streamlit UI to gather inputs
st.title("Investment Calculator")


selected_scheme = st.selectbox("Select Scheme", ["By Term", "By Expected Return"])
number_of_period = None
expected_total_return = None


if selected_scheme == "By Term":


    col1, col2 = st.columns(2)

    with col1:
        monthly_saving = st.number_input("Monthly Saving Amount", min_value=0.0, value=500.0)
        number_of_period = st.number_input("Number of Periods (Months)", min_value=1, value=12)
        
    with col2:
        interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.0)
        starting_amount = st.number_input("Starting Amount", min_value=0.0, value=1000.0)
        
else:
    col1, col2 = st.columns(2)
    with col1:
        monthly_saving = st.number_input("Monthly Saving Amount", min_value=0.0, value=500.0)
        expected_total_return = st.number_input("Expected Total Return", min_value=1, value=3000)
        
    with col2:
        interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.0)
        starting_amount = st.number_input("Starting Amount", min_value=0.0, value=1000.0)

# Run button
if st.button("Calculate"):
    
    if number_of_period is None and expected_total_return is not None:
        scheme = "By Expected Return"
    elif number_of_period is not None and expected_total_return is None:
        scheme = "By Term"
    # Prepare data for POST request
    data = {
        "monthly_saving": monthly_saving,
        "number_of_period": number_of_period,
        "interest_rate": interest_rate,
        "starting_amount": starting_amount,
        "expected_total_return": expected_total_return,
        "scheme": scheme
    }

    # Send data to the Flask API
    response = requests.post("http://127.0.0.1:5000/calculate", json=data)

    if response.status_code == 200:
        result = response.json()

        # Display the results in Streamlit
        st.write("### Investment Summary")
        st.write(result["summary"])

        st.write("### Savings Breakdown")
        savings_breakdown_df = pd.DataFrame(result["savings_breakdown"])
        st.dataframe(savings_breakdown_df, column_order=["Month", "Deposit", "Interest", "Ending Balance"], hide_index=True)
    else:
        st.error("Error: Could not retrieve data from the server.")
