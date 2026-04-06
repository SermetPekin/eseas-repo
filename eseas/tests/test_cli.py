"""Tests for eseas CLI tool"""

import pytest
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import CLI functions
from eseas.cli.main import (
    get_config_path,
    create_default_config,
    load_config,
    save_config,
    cmd_run,
    cmd_config,
    cmd_validate,
    cmd_doctor,
    cmd_logs,
    main,
)


class TestConfigPath:
    """Test configuration path functions"""

    def test_get_config_path(self):
        """Test getting config path"""
        config_path = get_config_path()
        assert config_path.name == "eseas_config.yaml"
        assert config_path.parent == Path.cwd()


class TestDefaultConfig:
    """Test default configuration creation"""

    def test_create_default_config_without_workspace(self):
        """Test creating default config without workspace path"""
        config = create_default_config()
        assert config["demetra_folder"] is None
        assert config["auto_download"] is True
        assert config["local_folder"] == "./eseas_output"
        assert config["csvlayout"] == "vtable"
        assert config["result_file_names"] == ["sa", "s", "cal"]

    def test_create_default_config_with_workspace(self, tmp_path):
        """Test creating default config with workspace path"""
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        config = create_default_config(str(workspace))
        assert config["demetra_folder"] == str(workspace.absolute())
        assert config["auto_download"] is True

    def test_default_config_has_all_required_keys(self):
        """Test that default config has all required keys"""
        config = create_default_config()
        required_keys = [
            "demetra_folder",
            "java_folder",
            "local_folder",
            "auto_download",
            "auto_approve",
            "csvlayout",
            "workspace_mode",
            "result_file_names",
            "verbose",
            "test",
            "replace_general_params",
            "replace_original_files",
            "file_name_explanation",
        ]
        for key in required_keys:
            assert key in config


class TestLoadSaveConfig:
    """Test configuration loading and saving"""

    def test_save_config(self, tmp_path):
        """Test saving configuration to file"""
        config_path = tmp_path / "test_config.yaml"
        config = create_default_config()

        save_config(config, config_path)

        assert config_path.exists()
        loaded = yaml.safe_load(config_path.read_text())
        assert loaded == config

    def test_load_config_existing(self, tmp_path):
        """Test loading existing configuration"""
        config_path = tmp_path / "test_config.yaml"
        test_config = {"key1": "value1", "key2": 123}

        with open(config_path, "w") as f:
            yaml.dump(test_config, f)

        loaded = load_config(config_path)
        assert loaded == test_config

    def test_load_config_nonexistent(self, tmp_path):
        """Test loading non-existent configuration"""
        config_path = tmp_path / "nonexistent.yaml"
        loaded = load_config(config_path)
        assert loaded == {}

    def test_load_config_invalid_yaml(self, tmp_path):
        """Test loading invalid YAML"""
        config_path = tmp_path / "invalid.yaml"
        config_path.write_text("invalid: yaml: content: [")

        with pytest.raises(SystemExit):
            load_config(config_path)

    def test_roundtrip_config(self, tmp_path):
        """Test save and load roundtrip"""
        config_path = tmp_path / "roundtrip.yaml"
        original_config = create_default_config("/test/workspace")

        save_config(original_config, config_path)
        loaded_config = load_config(config_path)

        assert loaded_config == original_config


class TestCmdValidate:
    """Test validate command"""

    def test_validate_existing_workspace(self, tmp_path):
        """Test validating an existing workspace with XML files"""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "test1.xml").touch()
        (workspace / "test2.xml").touch()

        args = MagicMock()
        args.workspace = str(workspace)

        # Should not raise exception
        cmd_validate(args)

    def test_validate_nonexistent_workspace(self, tmp_path):
        """Test validating non-existent workspace"""
        workspace = tmp_path / "nonexistent"

        args = MagicMock()
        args.workspace = str(workspace)

        with pytest.raises(SystemExit):
            cmd_validate(args)

    def test_validate_file_not_directory(self, tmp_path):
        """Test validating a file instead of directory"""
        not_a_dir = tmp_path / "file.txt"
        not_a_dir.touch()

        args = MagicMock()
        args.workspace = str(not_a_dir)

        with pytest.raises(SystemExit):
            cmd_validate(args)

    def test_validate_empty_workspace(self, tmp_path):
        """Test validating workspace with no XML files"""
        workspace = tmp_path / "empty"
        workspace.mkdir()

        args = MagicMock()
        args.workspace = str(workspace)

        # Should not raise, just warn
        cmd_validate(args)


class TestCmdDoctor:
    """Test doctor command"""

    @patch("subprocess.run")
    @patch("eseas.cli.main.get_config_path")
    def test_doctor_with_java(self, mock_get_config, mock_run, tmp_path):
        """Test doctor when Java is available"""
        # Mock Java check
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = 'java version "11.0.25"'
        mock_run.return_value = mock_result

        # Mock config path
        config_path = tmp_path / "eseas_config.yaml"
        config_path.touch()
        mock_get_config.return_value = config_path

        args = MagicMock()

        # Should not raise
        cmd_doctor(args)

    @patch("subprocess.run")
    def test_doctor_without_java(self, mock_run):
        """Test doctor when Java is not available"""
        mock_run.side_effect = FileNotFoundError()

        args = MagicMock()

        # Should not raise, just warn
        cmd_doctor(args)


class TestCmdLogs:
    """Test logs command"""

    def test_logs_no_directory(self, tmp_path):
        """Test logs when no logs directory exists"""
        # Change to temp directory
        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.type = None
            args.lines = None

            # Should not raise
            cmd_logs(args)
        finally:
            os.chdir(orig_cwd)

    def test_logs_success_type(self, tmp_path):
        """Test viewing success logs"""
        logs_dir = tmp_path / ".eseas" / ".logs"
        logs_dir.mkdir(parents=True)
        log_file = logs_dir / "last_good_run.log"
        log_file.write_text("Test log content\nLine 2\nLine 3")

        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.type = "success"
            args.lines = 10

            cmd_logs(args)
        finally:
            os.chdir(orig_cwd)

    def test_logs_error_type(self, tmp_path):
        """Test viewing error logs"""
        logs_dir = tmp_path / ".eseas" / ".logs"
        logs_dir.mkdir(parents=True)
        log_file = logs_dir / "failed_runs.log"
        log_file.write_text("Error log content")

        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.type = "error"
            args.lines = 50

            cmd_logs(args)
        finally:
            os.chdir(orig_cwd)

    def test_logs_list_all(self, tmp_path):
        """Test listing all log files"""
        logs_dir = tmp_path / ".eseas" / ".logs"
        logs_dir.mkdir(parents=True)
        (logs_dir / "last_good_run.log").write_text("success")
        (logs_dir / "failed_runs.log").write_text("errors")

        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.type = None
            args.lines = None

            cmd_logs(args)
        finally:
            os.chdir(orig_cwd)


class TestCmdConfig:
    """Test config command"""

    def test_config_show_no_file(self, tmp_path):
        """Test showing config when no file exists"""
        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.action = "show"
            args.config = None

            # Should not raise
            cmd_config(args)
        finally:
            os.chdir(orig_cwd)

    def test_config_show_existing(self, tmp_path):
        """Test showing existing config"""
        config_path = tmp_path / "eseas_config.yaml"
        config = create_default_config()
        save_config(config, config_path)

        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.action = "show"
            args.config = None

            cmd_config(args)
        finally:
            os.chdir(orig_cwd)

    def test_config_set_value(self, tmp_path):
        """Test setting a config value"""
        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.action = "set"
            args.key = "verbose"
            args.value = "true"
            args.config = None

            cmd_config(args)

            # Verify config was created and value set
            config_path = tmp_path / "eseas_config.yaml"
            assert config_path.exists()
            config = load_config(config_path)
            assert config["verbose"] is True
        finally:
            os.chdir(orig_cwd)

    def test_config_set_list_value(self, tmp_path):
        """Test setting a list value"""
        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.action = "set"
            args.key = "result_file_names"
            args.value = "sa,s,t,cal"
            args.config = None

            cmd_config(args)

            config_path = tmp_path / "eseas_config.yaml"
            config = load_config(config_path)
            assert config["result_file_names"] == ["sa", "s", "t", "cal"]
        finally:
            os.chdir(orig_cwd)

    def test_config_set_boolean_values(self, tmp_path):
        """Test setting boolean values with different representations"""
        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Test "true"
            args = MagicMock()
            args.action = "set"
            args.key = "verbose"
            args.value = "true"
            args.config = None
            cmd_config(args)

            config_path = tmp_path / "eseas_config.yaml"
            config = load_config(config_path)
            assert config["verbose"] is True

            # Test "false"
            args.value = "false"
            cmd_config(args)
            config = load_config(config_path)
            assert config["verbose"] is False

            # Test "yes"
            args.value = "yes"
            cmd_config(args)
            config = load_config(config_path)
            assert config["verbose"] is True

            # Test "no"
            args.value = "no"
            cmd_config(args)
            config = load_config(config_path)
            assert config["verbose"] is False
        finally:
            os.chdir(orig_cwd)

    def test_config_init_new(self, tmp_path):
        """Test initializing new config"""
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.action = "init"
            args.workspace = str(workspace)
            args.config = None
            args.force = False

            cmd_config(args)

            config_path = tmp_path / "eseas_config.yaml"
            assert config_path.exists()
            config = load_config(config_path)
            assert config["demetra_folder"] == str(workspace.absolute())
        finally:
            os.chdir(orig_cwd)

    def test_config_init_existing_no_force(self, tmp_path):
        """Test initializing when config exists without force"""
        config_path = tmp_path / "eseas_config.yaml"
        config_path.write_text("existing: config")

        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.action = "init"
            args.workspace = None
            args.config = None
            args.force = False

            # Should not overwrite
            cmd_config(args)

            content = config_path.read_text()
            assert "existing: config" in content
        finally:
            os.chdir(orig_cwd)

    def test_config_init_existing_with_force(self, tmp_path):
        """Test initializing when config exists with force"""
        config_path = tmp_path / "eseas_config.yaml"
        config_path.write_text("existing: config")

        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.action = "init"
            args.workspace = None
            args.config = None
            args.force = True

            cmd_config(args)

            # Should be overwritten
            config = load_config(config_path)
            assert "existing" not in config
            assert "demetra_folder" in config
        finally:
            os.chdir(orig_cwd)


class TestCmdRun:
    """Test run command"""

    @patch("eseas.Seasonal")
    @patch("eseas.Options")
    def test_run_first_time_with_workspace(self, mock_options, mock_seasonal, tmp_path):
        """Test first run with workspace path"""
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.workspace = str(workspace)
            args.demetra_folder = None
            args.config = None
            args.output = None
            args.verbose = None
            args.test = None
            args.csvlayout = None

            cmd_run(args)

            # Verify config was created
            config_path = tmp_path / "eseas_config.yaml"
            assert config_path.exists()

            # Verify Options and Seasonal were called
            mock_options.assert_called_once()
            mock_seasonal.assert_called_once()
            mock_seasonal.return_value.run.assert_called_once()
        finally:
            os.chdir(orig_cwd)

    @patch("eseas.Seasonal")
    @patch("eseas.Options")
    def test_run_with_existing_config(self, mock_options, mock_seasonal, tmp_path):
        """Test run with existing config file"""
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        config_path = tmp_path / "eseas_config.yaml"
        config = create_default_config(str(workspace))
        save_config(config, config_path)

        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.workspace = None
            args.demetra_folder = None
            args.config = None
            args.output = None
            args.verbose = None
            args.test = None
            args.csvlayout = None

            cmd_run(args)

            mock_options.assert_called_once()
            mock_seasonal.assert_called_once()
        finally:
            os.chdir(orig_cwd)

    def test_run_no_workspace_no_config(self, tmp_path):
        """Test run without workspace and without config"""
        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.workspace = None
            args.demetra_folder = None
            args.config = None
            args.output = None
            args.verbose = None
            args.test = None
            args.csvlayout = None

            with pytest.raises(SystemExit):
                cmd_run(args)
        finally:
            os.chdir(orig_cwd)

    @patch("eseas.Seasonal")
    @patch("eseas.Options")
    def test_run_with_overrides(self, mock_options, mock_seasonal, tmp_path):
        """Test run with command-line overrides"""
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        config_path = tmp_path / "eseas_config.yaml"
        config = create_default_config(str(workspace))
        save_config(config, config_path)

        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.workspace = None
            args.demetra_folder = None
            args.config = None
            args.output = "/custom/output"
            args.verbose = True
            args.test = True
            args.csvlayout = "list"

            cmd_run(args)

            # Verify Options was called with overrides
            call_kwargs = mock_options.call_args[1]
            assert call_kwargs["local_folder"] == "/custom/output"
            assert call_kwargs["verbose"] is True
            assert call_kwargs["test"] is True
            assert call_kwargs["csvlayout"] == "list"
        finally:
            os.chdir(orig_cwd)

    @patch("eseas.Seasonal")
    @patch("eseas.Options")
    def test_run_custom_config_file(self, mock_options, mock_seasonal, tmp_path):
        """Test run with custom config file"""
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        custom_config = tmp_path / "custom.yaml"
        config = create_default_config(str(workspace))
        save_config(config, custom_config)

        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.workspace = None
            args.demetra_folder = None
            args.config = str(custom_config)
            args.output = None
            args.verbose = None
            args.test = None
            args.csvlayout = None

            cmd_run(args)

            mock_options.assert_called_once()
            mock_seasonal.assert_called_once()
        finally:
            os.chdir(orig_cwd)

    def test_run_nonexistent_custom_config(self, tmp_path):
        """Test run with non-existent custom config file"""
        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.workspace = None
            args.demetra_folder = None
            args.config = "nonexistent.yaml"
            args.output = None
            args.verbose = None
            args.test = None
            args.csvlayout = None

            with pytest.raises(SystemExit):
                cmd_run(args)
        finally:
            os.chdir(orig_cwd)


class TestMainCLI:
    """Test main CLI entry point"""

    def test_main_no_args(self):
        """Test main with no arguments"""
        with patch("sys.argv", ["eseas"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    @patch("eseas.cli.main.cmd_doctor")
    def test_main_doctor_command(self, mock_cmd):
        """Test main with doctor command"""
        with patch("sys.argv", ["eseas", "doctor"]):
            main()
            mock_cmd.assert_called_once()

    @patch("eseas.cli.main.cmd_validate")
    def test_main_validate_command(self, mock_cmd):
        """Test main with validate command"""
        with patch("sys.argv", ["eseas", "validate", "/path/to/workspace"]):
            main()
            mock_cmd.assert_called_once()

    @patch("eseas.cli.main.cmd_config")
    def test_main_config_show_command(self, mock_cmd):
        """Test main with config show command"""
        with patch("sys.argv", ["eseas", "config", "show"]):
            main()
            mock_cmd.assert_called_once()

    def test_main_version_flag(self):
        """Test main with --version flag"""
        with patch("sys.argv", ["eseas", "--version"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    def test_main_version_short_flag(self):
        """Test main with -V flag"""
        with patch("sys.argv", ["eseas", "-V"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0


class TestConfigEdgeCases:
    """Test edge cases in configuration handling"""

    def test_config_with_special_characters(self, tmp_path):
        """Test config with special characters in paths"""
        workspace = tmp_path / "workspace with spaces"
        workspace.mkdir()

        config = create_default_config(str(workspace))
        config_path = tmp_path / "test.yaml"
        save_config(config, config_path)

        loaded = load_config(config_path)
        assert "with spaces" in loaded["demetra_folder"]

    def test_config_with_unicode(self, tmp_path):
        """Test config with unicode characters"""
        config = create_default_config()
        config["demetra_folder"] = "/path/with/ğüşıöç/chars"

        config_path = tmp_path / "unicode.yaml"
        save_config(config, config_path)

        loaded = load_config(config_path)
        assert "ğüşıöç" in loaded["demetra_folder"]

    def test_config_set_without_key_value(self, tmp_path):
        """Test config set without key or value"""
        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args = MagicMock()
            args.action = "set"
            args.key = None
            args.value = None
            args.config = None

            with pytest.raises(SystemExit):
                cmd_config(args)
        finally:
            os.chdir(orig_cwd)


class TestIntegration:
    """Integration tests for CLI workflows"""

    @patch("eseas.Seasonal")
    @patch("eseas.Options")
    def test_full_workflow_first_run_then_rerun(
        self, mock_options, mock_seasonal, tmp_path
    ):
        """Test complete workflow: first run, then subsequent run"""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "test.xml").touch()

        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # First run
            args1 = MagicMock()
            args1.workspace = str(workspace)
            args1.demetra_folder = None
            args1.config = None
            args1.output = None
            args1.verbose = None
            args1.test = None
            args1.csvlayout = None

            cmd_run(args1)

            # Verify config was created
            config_path = tmp_path / "eseas_config.yaml"
            assert config_path.exists()

            # Second run (no workspace arg)
            args2 = MagicMock()
            args2.workspace = None
            args2.demetra_folder = None
            args2.config = None
            args2.output = None
            args2.verbose = None
            args2.test = None
            args2.csvlayout = None

            cmd_run(args2)

            # Should have been called twice
            assert mock_seasonal.call_count == 2
        finally:
            os.chdir(orig_cwd)

    def test_validate_then_run_workflow(self, tmp_path):
        """Test workflow: validate workspace, then run"""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        (workspace / "test.xml").touch()

        # Validate
        args_validate = MagicMock()
        args_validate.workspace = str(workspace)
        cmd_validate(args_validate)  # Should not raise

        # Then config init
        import os

        orig_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            args_init = MagicMock()
            args_init.action = "init"
            args_init.workspace = str(workspace)
            args_init.config = None
            args_init.force = False

            cmd_config(args_init)

            config_path = tmp_path / "eseas_config.yaml"
            assert config_path.exists()
        finally:
            os.chdir(orig_cwd)
