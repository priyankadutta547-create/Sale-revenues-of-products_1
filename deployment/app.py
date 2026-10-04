import streamlit as st
import pandas as pd
import joblib
import requests

# Load the trained regression model
def load_model():
    return joblib.load("SuparKart_sale_prediction_v1.0.joblib")

model = load_model()
#Base URL for backend
BACKEND_URL = "http://backend:7860"

# Streamlit UI for Boston Housing Price Prediction
st.title("Stores' total sales based on product ")
st.write("This app predicts the sales forecast predicting the future sales based on historical data.")
st.write("Enter the details:")

# Collect user input using sliders
Product_Id = st.selectbox("Unique identifier of each product", ['FD6114', 'FD5484', 'NC1071', 'FD3342'])
Product_Weight = st.number_input("Weight of each product", min_value=4.28, value=5.0, step=0.01)
Product_Sugar_Content = st.selectbox("Sugar content of each product", ['Low Sugar', 'No Sugar', 'Regular', 'Reg'])
Product_Allocated_Area = st.number_input("Ratio of the allocated display area", min_value=0.004, max_value=1.0, step=0.001, value=0.010)
Product_Type = st.selectbox("Type of product", ['Frozen Fruit', 'Canned', 'Health and Hygiene', 'Meat'])
Product_MRP = st.number_input("MRP of each product", min_value=41.84, value=51.0, step=0.01)
Store_Id = st.selectbox("Unique identifier of each store", ['OUT001', 'OUT002', 'OUT004', 'OUT005'])
Store_Establishment_Year = st.number_input("Year of establishment", min_value=1987, max_value=2009, step=1, value=1999)
Store_Size = st.selectbox("Size of the store, depending on sq. feet", ['High', 'Medium', 'Low'])
Store_Location_City_Type = st.selectbox("Store located city", ['Tier 1', 'Tier 2', 'Tier 3'])
Store_Type = st.selectbox("Type of store", ['Departmental Store', 'Supermarket Type 1', 'Supermarket Type 2', 'Food Mart'])

# Create input DataFrame
input_data = pd.DataFrame([{
    'Product_Id': Product_Id,
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_Type': Product_Type,
    'Product_MRP': Product_MRP,
    'Store_Id': Store_Id,
    'Store_Establishment_Year': Store_Establishment_Year,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type
}])

# Predict button

if st.button("Predict Sales", type="primary"):
    response = requests.post(
        f"{BACKEND_URL}/v1/rental",
        json=input_data.to_dict(orient='records')[0]
    )

    if response.status_code == 200:
        prediction = response.json()['Predicted Sales Revenue']
        st.success(f"Predicted Product Store Sales Total: {prediction}")
    else:
        st.error("Unable to connect to the prediction API")
  
#Section for Batch prediction
st.subheader("Batch Prediction")

# Allowing user to upload the csv file for batch prediction
uploaded_file = st.file_uploader(
    "Upload the CSV file",
    type=["csv"]
)

# Making the batch prediction
if uploaded_file is not None:
    if st.button("Predict for Batch", type="primary"):

        response = requests.post(
            f"{BACKEND_URL}/v1/rentalbatch",
            files={"file": uploaded_file}
        )

        if response.status_code == 200:
            result = response.json()

            st.header("Batch Prediction Results")
            st.write(result)
        else:
            st.error("Unable to connect to prediction API")
