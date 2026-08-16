from unittest.mock import patch, Mock
from version_checker import is_tool_installed, get_version

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
