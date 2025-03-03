# AKShare MCP Server

A Model Context Protocol (MCP) server that provides financial data analysis capabilities using the AKShare library.

## Features

- Access to Chinese and global financial market data through AKShare
- Integration with Claude Desktop via MCP protocol
- Support for various financial data queries and analysis

## Installation

### Using uv (recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/akshare_mcp_server.git
cd akshare_mcp_server

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies with uv
uv pip install -e .
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/akshare_mcp_server.git
cd akshare_mcp_server

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Usage

### Running the server

```bash
# Activate the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the server
python run_server.py
```

### Integrating with Claude Desktop

1. Add the following configuration to your Claude Desktop configuration:

```json
"mcpServers": {
    "akshare-mcp": {
        "command": "uv",
        "args": [
            "--directory",
            "/path/to/akshare_mcp_server",
            "run",
            "akshare-mcp"
        ],
        "env": {
            "AKSHARE_API_KEY": "<your_api_key_if_needed>"
        }
    }
}
```

2. Restart Claude Desktop
3. Select the AKShare MCP server from the available tools

## Available Tools

The AKShare MCP server provides the following tools:

- Stock data queries
- Fund data queries
- Bond data queries
- Futures data queries
- Forex data queries
- Macroeconomic data queries
- And more...

## Development

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest
```

## Docker

You can also run the server using Docker:

```bash
# Build the Docker image
docker build -t akshare-mcp-server .

# Run the Docker container
docker run -p 8000:8000 akshare-mcp-server
```

## License

MIT 