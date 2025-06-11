"""
model01.py is an example of how to access model parameter values that you are storing
in the database and use them to make a prediction when a route associated with prediction is
accessed. 
"""
from backend.db_connection import db
import numpy as np
# import logging

from flask import current_app
import requests 
import pandas as pd
import json


def get_similar(chosen_country, weights_vect, ghs_index_2021, ghs_index_2021_scaled):
  print(weights_vect)  

  #weights_vect = float(weights_vect)

  # Fix this to not just call API here and get from database table
  #ghs_index = pd.read_csv('https://www.ghsindex.org/wp-content/uploads/2022/04/2021-GHS-Index-April-2022.csv')


  #ghs_index_2021 = ghs_index[(ghs_index['Year'] == 2021)]

  #print("This is the uncleaned ghs_index")
  #print(ghs_index_2021)

  #print("This is the cleaned ghs_index")
  #print(ghs_index_2021_scaled)

  #converting country code to country
# Your backend endpoint URL
  country_url = "http://host.docker.internal:4000/country/countries"  


  try:
    headers = {
        "User-Agent": "Python/requests",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.get(country_url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    df_country_and_code = pd.DataFrame(data)
    #print(df_country_and_code)

    for index, row in df_country_and_code.iterrows():
       if row['name'] == chosen_country:
         chosen_country = row['code']
  except requests.exceptions.RequestException as e:
    print("API request failed:", e)

  sum = 0
  #scaling the weights correctly 
  for x in weights_vect:
    sum += x
    
  for i in range(len(weights_vect)):
    weights_vect[i] = weights_vect[i]/sum
    
  #print("THIS IS MY ATTEMPT TO FIX THE WEIGHTS:", weights_vect)

  # which countries are most similar to the given country
  country_index = ghs_index_2021.index[ghs_index_2021['country'] == chosen_country].tolist()
  #print(f'Country index: {country_index}')
  the_country_vec = ghs_index_2021_scaled.iloc[country_index].to_numpy()
  #print("This is the full data point for country:\n", the_country_vec)
  #print("WEIGHTS VECTOR:\n", weights_vect)
  #doing the weight scaling for chosen country 
  the_country_vec = np.multiply(the_country_vec, weights_vect)
  #print(the_country_vec)

  


  # this creates empty lists to fill in with the dot products and cos(theta) of each country relative to Vietnam
  the_country_dot_products = []
  the_country_cosines = []

  # this goes iteratively (loops) through each country in the data set and:
  # (a) calculates the dot product between the chosen country and the current country 
  # (b) calculates the cosine(theta) between the chosen country and the current country
  for country in range(ghs_index_2021_scaled.shape[0]):

    temp_country_vec = ghs_index_2021_scaled.iloc[country].to_numpy()

    #print("THE VECTOR BEFORE:", temp_country_vec.shape)
    #doing the weight scaling for temp country 
    temp_country_vec = np.multiply(temp_country_vec, weights_vect)
    #print("This is the temp country vec as you can see:")
    #print(temp_country_vec)
    #print("THE VECTOR AFTER:", the_country_vec.shape)

    temp_dot = np.dot(the_country_vec, temp_country_vec)
    temp_cos = temp_dot/(np.linalg.norm(the_country_vec) * np.linalg.norm(temp_country_vec))

    #adding to the respective lists
    the_country_dot_products.append(temp_dot[0])
    the_country_cosines.append(temp_cos[0])

  # this puts the country similarity info into a dataframe 
  dict_country = {'Country': ghs_index_2021.country,
            'the_country_dot_product': the_country_dot_products,
            'the_country_cosine': the_country_cosines}
  df_country = pd.DataFrame(dict_country)

  # this sorts the data by the cosine score
  sorted_df_country = df_country.sort_values(by='the_country_cosine', ascending=False)

  return sorted_df_country




