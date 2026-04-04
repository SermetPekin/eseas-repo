import json
import logging
from pathlib import Path
from datetime import datetime
import traceback

def setup_eseas_logger():
    cwd = Path.cwd()
    eseas_dir = cwd / ".eseas"
    logs_dir = eseas_dir / ".logs"
    
    # Create the necessary directories
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Dump a helpful example script to guide users if it doesn't already exist
    example_script = eseas_dir / "quick_start_example.py"
    if not example_script.exists():
        example_content = r"""# Auto-generated Quick Start Example for eseas
from eseas import Options, Seasonal

def main():
    # Example utilizing auto_download for a completely smooth setup 
    options = Options(
        demetra_source_folder=r"C:\Data\your_demetra_xmls",
        local_folder=r"C:\Data\eseas_outputs", 
        auto_download=True,
        auto_approve=False
    )
    
    seas = Seasonal(options)
    seas.run()

if __name__ == "__main__":
    main()
"""
        try:
            example_script.write_text(example_content, encoding='utf-8')
        except Exception:
            pass

    # Dump a README for the .eseas directory explicitly
    readme_file = eseas_dir / "README.txt"
    if not readme_file.exists():
        readme_content = """This .eseas directory is automatically generated.
It contains diagnostic logs in the .logs/ folder (e.g. failed_runs.log) to help you troubleshoot any crashes.
A quick_start_example.py has also been provided for your convenience.
"""
        try:
            readme_file.write_text(readme_content, encoding='utf-8')
        except Exception:
            pass
            
    # Set up the logger
    logger = logging.getLogger("eseas_error_logger")
    if not logger.handlers:
        logger.setLevel(logging.ERROR)
        
        log_file = logs_dir / "failed_runs.log"
        handler = logging.FileHandler(log_file, encoding='utf-8')
        handler.setLevel(logging.ERROR)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        
    return logger

def log_eseas_error(error_msg: str, options=None):
    try:
        import importlib.metadata
        eseas_version = importlib.metadata.version('eseas')
    except Exception:
        eseas_version = "Unknown"
        
    logger = setup_eseas_logger()
    
    options_dict = {}
    if options:
        try:
            if hasattr(options, "__dict__"):
                for k, v in options.__dict__.items():
                    options_dict[k] = str(v)
            else:
                options_dict = {"repr": repr(options)}
        except Exception:
            options_dict = {"repr": "Could not parse options."}
            
    log_data = {
        "eseas_version": eseas_version,
        "error": str(error_msg),
        "options": options_dict
    }
    
    logger.error(json.dumps(log_data, indent=2))

