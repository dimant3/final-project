import pandas as pd

# formatting Nasdaq csv: date format and column split
nasdaq = pd.read_csv('Nasdaq OMX baltic.csv')
nasdaq['Date'] = pd.to_datetime(nasdaq['Date'])
nasdaq['Date'] = nasdaq['Date'].dt.strftime('%Y-%m')
print(nasdaq)

# formatting Russell 2000 index csv: date format, 2 column pick (Date and Close) + round
rusell = pd.read_csv('RUT Russell 2000.csv')
rusell['Date'] = pd.to_datetime(rusell['Date'])
rusell['Date'] = rusell['Date'].dt.strftime('%Y-%m')
rusell['Close'] = round(rusell['Close'], 2)
rusell_columns = rusell[['Date', 'Close']]
# print(rusell_columns)

# formatting SP500 csv: date format and column split
sp500 = pd.read_csv('SP500.csv')
sp500['Date'] = pd.to_datetime(sp500['Date'])
sp500['Date'] = sp500['Date'].dt.strftime('%Y-%m')
print(sp500)