import subprocess
from tool_registry import TOOLS
import platform

def update_tool(tool_name):
    if tool_name not in TOOLS:
        return "Unknown tool"

    tool = TOOLS[tool_name]
    os_name = platform.system()

    commands = tool["commands"][os_name]["update"]

    for command in commands:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return result.stderr or "Update failed"

    return "Update successful"