import urllib.request
import zipfile
import time
from pathlib import Path

CRUNCHER_VERSION = "2.2.5"
CRUNCHER_URL = f"https://github.com/jdemetra/jwsacruncher/releases/download/v{CRUNCHER_VERSION}/jwsacruncher-{CRUNCHER_VERSION}-bin.zip"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def download_jwsacruncher(target_dir: str | Path) -> Path:
    """
    Download and extract jwsacruncher to the specified directory.
    Returns the path to the extracted 'bin' folder.
    """
    target_dir = Path(target_dir)
    # The actual bin path after extraction will be target_dir/jwsacruncher-{CRUNCHER_VERSION}/bin
    expected_bin_path = target_dir / f"jwsacruncher-{CRUNCHER_VERSION}" / "bin"
    
    if expected_bin_path.exists() and expected_bin_path.is_dir():
        print(f"jwsacruncher already available at {expected_bin_path}")
        return expected_bin_path

    print(f"\nDownloading jwsacruncher {CRUNCHER_VERSION} to {target_dir}...")
    target_dir.mkdir(parents=True, exist_ok=True)
    zip_file = target_dir / f"jwsacruncher-{CRUNCHER_VERSION}-bin.zip"

    for attempt in range(MAX_RETRIES):
        try:
            print(f"Download attempt {attempt + 1}/{MAX_RETRIES}...")
            
            # Custom request with User-Agent
            req = urllib.request.Request(
                CRUNCHER_URL,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                with open(zip_file, 'wb') as out_file:
                    out_file.write(response.read())
            
            print(f"Downloaded to {zip_file}")
            print(f"Extracting to {target_dir}...")
            
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(target_dir)

            zip_file.unlink()  # Remove zip file after extraction
            
            # Make the unix script executable
            import os
            import stat
            unix_cruncher = expected_bin_path / "jwsacruncher"
            if unix_cruncher.exists():
                st = os.stat(unix_cruncher)
                os.chmod(unix_cruncher, st.st_mode | stat.S_IEXEC)
                
            print(f"jwsacruncher extracted successfully. Bin path: {expected_bin_path}")
            return expected_bin_path

        except Exception as e:
            print(f"Download attempt {attempt + 1} failed: {e}")
            if zip_file.exists():
                try:
                    zip_file.unlink()
                except Exception:
                    pass
            
            if attempt < MAX_RETRIES - 1:
                print(f"Waiting {RETRY_DELAY} seconds before retry...")
                time.sleep(RETRY_DELAY)
            else:
                raise RuntimeError(f"Failed to download jwsacruncher after {MAX_RETRIES} attempts.")
