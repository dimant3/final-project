import psycopg2

# postgres connection settings
def db_con():
    db_settings = {
        'host': 'localhost',
        'port': 5432,
        'database': 'vcs_final_project',
        'user': 'postgres',
        'password': '123654'
    }
    return db_settings
# Function to create table into vcs_final_project database
def create_table():
    # ** these two asterixes transmits dictionary (db_settings) values into connection
    connection = psycopg2.connect(**db_con())

    create_table_query = """
    CREATE TABLE IF NOT EXISTS sp500 (
    id SERIAL PRIMARY KEY,
    Date DATE,
    Close numeric
    )
    """

    cursor = connection.cursor()
    # executing create_table_query to create table into database
    cursor.execute(create_table_query)

    connection.commit()
    # closing cursor and connection
    cursor.close()
    connection.close()


# connect to database for data analysis (no need to always request info from site)
def work_with_database():
    connection = psycopg2.connect(**db_con())
    cursor = connection.cursor()
    select_query = """
    SELECT Date, Close FROM sp500
    ORDER BY Date asc
    """
    cursor.execute(select_query)

    # fetches all the rows of a query result
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows



