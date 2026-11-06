# tarot calculation core

Bundled in the `shunshi-tarot-mcp` distribution. Import `shunshi_tarot` without starting the MCP server.

See the root README for installation, input conventions and capability limits, and SOURCE.md for calculation provenance.

```python
from shunshi_tarot import card, draw
print(card("the-fool", "en"))
print(draw(["Past", "Present", "Future"]))
```
