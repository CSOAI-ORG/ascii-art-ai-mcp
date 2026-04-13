"""
ASCII Art AI MCP Server
ASCII art and text formatting tools powered by MEOK AI Labs.
"""

import time
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ascii-art-ai-mcp")

_call_counts: dict[str, list[float]] = defaultdict(list)
FREE_TIER_LIMIT = 50
WINDOW = 86400

def _check_rate_limit(tool_name: str) -> None:
    now = time.time()
    _call_counts[tool_name] = [t for t in _call_counts[tool_name] if now - t < WINDOW]
    if len(_call_counts[tool_name]) >= FREE_TIER_LIMIT:
        raise ValueError(f"Rate limit exceeded for {tool_name}. Free tier: {FREE_TIER_LIMIT}/day. Upgrade at https://meok.ai/pricing")
    _call_counts[tool_name].append(now)

BLOCK_FONT = {
    'A': ["  #  ", " # # ", "#####", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#### ", "#   #", "#### "],
    'C': [" ####", "#    ", "#    ", "#    ", " ####"],
    'D': ["#### ", "#   #", "#   #", "#   #", "#### "],
    'E': ["#####", "#    ", "#### ", "#    ", "#####"],
    'F': ["#####", "#    ", "#### ", "#    ", "#    "],
    'G': [" ####", "#    ", "# ###", "#   #", " ####"],
    'H': ["#   #", "#   #", "#####", "#   #", "#   #"],
    'I': ["#####", "  #  ", "  #  ", "  #  ", "#####"],
    'J': ["#####", "    #", "    #", "#   #", " ### "],
    'K': ["#   #", "#  # ", "###  ", "#  # ", "#   #"],
    'L': ["#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#### ", "#    ", "#    "],
    'Q': [" ### ", "#   #", "# # #", "#  ##", " ####"],
    'R': ["#### ", "#   #", "#### ", "#  # ", "#   #"],
    'S': [" ####", "#    ", " ### ", "    #", "#### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", " # # ", " # # ", "  #  "],
    'W': ["#   #", "#   #", "# # #", "## ##", "#   #"],
    'X': ["#   #", " # # ", "  #  ", " # # ", "#   #"],
    'Y': ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    'Z': ["#####", "   # ", "  #  ", " #   ", "#####"],
    '0': [" ### ", "#  ##", "# # #", "##  #", " ### "],
    '1': ["  #  ", " ##  ", "  #  ", "  #  ", " ### "],
    '2': [" ### ", "#   #", "  ## ", " #   ", "#####"],
    '3': ["#### ", "    #", " ### ", "    #", "#### "],
    '4': ["#   #", "#   #", "#####", "    #", "    #"],
    '5': ["#####", "#    ", "#### ", "    #", "#### "],
    '6': [" ### ", "#    ", "#### ", "#   #", " ### "],
    '7': ["#####", "    #", "   # ", "  #  ", "  #  "],
    '8': [" ### ", "#   #", " ### ", "#   #", " ### "],
    '9': [" ### ", "#   #", " ####", "    #", " ### "],
    ' ': ["     ", "     ", "     ", "     ", "     "],
    '!': ["  #  ", "  #  ", "  #  ", "     ", "  #  "],
}


@mcp.tool()
def text_to_ascii(text: str, char: str = "#") -> dict:
    """Convert text to large ASCII art block letters.

    Args:
        text: Text to convert (A-Z, 0-9, space, !)
        char: Character to use for blocks (default #)
    """
    _check_rate_limit("text_to_ascii")
    text = text.upper()[:30]
    rows = [""] * 5
    for c in text:
        glyph = BLOCK_FONT.get(c, ["?????"] * 5)
        for i in range(5):
            row = glyph[i].replace("#", char)
            rows[i] += row + " "
    art = "\n".join(rows)
    return {"art": art, "text": text, "width": len(rows[0]), "height": 5}


@mcp.tool()
def generate_box(text: str, style: str = "single", padding: int = 1) -> dict:
    """Generate a box around text content.

    Args:
        text: Text content (supports multi-line)
        style: Box style: 'single', 'double', 'rounded', 'heavy', 'ascii'
        padding: Inner padding (default 1)
    """
    _check_rate_limit("generate_box")
    styles = {
        "single":  {"tl": "\u250c", "tr": "\u2510", "bl": "\u2514", "br": "\u2518", "h": "\u2500", "v": "\u2502"},
        "double":  {"tl": "\u2554", "tr": "\u2557", "bl": "\u255a", "br": "\u255d", "h": "\u2550", "v": "\u2551"},
        "rounded": {"tl": "\u256d", "tr": "\u256e", "bl": "\u2570", "br": "\u256f", "h": "\u2500", "v": "\u2502"},
        "heavy":   {"tl": "\u250f", "tr": "\u2513", "bl": "\u2517", "br": "\u251b", "h": "\u2501", "v": "\u2503"},
        "ascii":   {"tl": "+", "tr": "+", "bl": "+", "br": "+", "h": "-", "v": "|"},
    }
    s = styles.get(style, styles["single"])
    lines = text.split('\n')
    max_w = max(len(l) for l in lines)
    inner_w = max_w + padding * 2
    result = [s["tl"] + s["h"] * inner_w + s["tr"]]
    for _ in range(padding):
        result.append(s["v"] + " " * inner_w + s["v"])
    for line in lines:
        padded = " " * padding + line.ljust(max_w) + " " * padding
        result.append(s["v"] + padded + s["v"])
    for _ in range(padding):
        result.append(s["v"] + " " * inner_w + s["v"])
    result.append(s["bl"] + s["h"] * inner_w + s["br"])
    return {"box": "\n".join(result), "style": style, "inner_width": inner_w}


@mcp.tool()
def table_formatter(headers: list[str], rows: list[list[str]], style: str = "grid") -> dict:
    """Format data as an ASCII table.

    Args:
        headers: Column header names
        rows: List of row data (each row is a list of strings)
        style: 'grid', 'simple', 'pipe' (markdown)
    """
    _check_rate_limit("table_formatter")
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    def fmt_row(cells, sep="|"):
        parts = [f" {str(c).ljust(col_widths[i])} " for i, c in enumerate(cells)]
        return sep + sep.join(parts) + sep
    if style == "pipe":
        lines = [fmt_row(headers)]
        lines.append("|" + "|".join(["-" * (w + 2) for w in col_widths]) + "|")
        for row in rows:
            lines.append(fmt_row(row))
    elif style == "simple":
        lines = [fmt_row(headers, " ")]
        lines.append(" " + " ".join(["-" * (w + 2) for w in col_widths]))
        for row in rows:
            lines.append(fmt_row(row, " "))
    else:
        border = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
        lines = [border, fmt_row(headers), border]
        for row in rows:
            lines.append(fmt_row(row))
        lines.append(border)
    return {"table": "\n".join(lines), "style": style, "columns": len(headers), "rows": len(rows)}


@mcp.tool()
def progress_bar_generator(
    current: int, total: int, width: int = 40, style: str = "block"
) -> dict:
    """Generate an ASCII progress bar.

    Args:
        current: Current value
        total: Total/maximum value
        width: Bar width in characters (default 40)
        style: 'block', 'arrow', 'dots', 'shade'
    """
    _check_rate_limit("progress_bar_generator")
    pct = min(current / max(total, 1), 1.0)
    filled = int(width * pct)
    empty = width - filled
    styles_map = {
        "block":  {"filled": "\u2588", "empty": "\u2591", "left": "[", "right": "]"},
        "arrow":  {"filled": "=", "empty": " ", "left": "[", "right": "]"},
        "dots":   {"filled": "\u25cf", "empty": "\u25cb", "left": "", "right": ""},
        "shade":  {"filled": "\u2593", "empty": "\u2591", "left": "\u2502", "right": "\u2502"},
    }
    s = styles_map.get(style, styles_map["block"])
    if style == "arrow" and filled > 0:
        bar = s["left"] + s["filled"] * (filled - 1) + ">" + s["empty"] * empty + s["right"]
    else:
        bar = s["left"] + s["filled"] * filled + s["empty"] * empty + s["right"]
    label = f" {pct*100:.1f}% ({current}/{total})"
    return {"bar": bar + label, "percentage": round(pct * 100, 1), "current": current,
            "total": total, "style": style}


if __name__ == "__main__":
    mcp.run()
