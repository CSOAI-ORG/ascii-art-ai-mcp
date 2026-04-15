# ASCII Art AI MCP Server

> By [MEOK AI Labs](https://meok.ai) — ASCII art generation, box drawing, tables, and progress bars

## Installation

```bash
pip install ascii-art-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install ascii-art-ai-mcp
```

## Tools

### `text_to_ascii`
Convert text to ASCII art using built-in block font (A-Z, 0-9, space, punctuation).

**Parameters:**
- `text` (str): Text to convert (max 30 chars)
- `font` (str): Font style (default 'block')

### `generate_box`
Generate a box around text with various border styles.

**Parameters:**
- `text` (str): Text content (supports multi-line)
- `style` (str): Border style — 'single', 'double', 'rounded', 'heavy', 'ascii'
- `padding` (int): Internal padding (default 1)
- `width` (int): Fixed width (0 = auto-fit)

### `table_formatter`
Format data as an ASCII table (grid, simple, or markdown pipe style).

**Parameters:**
- `headers` (list[str]): Column header strings
- `rows` (list[list[str]]): List of row data
- `style` (str): Table style — 'grid', 'simple', 'pipe'

### `progress_bar_generator`
Generate an ASCII progress bar in block, arrow, dots, or hash style.

**Parameters:**
- `progress` (float): Progress value 0.0-1.0 (or 0-100)
- `width` (int): Bar width in characters (default 30)
- `style` (str): Bar style — 'block', 'arrow', 'dots', 'hash'

## Authentication

Free tier: 50 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
