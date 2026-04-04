import pandas as pd
from io import StringIO
from urllib.parse import quote
from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET
from eseas.data_for_testing.csv_content import air_passenger


def _fix_xlsx_shared_strings(xlsx_path: Path) -> None:
    """
    openpyxl 3.1+ writes strings as inlineStr cells, omitting sharedStrings.xml.
    JDemetra+'s XCLPRVDR parser requires sharedStrings.xml to be present.
    This function converts inline strings to a proper shared strings table in-place.
    """
    import io

    with zipfile.ZipFile(xlsx_path, 'r') as zin:
        names = zin.namelist()
        files = {name: zin.read(name) for name in names}

    sheet_xml = files.get('xl/worksheets/sheet1.xml', b'')
    tree = ET.fromstring(sheet_xml)
    ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'

    strings: list[str] = []
    index_map: dict[str, int] = {}

    def intern_string(value: str) -> int:
        if value not in index_map:
            index_map[value] = len(strings)
            strings.append(value)
        return index_map[value]

    # Convert inlineStr cells to shared-string references
    for c in tree.iter(f'{{{ns}}}c'):
        if c.attrib.get('t') == 'inlineStr':
            is_elem = c.find(f'{{{ns}}}is')
            t_elem = is_elem.find(f'{{{ns}}}t') if is_elem is not None else None
            value = t_elem.text if t_elem is not None else ''
            idx = intern_string(value or '')
            c.attrib['t'] = 's'
            for child in list(c):
                c.remove(child)
            v_elem = ET.SubElement(c, f'{{{ns}}}v')
            v_elem.text = str(idx)

    if not strings:
        return  # nothing to do

    # Rebuild the sheet XML bytes
    files['xl/worksheets/sheet1.xml'] = ET.tostring(tree, encoding='unicode', xml_declaration=False).encode('utf-8')

    # Build sharedStrings.xml
    ss_root = ET.Element('sst')
    ss_root.attrib['xmlns'] = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    ss_root.attrib['count'] = str(len(strings))
    ss_root.attrib['uniqueCount'] = str(len(strings))
    for s in strings:
        si = ET.SubElement(ss_root, 'si')
        t = ET.SubElement(si, 't')
        t.text = s
    ss_xml = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + ET.tostring(ss_root, encoding='unicode').encode('utf-8')
    files['xl/sharedStrings.xml'] = ss_xml

    # Update [Content_Types].xml to register sharedStrings
    ct_xml = files['[Content_Types].xml'].decode('utf-8')
    if 'sharedStrings' not in ct_xml:
        ct_xml = ct_xml.replace(
            '</Types>',
            '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>'
        )
        files['[Content_Types].xml'] = ct_xml.encode('utf-8')

    # Update xl/_rels/workbook.xml.rels:
    #  1. Convert absolute targets like "/xl/foo" → "foo" (relative to xl/ base)
    #     JDemetra's xlsx reader prepends "xl/" to every target, so absolute paths
    #     like "/xl/worksheets/sheet1.xml" would become "xl//xl/worksheets/sheet1.xml".
    #  2. Add the sharedStrings relationship.
    rels_xml = files['xl/_rels/workbook.xml.rels'].decode('utf-8')
    rels_xml = re.sub(r'Target="/xl/', 'Target="', rels_xml)
    if 'sharedStrings' not in rels_xml:
        rels_xml = rels_xml.replace(
            '</Relationships>',
            '<Relationship Id="rIdSS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/></Relationships>'
        )
    files['xl/_rels/workbook.xml.rels'] = rels_xml.encode('utf-8')

    # Write back
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)
    xlsx_path.write_bytes(buf.getvalue())


def apply_test_patch(base_dir: Path):
    if not base_dir.exists():
        return
    
    # JDemetra requires explicit XCLPRVDR URL encoded components. Using standard
    # quote doesn't encode forward slashes. Force encode slashes for the test XML file
    df = pd.read_csv(StringIO(air_passenger), sep=';')
    excel_path = base_dir / 'air4.xlsx'
    df.to_excel(excel_path, sheet_name="Sheet1", index=False)
    _fix_xlsx_shared_strings(excel_path)
    
    abs_path = str(excel_path.absolute())
    mac_url_part = quote(abs_path, safe="") # strict encoding!
    excel_url = f'file={mac_url_part}'
    
    for xml_path in base_dir.rglob("*.xml"):
        content = xml_path.read_text()
        if "file=" in content and "air4.xlsx" in content:
            new_content = re.sub(r'file=[a-zA-Z0-9%_\-\./]+xlsx', excel_url, content)
            xml_path.write_text(new_content)
