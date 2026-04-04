import pandas as pd
from io import StringIO
from urllib.parse import quote
from pathlib import Path
import re
from eseas.data_for_testing.csv_content import air_passenger

def patch_all(base_dir):
    df = pd.read_csv(StringIO(air_passenger), sep=';')
    excel_path = base_dir / 'air4.xlsx'
    
    # We DO NOT parse dates, we just write it exactly as it came from CSV
    df.to_excel(excel_path, sheet_name="Sheet1", index=False)
    
    excel_url = f'file={quote(str(excel_path.absolute()), safe="")}'
    
    for xml_path in base_dir.rglob("*.xml"):
        content = xml_path.read_text()
        if "file=" in content and "air4.xlsx" in content:
            new_content = re.sub(r'file=[a-zA-Z0-9%_\-\./]+xlsx', excel_url, content)
            xml_path.write_text(new_content)

patch_all(Path("eseas/data_for_testing/unix"))
