"""Cognitive primitives MCP server."""

from __future__ import annotations

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

mcp = FastMCP(name="cognitive", instructions=INSTRUCTIONS)

primitives.register_tools(mcp)


def main() -> None:
    logger.info("Starting cognitive-mcp server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
