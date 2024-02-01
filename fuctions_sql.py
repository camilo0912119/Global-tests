import sqlite3
import pandas as pd
def create_table_from_df(df, table_name, database_name='my_database.db'):
    """
    Creates a new table in SQLite from a DataFrame.

    Parameters:
    - df: Pandas DataFrame with the data.
    - table_name: Name of the table in SQLite.
    - database_name: Name of the SQLite database file.

    Returns:
    - None
    """
    conn = sqlite3.connect(database_name)
    df.to_sql(table_name, conn, index=False, if_exists='replace')
    conn.close()
def select_all(table_name, database_name='my_database.db'):
    conn = sqlite3.connect(database_name)
    query = f"SELECT * FROM {table_name}"
    result_df = pd.read_sql_query(query, conn)
    conn.close()
    return result_df
def update_table_from_df(df, table_name, database_name='my_database.db'):
    """
    Updates an existing table in SQLite from a DataFrame.

    Parameters:
    - df: Pandas DataFrame with the new data.
    - table_name: Name of the table in SQLite.
    - database_name: Name of the SQLite database file.

    Returns:
    - None
    """
    conn = sqlite3.connect(database_name)
    df.to_sql(table_name, conn, index=False, if_exists='replace')
    conn.close()

def delete_table(table_name, database_name='my_database.db'):
    """
    Deletes an existing table in SQLite.

    Parameters:
    - table_name: Name of the table in SQLite.
    - database_name: Name of the SQLite database file.

    Returns:
    - None
    """
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    conn.close()
