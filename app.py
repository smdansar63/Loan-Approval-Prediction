import streamlit as st
import pickle
import pandas as pd

with open("loan_model.sav", "rb") as file:
    loaded_model = pickle.load(file)

with open("scaler.sav", "rb") as file:
    loaded_scaler = pickle.load(file)

st.title("Loan Approval Prediction")
st.write("Enter the application details below")

gender = st.selectbox("Gender", ["Male", "Female"])

married = st.selectbox("Marital Status", ["No", "Yes"])

dependents = st.selectbox("Number of Dependents", ["0", "1", "2", "3+"])

education = st.selectbox("Education", ["Graduate", "Not Graduate"])

self_employed = st.selectbox("Self Employed", ["No", "Yes"])

applicant_income = st.number_input(
    "Applicant Income (₹)",
    min_value=0,
    step=100
)

coapplicant_income = st.number_input(
    "Co-applicant Income (₹)",
    min_value=0,
    step=100
)

loan_amount = st.number_input(
    "Loan Amount (in thousands)",
    min_value=0,
    step=1
)

loan_term = st.selectbox(
    "Loan Amount Term (Months)",
    [12, 36, 60, 84, 120, 180, 240, 300, 360, 480]
)

credit_history = st.selectbox(
    "Credit History",
    ["Good", "Bad"]
)

property_area = st.selectbox(
    "Property Area",
    ["Rural", "Semiurban", "Urban"]
)

if st.button("Predict"):

    # Label Encoding
    gender = 1 if gender == "Male" else 0
    married = 1 if married == "Yes" else 0
    education = 0 if education == "Graduate" else 1
    self_employed = 1 if self_employed == "Yes" else 0
    credit_history = 1 if credit_history == "Good" else 0

    # Dependents
    if dependents == "3+":
        dependents = 3
    else:
        dependents = int(dependents)

    # One-Hot Encoding for Property Area
    if property_area == "Rural":
        property_area_semiurban = 0
        property_area_urban = 0

    elif property_area == "Semiurban":
        property_area_semiurban = 1
        property_area_urban = 0

    else:
        property_area_semiurban = 0
        property_area_urban = 1

    # Create DataFrame
    input_data = pd.DataFrame({
        "Gender": [gender],
        "Married": [married],
        "Dependents": [dependents],
        "Education": [education],
        "Self_Employed": [self_employed],
        "ApplicantIncome": [applicant_income],
        "CoapplicantIncome": [coapplicant_income],
        "LoanAmount": [loan_amount],
        "Loan_Amount_Term": [loan_term],
        "Credit_History": [credit_history],
        "Property_Area_Semiurban": [property_area_semiurban],
        "Property_Area_Urban": [property_area_urban]
    })

    # Scale numerical columns
    numerical_cols = [
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount"
    ]

    input_data[numerical_cols] = loaded_scaler.transform(
        input_data[numerical_cols]
    )

    # Prediction
    prediction = loaded_model.predict(input_data)

    # Display Result
    if prediction[0] == 1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Rejected")