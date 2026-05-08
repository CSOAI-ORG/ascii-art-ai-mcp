<div align="center">

# Ascii Art Ai MCP

**ASCII Art AI MCP Server**

[![PyPI](https://img.shields.io/pypi/v/meok-ascii-art-ai-mcp)](https://pypi.org/project/meok-ascii-art-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

ASCII Art AI MCP Server
ASCII art generation and formatting tools powered by MEOK AI Labs.

## Tools

| Tool | Description |
|------|-------------|
| `text_to_ascii` | Convert text to ASCII art using built-in block font. |
| `generate_box` | Generate a box around text with various border styles. |
| `table_formatter` | Format data as an ASCII table. |
| `progress_bar_generator` | Generate an ASCII progress bar. |

## Installation

```bash
pip install meok-ascii-art-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ascii-art-ai": {
      "command": "python",
      "args": ["-m", "meok_ascii_art_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
