#!/usr/bin/env python
"""
Script to fetch strong stock pool data and store it in a SQLite database.
"""

import json
import sys
import sqlite3
from datetime import datetime
import os

from fetch_strong_stock_pool import fetch_strong_stock_pool


def create_strong_stocks_table(conn):
    """
    Create the strong_stocks table if it doesn't exist.
    
    Args:
        conn: SQLite connection object
    """
    cursor = conn.cursor()
    
    # Create table with all columns from the DataFrame
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS strong_stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fetch_date TEXT NOT NULL,
        stock_number INTEGER,
        code TEXT,
        name TEXT,
        change_percent REAL,
        price REAL,
        limit_price REAL,
        turnover REAL,
        circulating_market_value REAL,
        total_market_value REAL,
        turnover_rate REAL,
        rise_speed REAL,
        is_new_high TEXT,
        volume_ratio REAL,
        limit_statistics TEXT,
        selection_reason TEXT,
        industry TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create index on code and fetch_date for faster queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_code ON strong_stocks (code)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_fetch_date ON strong_stocks (fetch_date)')
    
    conn.commit()


def store_strong_stocks(conn, df, fetch_date=None):
    """
    Store strong stocks data in the SQLite database.
    
    Args:
        conn: SQLite connection object
        df: DataFrame with strong stocks data
        fetch_date: Date for which data was fetched (YYYYMMDD format)
    
    Returns:
        Number of records inserted
    """
    if df.empty:
        print("No data to store")
        return 0
    
    if fetch_date is None:
        fetch_date = datetime.now().strftime('%Y%m%d')
    
    cursor = conn.cursor()
    
    # First, delete any existing records for this date to avoid duplicates
    cursor.execute('DELETE FROM strong_stocks WHERE fetch_date = ?', (fetch_date,))
    
    # Prepare data for insertion
    records = []
    for _, row in df.iterrows():
        record = (
            fetch_date,
            row.get('序号'),
            row.get('代码'),
            row.get('名称'),
            row.get('涨跌幅'),
            row.get('最新价'),
            row.get('涨停价'),
            row.get('成交额'),
            row.get('流通市值'),
            row.get('总市值'),
            row.get('换手率'),
            row.get('涨速'),
            row.get('是否新高'),
            row.get('量比'),
            row.get('涨停统计'),
            row.get('入选理由'),
            row.get('所属行业')
        )
        records.append(record)
    
    # Insert records
    cursor.executemany('''
    INSERT INTO strong_stocks (
        fetch_date, stock_number, code, name, change_percent, price, limit_price,
        turnover, circulating_market_value, total_market_value, turnover_rate,
        rise_speed, is_new_high, volume_ratio, limit_statistics, selection_reason, industry
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', records)
    
    conn.commit()
    return len(records)


def get_db_connection(db_path='strong_stocks.db'):
    """
    Get a connection to the SQLite database.
    
    Args:
        db_path: Path to the SQLite database file
    
    Returns:
        SQLite connection object
    """
    conn = sqlite3.connect(db_path)
    return conn


def main():
    """
    Main function to fetch strong stock pool data and store it in the database.
    """
    # Get date from command line argument or use today's date
    date = sys.argv[1] if len(sys.argv) > 1 else None
    
    print(f"Using date: {date if date else 'today'}")
    
    # Fetch data
    df = fetch_strong_stock_pool(date)
    
    if df.empty:
        print("No data available to store")
        return
    
    # Connect to database
    conn = get_db_connection()
    
    # Create table if it doesn't exist
    create_strong_stocks_table(conn)
    
    # Store data
    records_inserted = store_strong_stocks(conn, df, date)
    
    print(f"Stored {records_inserted} records in the database")
    
    # Print summary
    print(f"\nTotal strong stocks: {len(df)}")
    
    # Close connection
    conn.close()


if __name__ == "__main__":
    main() 