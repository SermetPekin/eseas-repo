from eseas import refresh, Path
from eseas.tests.test_utils import skip_if_unix

ROOT = Path(r"./excel_files")

@skip_if_unix
def test_refresh():
    if not ROOT.exists():
        return
    files = ["test.xlsx"]

    refresh(files, ROOT)
