#!/usr/bin/env python
"""
Custom MCP function for fetching strong stock data from East Money.
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

import akshare as ak
import pandas as pd


def fetch_strong_stock_data(date: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fetch strong stock pool data from East Money.
    
    Args:
        date: Date in format YYYYMMDD. If None, use today's date.
        Note: The AKShare API only provides data for the current trading day.
              Historical data is not available through this API.
    
    Returns:
        List of dictionaries with strong stock pool data.
    """
    if date is None:
        date = datetime.now().strftime('%Y%m%d')
    
    warning_message = "\n" + "="*80 + "\n"
    warning_message += "STRONG STOCK DATA RETRIEVAL\n"
    warning_message += "="*80 + "\n"
    warning_message += f"Requested date: {date}\n"
    warning_message += "IMPORTANT: The AKShare API only provides data for the current trading day.\n"
    warning_message += "           Historical data is not available through this API.\n"
    warning_message += "           If you specified a past date, you will likely get current day data instead.\n"
    warning_message += "="*80 + "\n"
    
    print(warning_message)
    
    try:
        # Try with the specified date
        df = ak.stock_zt_pool_strong_em(date=date)
        print(f"Result type: {type(df)}")
        print(f"Is DataFrame empty: {df.empty}")
        
        # If the DataFrame is empty, try without a date parameter
        if df.empty and date:
            print("Specified date returned no data. Trying current trading day data...")
            df = ak.stock_zt_pool_strong_em()
            print(f"Current day result type: {type(df)}")
            print(f"Current day is DataFrame empty: {df.empty}")
        
        # If we still have an empty DataFrame, try running the script directly
        if df.empty:
            print("Both attempts returned empty DataFrames. Trying direct script execution...")
            import subprocess
            
            # For direct script execution, we'll focus on getting current day data
            cmd = ["python", "fetch_strong_stock_pool.py"]
            print(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            print(f"Script execution exit code: {result.returncode}")
            
            if result.returncode == 0 and result.stdout:
                # Try to parse the JSON output from the script
                try:
                    # Find the JSON part in the output
                    json_start = result.stdout.find('[{')
                    if json_start == -1:
                        json_start = result.stdout.find('[\n  {')
                    
                    json_end = result.stdout.rfind('}]') + 2
                    
                    if json_start >= 0 and json_end > json_start:
                        json_str = result.stdout[json_start:json_end]
                        print(f"Found JSON data from position {json_start} to {json_end}")
                        print(f"JSON string length: {len(json_str)}")
                        print(f"First 100 chars: {json_str[:100]}")
                        print(f"Last 100 chars: {json_str[-100:] if len(json_str) > 100 else json_str}")
                        
                        data = json.loads(json_str)
                        print(f"Successfully parsed JSON data with {len(data)} records")
                        return data, warning_message
                    else:
                        # Try to find any JSON array in the output
                        import re
                        json_matches = re.findall(r'\[\s*\{.*?\}\s*\]', result.stdout, re.DOTALL)
                        if json_matches:
                            longest_match = max(json_matches, key=len)
                            print(f"Found JSON data using regex, length: {len(longest_match)}")
                            try:
                                data = json.loads(longest_match)
                                print(f"Successfully parsed JSON data with {len(data)} records")
                                return data, warning_message
                            except json.JSONDecodeError:
                                print("Failed to parse JSON from regex match")
                        
                        print(f"Could not find JSON data in script output. Start: {json_start}, End: {json_end}")
                        print(f"Output length: {len(result.stdout)}")
                        print(f"First 200 chars: {result.stdout[:200]}")
                        print(f"Last 200 chars: {result.stdout[-200:] if len(result.stdout) > 200 else result.stdout}")
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON from script output: {e}")
                    if 'json_str' in locals():
                        print(f"JSON string: {json_str[:100]}...{json_str[-100:] if len(json_str) > 100 else ''}")
            else:
                print(f"Script execution failed or returned no output")
                print(f"STDOUT: {result.stdout[:500]}...")
                print(f"STDERR: {result.stderr}")
        
        # If we have data in the DataFrame, convert it to a list of dictionaries
        if not df.empty:
            print(f"DataFrame shape: {df.shape}")
            print(f"DataFrame columns: {df.columns.tolist()}")
            return df.to_dict(orient="records"), warning_message
        
        # If all attempts failed, return an empty list
        return [], warning_message
    except Exception as e:
        print(f"Error fetching strong stock pool data: {e}")
        import traceback
        traceback.print_exc()
        return [], warning_message


def main():
    """
    Main function to fetch and display strong stock pool data.
    """
    # Get date from command line argument or use today's date
    date = sys.argv[1] if len(sys.argv) > 1 else None
    
    result, warning_message = fetch_strong_stock_data(date)
    
    if result:
        # Print the result as JSON
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # Print summary
        print(f"\nTotal strong stocks: {len(result)}")
        
        # Print industry distribution
        industries = {}
        for item in result:
            industry = item.get('所属行业')
            if industry:
                industries[industry] = industries.get(industry, 0) + 1
        
        if industries:
            print("\nIndustry Distribution:")
            for industry, count in sorted(industries.items(), key=lambda x: x[1], reverse=True):
                print(f"  {industry}: {count}")
        
        # Print the warning message again at the end to ensure it's visible
        print("\n" + warning_message)
    else:
        print("\n" + "="*80)
        print("NO STRONG STOCK DATA FOUND")
        print("="*80)
        print("The AKShare API only provides data for the current trading day.")
        print("If you're trying to get historical data, it's not available through this API.")
        print("Try running without a date parameter to get current day data.")
        print("="*80)


if __name__ == "__main__":
    main() 