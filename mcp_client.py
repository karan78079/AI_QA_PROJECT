import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _snapshot_text(result) -> str:
    parts = []
    for item in getattr(result, "content", []) or []:
        text = getattr(item, "text", None)
        if text:
            parts.append(text)
    return "\n".join(parts) or str(result)


async def get_page_snapshot(url):

    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp@latest", "--headless"]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            print("MCP connected")

            await session.call_tool(
                "browser_navigate",
                {
                    "url": url
                }
            )

            print("Website opened")

            result = await session.call_tool(
                "browser_snapshot",
                {}
            )

            return _snapshot_text(result)