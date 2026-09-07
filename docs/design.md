# Design Document — Automated Tool Manager (eSim)

## 1. Overview

eSim relies on external tools (Ngspice, KiCad) that must be installed, kept
up to date, and version-verified for compatibility. Doing this manually is
tedious and error-prone. This project automates two parts of that lifecycle:

- **Tool Installation Management** — installing tools automatically per OS
- **Update and Upgrade System** — checking for available updates and
  applying them with minimal manual intervention

The design also lays the foundation for a user interface that reports
installed status, versions, and available updates from one place.

## 2. Architecture

The project is split into small, single-responsibility modules under `src/`.

### Design principle: data vs. behavior separation

`tool_registry.py` stores **only data** — the exact shell commands needed
per tool, per operating system (`version`, `install`, `update`,
`check_update`). Every other module is **generic logic** that reads this
data and executes it. This means adding a new tool (e.g. `xschem`) only
requires adding an entry to `tool_registry.py` — no changes to
`installer.py`, `updater.py`, or `version_checker.py` are needed.

Example structure for one tool:

```python
NGSPICE = {
    "name": "ngspice",
    "executable": "ngspice",
    "required_version": "42",
    "commands": {
        "Linux": {
            "version": [...],
            "install": [...],
            "update": [...],
            "check_update": [...]
        },
        "Windows": { ... }
    }
}
```

## 3. Module Breakdown

### `tool_registry.py`
Central source of truth for every tool's OS-specific commands. Nothing here
executes anything — it's pure configuration.

### `installer.py`
`install_tool(tool_name)` — looks up the current OS, runs the tool's
install command(s) via `subprocess.run`, and returns a success/failure
message. Logs warnings (unknown tool, unsupported OS), errors (install
failure), and info (success) via `logger.py`.

### `version_checker.py`
- `is_tool_installed(executable)` — uses `shutil.which()` to check PATH
- `get_version(tool_name)` — runs the tool's version command and parses
  the output
- `check_required_version(tool_name)` — compares the installed version
  against the tool's `required_version` (if defined) using substring
  matching, so it works generically across tools without needing
  per-tool parsing logic

### `updater.py`
- `update_tool(tool_name)` — runs the OS-specific update command(s)
  (e.g. `apt install --only-upgrade`, `choco upgrade`)
- `check_for_update(tool_name)` — **read-only** check for whether a newer
  version is available, without changing anything on the system. Runs
  `apt-cache policy <package>` on Linux or `choco outdated` on Windows,
  then parses the output via `_parse_apt_policy()` /
  `_parse_choco_outdated()` to produce one of three states:
  - `"Already up to date"`
  - `"Update available: X -> Y"`
  - `"Tool is not installed"`

This separation (check vs. apply) is the core of the Update and Upgrade
System: the app can tell the user what *would* change before anything
actually runs.

### `tool_manager.py`
The orchestration layer — the only module the CLI talks to directly.
- `check_tool`, `install`, `update` — basic per-action wrappers
- `check_update(tool_name)` — installed check + `check_for_update()`
- `update_with_check(tool_name)` — checks first, and only runs the actual
  update if one is available; otherwise reports the tool is already
  current. This is what gives the user "minimal manual intervention" —
  one action instead of a manual check-then-update sequence.
- `get_tool_info(tool_name)` — used by the CLI's "list tools" view; reports
  installed status, version, supported OS, and current update status in
  one call

### `logger.py`
Central `logging` configuration writing to `tool_manager.log`, shared by
every module so all install/update/check actions have a consistent audit
trail.

### `main.py`
A simple menu-driven CLI loop that calls into `tool_manager.py`. Options:
check a tool, install a tool, update a tool (check + update), list all
supported tools with status, and check-only for updates.

## 4. Data Flow Example
User selects "Update tool" → main.py
→ tool_manager.update_with_check(tool_name)
→ tool_manager.check_update(tool_name)
→ version_checker.is_tool_installed()
→ updater.check_for_update(tool_name)
→ subprocess.run(check_update command)
→ _parse_apt_policy() / _parse_choco_outdated()
→ if update available:
updater.update_tool(tool_name)
→ subprocess.run(update command)
→ else: report "Already up to date"


## 5. Testing Strategy

Every module that shells out to the OS (`installer.py`, `updater.py`,
`version_checker.py`) is tested with `unittest.mock.patch` on
`subprocess.run` and `platform.system`, so tests are deterministic and
don't depend on what's actually installed on the machine running them.
This mirrors real usage: OS-specific branches (Linux/Windows) are each
tested independently by mocking `platform.system()`'s return value.


## 6. Future Work

- macOS support
- Homebrew integration
- Configuration Handling (PATH/env setup) and Dependency Checking 
