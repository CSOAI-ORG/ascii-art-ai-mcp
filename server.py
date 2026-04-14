"""
ASCII Art AI MCP Server
ASCII art generation and formatting tools powered by MEOK AI Labs.
"""


import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import time
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ascii-art-ai-mcp")

_call_counts: dict[str, list[float]] = defaultdict(list)
FREE_TIER_LIMIT = 50
WINDOW = 86400

FONT_3X5 = {
    'A': [" # ", "# #", "###", "# #", "# #"], 'B': ["## ", "# #", "## ", "# #", "## "],
    'C': [" ##", "#  ", "#  ", "#  ", " ##"], 'D': ["## ", "# #", "# #", "# #", "## "],
    'E': ["###", "#  ", "## ", "#  ", "###"], 'F': ["###", "#  ", "## ", "#  ", "#  "],
    'G': [" ##", "#  ", "# #", "# #", " ##"], 'H': ["# #", "# #", "###", "# #", "# #"],
    'I': ["###", " # ", " # ", " # ", "###"], 'J': ["###", "  #", "  #", "# #", " # "],
    'K': ["# #", "## ", "#  ", "## ", "# #"], 'L': ["#  ", "#  ", "#  ", "#  ", "###"],
    'M': ["# #", "###", "###", "# #", "# #"], 'N': ["# #", "###", "###", "# #", "# #"],
    'O': [" # ", "# #", "# #", "# #", " # "], 'P': ["## ", "# #", "## ", "#  ", "#  "],
    'Q': [" # ", "# #", "# #", " # ", "  #"], 'R': ["## ", "# #", "## ", "# #", "# #"],
    'S': [" ##", "#  ", " # ", "  #", "## "], 'T': ["###", " # ", " # ", " # ", " # "],
    'U': ["# #", "# #", "# #", "# #", " # "], 'V': ["# #", "# #", "# #", " # ", " # "],
    'W': ["# #", "# #", "###", "###", "# #"], 'X': ["# #", "# #", " # ", "# #", "# #"],
    'Y': ["# #", "# #", " # ", " # ", " # "], 'Z': ["###", "  #", " # ", "#  ", "###"],
    '0': [" # ", "# #", "# #", "# #", " # "], '1': [" # ", "## ", " # ", " # ", "###"],
    '2': [" # ", "# #", "  #", " # ", "###"], '3': ["## ", "  #", " # ", "  #", "## "],
    '4': ["# #", "# #", "###", "  #", "  #"], '5': ["###", "#  ", "## ", "  #", "## "],
    '6': [" ##", "#  ", "## ", "# #", " # "], '7': ["###", "  #", " # ", " # ", " # "],
    '8': [" # ", "# #", " # ", "# #", " # "], '9': [" # ", "# #", " ##", "  #", "## "],
    ' ': ["   ", "   ", "   ", "   ", "   "], '!': [" # ", " # ", " # ", "   ", " # "],
    '.': ["   ", "   ", "   ", "   ", " # "], '-': ["   ", "   ", "###", "   ", "   "],
}


def _check_rate_limit(tool_name: str) -> None:
    now = time.time()
    _call_counts[tool_name] = [t for t in _call_counts[tool_name] if now - t < WINDOW]
    if len(_call_counts[tool_name]) >= FREE_TIER_LIMIT:
        raise ValueError(f"Rate limit exceeded for {tool_name}. Free tier: {FREE_TIER_LIMIT}/day. Upgrade at https://meok.ai/pricing")
    _call_counts[tool_name].append(now)


@mcp.tool()
def text_to_ascii(text: str, font: str = "block", api_key: str = "") -> dict:
    """Convert text to ASCII art using built-in block font.

    Args:
        text: Text to convert (A-Z, 0-9, space, basic punctuation)
        font: Font style - 'block' (default)
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("text_to_ascii")
    text = text.upper()[:30]
    lines = [""] * 5
    for ch in text:
        glyph = FONT_3X5.get(ch, ["???", "???", "???", "???", "???"])
        for i in range(5):
            lines[i] += glyph[i] + " "
    art = "\n".join(lines)
    return {"art": art, "text": text, "width": len(lines[0]) if lines[0] else 0, "height": 5}


@mcp.tool()
def generate_box(text: str, style: str = "single", padding: int = 1, width: int = 0, api_key: str = "") -> dict:
    """Generate a box around text with various border styles.

    Args:
        text: Text content (supports multi-line with newlines)
        style: Border style - 'single', 'double', 'rounded', 'heavy', 'ascii'
        padding: Internal padding (default 1)
        width: Fixed width (0 = auto-fit)
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("generate_box")
    styles = {
        "single":  {"tl": "\u250c", "tr": "\u2510", "bl": "\u2514", "br": "\u2518", "h": "\u2500", "v": "\u2502"},
        "double":  {"tl": "\u2554", "tr": "\u2557", "bl": "\u255a", "br": "\u255d", "h": "\u2550", "v": "\u2551"},
        "rounded": {"tl": "\u256d", "tr": "\u256e", "bl": "\u2570", "br": "\u256f", "h": "\u2500", "v": "\u2502"},
        "heavy":   {"tl": "\u250f", "tr": "\u2513", "bl": "\u2517", "br": "\u251b", "h": "\u2501", "v": "\u2503"},
        "ascii":   {"tl": "+", "tr": "+", "bl": "+", "br": "+", "h": "-", "v": "|"},
    }
    s = styles.get(style, styles["single"])
    text_lines = text.split('\n')
    max_len = max(len(l) for l in text_lines) if text_lines else 0
    inner_w = max(width - 2 - padding * 2, max_len) if width else max_len
    result = []
    result.append(s["tl"] + s["h"] * (inner_w + padding * 2) + s["tr"])
    for _ in range(padding):
        result.append(s["v"] + " " * (inner_w + padding * 2) + s["v"])
    for line in text_lines:
        padded = " " * padding + line.ljust(inner_w) + " " * padding
        result.append(s["v"] + padded + s["v"])
    for _ in range(padding):
        result.append(s["v"] + " " * (inner_w + padding * 2) + s["v"])
    result.append(s["bl"] + s["h"] * (inner_w + padding * 2) + s["br"])
    box = "\n".join(result)
    return {"box": box, "style": style, "width": len(result[0]), "height": len(result)}


@mcp.tool()
def table_formatter(headers: list[str], rows: list[list[str]], style: str = "grid", api_key: str = "") -> dict:
    """Format data as an ASCII table.

    Args:
        headers: List of column header strings
        rows: List of rows (each row is a list of cell strings)
        style: Table style - 'grid', 'simple', 'pipe' (markdown)
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("table_formatter")
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    result = []
    if style == "pipe":
        header = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
        sep = "| " + " | ".join("-" * col_widths[i] for i in range(len(headers))) + " |"
        result.append(header)
        result.append(sep)
        for row in rows:
            line = "| " + " | ".join(str(row[i] if i < len(row) else "").ljust(col_widths[i]) for i in range(len(headers))) + " |"
            result.append(line)
    elif style == "simple":
        header = "  ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        sep = "  ".join("-" * col_widths[i] for i in range(len(headers)))
        result.extend([header, sep])
        for row in rows:
            result.append("  ".join(str(row[i] if i < len(row) else "").ljust(col_widths[i]) for i in range(len(headers))))
    else:
        sep = "+-" + "-+-".join("-" * col_widths[i] for i in range(len(headers))) + "-+"
        header = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
        result.extend([sep, header, sep])
        for row in rows:
            line = "| " + " | ".join(str(row[i] if i < len(row) else "").ljust(col_widths[i]) for i in range(len(headers))) + " |"
            result.append(line)
        result.append(sep)
    table = "\n".join(result)
    return {"table": table, "style": style, "columns": len(headers), "rows": len(rows)}


@mcp.tool()
def progress_bar_generator(progress: float, width: int = 30, style: str = "block", api_key: str = "") -> dict:
    """Generate an ASCII progress bar.

    Args:
        progress: Progress value 0.0 to 1.0 (or 0-100)
        width: Bar width in characters (default 30)
        style: Bar style - 'block', 'arrow', 'dots', 'hash'
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    _check_rate_limit("progress_bar_generator")
    if progress > 1.0:
        progress = progress / 100.0
    progress = max(0.0, min(1.0, progress))
    filled = int(width * progress)
    pct = f"{progress * 100:.1f}%"
    chars = {"block": ("\u2588", "\u2591"), "arrow": ("=", " "), "dots": ("\u25cf", "\u25cb"), "hash": ("#", ".")}
    fill_ch, empty_ch = chars.get(style, chars["block"])
    if style == "arrow" and filled < width:
        bar = fill_ch * max(0, filled - 1) + ">" + empty_ch * (width - filled)
    else:
        bar = fill_ch * filled + empty_ch * (width - filled)
    result = f"[{bar}] {pct}"
    return {"bar": result, "progress": round(progress, 4), "percentage": pct, "style": style}


if __name__ == "__main__":
    mcp.run()
