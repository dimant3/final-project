import pandas as pd
from postgres import work_with_database
import numpy as np

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
rusell_columns = rusell[['Date', 'Close']]
# print(rusell_columns)

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
rusell_starting_stocks_qty = initial_portfolio / rusell_columns['Close'][0]
sp500_starting_stocks_qty = initial_portfolio / sp500['close'][0]

# calculated portfolio value change by month for each index (graphic 1)
nasdaq_starting_stocks_qty = float(nasdaq_starting_stocks_qty)
nasdaq['Portfolio value'] = round(nasdaq_starting_stocks_qty * nasdaq['Close'], 2)

rusell_starting_stocks_qty = float(rusell_starting_stocks_qty)
rusell_columns['Portfolio value'] = round(rusell_starting_stocks_qty * rusell_columns['Close'], 2)

sp500_starting_stocks_qty = float(sp500_starting_stocks_qty)
sp500['Portfolio value'] = round(sp500_starting_stocks_qty * sp500['close'], 2)

# calculated ROI by month for each index (graphic 2)
nasdaq['ROI %'] = round((nasdaq['Close'].pct_change()) * 100, 2)
rusell_columns['ROI %'] = round((rusell_columns['Close'].pct_change()) * 100, 2)
sp500['ROI %'] = round((sp500['close'].pct_change()) * 100, 2)

# calculating deviation from average close price for each index (graphic 3). axis=0 is column
nasdaq['Deviation from average'] = round(nasdaq['Close'] - nasdaq['Close'].mean(axis=0), 2)
rusell_columns['Deviation from average'] = round(rusell_columns['Close'] - rusell_columns['Close'].mean(axis=0), 2)
sp500['Deviation from average'] = round(sp500['close'] - sp500['close'].mean(axis=0), 2)
# 'close' column average for each index: nasdaq = 1244.74 , rusell = 1875.87 , sp500 = 384.84














# nasdaq_index = np.array([nasdaq['Close']])
# rusell_index = np.array([rusell_columns['Close']])
# sp500_index = np.array([sp500['close']])

