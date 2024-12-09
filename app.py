from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

#User input form
st.title('Energy Forecasting Demo')

#Months
selected_months = st.slider("No. of Months you are looking to forecast? ",1, 24, (1))
st.write("You selected:", selected_months, " months")

#Sector
selected_sector = st.selectbox(
    "For which sector would you like to forecast?",
    ("All", "Commercial", "Industrial", "Residential","Transportation","Other"),
    index=None,
    placeholder="Select Report type",
)
st.write("You selected:", selected_sector, " report")

#Feild
selected_feild = st.selectbox(
    "What do you want to forecast?",
    ("Customers", "Sales", "Revenue", "Price"),
    index=None,
    placeholder="Select Feild",
)
st.write("You selected:", selected_feild)





#Forecast model function
def forecast_model(user_input, forecast_df):

    #Reading user input
    months_to_predict = user_input['months']
    selected_sector = user_input['sector']
    selected_field = user_input['feild']

    filtered_df = forecast_df[(forecast_df['sector'] == selected_sector) & (forecast_df['feild'] == selected_field)]
    
    # Get the current date and calculate the cutoff date
    current_date = datetime.now()
    filtered_df['time_period'] = pd.to_datetime(filtered_df['period'])

    start_of_current_month = current_date.replace(day=1)
    cutoff_date = current_date + relativedelta(months=months_to_predict)
    cutoff_date
    
    # Filter for dates within the next 'n' months
    # Filter for dates within the next 'n' months
    result_df = filtered_df[(filtered_df['time_period'] >= start_of_current_month) & 
                            (filtered_df['time_period'] <= cutoff_date)]
    
    out_df = result_df[['period', 'predicted']]

    return out_df
         
        
#Button click
if st.button("Forecast"):

    st.header("Forecast Ouput")

    #user input
    user_input = {
       'months': selected_months,
       'feild': selected_feild,
       'sector': selected_sector
    }

    forecast_df = pd.read_csv('forecast_output.csv')
    result_df = forecast_model(user_input, forecast_df)

    #Table
    st.write("Predicted consumption for:", selected_months ," months")
    st.dataframe(result_df)

    #Line chart
    st.line_chart(result_df.set_index('period')['predicted'])
