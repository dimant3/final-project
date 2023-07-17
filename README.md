# STOCK MARKET INDEXES (Nasdaq OMX baltic, Russell 2000 and S&P 500) ANALYSIS
## Details
**Created by: [Mantas Dilius](https://github.com/dimant3) and [Deividas Chochlovas](https://github.com/DeiCho)**

This is the end project in Vilnius Coding School 

Project theme: Stock market indexes data analysis

The main goal of the project is to find out in which of the 3 analyzed indexes our 10'000€ portfolio would perform best during 3 years period (2020.01-2022.12 or 36 months)

In this project we used to work with Python language, CSV files and Database (Postgres)

## Applied knowledge:

Used libraries: Pandas, NumPy, MatplotLib, SeaBorn, sklearn.linear_model

### postgres.py
Used database adapter: psycopg2

Steps:

1. Creating of postgres connection settings (def db_con():)
2. Writing function to create table into vcs_final_project database (def create_table():)
3. Creating connection to database for data analysis (def work_with_database():)

### web_scrap.py
Used imports: psycopg2, BeautifulSoup, requests, time, postgres.py

Steps:

1. Finding necessary S&P 500 index data from URL (https://finance.yahoo.com/quote/SPY/history)
2. Getting needed data from url as table using Beautiful soup and indicate analysis method (html.parser)
3. Using "if" and "for" received data inserted into table in Postgres

### final_project.py

This is the main project file where all calculations were made.

Steps:
1. Unified all INDEXES data by formating Dates and selected 'Close' price columns

2. Calculations for each index: 

    - stocks bought at the starting point on 2020.01
    - Monthly and whole 3Y period ROI%
    - Deviations from average close price
    - Finding highest, lowest and difference between min and max portfolio values

3. Visualisation of calculations:

    All visuals are controlled by functions (def), which helps to separate all graphs in the code
    
    - For example, if you call def "show_portfolio_values():" you will receive this view:
        ![alt_text](https://github.com/dimant3/final-project/blob/dev/Screenshots/show_portfolio_value.png)

    - Total ROI by Index:
        ![alt_text](https://github.com/dimant3/final-project/blob/dev/Screenshots/show_index_total_roi.png)

        Graph shows: Nasdaq: 38.15%, Russell 2000: 9.12%, S&P500: 18.87%

    - Function to show each index deviation from standard:

        For example if you call def "show_russell2000_deviation():" you will receive this view:
        
        ![alt_text](https://github.com/dimant3/final-project/blob/dev/Screenshots/show_russell2000_deviation.png)
        
        other indexes:
        def show_nasdaq_deviation():
        def show_sp500_deviation():

4. Forecast:

   From 2022 all the indexes started downtrend movement based on 2 major events: russia - Ukraine war and central banks aggressive rate      hikes. In our forecast model we skipped downturn movement and wanted to show how indexes would likely to perform if global situation      were steady based on LinearRegression model and historical data.

   Forecast of indexes performance based on 69% training of historical data.

    To create and train the model we used: LinearRegression

    Example of forecasted S&P500 index result:
        ![alt_text](https://github.com/dimant3/final-project/blob/dev/Screenshots/sp500_forecast.png)
        
        other indexes:
        def nasdaq_forecast():
        def russell_forecast():

## Conclusion

In addition, at the highest points of value, Nasdaq would bring us almost 6.5kEUR profit (while others less than 5kEUR) and it remained highest until the end of the analysed period. Also, using Boolean in our calculations to find out how many times INDEXES were above their average 'Close' price, it showed us, that Nasdaq Index was 20 months above it's average 'Close' price out of 36 months, while Russell 2000: 18 and S&P500: 19 months. The lowest points of our each portfolio were: Nasdaq Baltic OMX 7708 €, Russell - 7144 € and S&P500 - 8011 €. 

To sum up, after we made all calculations and visualizations, we found out that "Nasdaq OMX baltics" would be best choice to put our 10'000€ as it's performance was best out of three during whole period.
