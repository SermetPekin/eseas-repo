from pathlib import Path
from eseas.core._test_patcher import apply_test_patch

apply_test_patch(Path("eseas/data_for_testing/unix"))
apply_test_patch(Path("eseas/data_for_testing/win"))
