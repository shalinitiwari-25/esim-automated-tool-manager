from tool_registry import TOOLS
from version_checker import is_tool_installed, get_version

def check_tool(tool_name):

    if tool_name not in TOOLS:
        return 'Unknown tool'
    
    tool = TOOLS[tool_name]
    executable = tool["executable"]
    installed = is_tool_installed(executable)
    if not installed:
        return f'{tool_name} is not installed'
    
    return get_version(tool_name)

print(check_tool("ngspice"))
print(check_tool("blender"))