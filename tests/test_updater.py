from unittest.mock import patch

from updater import update_tool


def test_unknown_tool():
    assert update_tool("blender") == "Unknown tool"

def test_update_success():
    with patch("updater.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0

        result = update_tool("ngspice")

        assert result == "Update successful"

def test_update_failure():
    with patch("updater.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Permission denied"

        result = update_tool("ngspice")

        assert result == "Permission denied"

def test_kicad_linux_update_commands():
    with patch("updater.platform.system", return_value="Linux"):
        with patch("updater.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0

            result = update_tool("kicad")

            assert result == "Update successful"
            assert mock_run.call_count == 2

def test_kicad_windows_update_commands():
    with patch("updater.platform.system", return_value="Windows"):
        with patch("updater.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0

            result = update_tool("kicad")

            assert result == "Update successful"
            assert mock_run.call_count == 1

            mock_run.assert_called_once_with(
                ["choco", "upgrade", "kicad", "-y"],
                capture_output=True,
                text=True
            )

def test_update_unsupported_os():
    with patch("updater.platform.system", return_value="Darwin"):
        result = update_tool("ngspice")

        assert result == "Unsupported operating system: Darwin"