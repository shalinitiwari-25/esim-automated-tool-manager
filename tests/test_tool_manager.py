from unittest.mock import patch

from tool_manager import check_tool, install, update, list_tools, get_tool_info

def test_unknown_tool():
    assert check_tool("blender") == "Unknown tool"

def test_tool_not_installed():
    with patch("tool_manager.is_tool_installed", return_value=False):
        assert check_tool("ngspice") == "ngspice is not installed"

def test_install_already_installed():
    with patch("tool_manager.is_tool_installed") as mock_check:
        mock_check.return_value = True

        result = install("ngspice")

        assert result == "Already installed"

def test_install_not_installed():
    with patch("tool_manager.is_tool_installed") as mock_check:
        with patch("tool_manager.install_tool") as mock_install:
            mock_check.return_value = False
            mock_install.return_value = "Installation successful"

            result = install("ngspice")

            assert result == "Installation successful"
            mock_install.assert_called_once_with("ngspice")

def test_update_unknown_tool():
    assert update("blender") == "Unknown tool"

def test_update_not_installed():
    with patch("tool_manager.is_tool_installed") as mock_check:
        mock_check.return_value = False

        result = update("ngspice")

        assert result == "ngspice is not installed"

def test_update_success():
    with patch("tool_manager.is_tool_installed") as mock_check:
        with patch("tool_manager.update_tool") as mock_update:
            mock_check.return_value = True
            mock_update.return_value = "Update successful"

            result = update("ngspice")

            assert result == "Update successful"
            mock_update.assert_called_once_with("ngspice")

def test_kicad_is_registered():
    from tool_registry import TOOLS

    assert "kicad" in TOOLS
    assert "Linux" in TOOLS["kicad"]["commands"]
    assert "Windows" in TOOLS["kicad"]["commands"]

def test_kicad_linux_commands():
    from tool_registry import TOOLS

    linux_commands = TOOLS["kicad"]["commands"]["Linux"]

    assert linux_commands["version"] == ["kicad", "--version"]
    assert linux_commands["install"][0] == ["sudo", "apt", "update"]
    assert linux_commands["install"][1] == [
        "sudo", "apt", "install", "-y", "kicad"
    ]

def test_kicad_windows_commands():
    from tool_registry import TOOLS

    windows_commands = TOOLS["kicad"]["commands"]["Windows"]

    assert windows_commands["version"] == ["kicad", "--version"]
    assert windows_commands["install"] == [
        ["choco", "install", "kicad", "-y"]
    ]

def test_list_tools():
    tools = list_tools()

    assert "ngspice" in tools
    assert "kicad" in tools

def test_get_tool_info_unknown_tool():
    assert get_tool_info("blender") == "Unknown tool"

def test_get_tool_info_installed():
    with patch("tool_manager.is_tool_installed", return_value=True):
        with patch(
            "tool_manager.get_version",
            return_value="ngspice-42"
        ):
            result = get_tool_info("ngspice")

            assert result == "ngspice: Installed - ngspice-42"

def test_get_tool_info_not_installed():
    with patch("tool_manager.is_tool_installed", return_value=False):
        result = get_tool_info("ngspice")

        assert result == "ngspice: Not installed"