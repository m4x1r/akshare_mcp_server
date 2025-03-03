"""
MCP server implementation for AKShare.
"""

import asyncio
import json
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

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


# Create the server
server = Server("akshare")


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name=AKShareTools.STOCK_ZH_A_SPOT.value,
            description="Fetch A-share stock data from the Chinese market",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name=AKShareTools.STOCK_ZH_A_HIST.value,
            description="Fetch A-share stock historical data from the Chinese market",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock code"},
                    "period": {"type": "string", "description": "Data frequency: daily, weekly, monthly"},
                    "start_date": {"type": "string", "description": "Start date in format YYYYMMDD"},
                    "end_date": {"type": "string", "description": "End date in format YYYYMMDD"},
                    "adjust": {"type": "string", "description": "Price adjustment: '', qfq (forward), hfq (backward)"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AKShareTools.STOCK_ZH_INDEX_SPOT.value,
            description="Fetch Chinese stock market index data",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name=AKShareTools.STOCK_ZH_INDEX_DAILY.value,
            description="Fetch Chinese stock market index daily data",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Index code"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AKShareTools.FUND_ETF_CATEGORY_SINA.value,
            description="Fetch ETF fund data from Sina",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Fund category"},
                },
                "required": [],
            },
        ),
        types.Tool(
            name=AKShareTools.FUND_ETF_HIST_SINA.value,
            description="Fetch ETF fund historical data from Sina",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "ETF fund code"},
                },
                "required": ["symbol"],
            },
        ),
        types.Tool(
            name=AKShareTools.MACRO_CHINA_GDP.value,
            description="Fetch China GDP data",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name=AKShareTools.MACRO_CHINA_CPI.value,
            description="Fetch China CPI data",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name=AKShareTools.FOREX_SPOT_QUOTE.value,
            description="Fetch forex spot quotes",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name=AKShareTools.FUTURES_ZH_SPOT.value,
            description="Fetch Chinese futures market spot data",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name=AKShareTools.BOND_ZH_HS_COV_SPOT.value,
            description="Fetch Chinese convertible bond data",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    try:
        if arguments is None:
            arguments = {}
            
        result = None
        
        match name:
            case AKShareTools.STOCK_ZH_A_SPOT.value:
                result = await fetch_stock_zh_a_spot()
            case AKShareTools.STOCK_ZH_A_HIST.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")
                
                period = arguments.get("period", "daily")
                start_date = arguments.get("start_date")
                end_date = arguments.get("end_date")
                adjust = arguments.get("adjust", "")
                
                result = await fetch_stock_zh_a_hist(
                    symbol=symbol,
                    period=period,
                    start_date=start_date,
                    end_date=end_date,
                    adjust=adjust,
                )
            case AKShareTools.STOCK_ZH_INDEX_SPOT.value:
                result = await fetch_stock_zh_index_spot()
            case AKShareTools.STOCK_ZH_INDEX_DAILY.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")
                
                result = await fetch_stock_zh_index_daily(symbol=symbol)
            case AKShareTools.FUND_ETF_CATEGORY_SINA.value:
                category = arguments.get("category", "ETF基金")
                result = await fetch_fund_etf_category_sina(category=category)
            case AKShareTools.FUND_ETF_HIST_SINA.value:
                symbol = arguments.get("symbol")
                if not symbol:
                    raise ValueError("Missing required argument: symbol")
                
                result = await fetch_fund_etf_hist_sina(symbol=symbol)
            case AKShareTools.MACRO_CHINA_GDP.value:
                result = await fetch_macro_china_gdp()
            case AKShareTools.MACRO_CHINA_CPI.value:
                result = await fetch_macro_china_cpi()
            case AKShareTools.FOREX_SPOT_QUOTE.value:
                result = await fetch_forex_spot_quote()
            case AKShareTools.FUTURES_ZH_SPOT.value:
                result = await fetch_futures_zh_spot()
            case AKShareTools.BOND_ZH_HS_COV_SPOT.value:
                result = await fetch_bond_zh_hs_cov_spot()
            case _:
                raise ValueError(f"Unknown tool: {name}")
        
        # Convert result to JSON string with proper formatting
        result_json = json.dumps(result, ensure_ascii=False, indent=2)
        
        return [types.TextContent(text=result_json)]
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}", exc_info=True)
        error_message = f"Error executing tool {name}: {str(e)}"
        return [types.TextContent(text=error_message)]


async def main() -> None:
    """
    Main entry point for the server.
    """
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="akshare",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        ) 