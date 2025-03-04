import sqlite3
import sys

def query_by_industry(industry=None):
    """
    Query stocks by industry from the strong_stocks_20250303 table.
    
    Args:
        industry: Industry to filter by (optional)
    """
    conn = sqlite3.connect('strong_stocks.db')
    cursor = conn.cursor()
    
    if industry:
        # Query stocks for a specific industry
        query = """
        SELECT stock_code, stock_name, price_change, latest_price, industry
        FROM strong_stocks_20250303
        WHERE industry = ?
        ORDER BY price_change DESC
        """
        cursor.execute(query, (industry,))
    else:
        # List all industries with counts
        query = """
        SELECT industry, COUNT(*) as count, AVG(price_change) as avg_change
        FROM strong_stocks_20250303
        GROUP BY industry
        ORDER BY count DESC
        """
        cursor.execute(query)
    
    results = cursor.fetchall()
    
    if industry:
        # Print stocks for the specified industry
        print(f"Stocks in industry: {industry}")
        print("-" * 70)
        print(f"{'Code':<10} {'Name':<15} {'Price Change':<15} {'Latest Price':<15}")
        print("-" * 70)
        for row in results:
            print(f"{row[0]:<10} {row[1]:<15} {row[2]:<15.2f} {row[3]:<15.2f}")
        print(f"\n{len(results)} stocks found in {industry} industry")
    else:
        # Print all industries with counts
        print("Industry | Stock Count | Average Price Change")
        print("-" * 50)
        for row in results:
            print(f"{row[0]:<20} | {row[1]:<11} | {row[2]:<20.2f}")
        print(f"\n{len(results)} industries found")
    
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Get industry from command line argument
        industry = sys.argv[1]
        query_by_industry(industry)
    else:
        # If no industry provided, list all industries
        query_by_industry() 