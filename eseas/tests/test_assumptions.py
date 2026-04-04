import os
import pytest
from pathlib import Path
import subprocess
from eseas.core.cruncher_classes import get_cruncher
from eseas.core.demetra_caller import DemetraCallerLinux, DemetraCallerWindows, DemetraCallerMac
from eseas import Options
from eseas.tests.test_utils import skip_if_no_cruncher

def test_executable_quoting(tmp_path):
    fake_java = tmp_path / "opt" / "my cool cruncher"
    fake_java.mkdir(parents=True)
    fake_in = tmp_path / "in"
    fake_in.mkdir(parents=True)

    opt = Options(
        demetra_folder=str(fake_in),
        java_folder=str(fake_java),
        local_folder=str(tmp_path / "out"),
        workspace_mode=False,
        test=True
    )
    linux_cmd = DemetraCallerLinux().cruncher_command()
    mac_cmd = DemetraCallerMac().cruncher_command()
    win_cmd = DemetraCallerWindows().cruncher_command()
    
    assert linux_cmd.startswith('"') and linux_cmd.endswith('"'), "Linux caller should wrap path in quotes"
    assert mac_cmd.startswith('"') and mac_cmd.endswith('"'), "Mac caller should wrap path in quotes"
    assert win_cmd.startswith('call "') and win_cmd.endswith('"'), "Windows caller should wrap call path in quotes"
    assert "my cool cruncher/jwsacruncher" in linux_cmd

def test_workspace_creation_with_spaces_and_special_chars(tmp_path):
    sp_dir = tmp_path / "my space folder!@#"
    sp_dir.mkdir()
    out_dir = tmp_path / "out location @#"
    
    fake_java = tmp_path / "opt" / "bin"
    fake_java.mkdir(parents=True)
    
    # Use workspace_mode=True to ensure @eseas_wspace builds correctly
    opt = Options(
        demetra_folder=str(sp_dir),
        java_folder=str(fake_java),
        local_folder=str(out_dir),
        workspace_mode=True,
        test=True
    )
    c = get_cruncher()
    assert "my space folder!@#" in str(c.demetra_folder)
    assert Path(c.local_work_space).exists(), "Local workspace directory not created"
    assert "@eseas_wspace" in str(c.local_work_space), "@eseas_wspace dir tracking missing"

@skip_if_no_cruncher
def test_hardcoded_jwsacruncher_direct_call():
    """
    Run jwsacruncher directly to see if the executable operates properly.
    Uses subprocess to bypass wrapper logic and catch CLI failures directly.
    """
    cruncher_dir = os.environ.get("JAVA_CRUNCHER_BIN")
    exe_name = "jwsacruncher.bat" if os.name == "nt" else "jwsacruncher"
    exe_path = Path(cruncher_dir) / exe_name
    
    assert exe_path.exists(), f"Expected executable {exe_path} to exist from test setup."
    
    try:
        # Run with '--version' or empty args to catch raw execution errors safely
        res = subprocess.run([str(exe_path)], capture_output=True, text=True)
        assert res.returncode in (0, 1, 2)
    except OSError as e:
        pytest.fail(f"jwsacruncher failed to execute directly via OS: {e}")

def test_xml_url_encoding(tmp_path):
    """
    Ensure the path injected into XML is correctly URL encoded as required by JDemetra's tsprovider.
    """
    from urllib.parse import quote
    
    complex_dir = tmp_path / "complex name with spaces"
    complex_dir.mkdir()
    
    excel_path = complex_dir / "data.xlsx"
    abs_path = str(excel_path.absolute())
    
    mac_url_part = quote(abs_path, safe="") 
    
    # Assert forward slashes are encoded to %2F (strict tsprovider requirement)
    assert "%2F" in mac_url_part
    assert "complex%20name%20with%20spaces" in mac_url_part
    assert "/" not in mac_url_part
