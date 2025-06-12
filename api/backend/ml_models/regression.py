import requests
import pandas as pd
import numpy as np
import json
#import plotly.express as px
#import plotly.graph_objects as go
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
def dataframe(code):
    headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
           
    url2 = f"https://dw.euro.who.int/api/v3/measures/{code}?output=data"
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
        final_dict['value'] = item['value']['numeric']
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
    df_expenditure['year'] = df_expenditure['year'].astype(float)
    df_expenditure_country = df_expenditure[(df_expenditure['country'] == country_name)]

    X = np.array(df_expenditure_country['year'])
    y = np.array(df_expenditure_country['value'])

    train_test = train_test_split(X, y, test_size = 0.3, random_state=42)
    #train_test
    #finds the line of best fit based on the training data and compares it to the testing data
    fit = line_of_best_fit(train_test[0], train_test[2])
    relation_dict = linreg_predict(train_test[1], train_test[3], fit)
    #graph = show_fit(X, y, fit[1], fit[0])
    return {
        "slope": fit[1],
        "intercept": fit[0],
        "mse": relation_dict['mse'],
        "r2": relation_dict['r2']
    }
#function for creating the X and y for the autoregressive model
def create_xy(df, country_name):

    #df['year'] = df['year'].astype(float)
    df_country = df[(df['COUNTRY'] == country_name)]
    df_country = df_country.reset_index(drop=True)
    #X = np.array(df_country['year'])
    #y = np.array(df_country['value'])
    start_year = (int(df_country['YEAR'].min()) + 10) # grab the earliest year (post lag) for the country
    index_raw = df_country.index[df_country['YEAR'] == start_year] # replace 1990 with start_year
    if len(index_raw) != 0:
        index = index_raw[0]
    # if index is null, return empty x_matrix, y_matrix
        y_vector = df_country[index :]['VALUE'].tolist()
        x_matrix = []
        x_list = []
        while index < (len(df_country)):
            for i in range(1, 11):
                temp_index = index - i
                x_list.append(df_country.iloc[temp_index]['VALUE'])
            x_matrix.append(x_list) 
            x_list = []
            index += 1
    
        x_matrix = np.array(x_matrix)
        y_vector = np.array(y_vector)
        return x_matrix, y_vector
    
    
def autoreg_train(x_matrix, y_vector):
    """
    Creates a weight vector for the autoregression model

    Args:
        X (array) : matrix of predictor values not including bias terms
        y (array) : vector of corrseponding response values to X

    Return: 

        m (vector) : vector containing values corresponding to the line of best fit for the inputted values
    
    """
    # adds a bias column to the X input
    #X = add_bias_column(x_matrix)
    X = x_matrix
    #calculates the vector whos values correspond to the slope and intercept of the line of best fit 
    XtXinv = np.linalg.pinv(np.matmul(X.T, X))
    b = np.matmul(XtXinv, np.matmul(X.T, y_vector))
    return b


def autoreg_predict(x_matrix, y_vector, b, num):

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
    #x_matrix = add_bias_column(x_matrix)
    test_vec = x_matrix[len(x_matrix) - 1]
    test_vec = test_vec.tolist()
    y_pred = []
    for i in range(num):
        y_temp = np.dot(test_vec[i + 1: ], b)
        test_vec.append(y_temp)
        y_pred.append(y_temp)
    

    #ypreds = np.dot(, b)
    #res = ynew - ypreds
    #mse = (res**2).mean()
    #r2 = r2_score(ynew, ypreds)
    #adds the previously calculated values to a dictionary
    #result['ypreds'] = ypreds
    #result['resids'] = res
    #result['mse'] = mse
    #result['r2'] = r2

    # returns the dictionary
    return y_pred

def create_xy_full(df):
    #df['year'] = df['year'].astype(float)
    #sees how many different countries are in the dataset
    country_count = []
    for country in df['COUNTRY']:

        if country not in country_count:
            df_country = df[(df['COUNTRY'] == country)]
            df_country = df_country.reset_index(drop=True)
            #X = np.array(df_country['year'])
            #y = np.array(df_country['value'])
            start_year = (int(df_country['YEAR'].min()) + 10) # grab the earliest year (post lag) for the country
            #print("Start year")
            #print(start_year)
            index_raw = df_country.index[df_country['YEAR'] == start_year] # replace 1990 with start_year
            #print(index_raw)
            if len(index_raw) != 0:
                #if index_raw[0] > 10:
                    #index = index_raw[0]
                country_count.append(country)
    country_num = len(country_count)
    #print(country_count)
    #print(country_num)
    seen_country = []
    x_matrix_final = np.empty((0, country_num + 9))
    y_vector_final = np.empty((0,1))
    #start_year = str(int(df_country['year'].min()) + 10) # grab the earliest year (post lag) for the country
    #index_raw = df_country.index[df_country['year'] == start_year] # replace 1990 with start_year
    #if len(index_raw) != 0:
        #index = index_raw[0]
    #for i in range(len(country_count)):
    for i in range(country_num):
            country = country_count[i]
            if create_xy(df, country) != None:
                x_matrix = create_xy(df, country)[0]
                country_matrix = np.zeros((country_num-1, len(x_matrix)))
                country_matrix[i : i+1] = 1
                y_vector =  create_xy(df, country)[1].reshape(-1,1)
                x_matrix = np.hstack((country_matrix.T, x_matrix))
                x_matrix_final = np.vstack((x_matrix_final, x_matrix))
                #print(y_vector_final.shape)
                #print(y_vector.shape)
                y_vector_final = np.vstack((y_vector_final, y_vector))
    x_matrix_final = np.array(x_matrix_final)
    y_vector_final = np.array(y_vector_final)
    return x_matrix_final, y_vector_final, country_num
    

def create_xy_select(df, country_input):
    #df['year'] = df['year'].astype(float)
    #sees how many different countries are in the dataset
    #print("dataframe")
    #print(df)
    #print("country input")
    #print(country_input)
    country_count = []
    for country in df['COUNTRY']:

        if country not in country_count:
            df_country = df[(df['COUNTRY'] == country)]
            df_country = df_country.reset_index(drop=True)
            #X = np.array(df_country['year'])
            #y = np.array(df_country['value'])
            start_year = (int(df_country['YEAR'].min()) + 10) # grab the earliest year (post lag) for the country
            #print("start year")
            #print(start_year)
            index_raw = df_country.index[df_country['YEAR'] == start_year] # replace 1990 with start_year
            #print(index_raw)
            if len(index_raw) != 0:
                #if index_raw[0] > 10:
                    #index = index_raw[0]
                country_count.append(country)
    country_num = len(country_count)
    
    #print("Country Count")
    #print(country_count)
    #print(country_num)
    #seen_country = []
    x_matrix_final = np.empty((0, country_num + 9))
    y_vector_final = np.empty((0,1))
    #start_year = str(int(df_country['year'].min()) + 10) # grab the earliest year (post lag) for the country
    #index_raw = df_country.index[df_country['year'] == start_year] # replace 1990 with start_year
    #if len(index_raw) != 0:
        #index = index_raw[0]
    #for i in range(len(country_count)):
    i = country_count.index(country_input)
    x_matrix = create_xy(df, country_input)[0]
    country_matrix = np.zeros((country_num-1, len(x_matrix)))
    country_matrix[i : i+1] = 1
    y_vector_final = create_xy(df, country_input)[1].reshape(-1,1)
    x_matrix_final = np.hstack((country_matrix.T, x_matrix))
    x_matrix_final = np.array(x_matrix_final)
    y_vector_final = np.array(y_vector_final)
    return x_matrix_final, y_vector_final
    

def autoreg_predict_full(x_matrix, y_vector, b, num, country_num):

    """

    """
    #creates predicted values, residuals, mean squared error, and coefficient of determination
    #x_matrix = add_bias_column(x_matrix)
    test_vec = x_matrix[len(x_matrix) - 1]
    #test_vec = test_vec.tolist()
    #print(test_vec)
    y_pred = []
    for i in range(num):
        #print(test_vec)
        test_vec = np.array(test_vec)
        y_temp = np.dot(test_vec, b)
        y_temp = y_temp[0]
        #print(y_temp)
        test_vec = test_vec.tolist()
        test_vec.insert(country_num, y_temp)
        test_vec.pop()
        y_pred.append(y_temp)
    
    return y_pred
   


def add_predict(df, preds, country):
    #df_country = df[(df['COUNTRY'] == country)]
    #df = df_country.reset_index(drop=True)
    for i in range(len(preds)):
        year = int(df.iloc[len(df) - 1]['YEAR'])
        year = year + 1
        int_year = int(year)
        new_row = {'COUNTRY': country, 'YEAR': int_year, 'VALUE': preds[i]}
        df.loc[len(df)] = new_row
    return df
   

 

