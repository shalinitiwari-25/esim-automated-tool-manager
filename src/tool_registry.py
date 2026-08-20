NGSPICE = {
    "name": "ngspice",
    "executable": "ngspice",
    "required_version": "42",
    "commands": {
        "Linux": {
            "version": ["ngspice", "--version"],
            "install": [["sudo", "apt", "install", "-y", "ngspice"]],
            "update": [["sudo", "apt", "install", "--only-upgrade", "-y", "ngspice"]],
            "check_update": ["apt-cache", "policy", "ngspice"]
        },

        "Windows": {
            "version": ["ngspice", "--version"],
            "install": [["choco", "install", "ngspice", "-y"]],
            "update": [["choco", "upgrade", "ngspice", "-y"]],
            "check_update": ["choco", "outdated"]

        }
    }
}

KICAD = {
    "name": "kicad",
    "executable": "kicad",
    "required_version": "8.0",
    "commands": {
        "Linux": {
            "version": ["kicad", "--version"],
            "install": [
                ["sudo", "apt", "update"],
                ["sudo", "apt", "install", "-y", "kicad"]
            ],
            "update": [
                ["sudo", "apt", "update"],
                ["sudo", "apt", "install", "--only-upgrade", "-y", "kicad"]
            ],
            "check_update": ["apt-cache", "policy", "kicad"]
        },

        "Windows": {
            "version": ["kicad", "--version"],
            "install": [
                ["choco", "install", "kicad", "-y"]
            ],
            "update": [
                ["choco", "upgrade", "kicad", "-y"]
            ],
            "check_update": ["choco", "outdated"]
        }
    }
}

TOOLS = {
    "ngspice": NGSPICE,
    "kicad": KICAD
}