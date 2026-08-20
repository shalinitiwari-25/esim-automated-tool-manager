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

    output = result.stdout.strip()

    if tool_name == "ngspice":
        for line in output.splitlines():
            if "ngspice-" in line:
                version_part = line.strip("* ").strip()
                return version_part.split(":")[0].strip()

    return output

def check_required_version(tool_name):
    if tool_name not in TOOLS:
        return "Unknown tool"

    tool = TOOLS[tool_name]

    if "required_version" not in tool:
        return "No required version specified"

    required_version = tool["required_version"]
    installed_version = get_version(tool_name)

    if installed_version == f"{tool_name}-{required_version}":
        return "Correct version"

    return (
        f"Version mismatch: required {required_version}, "
        f"installed {installed_version}"
    )

def get_os():
    return platform.system()


