#!/usr/bin/env python
"""
Entry point for the AKShare FastMCP server in SSE mode.
"""

import asyncio
import logging
import sys

from src.mcp_server_akshare import main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print("Starting AKShare FastMCP server in SSE mode...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error running server: {e}", exc_info=True)
        sys.exit(1)
