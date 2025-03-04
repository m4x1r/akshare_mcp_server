import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('strong_stocks.db')
cursor = conn.cursor()

# Query to count the total number of records
cursor.execute('SELECT COUNT(*) FROM strong_stocks_20250303')
count = cursor.fetchone()[0]
print(f"Total records in strong_stocks_20250303: {count}")

# Query to get the top 10 stocks by price change
print("\nTop 10 stocks by price change:")
cursor.execute('''
    SELECT id, stock_code, stock_name, price_change, latest_price, industry 
    FROM strong_stocks_20250303 
    ORDER BY price_change DESC 
    LIMIT 10
''')
top_stocks = cursor.fetchall()

# Print the results in a formatted way
print(f"{'ID':<5} {'Code':<10} {'Name':<15} {'Price Change':<15} {'Latest Price':<15} {'Industry':<15}")
print("-" * 75)
for stock in top_stocks:
    print(f"{stock[0]:<5} {stock[1]:<10} {stock[2]:<15} {stock[3]:<15.2f} {stock[4]:<15.2f} {stock[5]:<15}")

# Query to get statistics by industry
print("\nStatistics by industry:")
cursor.execute('''
    SELECT industry, COUNT(*) as count, AVG(price_change) as avg_change
    FROM strong_stocks_20250303
    GROUP BY industry
    ORDER BY count DESC
    LIMIT 10
''')
industry_stats = cursor.fetchall()

# Print the results in a formatted way
print(f"{'Industry':<20} {'Count':<10} {'Avg Price Change':<20}")
print("-" * 50)
for stat in industry_stats:
    print(f"{stat[0]:<20} {stat[1]:<10} {stat[2]:<20.2f}")

# Close the connection
conn.close() 