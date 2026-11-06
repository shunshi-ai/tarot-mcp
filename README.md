# tarot-mcp

**Tarot · 塔罗 · 塔羅 · タロット · 타로**

[Shunshi.AI](https://shunshi.ai) local calculation core + Model Context Protocol server.
Python 3.11+, MIT. No API key, database connection or hosted LLM is required.

78 Rider–Waite–Smith card records with names in five languages, Golden Dawn correspondences, and the public-domain English text of Waite (1910). Secure random draws without replacement; optional independent 50% reversals. Positions are supplied before drawing. Waite source text stays English and a missing reversed meaning stays `null`; the calling AI may interpret it, without inventing an attributed quotation.

## Install and connect

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) from its official source. Add this configuration to an MCP client supporting stdio (Claude Desktop, Cursor, Cline or Codex):

```json
{
  "mcpServers": {
    "shunshi-tarot": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/shunshi-ai/tarot-mcp@v0.1.0",
        "shunshi-tarot-mcp"
      ]
    }
  }
}
```

This uses a tagged GitHub source release, **not a PyPI package**. Dependencies are installed from PyPI by uv; the source tag is pinned. Restart the client after adding the server.

For a local checkout:

```bash
git clone https://github.com/shunshi-ai/tarot-mcp.git
cd tarot-mcp
uv sync --locked
uv run shunshi-tarot-mcp
```

The server speaks JSON-RPC on stdout; it intentionally does not print a welcome message.

## Tools

- `listCards` — inspect its MCP schema for validated parameters.
- `getCardMeaning` — inspect its MCP schema for validated parameters.
- `drawCards` — inspect its MCP schema for validated parameters.

Example parameters for `listCards`:

```json
{
  "locale": "ko"
}
```

Results include a source URL. Computed values and reference text are separate from the calling AI's interpretation; this server does not promise future outcomes.

## Structure and development

`packages/core/src/` contains the reusable core; `src/shunshi_tarot_mcp/` contains the MCP adapter. Both ship in one wheel, so no unpublished sibling package is needed. The core can be imported without starting MCP. Calculation provenance is documented in [SOURCE.md](SOURCE.md).

```bash
uv sync --locked
uv run pytest -q
uv build
```

Tests include a real stdio MCP client handshake, tool calls, invalid inputs and recovery. Core reference tests are included where available. No production services are contacted.

## Privacy and license

Inputs stay in the local process; there is no product telemetry. Your MCP client's own model provider may receive tool inputs and outputs according to that client's configuration. Standard Python package installation downloads dependencies. Images, where present, are links; opening them is a separate client action.

MIT © 2026 Shunshi.AI. Preserve any upstream copyright in NOTICE.

Website: [https://shunshi.ai](https://shunshi.ai)

## CI template

`docs/github-actions-test.yml` is a ready-to-use GitHub Actions template for Python 3.11–3.13. It is not enabled in this initial release because the publishing credential does not have workflow scope. Tests and installation checks were run locally; enabling hosted CI is a separate step.
