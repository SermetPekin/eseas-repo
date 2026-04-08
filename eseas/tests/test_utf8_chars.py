import pytest
from pathlib import Path
import shutil
from eseas import Seasonal, Options
from eseas.tests.test_utils import skip_if_no_cruncher


@skip_if_no_cruncher
def test_turkish_characters_in_workspace_name(tmp_path):
    """
    Tests that a Demetra workspace containing Turkish/special characters
    in its name is successfully run by copying it to the safe encoded_name
    intermediate folder, and that results are properly collected.
    """
    from eseas.core.seas_testing_utils import get_testing_utils

    testing_utils = get_testing_utils()

    java_folder = testing_utils.java_folder
    unix_test_data = Path(testing_utils.demetra_folder)

    # Create a mock source folder with Turkish and French chars
    turkish_source = tmp_path / "Élément_Mevsimsel_Değerler_ÜĞŞÇÖı_çàé"
    turkish_source.mkdir()

    # Copy the 'airpassengers' structure into it but rename to a mix of UTF-8 chars
    orig_xml = unix_test_data / "airpassengers.xml"
    orig_dir = unix_test_data / "airpassengers"

    new_basename = "données_françaises_123_şçğ_çàé"

    target_xml = turkish_source / f"{new_basename}.xml"
    target_dir = turkish_source / new_basename

    shutil.copy(orig_xml, target_xml)
    shutil.copytree(orig_dir, target_dir)

    # Modify the generic workspace XML's "name" attribute just in case JDemetra cares
    content = target_xml.read_text()
    content = content.replace('name="airpassengers"', f'name="{new_basename}"')
    target_xml.write_text(content)

    # Output directory
    local_output = tmp_path / "eseas_output_utf8"

    options = Options(
        demetra_folder=str(turkish_source),
        java_folder=java_folder,
        local_folder=str(local_output),
        test=False,
        verbose=True,
        replace_original_files=False,
        auto_approve=True,
        result_file_names=("sa", "ycal"),
        workspace_mode=True,
    )

    m = Seasonal(options)
    m.run()

    # Check if the output was successfully generated and collected
    sa_files = list(local_output.rglob("series_sa.csv"))

    assert (
        len(sa_files) > 0
    ), "No series_sa.csv generated for Turkish named workspace! 'encoded_name' fallback might be broken."
    assert any(
        f.stat().st_size > 10 for f in sa_files
    ), "Output files are 0 bytes! Crunching failed silently."

    # Check if the final excel file was successfully collected into output folder
    excel_files = list(local_output.rglob("*.xlsx"))
    assert (
        len(excel_files) > 0
    ), "No combined Excel files were collected from the cruncher output!"

@skip_if_no_cruncher
def test_french_characters_in_workspace_name(tmp_path):
    """
    Tests that a Demetra workspace containing strictly French special characters
    in its name is successfully run by the cruncher safely routing encoding paths.
    """
    from eseas.core.seas_testing_utils import get_testing_utils

    testing_utils = get_testing_utils()

    java_folder = testing_utils.java_folder
    unix_test_data = Path(testing_utils.demetra_folder)

    # Create a mock source folder with French accents (é, è, ç, à, etc.)
    french_source = tmp_path / "Modèle_Prévision_Saisonnière_123_çàé"
    french_source.mkdir()

    orig_xml = unix_test_data / "airpassengers.xml"
    orig_dir = unix_test_data / "airpassengers"

    new_basename = "série_temporelle_données_très_bientôt_123"

    target_xml = french_source / f"{new_basename}.xml"
    target_dir = french_source / new_basename

    shutil.copy(orig_xml, target_xml)
    shutil.copytree(orig_dir, target_dir)

    content = target_xml.read_text()
    content = content.replace('name="airpassengers"', f'name="{new_basename}"')
    target_xml.write_text(content)

    local_output = tmp_path / "eseas_output_french"

    options = Options(
        demetra_folder=str(french_source),
        java_folder=java_folder,
        local_folder=str(local_output),
        test=False,
        verbose=True,
        replace_original_files=False,
        auto_approve=True,
    )

    m = Seasonal(options)
    m.run()

    sa_files = list(local_output.rglob("series_sa.csv"))

    assert (
        len(sa_files) > 0
    ), "No series_sa.csv generated for French named workspace! 'encoded_name' fallback might be broken."
    assert any(
        f.stat().st_size > 10 for f in sa_files
    ), "Output files are 0 bytes! Crunching failed silently due to encoding issues."

    excel_files = list(local_output.rglob("*.xlsx"))
    assert (
        len(excel_files) > 0
    ), "No combined Excel files were collected from the cruncher output!"
