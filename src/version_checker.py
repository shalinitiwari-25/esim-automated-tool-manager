import shutil
import subprocess
from tool_registry import TOOLS

def is_tool_installed(executable_name):
    path = shutil.which(executable_name)
    return bool(path)

def get_version(tool_name):
    command = TOOLS[tool_name]["version_command"]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print('STDOUT:', result.stdout)
        print('STDERR:', result.stderr)
        print('RETURN CODE:', result.returncode)
        if result.returncode!=0:
            return None
    except FileNotFoundError:
        return None
    
    return result.stdout or result.stderr

