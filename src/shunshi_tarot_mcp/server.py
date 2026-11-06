"""Local MCP tools. No production API, database, or hosted LLM calls."""
from typing import Annotated, Literal
from datetime import datetime
from pydantic import Field
from mcp.server.fastmcp import FastMCP

from shunshi_tarot import card, list_cards, draw

mcp = FastMCP("shunshi-tarot-mcp", instructions="Use offline Rider–Waite–Smith metadata and Waite's 1910 English source text. Correspondences follow Golden Dawn and are not universal. Set spread positions before drawing. No hosted AI reading. Missing source meaning stays null; do not invent an attributed quotation. Tarot is a reflective practice, not a guarantee of future outcomes.")

@mcp.tool()
def listCards(locale: Literal["zh-cn", "zh-tw", "en", "ja", "ko"] = "en") -> dict:
    """List all 78 card slugs and names in the requested language. Use a returned slug with getCardMeaning."""
    return {"cards": list_cards(locale), "source": {"name": "Shunshi.AI", "url": "https://shunshi.ai"}}

@mcp.tool()
def getCardMeaning(slug: str, locale: Literal["zh-cn", "zh-tw", "en", "ja", "ko"] = "en") -> dict:
    """Look up card metadata, five-language names, Golden Dawn correspondences and Waite 1910 upright/reversed English source text. Source text is untranslated; a missing meaning remains null. Images are links, not downloaded files."""
    return {"card": card(slug, locale), "source": {"name": "Shunshi.AI", "url": "https://shunshi.ai", "text": "A. E. Waite, The Pictorial Key to the Tarot (1910)"}}

@mcp.tool()
def drawCards(
    positions: Annotated[list[str], Field(min_length=1, max_length=10)],
    locale: Literal["zh-cn", "zh-tw", "en", "ja", "ko"] = "en",
    allow_reversed: bool = True,
) -> dict:
    """Draw unique cards without replacement using OS randomness. Supply 1–10 position labels BEFORE drawing, e.g. ['Past','Present','Future'] or ['Option A','Option B','Advice']. Reversals are independently 50% when enabled. Returns the cards, orientations and the matching Waite reference meanings; the calling AI interprets them. No prediction or LLM API calls."""
    return {"draw": draw(positions, locale, allow_reversed), "source": {"name": "Shunshi.AI", "url": "https://shunshi.ai"}}

def main():
    mcp.run(transport="stdio")
