import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import time

from modules.style import style_sidebar, set_background
style_sidebar()

SideBarLinks()

headers = {
    "User-Agent": "Python/requests",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# backend endpoint URL
API_URL = "http://host.docker.internal:4000/country/countries"  

country_list = []

try:
    #gathers the coutry data for the dropdown box (country and country code)
    response = requests.get(API_URL, headers=headers, timeout=10)
    response.raise_for_status()

    #converts gathered data into json
    data = response.json()

    country_list = [item["name"] for item in data]
    code_list = [item["code"] for item in data]
    #creates list of countrys and their corresponding country codes
    country_code_list = [item['name'] + '-' + item['code'] for item in data]
    print("Countries:", country_list)

#throws errors if get request was unsuccessful
except requests.exceptions.RequestException as e:
    print("API request failed:", e)
except (KeyError, TypeError) as e:
    print("Unexpected response format:", e)


st.title("SET AND MONITOR TARGET Values")
st.write("")

col1, col2 = st.columns(2)

with col1:
    #creates the dropdown box and returns only the country code of the selected country
    chosen_country2 = st.selectbox(
            "Choose Country:",
            country_code_list,
            index=None,
            placeholder="Select Country ..."
        )
    if chosen_country2:
        start_index = (str(chosen_country2)).index('-') + 1
        chosen_country = chosen_country2[start_index:]
        st.write("You selected ", chosen_country2)
    else:
        st.info("Please select a country to proceed")
     #st.form_submit_button(
        #  label="Submit", 
         # help=None, 
         # on_click=None, 
         # args=None,  
       # )
    submit = st.button("Submit", type="primary")

     
    if submit:
        col2.subheader("Current Scores for %s" %chosen_country)
        col2.write("Scores")

st.write("")
st.write("")
st.subheader("INPUT TARGET Values")
col_calculate, col_null = st.columns(2)
#creates the calculate button for calculating target values
with col_calculate:
    calculate_bool = False
    calculate = st.button("Calculate", type="primary")
    if calculate:
        calculate_bool = True
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
        

cola,colb,colc = st.columns(3)

expectancy_bool = False
births_bool = False
practitioners_bool = False
expenditure_bool = False
impoverished_bool = False



# creates input box for each W.H.O value

# each input box follows the same format as 
# demonstrated within the code for the life expectancy input box below.
with cola:
        #input box for life expectancy
        life_expectancy = st.number_input("Life Expectancy")
        if life_expectancy and calculate_bool:
            expectancy_value = life_expectancy
            expectancy_bool = True
            
            #data code for life expectancy and get request url which passes through country and data_code
            data_code = "H2020_17"
            api_url = f"http://host.docker.internal:4000/ml/ml/get_regression/{chosen_country},{data_code}"
            try:
                headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
                }
                #returns data gathered from the get request
                response = requests.get(api_url, headers=headers, timeout=10)
                response_text = requests.get(api_url, headers=headers, timeout=10).text

                #calculates the predicted date if the get request was successful 
                if response.status_code == 200:
                    if expectancy_bool and calculate_bool:
                        data = response.json()  
                        m = data['slope']
                        if m == 0:
                            m = 1
                        calculation = (float(expectancy_value) - data['intercept']) / m
                        st.write("The predicted date for this value is:")
                        st.write(round(calculation))
                        #st.badge(f"The predicted date for this value is: {round(calculation, 1)}", color='blue')
                # returns the status_code if an error with the get request is encountered
                # or if data for the requested country does not exist for the given dataset
                else:
                    st.error(f"Error: {response.status_code}")
                    st.error(f"No life expectancy data for: {chosen_country}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.write(f"URL that worked : {api_url}")   


             
        mortality = st.number_input("Infant Mortality Rate")
        if mortality and calculate_bool:
             mortality_bool = True
             mortality_value = mortality
             data_code = "H2020_19"
             api_url = f"http://host.docker.internal:4000/ml/ml/get_regression/{chosen_country},{data_code}"
             try:
                headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
                }

                response = requests.get(api_url, headers=headers, timeout=10)
                response_text = requests.get(api_url, headers=headers, timeout=10).text

                if response.status_code == 200:
                    if mortality_bool and calculate_bool:
                        data = response.json()  
                        m = data['slope']
                        if m == 0:
                            m = 1
                        calculation = (float(mortality_value) - data['intercept']) / m
                        st.write("The predicted date for this value is:")
                        st.write(round(calculation))
                        #st.badge(f"The predicted date for this value is: {round(calculation, 1)}", color='blue')
                else:
                    st.error(f"Error: {response.status_code}")
                    st.error(f"No life expectancy data for: {chosen_country}")
             except Exception as e:
                st.error(f"Error: {str(e)}")
                st.write(f"URL that worked : {api_url}")

with colb:
        live_births = st.number_input("Live Births per 1,000 Population")
        if live_births and calculate_bool:
             births_bool = True
             live_births_value = live_births
             data_code = "HFA_16"
             api_url = f"http://host.docker.internal:4000/ml/ml/get_regression/{chosen_country},{data_code}"
             try:
                headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
                }

                response = requests.get(api_url, headers=headers, timeout=10)
                response_text = requests.get(api_url, headers=headers, timeout=10).text

                if response.status_code == 200 :
                    if births_bool and calculate_bool:
                        data = response.json()  
                        m = data['slope']
                        if m == 0:
                            m = 1
                        calculation = (float(live_births_value) - data['intercept']) / m
                        st.write("The predicted date for this value is:")
                        st.write(round(calculation))
                        #st.badge(f"The predicted date for this value is: {round(calculation, 1)}", color='blue')
                else:
                    st.error(f"Error: {response.status_code}")
                    st.error(f"No life expectancy data for: {chosen_country}")
             except Exception as e:
                st.error(f"Error: {str(e)}")
                st.write(f"URL that worked : {api_url}")
             
        practitioners = st.number_input("General Practitioners Per 10,000 Population")
        if practitioners and calculate_bool:
             practitioners_value = practitioners
             practitioners_bool = True
             data_code = "HLTHRES_67"
             api_url = f"http://host.docker.internal:4000/ml/ml/get_regression/{chosen_country},{data_code}"
             try:
                headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
                }

                response = requests.get(api_url, headers=headers, timeout=10)
                response_text = requests.get(api_url, headers=headers, timeout=10).text

                if response.status_code == 200:
                    if practitioners_bool and calculate_bool:
                        data = response.json()  
                        m = data['slope']
                        if m == 0:
                            m = 1
                        calculation = (float(practitioners_value) - data['intercept']) / m
                        st.write("The predicted date for this value is:")
                        st.write(round(calculation))
                        #st.badge(f"The predicted date for this value is: {round(calculation, 1)}", color='blue')
                else:
                    st.error(f"Error: {response.status_code}")
                    st.error(f"No life expectancy data for: {chosen_country}")
             except Exception as e:
                st.error(f"Error: {str(e)}")
                st.write(f"URL that worked : {api_url}")
             
             
             
       


with colc:
        expenditure = st.number_input("Total Health Expenditure per Capita")
        if expenditure and calculate_bool:
            expenditure_value = expenditure
            expenditure_bool = True
            data_code = "HFA_570"
            api_url = f"http://host.docker.internal:4000/ml/ml/get_regression/{chosen_country},{data_code}"
            try:
                headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
                }

                response = requests.get(api_url, headers=headers, timeout=10)
                response_text = requests.get(api_url, headers=headers, timeout=10).text

                if response.status_code == 200 :
                    if expenditure_bool and calculate_bool:
                        data = response.json()  
                        m = data['slope']
                        if m == 0:
                            m = 1
                        calculation = (float(expenditure_value) - data['intercept']) / m
                        st.write("The predicted date for this value is:")
                        st.write(round(calculation))
                        #st.badge(f"The predicted date for this value is: {round(calculation, 1)}", color='blue')
                else:
                    st.error(f"Error: {response.status_code}")
                    st.error(f"No life expectancy data for: {chosen_country}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.write(f"URL that worked : {api_url}")
            
             

        impoverished = st.number_input("Impoverished Households")
        if impoverished and calculate_bool:
            impoverished_value = impoverished
            impoverished_bool = True
            data_code = "UHCFP_2"
            api_url = f"http://host.docker.internal:4000/ml/ml/get_regression/{chosen_country},{data_code}"
            try:
                headers = {
                "User-Agent": "Python/requests",
                "Accept": "application/json",
                "Content-Type": "application/json"
                }

                response = requests.get(api_url, headers=headers, timeout=10)
                response_text = requests.get(api_url, headers=headers, timeout=10).text

                if response.status_code == 200 :
                    data = response.json()  
                    m = data['slope']
                    if m == 0:
                        m = 1
                    if impoverished_bool and calculate_bool:
                        
                        calculation = (float(impoverished_value) - data['intercept']) / m
                        st.write("The predicted date for this value is:")
                        st.write(round(calculation))
                        #st.badge(f"The predicted date for this value is: {round(calculation, 1)}", color='blue')
                else:
                    st.error(f"Error: {response.status_code}")
                    st.error(f"No life expectancy data for: {chosen_country}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.write(f"URL that worked : {api_url}")

        









