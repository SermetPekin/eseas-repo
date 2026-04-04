"""Tests for eseas.core.refresh_excel module"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from eseas.core.refresh_excel import (
    ask_permission,
    excel_running,
    File,
)

# Conditionally import Windows-specific functions
if sys.platform == "win32":
    from eseas.core.refresh_excel import shut_excel, get_excel_app, refresh


class TestAskPermission:
    """Test ask_permission function"""

    @patch("eseas.core.refresh_excel.get_input")
    def test_ask_permission_yes(self, mock_input):
        """Test permission granted with 'yes'"""
        mock_input.return_value = "yes"
        assert ask_permission() is True

    @patch("eseas.core.refresh_excel.get_input")
    def test_ask_permission_y(self, mock_input):
        """Test permission granted with 'y'"""
        mock_input.return_value = "y"
        assert ask_permission() is True

    @patch("eseas.core.refresh_excel.get_input")
    def test_ask_permission_ok(self, mock_input):
        """Test permission granted with 'ok'"""
        mock_input.return_value = "ok"
        assert ask_permission() is True

    @patch("eseas.core.refresh_excel.get_input")
    def test_ask_permission_good(self, mock_input):
        """Test permission granted with 'good'"""
        mock_input.return_value = "good"
        assert ask_permission() is True

    @patch("eseas.core.refresh_excel.get_input")
    def test_ask_permission_no(self, mock_input):
        """Test permission denied with 'no'"""
        mock_input.return_value = "no"
        assert ask_permission() is False

    @patch("eseas.core.refresh_excel.get_input")
    def test_ask_permission_n(self, mock_input):
        """Test permission denied with 'n'"""
        mock_input.return_value = "n"
        assert ask_permission() is False

    @patch("eseas.core.refresh_excel.get_input")
    def test_ask_permission_uppercase(self, mock_input):
        """Test permission with uppercase input"""
        mock_input.return_value = "YES"
        assert ask_permission() is True

    @patch("eseas.core.refresh_excel.get_input")
    def test_ask_permission_mixed_case(self, mock_input):
        """Test permission with mixed case input"""
        mock_input.return_value = "YeS"
        assert ask_permission() is True


class TestExcelRunning:
    """Test excel_running function"""

    @patch("eseas.core.refresh_excel.psutil.process_iter")
    def test_excel_not_running(self, mock_process_iter):
        """Test when Excel is not running"""
        mock_process_iter.return_value = [
            MagicMock(info={"name": "python.exe"}),
            MagicMock(info={"name": "chrome.exe"}),
        ]
        assert excel_running() is False

    @patch("eseas.core.refresh_excel.psutil.process_iter")
    def test_excel_running(self, mock_process_iter):
        """Test when Excel is running"""
        mock_process_iter.return_value = [
            MagicMock(info={"name": "python.exe"}),
            MagicMock(info={"name": "EXCEL.EXE"}),
        ]
        assert excel_running() is True

    @patch("eseas.core.refresh_excel.psutil.process_iter")
    def test_excel_running_lowercase(self, mock_process_iter):
        """Test when Excel process name is lowercase"""
        mock_process_iter.return_value = [
            MagicMock(info={"name": "excel.exe"}),
        ]
        assert excel_running() is True

    @patch("eseas.core.refresh_excel.psutil.process_iter")
    def test_excel_running_mixed_case(self, mock_process_iter):
        """Test when Excel process name is mixed case"""
        mock_process_iter.return_value = [
            MagicMock(info={"name": "Excel.exe"}),
        ]
        assert excel_running() is True

    @patch("eseas.core.refresh_excel.psutil.process_iter")
    def test_no_processes_running(self, mock_process_iter):
        """Test when no processes are running"""
        mock_process_iter.return_value = []
        assert excel_running() is False


class TestFileClass:
    """Test File class"""

    def test_file_init(self, tmp_path):
        """Test File initialization"""
        file_name = "test.xlsx"
        file = File(file_name, tmp_path)
        assert file.name == file_name
        assert file.folder == tmp_path
        assert isinstance(file.path, Path)

    def test_file_str_representation(self, tmp_path):
        """Test File string representation"""
        file = File("test.xlsx", tmp_path)
        str_repr = str(file)
        assert "<File [" in str_repr
        assert "]>" in str_repr
        assert "test.xlsx" in str_repr

    def test_file_exists_true(self, tmp_path):
        """Test File.exists() when file exists"""
        test_file = tmp_path / "test.xlsx"
        test_file.touch()
        file = File("test.xlsx", tmp_path)
        assert file.exists() is True

    def test_file_exists_false(self, tmp_path):
        """Test File.exists() when file doesn't exist"""
        file = File("nonexistent.xlsx", tmp_path)
        assert file.exists() is False

    def test_file_check_success(self, tmp_path):
        """Test File.check() when file exists"""
        test_file = tmp_path / "test.xlsx"
        test_file.touch()
        file = File("test.xlsx", tmp_path)
        # Should not raise exception
        file.check()

    def test_file_check_failure(self, tmp_path):
        """Test File.check() when file doesn't exist"""
        file = File("nonexistent.xlsx", tmp_path)
        with pytest.raises(ValueError, match="File Not found"):
            file.check()

    def test_file_path_is_absolute(self, tmp_path):
        """Test that File.path is absolute"""
        file = File("test.xlsx", tmp_path)
        assert file.path.is_absolute()

    def test_file_with_current_directory(self):
        """Test File with current directory"""
        file = File("test.xlsx", Path("."))
        assert isinstance(file.folder, Path)
        assert file.path.is_absolute()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific tests")
class TestWindowsSpecific:
    """Tests for Windows-specific functionality"""

    @patch("eseas.core.refresh_excel.subprocess.run")
    @patch("eseas.core.refresh_excel.ask_permission")
    def test_shut_excel_with_permission(self, mock_ask, mock_run):
        """Test shutting down Excel with user permission"""
        mock_ask.return_value = True
        mock_run.return_value = MagicMock(stdout="SUCCESS: Process terminated.")

        shut_excel(approve=False)

        mock_ask.assert_called_once()
        mock_run.assert_called_once()
        assert "taskkill" in mock_run.call_args[0][0]

    @patch("eseas.core.refresh_excel.subprocess.run")
    def test_shut_excel_auto_approve(self, mock_run):
        """Test shutting down Excel with auto-approve"""
        mock_run.return_value = MagicMock(stdout="SUCCESS: Process terminated.")

        shut_excel(approve=True)

        mock_run.assert_called_once()

    @patch("eseas.core.refresh_excel.ask_permission")
    def test_shut_excel_permission_denied(self, mock_ask):
        """Test shutting down Excel when permission is denied"""
        mock_ask.return_value = False

        with pytest.raises(ValueError, match="User did not confirm"):
            shut_excel(approve=False)

    @patch("eseas.core.refresh_excel.excel_running")
    @patch("eseas.core.refresh_excel.shut_excel")
    @patch("eseas.core.refresh_excel.win32com.client.Dispatch")
    def test_get_excel_app_excel_running(self, mock_dispatch, mock_shut, mock_running):
        """Test getting Excel app when Excel is running"""
        mock_running.return_value = True
        mock_excel = MagicMock()
        mock_dispatch.return_value = mock_excel

        result = get_excel_app(approve=True)

        mock_shut.assert_called_once_with(True)
        mock_dispatch.assert_called_once_with("Excel.Application")
        assert result == mock_excel

    @patch("eseas.core.refresh_excel.excel_running")
    @patch("eseas.core.refresh_excel.win32com.client.Dispatch")
    def test_get_excel_app_excel_not_running(self, mock_dispatch, mock_running):
        """Test getting Excel app when Excel is not running"""
        mock_running.return_value = False
        mock_excel = MagicMock()
        mock_dispatch.return_value = mock_excel

        result = get_excel_app(approve=False)

        mock_dispatch.assert_called_once_with("Excel.Application")
        assert result == mock_excel


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific tests")
class TestFileRefresh:
    """Tests for File.refresh() method"""

    @patch("eseas.core.refresh_excel.get_excel_app")
    @patch("eseas.core.refresh_excel.time.sleep")
    def test_file_refresh_success(self, mock_sleep, mock_get_excel, tmp_path):
        """Test successful file refresh"""
        # Create a test file
        test_file = tmp_path / "test.xlsx"
        test_file.touch()

        # Mock Excel app
        mock_excel = MagicMock()
        mock_wb = MagicMock()
        mock_excel.Workbooks.Open.return_value = mock_wb
        mock_get_excel.return_value = mock_excel

        # Create File and refresh
        file = File("test.xlsx", tmp_path, approve=True)
        file.refresh()

        # Verify Excel operations
        mock_excel.Workbooks.Open.assert_called_once()
        mock_wb.RefreshAll.assert_called_once()
        mock_wb.Save.assert_called_once()
        mock_wb.Close.assert_called_once_with(False)

    @patch("eseas.core.refresh_excel.get_excel_app")
    def test_file_refresh_error_handling(self, mock_get_excel, tmp_path):
        """Test file refresh error handling"""
        # Create a test file
        test_file = tmp_path / "test.xlsx"
        test_file.touch()

        # Mock Excel app to raise exception
        mock_excel = MagicMock()
        mock_excel.Workbooks.Open.side_effect = Exception("Test error")
        mock_get_excel.return_value = mock_excel

        # Create File and refresh (should handle exception gracefully)
        file = File("test.xlsx", tmp_path, approve=True)
        # Should not raise exception
        file.refresh()


class TestCheckAndGetFiles:
    """Test check_and_get_files generator function"""

    def test_check_and_get_files_all_exist(self, tmp_path):
        """Test with all files existing"""
        # Create test files
        file1 = tmp_path / "file1.xlsx"
        file2 = tmp_path / "file2.xlsx"
        file1.touch()
        file2.touch()

        from eseas.core.refresh_excel import check_and_get_files

        files = ["file1.xlsx", "file2.xlsx"]
        result = list(check_and_get_files(files, tmp_path, approve=True))

        assert len(result) == 2
        assert all(isinstance(f, File) for f in result)

    def test_check_and_get_files_missing_file(self, tmp_path):
        """Test with missing file"""
        file1 = tmp_path / "file1.xlsx"
        file1.touch()

        from eseas.core.refresh_excel import check_and_get_files

        files = ["file1.xlsx", "missing.xlsx"]

        with pytest.raises(ValueError, match="File Not found"):
            list(check_and_get_files(files, tmp_path, approve=True))

    def test_check_and_get_files_empty_list(self, tmp_path):
        """Test with empty file list"""
        from eseas.core.refresh_excel import check_and_get_files

        result = list(check_and_get_files([], tmp_path, approve=True))
        assert len(result) == 0


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific tests")
class TestRefreshFunction:
    """Tests for refresh() main function"""

    @patch("eseas.core.refresh_excel.pythoncom")
    @patch("eseas.core.refresh_excel.check_and_get_files")
    @patch("eseas.core.refresh_excel.excel_app", None)
    def test_refresh_function(self, mock_check_files, mock_com, tmp_path):
        """Test main refresh function"""
        # Create mock files
        mock_file1 = MagicMock(spec=File)
        mock_file2 = MagicMock(spec=File)
        mock_check_files.return_value = [mock_file1, mock_file2]

        files = ["file1.xlsx", "file2.xlsx"]
        refresh(files, tmp_path, approve=True)

        # Verify COM initialization
        mock_com.CoInitialize.assert_called_once()
        mock_com.CoUninitialize.assert_called_once()

        # Verify refresh called for each file
        mock_file1.refresh.assert_called_once()
        mock_file2.refresh.assert_called_once()

    @patch("eseas.core.refresh_excel.pythoncom")
    @patch("eseas.core.refresh_excel.check_and_get_files")
    def test_refresh_function_with_excel_app(self, mock_check_files, mock_com, tmp_path):
        """Test refresh function with existing excel_app"""
        import eseas.core.refresh_excel as refresh_module

        # Mock excel app
        mock_excel = MagicMock()
        refresh_module.excel_app = mock_excel

        mock_file = MagicMock(spec=File)
        mock_check_files.return_value = [mock_file]

        try:
            refresh(["file1.xlsx"], tmp_path, approve=True)

            # Verify Excel quit was called
            mock_excel.Quit.assert_called_once()
        finally:
            # Clean up
            refresh_module.excel_app = None
