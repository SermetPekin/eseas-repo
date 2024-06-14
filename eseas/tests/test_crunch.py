from eseas.core.seas_utils import search_demetra_folder
from eseas.core.seas_utils import filter_xml
from eseas.core.seas_utils import filter_xml_demetra
from .test_utils import skip_if_github


@skip_if_github
def test_search_demetra_folder(capsys):
    with capsys.disabled():

        fold = "unix"
        demetra_folder = rf"./eseas/data_for_testing/{fold}"
        fs = search_demetra_folder(demetra_folder, None)
        assert fs
        fs2 = search_demetra_folder(demetra_folder, filter_xml)
        fs3 = filter_xml_demetra(fs2)
        print(fs3)
        assert len(fs3) == 1
