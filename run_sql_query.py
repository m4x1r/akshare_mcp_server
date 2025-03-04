import sqlite3
import sys

def run_query(query):
    """
    Run a SQL query against the strong_stocks.db database.
    
    Args:
        query: SQL query to execute
        
    Returns:
        Query results
    """
    conn = sqlite3.connect('strong_stocks.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        
        # Check if it's a SELECT query
        if query.strip().upper().startswith('SELECT'):
            # Fetch all results
            results = cursor.fetchall()
            
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            # Print column headers
            print(' | '.join(column_names))
            print('-' * (sum(len(name) + 3 for name in column_names)))
            
            # Print rows
            for row in results:
                # Convert row to dictionary
                row_dict = dict(row)
                # Print values
                print(' | '.join(str(row_dict[col]) for col in column_names))
                
            print(f"\n{len(results)} rows returned")
        else:
            # For non-SELECT queries, commit changes and print affected rows
            conn.commit()
            print(f"{cursor.rowcount} rows affected")
    
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Get query from command line argument
        query = sys.argv[1]
        run_query(query)
    else:
        # If no query provided, run a sample query
        sample_query = """
        SELECT COUNT(*) as total_stocks, 
               SUM(CASE WHEN price_change > 0 THEN 1 ELSE 0 END) as positive_change,
               SUM(CASE WHEN price_change < 0 THEN 1 ELSE 0 END) as negative_change,
               AVG(price_change) as avg_change,
               MAX(price_change) as max_change,
               MIN(price_change) as min_change
        FROM strong_stocks_20250303;
        """
        print("Running sample query:")
        print(sample_query)
        run_query(sample_query) 