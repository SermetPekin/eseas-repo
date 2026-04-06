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


@patch("eseas.core.seasonal_general.get_input_from_user")
@patch("eseas.core.seasonal_general.SeasonalADV.part2")
@patch("eseas.core.seasonal_general.run_bat_commands")
@patch("eseas.core.seasonal_general.get_demetra_files")
@patch("eseas.core.seasonal_general.write_bat_file_demetra")
def test_auto_approve_true(
    mock_write_bat,
    mock_get_demetra,
    mock_run_bat_commands,
    mock_part2,
    mock_get_input,
    tmp_path,
):
    """Test if auto_approve bypasses the get_input_from_user prompt."""
    with patch("eseas.core.cruncher_classes.check_cruncher", return_value=True):
        opts = Options(
            demetra_folder="fake_source",
            java_folder=str(tmp_path),
            local_folder="fake_local",
            auto_approve=True,
        )

        m = Seasonal(opts)

        try:
            m.part1()
        except Exception:
            pass

        mock_get_input.assert_not_called()


@patch("eseas.core.seasonal_general.get_input_from_user")
@patch("eseas.core.seasonal_general.SeasonalADV.part2")
@patch("eseas.core.seasonal_general.run_bat_commands")
@patch("eseas.core.seasonal_general.get_demetra_files")
@patch("eseas.core.seasonal_general.write_bat_file_demetra")
def test_auto_approve_false(
    mock_write_bat,
    mock_get_demetra,
    mock_run_bat_commands,
    mock_part2,
    mock_get_input,
    tmp_path,
):
    """Test if auto_approve=False correctly calls the get_input_from_user prompt."""
    with patch("eseas.core.cruncher_classes.check_cruncher", return_value=True):
        opts = Options(
            demetra_folder="fake_source",
            java_folder=str(tmp_path),
            local_folder="fake_local",
            auto_approve=False,
        )

        mock_get_input.return_value = True  # Simulate user pressing "Y"
        mock_get_demetra.return_value = []
        m = Seasonal(opts)

        try:
            m.part1()
        except Exception as e:
            print(f"Exception happened: {e}")

        mock_get_input.assert_called_once()
