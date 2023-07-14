# STOCK MARKET INDEXES (Nasdaq OMX baltic, Russell 2000 and S&P 500) ANALYSIS
## Details
**Created by:[Mantas Dilius](https://github.com/dimant3) and [Deividas Chochlovas](https://github.com/DeiCho)**

This is the end project in Vilnius Coding School 

Project theme: Stock market indexes data analysis

The main goal of the project is to find out in which of the 3 analyzed indexes our 10'000€ portfolio would perform best from 2020.01
Analyzed date period was 3 years (2020.01-2022.12)

In this project we used to work with Python language, CSV files and Database (Postgres)

## Applied knowledge:

Used libraries: Pandas, NumPy, MatplotLib, SeaBorn, sklearn.linear_model

**[Title](postgres.py)**
Used database adapter: psycopg2
Steps:
1. Creating of postgres connection settings (def db_con():)
2. Writing function to create table into vcs_final_project database (def create_table():)
3. Creating connection to database for data analysis (def work_with_database():)

**[Title](web_scrap.py)**
Used imports: psycopg2, BeautifulSoup, requests, time, postgres.py
Steps:
1. Finding necessary S&P 500 index data from URL (https://finance.yahoo.com/quote/SPY/history?)
2. Getting needed data from url as table using Beautiful soup and indicate analysis method (html.parser)
3. Using "if" and "for" received data inserted into table in Postgres

**[Title](final_project.py)**

This is the main project file where all calculations were made.

Steps:
1. Unified all INDEXES data by formating dates and selected 'Close' price columns

2. Calculations for each index: 
    - stocks bought at the starting point on 2020.01
    - Monthly and whole 3Y period ROI%
    - Deviations from average close price
    - Finding highest, lowest and difference between min and max portfolio value

3. Visualisation of calculations:
    All visuals are controlled by functions, which helps to separate all graphs in the code
    
    If you call i.e. "def show_portfolio_values():" you will receive this view
        ![alt_text](https://github.com/dimant3/final-project/blob/dev/Screenshots/show_portfolio_value.png)

    Other functions:
    ROI for each index:
        ![alt_text](https://github.com/dimant3/final-project/blob/dev/Screenshots/show_index_total_roi.png) PAKEISTI

    function to show each index deviation from standard:
    If you call i.e. "def show_russell2000_deviation():" you will receive this view
        ![alt_text](https://github.com/dimant3/final-project/blob/dev/Screenshots/show_russell2000_deviation.png)
        
        other indexes:
        def show_nasdaq_deviation():
        def show_sp500_deviation():

4. Forecast:
    Forecast of indexes performance based on 69% training of historical data.

    To create and train the model we used: LinearRegression

    Example of forecasted S&P500 index result:
        ![alt_text](https://github.com/dimant3/final-project/blob/dev/Screenshots/sp500_forecast.png)
        
        other indexes:
        def nasdaq_forecast():
        def russell_forecast():

# Conlusion
