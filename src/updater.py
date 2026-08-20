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

def check_for_update(tool_name):
    if tool_name not in TOOLS:
        logger.warning(f"Unknown tool: {tool_name}")
        return "Unknown tool"

    tool = TOOLS[tool_name]
    os_name = platform.system()

    if os_name not in tool["commands"]:
        return f"Unsupported operating system: {os_name}"

    command = tool["commands"][os_name]["check_update"]

    result = subprocess.run(command, capture_output=True, text=True)

    if os_name == "Linux":
        status = _parse_apt_policy(result.stdout)
    elif os_name == "Windows":
        status = _parse_choco_outdated(result.stdout, tool["name"])
    else:
        status = "Unable to determine update status"

    logger.info(f"Checked updates for {tool_name}: {status}")
    return status

def _parse_apt_policy(output):
    installed = None
    candidate = None

    for line in output.splitlines():
        line = line.strip()
        if line.startswith("Installed:"):
            installed = line.split(":", 1)[1].strip()
        elif line.startswith("Candidate:"):
            candidate = line.split(":", 1)[1].strip()

    if installed is None or installed == "(none)":
        return "Tool is not installed"

    if candidate is None or candidate == installed:
        return "Already up to date"

    return f"Update available: {installed} -> {candidate}"

def _parse_choco_outdated(output, package_name):
    for line in output.splitlines():
        if line.lower().startswith(package_name.lower() + "|"):
            parts = line.split("|")
            if len(parts) >= 3:
                installed, available = parts[1], parts[2]
                if installed != available:
                    return f"Update available: {installed} -> {available}"
    return "Already up to date"