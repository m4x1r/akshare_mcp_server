import csv
import sqlite3
import os

# Database file path
db_path = 'strong_stocks.db'

# Create the database file if it doesn't exist
if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
    print(f"Creating new database file: {db_path}")

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS strong_stocks_20250303 (
    id INTEGER PRIMARY KEY,
    stock_code TEXT,
    stock_name TEXT,
    price_change REAL,
    latest_price REAL,
    limit_up_price REAL,
    transaction_amount REAL,
    circulating_market_value REAL,
    total_market_value REAL,
    turnover_rate REAL,
    rise_speed REAL,
    is_new_high TEXT,
    volume_ratio REAL,
    limit_up_stats TEXT,
    selection_reason TEXT,
    industry TEXT
)
''')
conn.commit()

# Open the CSV file
with open('data/strong_stocks_20250303.csv', 'r', encoding='utf-8') as file:
    # Skip the header row
    next(file)
    
    # Read the CSV file
    csv_reader = csv.reader(file)
    
    # Insert each row into the database
    for row in csv_reader:
        # Check if we have enough columns
        if len(row) >= 16:
            # Extract data from the row
            serial_number = row[0]
            stock_code = row[1]
            stock_name = row[2]
            price_change = float(row[3]) if row[3] else None
            latest_price = float(row[4]) if row[4] else None
            limit_up_price = float(row[5]) if row[5] else None
            transaction_amount = float(row[6]) if row[6] else None
            circulating_market_value = float(row[7]) if row[7] else None
            total_market_value = float(row[8]) if row[8] else None
            turnover_rate = float(row[9]) if row[9] else None
            rise_speed = float(row[10]) if row[10] else None
            is_new_high = row[11]
            volume_ratio = float(row[12]) if row[12] else None
            limit_up_stats = row[13]
            selection_reason = row[14]
            industry = row[15]
            
            # Insert data into the table
            cursor.execute('''
                INSERT INTO strong_stocks_20250303 (
                    id, stock_code, stock_name, price_change, latest_price, 
                    limit_up_price, transaction_amount, circulating_market_value, 
                    total_market_value, turnover_rate, rise_speed, is_new_high, 
                    volume_ratio, limit_up_stats, selection_reason, industry
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                serial_number, stock_code, stock_name, price_change, latest_price, 
                limit_up_price, transaction_amount, circulating_market_value, 
                total_market_value, turnover_rate, rise_speed, is_new_high, 
                volume_ratio, limit_up_stats, selection_reason, industry
            ))

# Commit the changes and close the connection
conn.commit()
print(f"Data imported successfully into strong_stocks_20250303 table")
conn.close() 