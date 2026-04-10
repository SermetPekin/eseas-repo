from unittest.mock import patch
from eseas.core.seasonal_options import SeasonalOptions as Options
from eseas.core.seasonal_general import SeasonalADV as Seasonal


def test_auto_download_enabled(tmp_path):
    """Test if auto_download=True properly invokes the download function."""
    with patch("eseas.core.download_tools.download_jwsacruncher") as mock_download:
        with patch("eseas.core.cruncher_classes.check_cruncher", return_value=True):
            fake_bin_path = tmp_path / "mock_bin"
            mock_download.return_value = fake_bin_path

            opts = Options(
                demetra_folder="fake_source",
                java_folder=str(tmp_path),
                local_folder="fake_local",
                auto_download=True,
            )

            # Verify the downloader was called
            mock_download.assert_called_once()

            # Verify the options java_folder has been updated with the result
            assert str(opts.java_folder) == str(fake_bin_path)


def test_auto_download_disabled(tmp_path):
    """Test if auto_download=False skips the download function."""
    with patch("eseas.core.download_tools.download_jwsacruncher") as mock_download:
        with patch("eseas.core.cruncher_classes.check_cruncher", return_value=True):
            opts = Options(
                demetra_folder="fake_source",
                java_folder=str(tmp_path),
                local_folder="fake_local",
                auto_download=False,
            )

            # Verify the downloader was NOT called
            mock_download.assert_not_called()
            assert str(opts.java_folder) == str(tmp_path)




def test_seasonal_options_pydantic_defaults():
    """Test that Pydantic properly assigns the default values."""
    from eseas.core.seasonal_options import SeasonalOptions as Options
    
    with patch("eseas.core.cruncher_classes.check_cruncher", return_value=True):
        opts = Options()
        assert opts.csvlayout == "Vtable"
        assert opts.workspace_mode is True
        assert opts.test is False
        assert opts.auto_approve is False
        assert opts.result_file_names == ("sa", "s", "cal")

def test_seasonal_options_pydantic_type_conversion():
    """Test that Pydantic properly converts compatible types like strings 'yes'/'no' or ints 1/0 to bool."""
    from eseas.core.seasonal_options import SeasonalOptions as Options
    
    with patch("eseas.core.cruncher_classes.check_cruncher", return_value=True):
        # 1 -> True, "yes" -> True, 0 -> False
        opts = Options(test=1, verbose="yes", replace_original_files=0)
        assert opts.test is True
        assert opts.verbose is True
        assert opts.replace_original_files is False

def test_seasonal_options_pydantic_validation_error():
    """Test that Pydantic rejects completely incompatible types with a ValidationError."""
    import pydantic
    import pytest
    from eseas.core.seasonal_options import SeasonalOptions as Options
    
    with pytest.raises(pydantic.ValidationError):
        # "not a bool string" cannot be parsed into a boolean
        Options(test="not a bool string")

def test_seasonal_options_positional_args():
    """Test that the first 3 positional arguments are successfully mapped to demetra, java, and local folders."""
    from eseas.core.seasonal_options import SeasonalOptions as Options
    
    with patch("eseas.core.cruncher_classes.check_cruncher", return_value=True):
        opts = Options("mock_demetra", "mock_java", "mock_local")
        
        assert "mock_demetra" in opts.demetra_folder
        assert "mock_java" in opts.java_folder
        assert "mock_local" in opts.local_folder
