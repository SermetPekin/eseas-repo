from eseas import Seasonal, Options

def main():
    """
    Example 5: Auto-Downloading to a Specific Custom Path
    
    By default, setting `auto_download=True` without a `java_folder` downloads
    the cruncher to a hidden `.eseas` folder in your user's home directory.
    
    However, if you provide a `java_folder` AND `auto_download=True`, 
    eseas will download and extract the cruncher precisely into that target path.
    
    IMPORTANT: If eseas detects that the jwsacruncher binaries are already 
    present in this folder from an earlier run, it will SKIP the download 
    and proceed straight to the seasonal adjustment! This makes it perfectly 
    safe and efficient to leave `auto_download=True` in your scripts without 
    re-downloading a 30MB file every time you run it.
    """
    options = Options(
        demetra_source_folder=r"C:\Data\demetra_source_folder",
        local_folder=r"C:\Data\test_out",
        
        # Target destination for the automatic download:
        java_folder=r"C:\Tools\JDemetra_Cruncher", 
        
        result_file_names=("sa", "s_f", "cal"),
        workspace_mode=True,
        auto_download=True,   # Will download TO the java_folder above (if not already there)
        auto_approve=True
    )

    # Initialize and execute the seasonal adjustment process synchronously
    seas = Seasonal(options)
    seas.run()

if __name__ == "__main__":
    main()
