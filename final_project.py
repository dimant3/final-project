import pandas as pd
from postgres import work_with_database
import numpy as np
import matplotlib.pyplot as plt

# formatting Nasdaq csv: date format and column split
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

# calculated ROI by month for each index (graph 2)
nasdaq['ROI %'] = round((nasdaq['Close'].pct_change()) * 100, 2)
rusell['ROI %'] = round((rusell['Close'].pct_change()) * 100, 2)
sp500['ROI %'] = round((sp500['close'].pct_change()) * 100, 2)

# calculating deviation from average close price for each index (graph 3). axis=0 is column
nasdaq['Deviation from average'] = round(nasdaq['Close'] - nasdaq['Close'].mean(axis=0), 2)
rusell['Deviation from average'] = round(rusell['Close'] - rusell['Close'].mean(axis=0), 2)
sp500['Deviation from average'] = round(sp500['close'] - sp500['close'].mean(axis=0), 2)
# 'close' column average for each index: nasdaq = 1244.74 , rusell = 1875.87 , sp500 = 384.84


#Now finding how many months each INDEX closed above the average price using Boolean ( just to mention in presentation)
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
min_value_nasdaq = np.min(nasdaq['Portfolio value']) # 7708.17
max_value_nasdaq = np.max(nasdaq['Portfolio value']) # 16429.45

min_max_dif_rusell = np.ptp(rusell['Portfolio value'])
min_value_rusell = np.min(rusell['Portfolio value']) # 7144.1
max_value_rusell = np.max(rusell['Portfolio value']) # 14315.14

min_max_dif_sp500 = np.ptp(sp500['Portfolio value'])
min_value_sp500 = np.min(sp500['Portfolio value']) # 8011.38
max_value_sp500 = np.max(sp500['Portfolio value']) # 14762.69
# we found out highest difference between min and max in: nasdaq = 8721.28, rusell = 7171.04 , sp500 = 6751.31


        # In next steps we creating visualization with matplotlib and seaborn

# Adding x variable for X-Axis "Date" values
x = rusell['Date']

#plot each INDEX portfolio value
plt.plot(x, nasdaq['Portfolio value'], label='Nasdaq', color='green')
plt.plot(rusell['Portfolio value'], label='Rusell2000', color='blue')
plt.plot(sp500['Portfolio value'], label='SP500', color='red')

# Marking highest value points in each index
plt.plot(highest_nasdaq_value_index, max_value_nasdaq, marker='o', color='black', label="Highest")
plt.plot(lowest_nasdaq_value_index, min_value_nasdaq, marker='o', color='black', label="Highest")

plt.plot(highest_rusell_value_index, max_value_rusell, marker='o', color='black')
plt.plot(lowest_rusell_value_index, min_value_rusell, marker='o', color='black')

plt.plot(highest_sp500_value_index, max_value_sp500, marker='o', color='black')
plt.plot(lowest_sp500_value_index, min_value_sp500, marker='o', color='black')


#add legend
plt.legend(title='Portflio values by INDEX')

#add x and y axes with labels and a title
plt.ylabel('Value €', fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.title('Portfolios by INDEX', fontsize=16)
plt.xticks(x, rotation=45)
plt.grid()
plt.show()




# print(nasdaq)
# print(rusell)
# print(sp500)


# nasdaq_index = np.array([nasdaq['Date']])
# rusell_index = np.array([rusell['Close']])
# sp500_index = np.array([sp500['close']])
# print(rusell_index)