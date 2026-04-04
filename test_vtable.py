from eseas import Seasonal, Options
from pathlib import Path
import shutil

java_folder = "jwsacruncher/jwsacruncher-2.2.6/bin"
demetra_folder = "eseas/data_for_testing/unix"

temp_dir = Path("/tmp/temp_output_debug")
if temp_dir.exists():
    shutil.rmtree(temp_dir)
temp_dir.mkdir()

options = Options(
    demetra_folder,
    java_folder,
    local_folder=str(temp_dir),
    test=False,
    verbose=True,
    replace_original_files=False,
    auto_approve=True,  # SKIP PROMPT
    result_file_names=("sa", "s", "cal"),
    workspace_mode=True,
    java_bin=None,
)

m = Seasonal(options)
m.run()
