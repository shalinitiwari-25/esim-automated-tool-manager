import shutil
import subprocess
from tool_registry import TOOLS
import platform

def is_tool_installed(executable_name):
    path = shutil.which(executable_name)
    return bool(path)

def get_version(tool_name):
    tool = TOOLS[tool_name]
    os_name = get_os()

    command = tool["commands"][os_name]["version"]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()

def get_os():
    return platform.system()


