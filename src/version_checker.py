import shutil
import subprocess
from tool_registry import TOOLS
import platform

def is_tool_installed(executable_name):
    path = shutil.which(executable_name)
    return bool(path)

def get_version(tool_name):

    if tool_name not in TOOLS:
        return "Unknown tool"

    tool = TOOLS[tool_name]
    os_name = get_os()

    if os_name not in tool["commands"]:
        return f"Unsupported operating system: {os_name}"

    command = tool["commands"][os_name]["version"]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()

def get_os():
    return platform.system()


