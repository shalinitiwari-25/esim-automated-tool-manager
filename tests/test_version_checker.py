from unittest.mock import patch, Mock
from version_checker import is_tool_installed, get_version
from tool_registry import TOOLS
from version_checker import check_required_version

def test_ngspice_is_installed():
    assert is_tool_installed("ngspice") is True

def test_cate_is_not_installed():
    assert is_tool_installed("cate") is False

def test_ngspice_version():
    mock_result = Mock()
    mock_result.stdout = "ngspice version 45"
    
    with patch("version_checker.subprocess.run", return_value=mock_result):
        version = get_version("ngspice")

    assert version == "ngspice version 45"

def test_unsupported_os():
    with patch("version_checker.get_os", return_value="Darwin"):
        result = get_version("ngspice")

        assert result == "Unsupported operating system: Darwin"

def test_required_version():
    assert TOOLS["ngspice"]["required_version"] == "42"

def test_correct_required_version():
    with patch("version_checker.get_version", return_value="ngspice-42"):
        assert check_required_version("ngspice") == "Correct version"

def test_version_mismatch():
    with patch("version_checker.get_version", return_value="ngspice-41"):
        result = check_required_version("ngspice")

        assert result == "Version mismatch: required 42, installed ngspice-41"