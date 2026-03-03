from eseas import refresh, Path

ROOT = Path(r"./excel_files")


def test_refresh():
    if not ROOT.exists():
        return
    files = ["test.xlsx"]

    refresh(files, ROOT)
