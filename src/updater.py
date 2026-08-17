import subprocess
from tool_registry import TOOLS
import platform
from logger import logger

def update_tool(tool_name):
    if tool_name not in TOOLS:
        logger.warning(f"Unknown tool: {tool_name}")
        return "Unknown tool"

    tool = TOOLS[tool_name]
    os_name = platform.system()

    if os_name not in tool["commands"]:
        logger.warning(
            f"Unsupported OS for {tool_name}: {os_name}"
        )
        return f"Unsupported operating system: {os_name}"

    commands = tool["commands"][os_name]["update"]

    for command in commands:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            logger.error(f"Update failed for {tool_name}")
            return result.stderr or "Update failed"
    
    logger.info(f"Updated {tool_name} successfully")
    return "Update successful"