import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('strong_stocks.db')
cursor = conn.cursor()

# Query to get the distribution of price changes
query = """
SELECT 
  CASE 
    WHEN price_change >= 20 THEN '20% and above'
    WHEN price_change >= 10 AND price_change < 20 THEN '10% to 20%'
    WHEN price_change >= 5 AND price_change < 10 THEN '5% to 10%'
    WHEN price_change >= 0 AND price_change < 5 THEN '0% to 5%'
    WHEN price_change >= -5 AND price_change < 0 THEN '-5% to 0%'
    WHEN price_change >= -10 AND price_change < -5 THEN '-10% to -5%'
    ELSE 'Below -10%'
  END as price_change_range,
  COUNT(*) as count,
  AVG(price_change) as avg_change
FROM strong_stocks_20250303
GROUP BY price_change_range
ORDER BY 
  CASE 
    WHEN price_change_range = '20% and above' THEN 1
    WHEN price_change_range = '10% to 20%' THEN 2
    WHEN price_change_range = '5% to 10%' THEN 3
    WHEN price_change_range = '0% to 5%' THEN 4
    WHEN price_change_range = '-5% to 0%' THEN 5
    WHEN price_change_range = '-10% to -5%' THEN 6
    ELSE 7
  END;
"""

cursor.execute(query)
results = cursor.fetchall()

# Print the results
print("Price Change Range | Count | Average Change")
print("-" * 50)
for row in results:
    print(f"{row[0]:<20} | {row[1]:<5} | {row[2]:<15.2f}")

# Close the connection
conn.close()

# Print summary
print("\nSummary of price change distribution in strong_stocks_20250303 table") 