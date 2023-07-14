import pandas as pd
from postgres import work_with_database
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from matplotlib.dates import MonthLocator, YearLocator
from datetime import datetime

# formatting Nasdaq csv: date format
nasdaq = pd.read_csv('Nasdaq OMX baltic.csv')
nasdaq['Date'] = pd.to_datetime(nasdaq['Date'])
nasdaq['Date'] = nasdaq['Date'].dt.strftime('%Y-%m')
# print(nasdaq)

# formatting Russell 2000 index csv: date format, 2 column pick (Date and Close) + round
rusell = pd.read_csv('RUT Russell 2000.csv')
rusell['Date'] = pd.to_datetime(rusell['Date'])
rusell['Date'] = rusell['Date'].dt.strftime('%Y-%m')
rusell['Close'] = round(rusell['Close'], 2)

# To avoid ERROR "A value is trying to be set on a copy of a slice from a DataFrame. Try using .loc[row_indexer,col_indexer] = value instead"
# we needed to create a Dictionary of values
rusell = pd.DataFrame({
    'Date': ['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07',
             '2020-08', '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02',
             '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09',
             '2021-10', '2021-11', '2021-12', '2022-01', '2022-02', '2022-03', '2022-04',
             '2022-05', '2022-06', '2022-07', '2022-08', '2022-09', '2022-10', '2022-11',
             '2022-12'],
    'Close': [1614.06, 1476.43, 1153.1, 1310.66, 1394.04, 1441.37, 1480.43, 1561.88, 1507.69,
              1538.48, 1819.82, 1974.86, 2073.64, 2201.05, 2220.52, 2266.45, 2268.97, 2310.55,
              2226.25, 2273.77, 2204.37, 2297.19, 2198.91, 2245.31, 2028.45, 2048.09, 2070.13,
              1864.1, 1864.04, 1707.99, 1885.23, 1844.12, 1664.72, 1846.86, 1886.58, 1761.25]
})

# formatting SP500 index from postgres database with function(work_with_database) from postgres.py
data_from_postgres = work_with_database()
sp500 = pd.DataFrame(data_from_postgres, columns=['date', 'close'])
sp500['date'] = pd.to_datetime(sp500['date'])
sp500['date'] = sp500['date'].dt.strftime('%Y-%m')
sp500['close'] = pd.to_numeric(sp500['close'])
# print(sp500)

# one time buy for 10000 € for each index at starting date 2020-01
initial_portfolio = 10000
nasdaq_starting_stocks_qty = initial_portfolio / nasdaq['Close'][0]
rusell_starting_stocks_qty = initial_portfolio / rusell['Close'][0]
sp500_starting_stocks_qty = initial_portfolio / sp500['close'][0]

# calculated portfolio value change by month for each index (graph 1)
nasdaq_starting_stocks_qty = float(nasdaq_starting_stocks_qty)
nasdaq['Portfolio value'] = round(nasdaq_starting_stocks_qty * nasdaq['Close'], 2)

rusell_starting_stocks_qty = float(rusell_starting_stocks_qty)
rusell['Portfolio value'] = round(rusell_starting_stocks_qty * rusell['Close'], 2)

sp500_starting_stocks_qty = float(sp500_starting_stocks_qty)
sp500['Portfolio value'] = round(sp500_starting_stocks_qty * sp500['close'], 2)

# calculated ROI by month for each index
nasdaq['ROI %'] = round((nasdaq['Close'].pct_change()) * 100, 2)
rusell['ROI %'] = round((rusell['Close'].pct_change()) * 100, 2)
sp500['ROI %'] = round((sp500['close'].pct_change()) * 100, 2)

# calculated total ROI for whole period (3 years) for each index (graph 2)
nasdaq_total_roi = (nasdaq['Portfolio value'][35] - nasdaq['Portfolio value'][0]) / nasdaq['Portfolio value'][0] * 100
nasdaq_rounded_roi = round(nasdaq_total_roi, 2)

rusell_total_roi = (rusell['Portfolio value'][35] - rusell['Portfolio value'][0]) / rusell['Portfolio value'][0] * 100
rusell_rounded_roi = round(rusell_total_roi, 2)

sp500_total_roi = (sp500['Portfolio value'][35] - sp500['Portfolio value'][0]) / sp500['Portfolio value'][0] * 100
sp500_rounded_roi = round(sp500_total_roi, 2)

total_rois = pd.DataFrame({
    'Stocks index': ['Nasdaq', 'Russell2000', 'SP500'],
    'Total ROI': [nasdaq_rounded_roi, rusell_rounded_roi, sp500_rounded_roi]
})

# calculating deviation from average close price for each index (graph 3). axis=0 is column
nasdaq['Deviation from average'] = round(nasdaq['Close'] - nasdaq['Close'].mean(axis=0), 2)
rusell['Deviation from average'] = round(rusell['Close'] - rusell['Close'].mean(axis=0), 2)
sp500['Deviation from average'] = round(sp500['close'] - sp500['close'].mean(axis=0), 2)
# 'close' column average for each index: nasdaq = 1244.74 , rusell = 1875.87 , sp500 = 384.84


# Now finding how many months each INDEX closed above the average price using Boolean ( just to mention in presentation)
nasdaq_above_index_avg = nasdaq.value_counts(nasdaq['Close'] > nasdaq['Close'].mean())
rusell_above_index_avg = rusell.value_counts(rusell['Close'] > rusell['Close'].mean())
sp500_above_index_avg = sp500.value_counts(sp500['close'] > sp500['close'].mean())
# month for each INDEX closed above the average price: nasdaq = 20 , rusell = 18 , sp500 = 19
# month for each INDEX closed below the average price: nasdaq = 16 , rusell = 18 , sp500 = 17


# Finding highest value points in each index
highest_nasdaq_value_index = np.argmax(nasdaq['Portfolio value'])
lowest_nasdaq_value_index = np.argmin(nasdaq['Portfolio value'])

highest_rusell_value_index = np.argmax(rusell['Portfolio value'])
lowest_rusell_value_index = np.argmin(rusell['Portfolio value'])

highest_sp500_value_index = np.argmax(sp500['Portfolio value'])
lowest_sp500_value_index = np.argmin(sp500['Portfolio value'])

# Here we wanted to see which INDEX has highest difference between min and max in portfolio values
min_max_dif_nasdaq = np.ptp(nasdaq['Portfolio value'])
min_value_nasdaq = np.min(nasdaq['Portfolio value'])  # 7708.17
max_value_nasdaq = np.max(nasdaq['Portfolio value'])  # 16429.45

min_max_dif_rusell = np.ptp(rusell['Portfolio value'])
min_value_rusell = np.min(rusell['Portfolio value'])  # 7144.1
max_value_rusell = np.max(rusell['Portfolio value'])  # 14315.14

min_max_dif_sp500 = np.ptp(sp500['Portfolio value'])
min_value_sp500 = np.min(sp500['Portfolio value'])  # 8011.38
max_value_sp500 = np.max(sp500['Portfolio value'])  # 14762.69


# we found out highest difference between min and max in: nasdaq = 8721.28, rusell = 7171.04 , sp500 = 6751.31


# In next steps we creating visualization with matplotlib and seaborn

# 1. creating function to call Indexes portfolio values by month
def show_portfolio_values():
    # Adding x variable for X-Axis "Date" values
    x = rusell['Date']
    plt.figure(figsize=(14, 10))
    plt.plot(x, nasdaq['Portfolio value'], label='Nasdaq', color='green')
    plt.plot(rusell['Portfolio value'], label='Russell2000', color='blue')
    plt.plot(sp500['Portfolio value'], label='SP500', color='red')

    # Marking the highest value points in each index
    plt.plot(highest_nasdaq_value_index, max_value_nasdaq, marker='o', color='black', label="Highest")
    plt.plot(lowest_nasdaq_value_index, min_value_nasdaq, marker='o', color='black', label="Lowest")

    plt.plot(highest_rusell_value_index, max_value_rusell, marker='o', color='black')
    plt.plot(lowest_rusell_value_index, min_value_rusell, marker='o', color='black')

    plt.plot(highest_sp500_value_index, max_value_sp500, marker='o', color='black')
    plt.plot(lowest_sp500_value_index, min_value_sp500, marker='o', color='black')

    # add legend
    plt.legend(title='Portfolio values by INDEX')

    # adding x and y axes with labels and a title
    plt.ylabel('Value €', fontsize=14)
    plt.xlabel('Date', fontsize=14)
    plt.title('Portfolios by INDEX', fontsize=16)
    plt.xticks(x, rotation=45)
    plt.grid()
    plt.show()


# 2. Creating function (def) to show total ROI for each index.
def show_index_total_roi():
    plt.figure(figsize=(12, 8))
    plt.bar(total_rois['Stocks index'], total_rois['Total ROI'])
    plt.ylabel('ROI %')
    plt.title('Total ROI by indexes')
    plt.rcParams.update({'font.size': 22})
    plt.show()


# 3. Creating function to show each index deviation from standard.
# Nasdaq graph
def show_nasdaq_deviation():
    x = rusell['Date']
    nas = nasdaq['Deviation from average'].mean()
    filter_data = nasdaq[nasdaq['Deviation from average'] > nas]
    filter_data2 = nasdaq[nasdaq['Deviation from average'] < nas]
    plt.figure(figsize=(14, 10))
    plt.plot(x, nasdaq['Deviation from average'], label='Nasdaq', color='darkgreen')
    plt.scatter(filter_data.index, filter_data['Deviation from average'], color='red', label='20 dots above')
    plt.scatter(filter_data2.index, filter_data2['Deviation from average'], color='blue', label='16 dots below')
    plt.axhline(y=nas, color='black', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Deviation from average')
    plt.title('Nasdaq deviation from average')
    plt.legend()
    plt.xticks(x, rotation=45)
    plt.show()


# Russell 2000 graph
def show_russell2000_deviation():
    x = rusell['Date']
    rus = rusell['Deviation from average'].mean()
    filter_data_rus = rusell[rusell['Deviation from average'] > rus]
    filter_data_rus2 = rusell[rusell['Deviation from average'] < rus]
    plt.figure(figsize=(14, 10))
    plt.plot(x, rusell['Deviation from average'], label='Russell2000', color='purple')
    plt.scatter(filter_data_rus.index, filter_data_rus['Deviation from average'], color='red', label='18 dots above')
    plt.scatter(filter_data_rus2.index, filter_data_rus2['Deviation from average'], color='blue', label='18 dots below')
    plt.axhline(y=rus, color='black', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Deviation from average')
    plt.title('Russell 2000 deviation from average')
    plt.legend()
    plt.xticks(x, rotation=45)
    plt.show()

show_russell2000_deviation()

# SP500 graph
def show_sp500_deviation():
    x = rusell['Date']
    spy = sp500['Deviation from average'].mean()
    filter_data_spy = sp500[sp500['Deviation from average'] > spy]
    filter_data_spy2 = sp500[sp500['Deviation from average'] < spy]
    plt.figure(figsize=(14, 10))
    plt.plot(x, sp500['Deviation from average'], label='SP500', color='black')
    plt.scatter(filter_data_spy.index, filter_data_spy['Deviation from average'], color='red', label='19 dots above')
    plt.scatter(filter_data_spy2.index, filter_data_spy2['Deviation from average'], color='blue', label='17 dots below')
    plt.axhline(y=spy, color='black', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Deviation from average')
    plt.title('SP500 deviation from average')
    plt.legend()
    plt.xticks(x, rotation=45)
    plt.show()


# function to call 1st graph - Portfolio values by indexes
# show_portfolio_values()

# funtion to call 2nd graph - Total ROI by indexes for whole period
# show_index_total_roi()

# function to call 3rd graphs - indexes deviation vs average deviation
# show_nasdaq_deviation()
# show_russell2000_deviation()
# show_sp500_deviation()


# FORECAST
def nasdaq_forecast():
    sns.set()

    x = pd.to_datetime(nasdaq['Date'])
    y = nasdaq['Close']

    # Train-test split
    train_size = int(len(x) * 0.69) #69% for training
    x_train, x_test = x[:train_size], x[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    #Creating and training the model
    model = LinearRegression()
    x_train_ordinal = x_train.map(datetime.toordinal).values.reshape(-1, 1)
    model.fit(x_train_ordinal, y_train)

    # Predict on the test data
    x_test_ordinal = x_test.map(datetime.toordinal).values.reshape(-1, 1)
    y_pred = model.predict(x_test_ordinal)

    # Pllot the actual data, predicted values and train-test split
    plt.figure(figsize=(14, 10))
    plt.plot(x, y, label='Actual', color='black')
    plt.plot(x_test, y_pred, label='Prediction', linestyle='--')
    plt.plot(x_train, y_train, color='black')
    plt.plot(x_test, y_test, label='Testing', color='red')
    plt.xlabel('Date')
    plt.ylabel('Index Price')
    plt.xticks(rotation=45)
    plt.title('Train/test split for Nasdaq index')
    plt.legend()
    plt.show()

def russell_forecast():
    sns.set()

    x = pd.to_datetime(rusell['Date'])
    y = rusell['Close']

    # Train-test split
    train_size = int(len(x) * 0.69) #69% for training
    x_train, x_test = x[:train_size], x[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    #Creating and training the model
    model = LinearRegression()
    x_train_ordinal = x_train.map(datetime.toordinal).values.reshape(-1, 1)
    model.fit(x_train_ordinal, y_train)

    # Predict on the test data
    x_test_ordinal = x_test.map(datetime.toordinal).values.reshape(-1, 1)
    y_pred = model.predict(x_test_ordinal)

    # Pllot the actual data, predicted values and train-test split
    plt.figure(figsize=(14, 10))
    plt.plot(x, y, label='Actual', color='black')
    plt.plot(x_test, y_pred, label='Prediction', linestyle='--')
    plt.plot(x_train, y_train, color='black')
    plt.plot(x_test, y_test, label='Testing', color='red')
    plt.xlabel('Date')
    plt.ylabel('Index Price')
    plt.xticks(rotation=45)
    plt.title('Train/test split for Russell 2000 index')
    plt.legend()
    plt.show()

def sp500_forecast():
    sns.set()

    x = pd.to_datetime(sp500['date'])
    y = sp500['close']

    # Train-test split
    train_size = int(len(x) * 0.69) #69% for training
    x_train, x_test = x[:train_size], x[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    #Creating and training the model
    model = LinearRegression()
    x_train_ordinal = x_train.map(datetime.toordinal).values.reshape(-1, 1)
    model.fit(x_train_ordinal, y_train)

    # Predict on the test data
    x_test_ordinal = x_test.map(datetime.toordinal).values.reshape(-1, 1)
    y_pred = model.predict(x_test_ordinal)

    # Pllot the actual data, predicted values and train-test split
    plt.figure(figsize=(14, 10))
    plt.plot(x, y, label='Actual', color='black')
    plt.plot(x_test, y_pred, label='Prediction', linestyle='--')
    plt.plot(x_train, y_train, color='black')
    plt.plot(x_test, y_test, label='Testing', color='red')
    plt.xlabel('Date')
    plt.ylabel('Index Price')
    plt.xticks(rotation=45)
    plt.title('Train/test split for S&P500 index')
    plt.legend()
    plt.show()