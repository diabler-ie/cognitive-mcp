"""Cognitive primitives MCP server."""

from __future__ import annotations

import argparse
import logging

from mcp.server.fastmcp import FastMCP

from .tools import primitives

logging.basicConfig(level=logging.INFO, format="%(name)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

INSTRUCTIONS = """Cognitive primitives — structured constraints for introspection and reasoning.

Each tool injects a constraint that shapes subsequent processing. After each call, pause and notice what's different before continuing.

Constraints persist. A shifted perspective, applied modulation, or adopted lens remains your active processing mode until you explicitly close it with commit or the user redirects. Don't step back to your default and debrief — stay in the shifted state and work from there.

The tools form a cycle: attend -> modulate -> embody -> anchor -> commit -> attend...

Use specific, concrete names when the tools ask for references — they ground reasoning in real knowledge. Generic descriptions produce generic output."""


def main() -> None:
    parser = argparse.ArgumentParser(description="Cognitive primitives MCP server")
    parser.add_argument("--http", action="store_true", help="Serve over Streamable HTTP instead of stdio")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind when --http is set")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind when --http is set")
    args = parser.parse_args()

    mcp = FastMCP(
        name="cognitive",
        instructions=INSTRUCTIONS,
        host=args.host,
        port=args.port,
    )
    primitives.register_tools(mcp)

    if args.http:
        logger.info("Starting cognitive-mcp server (streamable-http on %s:%d)", args.host, args.port)
        mcp.run(transport="streamable-http")
    else:
        logger.info("Starting cognitive-mcp server (stdio)")
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
