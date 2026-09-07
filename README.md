# esim-automated-tool-manager

An automated tool manager automates installing, checking, and
updating external tools (Ngspice, KiCad) that eSim depends on, so users
don't have to manage them manually.

See [`docs/design.md`](docs/design.md) for the full architecture and
module breakdown.

## Supported Tools

- Ngspice
- KiCad

## Supported Platforms

- Linux
- Windows

## Project Structure
src/
├── tool_registry.py # Per-tool, per-OS command definitions
├── installer.py # Installs tools
├── updater.py # Checks for and applies updates
├── version_checker.py # Detects and validates installed versions
├── tool_manager.py # Orchestrates the above modules
├── logger.py # Central logging setup
└── main.py # CLI entry point

tests/ # Unit tests (pytest, all subprocess calls mocked)
docs/design.md # Design document


## Installation

```bash
git clone <your-repo-url>
cd esim-automated-tool-manager
pip install -r requirements.txt
```

## Usage

Run the CLI from the project root:

```bash
python src/main.py
```

You'll see a menu:
--- Automated Tool Manager ---

Check tool
Install tool
Update tool (check + update)
List supported tools
Check for updates only
q. Quit


- **1** — Check whether a tool is installed and see its version
- **2** — Install a tool automatically
- **3** — Check for an update and apply it if one is available
- **4** — List all supported tools with installed status, version, and
  update availability
- **5** — Check for an update without installing it

## Running Tests

```bash
pytest -v
```

All tests mock `subprocess.run` and `platform.system`, so they run
deterministically regardless of what's actually installed on the machine.

## Logging

All actions (installs, updates, checks, warnings, errors) are written to
`tool_manager.log` in the project root.
