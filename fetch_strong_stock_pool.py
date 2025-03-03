#!/usr/bin/env python
"""
Script to fetch strong stock pool data from East Money using AKShare.
"""

import json
import sys
from datetime import datetime

import akshare as ak
import pandas as pd


def fetch_strong_stock_pool(date=None):
    """
    Fetch strong stock pool data from East Money.
    
    Args:
        date: Date in format YYYYMMDD. If None, use today's date.
    
    Returns:
        DataFrame with strong stock pool data.
    """
    if date is None:
        date = datetime.now().strftime('%Y%m%d')
    
    print(f"Fetching strong stock pool data for date: {date}")
    
    try:
        print("Calling ak.stock_zt_pool_strong_em...")
        # Try with and without date parameter to see if that makes a difference
        if date:
            print(f"Calling with date parameter: {date}")
            df = ak.stock_zt_pool_strong_em(date=date)
        else:
            print("Calling without date parameter")
            df = ak.stock_zt_pool_strong_em()
            
        print(f"Result type: {type(df)}")
        print(f"Is DataFrame empty: {df.empty}")
        
        if not df.empty:
            print(f"DataFrame shape: {df.shape}")
            print(f"DataFrame columns: {df.columns.tolist()}")
            # Print first row for debugging
            print(f"First row: {df.iloc[0].to_dict() if len(df) > 0 else 'No rows'}")
        else:
            print(f"No data available for date: {date}")
            
            # Try without date parameter as a fallback
            if date:
                print("Trying again without date parameter as fallback...")
                df_fallback = ak.stock_zt_pool_strong_em()
                print(f"Fallback result type: {type(df_fallback)}")
                print(f"Fallback is DataFrame empty: {df_fallback.empty}")
                
                if not df_fallback.empty:
                    print(f"Fallback DataFrame shape: {df_fallback.shape}")
                    print(f"Fallback DataFrame columns: {df_fallback.columns.tolist()}")
                    df = df_fallback
                else:
                    print("Fallback also returned empty DataFrame")
        
        return df
    except Exception as e:
        print(f"Error fetching strong stock pool data: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


def main():
    """
    Main function to fetch and display strong stock pool data.
    """
    # Get date from command line argument or use today's date
    date = sys.argv[1] if len(sys.argv) > 1 else None
    
    print(f"Using date: {date if date else 'today'}")
    df = fetch_strong_stock_pool(date)
    
    if not df.empty:
        # Convert to JSON for pretty printing
        result = df.to_dict(orient="records")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # Print summary
        print(f"\nTotal strong stocks: {len(df)}")
        
        # Print industry distribution
        if '所属行业' in df.columns:
            industry_counts = df['所属行业'].value_counts()
            print("\nIndustry Distribution:")
            for industry, count in industry_counts.items():
                print(f"  {industry}: {count}")


if __name__ == "__main__":
    main() 