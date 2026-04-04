import re

fname = "eseas/core/error_logger.py"
content = open(fname).read()

new_get_paths = """def get_paths_info():
    paths = {}
    try:
        from .cruncher_classes import get_cruncher
        from .create_bat_command import get_demetra_type
        
        cruncher = get_cruncher()
        ws = cruncher.local_work_space
        paths["local_workspace"] = str(ws)
        paths["demetra_folder"] = str(cruncher.demetra_folder)
        paths["cruncher_folder"] = str(cruncher.crunch_folder)
        paths["general_params"] = str(Path(ws) / "general.params")
        try:
            paths["execution_script"] = str(get_demetra_type().demetra_command_file_name())
        except Exception:
            paths["execution_script"] = "Could not resolve"
            
        # check script content
        try:
            exec_path = Path(paths["execution_script"])
            if exec_path.exists():
                paths["script_content"] = exec_path.read_text(encoding="utf-8")
        except Exception:
            pass
            
    except Exception as e:
        paths["error"] = f"Could not resolve workspace paths: {e}"
        
    return paths
"""

content = re.sub(r'def get_paths_info\(\):.*?return paths\n', new_get_paths, content, flags=re.DOTALL)
open(fname, 'w').write(content)
