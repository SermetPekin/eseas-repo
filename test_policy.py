from eseas import Seasonal, Options
from pathlib import Path
import shutil
import eseas.core._general_params as gp

java_folder = "jwsacruncher/jwsacruncher-2.2.6/bin"
demetra_folder = "eseas/data_for_testing/unix"

temp_dir = Path("/tmp/temp_output_debug3")
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
    auto_approve=True,
    result_file_names=("sa", "s", "cal"),
    workspace_mode=True,
    java_bin=None,
)

_orig = gp.get_general_params
def get_gen_p():
    return _orig().replace('<refreshall>true</refreshall>', '<refreshall>false</refreshall>')
gp.get_general_params = get_gen_p
from eseas.core.create_bat_command import create_general_params

m = Seasonal(options)
m.run()
