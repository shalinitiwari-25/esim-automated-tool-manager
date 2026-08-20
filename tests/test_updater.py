from unittest.mock import patch

from updater import update_tool, check_for_update


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

def test_update_success_logs():
    with patch("updater.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0

        with patch("updater.logger.info") as mock_log:
            result = update_tool("ngspice")

            assert result == "Update successful"
            mock_log.assert_called_once_with(
                "Updated ngspice successfully"
            )

def test_check_update_unknown_tool():
    assert check_for_update("blender") == "Unknown tool"

def test_check_update_available_linux():
    apt_output = (
        "ngspice:\n"
        "  Installed: 41-1\n"
        "  Candidate: 42-1\n"
    )
    with patch("updater.platform.system", return_value="Linux"):
        with patch("updater.subprocess.run") as mock_run:
            mock_run.return_value.stdout = apt_output

            result = check_for_update("ngspice")

            assert result == "Update available: 41-1 -> 42-1"

def test_check_update_already_latest_linux():
    apt_output = (
        "ngspice:\n"
        "  Installed: 42-1\n"
        "  Candidate: 42-1\n"
    )
    with patch("updater.platform.system", return_value="Linux"):
        with patch("updater.subprocess.run") as mock_run:
            mock_run.return_value.stdout = apt_output

            result = check_for_update("ngspice")

            assert result == "Already up to date"

def test_check_update_not_installed_linux():
    apt_output = (
        "ngspice:\n"
        "  Installed: (none)\n"
        "  Candidate: 42-1\n"
    )
    with patch("updater.platform.system", return_value="Linux"):
        with patch("updater.subprocess.run") as mock_run:
            mock_run.return_value.stdout = apt_output

            result = check_for_update("ngspice")

            assert result == "Tool is not installed"

def test_check_update_available_windows():
    choco_output = "ngspice|41.0|42.0|false"

    with patch("updater.platform.system", return_value="Windows"):
        with patch("updater.subprocess.run") as mock_run:
            mock_run.return_value.stdout = choco_output

            result = check_for_update("ngspice")

            assert result == "Update available: 41.0 -> 42.0"

def test_check_update_already_latest_windows():
    choco_output = "ngspice|42.0|42.0|false"

    with patch("updater.platform.system", return_value="Windows"):
        with patch("updater.subprocess.run") as mock_run:
            mock_run.return_value.stdout = choco_output

            result = check_for_update("ngspice")

            assert result == "Already up to date"