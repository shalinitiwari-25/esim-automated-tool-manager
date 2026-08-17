import subprocess
from tool_registry import TOOLS
import platform

def install_tool(tool_name):
    if tool_name not in TOOLS:
        return "Unknown tool"

    tool = TOOLS[tool_name]
    os_name = platform.system()

    if os_name not in tool["commands"]:
        return f"Unsupported operating system: {os_name}"

    commands = tool["commands"][os_name]["install"]

    for command in commands:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return result.stderr or "Installation failed"

    return "Installation successful"

def test_install_unsupported_os():
    with patch("installer.platform.system", return_value="Darwin"):
        result = install_tool("ngspice")

        assert result == "Unsupported operating system: Darwin"