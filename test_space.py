from eseas.core.seasonal_options import set_options
from eseas.core.demetra import demetra_main
from pathlib import Path

set_options(
    demetra_folder=Path("test space folder/unix"),
    local_work_space=Path("/tmp/test space tmp")
)
demetra_main()
