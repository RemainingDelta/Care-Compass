import requests
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

def add_bias_column(X):
    """
    Args:
        X (array): can be either 1-d or 2-d
    
    Returns:
        Xnew (array): the same array, but 2-d with a column of 1's in the first spot
    """
    
    # If the array is 1-d
    if len(X.shape) == 1:
        Xnew = np.column_stack([np.ones(X.shape[0]), X])
    
    # If the array is 2-d
    elif len(X.shape) == 2:
        bias_col = np.ones((X.shape[0], 1))
        Xnew = np.hstack([bias_col, X])
        
    else:
        raise ValueError("Input array must be either 1-d or 2-d")

    return Xnew

def line_of_best_fit(X, y):
    """
    Creates a vector which represents the line of best fit for the inputs

    Args:
        X (array) : array of predictor values not including bias terms
        y (1D array) : array of corrseponding response values to X

    Return: 

        m (vector) : vector containing values corresponding to the line of best fit for the inputted values
    
    """
    # adds a bias column to the X input
    X = add_bias_column(X)
    #calculates the vector whos values correspond to the slope and intercept of the line of best fit 
    XtXinv = np.linalg.inv(np.matmul(X.T, X))
    m = np.matmul(XtXinv, np.matmul(X.T, y))

    #returns the line of best fit vector
    return m

def linreg_predict(Xnew, ynew, b):
    """
    Returns a dictionary containing predicted values, residuals, the mean squared error, and the coefficient of determination

    Args:
        Xnew (array) : array of the predictor features, not including the bias term
        ynew (1D array) : 1D array of the corresponding response values to Xnew
        b (1D array) : array of length p+1 containing the coefficients from the line of best fit

    Return:
        result (dictionary) : dictionary containing predicted values, residuals, the mean squared error, and the coefficient of determination
    
    """
    #creates predicted values, residuals, mean squared error, and coefficient of determination
    Xnew = add_bias_column(Xnew)
    ypreds = np.dot(Xnew, b)
    res = ynew - ypreds
    mse = (res**2).mean()
    r2 = r2_score(ynew, ypreds)
    #adds the previously calculated values to a dictionary
    result = dict()
    result['ypreds'] = ypreds
    result['resids'] = res
    result['mse'] = mse
    result['r2'] = r2

    # returns the dictionary
    return result

def get_mse(y_true, y_pred):
    """ gets the MSE

    Args:
        y_true (array): the true y values
        y_pred (array): the predicted y values

    Returns:
        the mean squared error

    """
    
    return np.mean((y_true - y_pred) ** 2)

def show_fit(X, y, slope, intercept):
    """ plots a simple linear regression line through x y points and prints the slope, intercept, and MSE

    Args:
        X (array): the design matrix
        y (array): the response variable
        slope (float): the slope
        intercept (float): the intercept

    Returns:
        A plot (I'm getting lazy with these...)
    """
    
    plt.figure()
    
    # in case this wasn't done before, transform the input data into numpy arrays and flatten them
    x = np.array(X).ravel()
    y = np.array(y).ravel()
    
    # plot the actual data
    plt.scatter(x, y, label='data')
    
    # compute linear predictions 
    # x is a numpy array so each element gets multiplied by slope and intercept is added
    y_pred = slope * x + intercept
    
    # plot the linear fit
    plt.plot(x, y_pred, color='black',
             ls=':',
             label='linear fit')
    
    plt.legend()
    
    plt.xlabel('x')
    plt.ylabel('y')
    
    # print the mean squared error
    y_pred = slope * x + intercept
    mse = get_mse(y_true=y, y_pred=y_pred)
    plt.suptitle(f'y_hat = {slope:.3f} * x + {intercept:.3f}, MSE = {mse:.3f}')

#gathers a creates dataframe for expenditure dataset
def dataframe():
    headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
           
    url2 = f'https://dw.euro.who.int/api/v3/measures/HFA_570?output=data'
    url_text2 = requests.get(url2, headers=headers).text
    result2 = json.loads(url_text2)
    #print(result2)

    data = result2['data']

    #print(data)
    df_expenditure = pd.DataFrame()
    final_dict = dict()

    for item in data:
    
        final_dict['country'] = item['dimensions']['COUNTRY']
        #final_dict['country_grp'] = item['dimensions']['COUNTRY_GRP']
        final_dict['year'] = item['dimensions']['YEAR']
        #final_dict['sex'] = item['dimensions']['SEX']
        final_dict['expenditure'] = item['value']['numeric']
        series = pd.Series(final_dict)
        df_expenditure = pd.concat([df_expenditure, series.to_frame().T], ignore_index = True)

    #data = df_expenditure.to_json()
    #post = requests.post("http://localhost:4000/country/countries/post_any_data", json=data)

    #get_response = requests.get("http://localhost:4000/country/countries/get_data")

    #if get_response.status_code == 200:
        #df = pd.DataFrame(get_response.json())
    #else:
        #print("Failed to get data:", get_response.status_code)

    return df_expenditure
    
#predict function that returns the array of the line of best fit (weights)
def predict(df_expenditure, country_name):
    #print(series)
    #pd.set_option('display.max_rows', None)
    col_num_list = ['year', 'expenditure']
    df_expenditure_num = df_expenditure.loc[:, col_num_list]
    df_expenditure_scaled = pd.DataFrame()
    for item in df_expenditure_num.columns:
        df_expenditure_scaled[f'{item}_scaled'] = ((df_expenditure_num[item] - df_expenditure_num[item].mean()) / df_expenditure_num[item].std()).round(3)
    
    df_expenditure_country = df_expenditure_scaled[(df_expenditure_scaled['country'] == country_name)]

    X = np.array(df_expenditure_country['year'])
    y = np.array(df_expenditure_country['expenditure'])

    train_test = train_test_split(X, y, test_size = 0.3, random_state=42)
    #train_test
    #finds the line of best fit based on the training data and compares it to the testing data
    fit = line_of_best_fit(train_test[0], train_test[2])
    relation_dict = linreg_predict(train_test[1], train_test[3], fit)
    graph = show_fit(X, y, fit[1], fit[0])
    return fit


    #prints the mse and r^2 of the dataset
    print(f'MSE: {relation_dict['mse']}')
    print(f'R2: {relation_dict['r2']}')

