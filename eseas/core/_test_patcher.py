import pandas as pd
from io import StringIO
from urllib.parse import quote
from pathlib import Path
import re
from eseas.data_for_testing.csv_content import air_passenger

def apply_test_patch(base_dir: Path):
    if not base_dir.exists():
        return
    
    # JDemetra requires explicit XCLPRVDR URL encoded components. Using standard
    # quote doesn't encode forward slashes. Force encode slashes for the test XML file
    df = pd.read_csv(StringIO(air_passenger), sep=';')
    excel_path = base_dir / 'air4.xlsx'
    df.to_excel(excel_path, sheet_name="Sheet1", index=False)
    
    abs_path = str(excel_path.absolute())
    mac_url_part = quote(abs_path, safe="") # strict encoding!
    excel_url = f'file={mac_url_part}'
    
    for xml_path in base_dir.rglob("*.xml"):
        content = xml_path.read_text()
        if "file=" in content and "air4.xlsx" in content:
            new_content = re.sub(r'file=[a-zA-Z0-9%_\-\./]+xlsx', excel_url, content)
            xml_path.write_text(new_content)
