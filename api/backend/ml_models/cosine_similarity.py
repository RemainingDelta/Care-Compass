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


def get_similar(chosen_country):

  headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
  }

# Fix this to not just call API here?
  ghs_index = pd.read_csv('https://www.ghsindex.org/wp-content/uploads/2022/04/2021-GHS-Index-April-2022.csv')


  ghs_index_2021 = ghs_index[(ghs_index['Year'] == 2021)]
  ghs_index_2021_factors = ghs_index_2021[["1) PREVENTION OF THE EMERGENCE OR RELEASE OF PATHOGENS", "2) EARLY DETECTION & REPORTING FOR EPIDEMICS OF POTENTIAL INT'L CONCERN", "3) RAPID RESPONSE TO AND MITIGATION OF THE SPREAD OF AN EPIDEMIC",
                          "4) SUFFICIENT & ROBUST HEALTH SECTOR TO TREAT THE SICK & PROTECT HEALTH WORKERS","5) COMMITMENTS TO IMPROVING NATIONAL CAPACITY, FINANCING AND ADHERENCE TO NORMS", "6) OVERALL RISK ENVIRONMENT AND COUNTRY VULNERABILITY TO BIOLOGICAL THREATS"]]
  # gets the numeric features for the 6 main categories for ghs_index and standardizes them
  ghs_index_2021_scaled = ghs_index_2021_factors[["1) PREVENTION OF THE EMERGENCE OR RELEASE OF PATHOGENS", "2) EARLY DETECTION & REPORTING FOR EPIDEMICS OF POTENTIAL INT'L CONCERN", "3) RAPID RESPONSE TO AND MITIGATION OF THE SPREAD OF AN EPIDEMIC",
                          "4) SUFFICIENT & ROBUST HEALTH SECTOR TO TREAT THE SICK & PROTECT HEALTH WORKERS","5) COMMITMENTS TO IMPROVING NATIONAL CAPACITY, FINANCING AND ADHERENCE TO NORMS", "6) OVERALL RISK ENVIRONMENT AND COUNTRY VULNERABILITY TO BIOLOGICAL THREATS"]]
  for feat in ghs_index_2021_scaled.columns:
    ghs_index_2021_scaled[feat] = (ghs_index_2021_scaled[feat] - ghs_index_2021_scaled[feat].mean()) / ghs_index_2021_scaled[feat].std()

  #ghs_index_2021.head()
  #ghs_index_2021_scaled.head()

  # which countries are most similar to Vietnam (example)
  country_index = ghs_index_2021.index[ghs_index_2021['Country'] == chosen_country].tolist()
  #print(f'Country index: {country_index}')
  the_country_vec = ghs_index_2021_scaled.iloc[country_index].to_numpy()
  print("This is the full data point for country:\n", the_country_vec)

  # this creates empty lists to fill in with the dot products and cos(theta) of each country relative to Vietnam
  the_country_dot_products = []
  the_country_cosines = []

  # this goes iteratively (loops) through each song in the data set and:
  # (a) calculates the dot product between Mr. Brightside and the song
  # (b) calculates the cosine(theta) between Mr. Brightside and the song
  for country in range(ghs_index_2021_scaled.shape[0]):

    temp_country_vec = ghs_index_2021_scaled.iloc[country].to_numpy()

    temp_dot = np.dot(the_country_vec, temp_country_vec)
    temp_cos = temp_dot/(np.linalg.norm(the_country_vec) * np.linalg.norm(temp_country_vec))

    the_country_dot_products.append(temp_dot[0])
    the_country_cosines.append(temp_cos[0])

  # this puts the country similarity info into a dataframe 
  dict_country = {'Country': ghs_index_2021.Country,
            'the_country_dot_product': the_country_dot_products,
            'the_country_cosine': the_country_cosines}
  df_country = pd.DataFrame(dict_country)

  # this sorts the data by the cosine score
  sorted_df_country = df_country.sort_values(by='the_country_cosine', ascending=False)

  return sorted_df_country




