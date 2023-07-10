import pandas as pd

# formatting Nasdaq csv: date format and column split
nasdaq = pd.read_csv('Nasdaq OMX baltic.csv')
nasdaq['Date'] = pd.to_datetime(nasdaq['Date'])
nasdaq['Date'] = nasdaq['Date'].dt.strftime('%Y-%m')
print(nasdaq)

# 2x csv failai neirasomi i postgres (tik sutvarkomi duomenys), o web scrap supumpuojam i postgres


