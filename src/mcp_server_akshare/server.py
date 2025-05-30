"""
MCP server implementation for AKShare using FastMCP.
"""

import json
import logging
from enum import Enum
from typing import Optional

from fastmcp import FastMCP

from .api import (
    fetch_bond_zh_hs_cov_spot,
    fetch_forex_spot_quote,
    fetch_fund_etf_category_sina,
    fetch_fund_etf_hist_sina,
    fetch_futures_zh_spot,
    fetch_macro_china_cpi,
    fetch_macro_china_gdp,
    fetch_stock_zh_a_hist,
    fetch_stock_zh_a_spot,
    fetch_stock_zh_index_daily,
    fetch_stock_zh_index_spot,
    fetch_stock_zt_pool_strong_em,
)

# Configure logging
logger = logging.getLogger(__name__)


class AKShareTools(str, Enum):
    """
    Enum for AKShare tools.
    """
    STOCK_ZH_A_SPOT = "stock_zh_a_spot"
    STOCK_ZH_A_HIST = "stock_zh_a_hist"
    STOCK_ZH_INDEX_SPOT = "stock_zh_index_spot"
    STOCK_ZH_INDEX_DAILY = "stock_zh_index_daily"
    FUND_ETF_CATEGORY_SINA = "fund_etf_category_sina"
    FUND_ETF_HIST_SINA = "fund_etf_hist_sina"
    MACRO_CHINA_GDP = "macro_china_gdp"
    MACRO_CHINA_CPI = "macro_china_cpi"
    FOREX_SPOT_QUOTE = "forex_spot_quote"
    FUTURES_ZH_SPOT = "futures_zh_spot"
    BOND_ZH_HS_COV_SPOT = "bond_zh_hs_cov_spot"
    STOCK_ZT_POOL_STRONG_EM = "stock_zt_pool_strong_em"


# Create FastMCP server
mcp = FastMCP(
    "akshare",
    version="0.1.0",
    description="AKShare金融数据服务API"
)


@mcp.tool(name=AKShareTools.STOCK_ZH_A_SPOT.value)
async def stock_zh_a_spot() -> str:
    """获取中国A股市场股票实时数据"""
    result = await fetch_stock_zh_a_spot()
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name=AKShareTools.STOCK_ZH_A_HIST.value)
async def stock_zh_a_hist(
    symbol: str,
    period: str = "daily",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    adjust: str = ""
) -> str:
    """获取中国A股市场股票历史数据

    Args:
        symbol: 股票代码
        period: 数据频率：daily（日）、weekly（周）、monthly（月）
        start_date: 开始日期，格式为YYYYMMDD
        end_date: 结束日期，格式为YYYYMMDD
        adjust: 价格调整方式：''（不调整）、qfq（前复权）、hfq（后复权）
    """
    result = await fetch_stock_zh_a_hist(
        symbol=symbol,
        period=period,
        start_date=start_date,
        end_date=end_date,
        adjust=adjust,
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name=AKShareTools.STOCK_ZH_INDEX_SPOT.value)
async def stock_zh_index_spot() -> str:
    """获取中国股票市场指数实时数据"""
    result = await fetch_stock_zh_index_spot()
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name=AKShareTools.STOCK_ZH_INDEX_DAILY.value)
async def stock_zh_index_daily(symbol: str) -> str:
    """获取中国股票市场指数每日数据

    Args:
        symbol: 指数代码
    """
    result = await fetch_stock_zh_index_daily(symbol=symbol)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name=AKShareTools.FUND_ETF_CATEGORY_SINA.value)
async def fund_etf_category_sina(category: str = "ETF基金") -> str:
    """从新浪获取ETF基金数据

    Args:
        category: 基金类别
    """
    result = await fetch_fund_etf_category_sina(category=category)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name=AKShareTools.FUND_ETF_HIST_SINA.value)
async def fund_etf_hist_sina(symbol: str) -> str:
    """从新浪获取ETF基金历史数据

    Args:
        symbol: ETF基金代码
    """
    result = await fetch_fund_etf_hist_sina(symbol=symbol)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name=AKShareTools.MACRO_CHINA_GDP.value)
async def macro_china_gdp() -> str:
    """获取中国GDP数据"""
    result = await fetch_macro_china_gdp()
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name=AKShareTools.MACRO_CHINA_CPI.value)
async def macro_china_cpi() -> str:
    """获取中国CPI数据"""
    result = await fetch_macro_china_cpi()
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name=AKShareTools.FOREX_SPOT_QUOTE.value)
async def forex_spot_quote() -> str:
    """获取外汇实时行情数据"""
    result = await fetch_forex_spot_quote()
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name=AKShareTools.FUTURES_ZH_SPOT.value)
async def futures_zh_spot() -> str:
    """获取中国期货市场实时数据"""
    result = await fetch_futures_zh_spot()
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name=AKShareTools.BOND_ZH_HS_COV_SPOT.value)
async def bond_zh_hs_cov_spot() -> str:
    """获取中国可转债实时数据"""
    result = await fetch_bond_zh_hs_cov_spot()
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(name=AKShareTools.STOCK_ZT_POOL_STRONG_EM.value)
async def stock_zt_pool_strong_em(date: Optional[str] = None) -> str:
    """从东方财富获取今日强势股票池数据

    Args:
        date: 日期，格式为YYYYMMDD
    """
    result = await fetch_stock_zt_pool_strong_em(date=date)
    return json.dumps(result, ensure_ascii=False, indent=2)
