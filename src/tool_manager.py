from tool_registry import TOOLS
from version_checker import is_tool_installed, get_version
from installer import install_tool
from updater import update_tool

def check_tool(tool_name):

    if tool_name not in TOOLS:
        return 'Unknown tool'
    
    tool = TOOLS[tool_name]
    executable = tool["executable"]
    installed = is_tool_installed(executable)
    if not installed:
        return f'{tool_name} is not installed'
    
    return get_version(tool_name)

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

def list_tools():
    return list(TOOLS.keys())

def get_tool_info(tool_name):
    if tool_name not in TOOLS:
        return "Unknown tool"

    tool = TOOLS[tool_name]
    installed = is_tool_installed(tool["executable"])

    if installed:
        version = get_version(tool_name)
        return f"{tool_name}: Installed - {version}"

    return f"{tool_name}: Not installed"

