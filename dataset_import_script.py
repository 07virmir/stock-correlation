import os
import sqlite3
import pandas as pd

# Define the paths to the "stocks" folder and the SQLite database file
stocks_folder_path = "dataset/stocks"
sqlite_db_path = "data_viz_db.sqlite"

# Connect to the SQLite database
conn = sqlite3.connect(sqlite_db_path)
cursor = conn.cursor()

# Create the combined_data table if it doesn't exist with the specified data types
create_combined_table_query = """
CREATE TABLE IF NOT EXISTS stock_data (
    Date DATE,
    Open REAL,
    High REAL,
    Low REAL,
    Close REAL,
    Adj_Close REAL,
    Volume INTEGER,
    Ticker TEXT
);
"""
cursor.execute(create_combined_table_query)

# List all CSV files in the "stocks" folder
csv_files = [f for f in os.listdir(stocks_folder_path) if f.endswith('.csv')]

# Iterate through the price data CSV files and add data to the combined_data table
for csv_file in csv_files:
    table_name = os.path.splitext(csv_file)[0]
    csv_file_path = os.path.join(stocks_folder_path, csv_file)
    
    # Read the CSV file
    price_data_df = pd.read_csv(csv_file_path)
    
    # Add a "ticker" column with the corresponding stock symbol
    stock_symbol = table_name  # Assuming the table name corresponds to the stock symbol
    price_data_df['Ticker'] = stock_symbol
    
    # Insert the data into the combined_data table
    price_data_df.to_sql('temp_table', conn, if_exists='replace', index=False)
    insert_data_query = f"""
    INSERT INTO stock_data
    SELECT * FROM temp_table;
    """
    cursor.execute(insert_data_query)

    # Drop the temporary table
    drop_temp_table_query = "DROP TABLE temp_table;"
    cursor.execute(drop_temp_table_query)

# Commit the changes and close the SQLite connection
conn.commit()
conn.close()

