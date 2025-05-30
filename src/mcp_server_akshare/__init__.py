"""
MCP server for AKShare financial data using FastMCP.
"""

import logging
from typing import Optional

from .server import mcp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Main entry point for the AKShare MCP server.
    """
    logger.info("Starting AKShare FastMCP server in SSE mode...")
    try:
        # 直接使用fastmcp对象的run方法，不使用异步
        # FastMCP.run不接受server_name和server_version参数
        mcp.run(
            transport="sse",
            host="0.0.0.0",
            port=18000
        )
    except Exception as e:
        logger.error(f"Error running AKShare MCP server: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
