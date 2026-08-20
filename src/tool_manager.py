from tool_registry import TOOLS
from version_checker import is_tool_installed, get_version, check_required_version
from installer import install_tool
from updater import update_tool, check_for_update

def check_tool(tool_name):

    if tool_name not in TOOLS:
        return "Unknown tool"

    tool = TOOLS[tool_name]
    executable = tool["executable"]

    if not is_tool_installed(executable):
        return f"{tool_name} is not installed"

    version = get_version(tool_name)
    version_status = check_required_version(tool_name)

    return (
        f"{tool_name}\n"
        f"Installed version: {version}\n"
        f"Version status: {version_status}"
    )

def install(tool_name):
     
    if tool_name not in TOOLS:
        return "Unknown tool"

    tool = TOOLS[tool_name]
    executable = tool["executable"]

    if is_tool_installed(executable):
        return "Already installed"

    return install_tool(tool_name)

def update(tool_name):

    if tool_name not in TOOLS:
        return "Unknown tool"

    tool = TOOLS[tool_name]
    executable = tool["executable"]

    if not is_tool_installed(executable):
        return f'{tool_name} is not installed'

    return update_tool(tool_name)

def check_update(tool_name):
    if tool_name not in TOOLS:
        return "Unknown tool"

    tool = TOOLS[tool_name]
    executable = tool["executable"]

    if not is_tool_installed(executable):
        return f"{tool_name} is not installed"

    return check_for_update(tool_name)


def update_with_check(tool_name):
    status = check_update(tool_name)

    if status == "Already up to date":
        return status

    if status in ("Unknown tool",) or status.endswith("is not installed"):
        return status

    if status.startswith("Unsupported operating system"):
        return status

    if status.startswith("Update available"):
        result = update_tool(tool_name)
        return f"{status}\n{result}"

    return update_tool(tool_name)

def list_tools():
    return list(TOOLS.keys())

def get_tool_info(tool_name):
    if tool_name not in TOOLS:
        return "Unknown tool"

    tool = TOOLS[tool_name]
    supported_os = ", ".join(tool["commands"].keys())
    installed = is_tool_installed(tool["executable"])

    if installed:
        version = get_version(tool_name)
        update_status = check_for_update(tool_name)
        return (
            f"{tool_name}: Installed - {version}\n"
            f"  Supported OS: {supported_os}\n"
            f"  Update status: {update_status}"
        )

    return (
        f"{tool_name}: Not installed\n"
        f"  Supported OS: {supported_os}"
    )