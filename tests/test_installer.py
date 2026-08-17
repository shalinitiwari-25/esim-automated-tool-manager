from unittest.mock import patch
from installer import install_tool


def test_unknown_tool():
    assert install_tool("blender") == "Unknown tool"

def test_installation_success():
    with patch("installer.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0

        result = install_tool("ngspice")

        assert result == "Installation successful"

def test_installation_failure():
    with patch("installer.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Permission denied"

        result = install_tool("ngspice")

        assert result == "Permission denied"
    
def test_kicad_linux_install_commands():
    with patch("installer.platform.system", return_value="Linux"):
        with patch("installer.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0

            result = install_tool("kicad")

            assert result == "Installation successful"
            assert mock_run.call_count == 2

def test_kicad_windows_install_commands():
    with patch("installer.platform.system", return_value="Windows"):
        with patch("installer.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0

            result = install_tool("kicad")

            assert result == "Installation successful"
            assert mock_run.call_count == 1

            mock_run.assert_called_once_with(
                ["choco", "install", "kicad", "-y"],
                capture_output=True,
                text=True
            )

def test_install_unsupported_os():
    with patch("installer.platform.system", return_value="Darwin"):
        result = install_tool("ngspice")

        assert result == "Unsupported operating system: Darwin"

def test_install_success_logs():
    with patch("installer.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0

        with patch("installer.logger.info") as mock_log:
            result = install_tool("ngspice")

            assert result == "Installation successful"
            mock_log.assert_called_once_with(
                "Installed ngspice successfully"
            )