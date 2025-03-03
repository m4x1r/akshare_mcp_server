"""
API functions for interacting with AKShare.
"""

import logging
import os
from typing import Any, Dict, List, Optional, Union

import akshare as ak
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Optional API key (if needed for certain endpoints)
API_KEY = os.getenv("AKSHARE_API_KEY")


def dataframe_to_dict(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert a pandas DataFrame to a list of dictionaries.
    """
    return df.to_dict(orient="records")


def dataframe_to_json(df: pd.DataFrame) -> str:
    """
    Convert a pandas DataFrame to a JSON string.
    """
    return df.to_json(orient="records", date_format="iso")


async def fetch_stock_zh_a_spot() -> List[Dict[str, Any]]:
    """
    Fetch A-share stock data.
    """
    try:
        df = ak.stock_zh_a_spot()
        return dataframe_to_dict(df)
    except Exception as e:
        logger.error(f"Error fetching A-share stock data: {e}")
        raise


async def fetch_stock_zh_a_hist(
    symbol: str, 
    period: str = "daily", 
    start_date: str = None, 
    end_date: str = None,
    adjust: str = ""
) -> List[Dict[str, Any]]:
    """
    Fetch A-share stock historical data.
    
    Args:
        symbol: Stock code
        period: Data frequency, options: daily, weekly, monthly
        start_date: Start date in format YYYYMMDD
        end_date: End date in format YYYYMMDD
        adjust: Price adjustment, options: "", qfq (forward), hfq (backward)
    """
    try:
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period=period,
            start_date=start_date,
            end_date=end_date,
            adjust=adjust
        )
        return dataframe_to_dict(df)
    except Exception as e:
        logger.error(f"Error fetching stock historical data for {symbol}: {e}")
        raise


async def fetch_stock_zh_index_spot() -> List[Dict[str, Any]]:
    """
    Fetch Chinese stock market index data.
    """
    try:
        df = ak.stock_zh_index_spot()
        return dataframe_to_dict(df)
    except Exception as e:
        logger.error(f"Error fetching stock index data: {e}")
        raise


async def fetch_stock_zh_index_daily(symbol: str) -> List[Dict[str, Any]]:
    """
    Fetch Chinese stock market index daily data.
    
    Args:
        symbol: Index code
    """
    try:
        df = ak.stock_zh_index_daily(symbol=symbol)
        return dataframe_to_dict(df)
    except Exception as e:
        logger.error(f"Error fetching stock index daily data for {symbol}: {e}")
        raise


async def fetch_fund_etf_category_sina(category: str = "ETF基金") -> List[Dict[str, Any]]:
    """
    Fetch ETF fund data from Sina.
    
    Args:
        category: Fund category
    """
    try:
        df = ak.fund_etf_category_sina(category=category)
        return dataframe_to_dict(df)
    except Exception as e:
        logger.error(f"Error fetching ETF fund data: {e}")
        raise


async def fetch_fund_etf_hist_sina(symbol: str) -> List[Dict[str, Any]]:
    """
    Fetch ETF fund historical data from Sina.
    
    Args:
        symbol: ETF fund code
    """
    try:
        df = ak.fund_etf_hist_sina(symbol=symbol)
        return dataframe_to_dict(df)
    except Exception as e:
        logger.error(f"Error fetching ETF fund historical data for {symbol}: {e}")
        raise


async def fetch_macro_china_gdp() -> List[Dict[str, Any]]:
    """
    Fetch China GDP data.
    """
    try:
        df = ak.macro_china_gdp()
        return dataframe_to_dict(df)
    except Exception as e:
        logger.error(f"Error fetching China GDP data: {e}")
        raise


async def fetch_macro_china_cpi() -> List[Dict[str, Any]]:
    """
    Fetch China CPI data.
    """
    try:
        df = ak.macro_china_cpi()
        return dataframe_to_dict(df)
    except Exception as e:
        logger.error(f"Error fetching China CPI data: {e}")
        raise


async def fetch_forex_spot_quote() -> List[Dict[str, Any]]:
    """
    Fetch forex spot quotes.
    """
    try:
        df = ak.forex_spot_quote()
        return dataframe_to_dict(df)
    except Exception as e:
        logger.error(f"Error fetching forex spot quotes: {e}")
        raise


async def fetch_futures_zh_spot() -> List[Dict[str, Any]]:
    """
    Fetch Chinese futures market spot data.
    """
    try:
        df = ak.futures_zh_spot()
        return dataframe_to_dict(df)
    except Exception as e:
        logger.error(f"Error fetching futures spot data: {e}")
        raise


async def fetch_bond_zh_hs_cov_spot() -> List[Dict[str, Any]]:
    """
    Fetch Chinese convertible bond data.
    """
    try:
        df = ak.bond_zh_hs_cov_spot()
        return dataframe_to_dict(df)
    except Exception as e:
        logger.error(f"Error fetching convertible bond data: {e}")
        raise 