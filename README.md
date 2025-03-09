

[![PyPI](https://img.shields.io/pypi/v/eseas)](https://img.shields.io/pypi/v/eseas) 
![t](https://img.shields.io/badge/status-maintained-yellow.svg) [![](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) 
[![Windows](https://github.com/SermetPekin/eseas-repo/actions/workflows/latest_cr_version_win.yml/badge.svg?1)](https://github.com/SermetPekin/eseas-repo/actions/workflows/latest_cr_version_win.yml?1)
[![Ubuntu / Mac ](https://github.com/SermetPekin/eseas-repo/actions/workflows/latest_cr_version.yml/badge.svg?2)](https://github.com/SermetPekin/eseas-repo/actions/workflows/latest_cr_version.yml?2)

[![Downloads](https://static.pepy.tech/badge/eseas)](https://pepy.tech/project/eseas) [![Downloads](https://static.pepy.tech/badge/eseas/month)](https://pepy.tech/project/eseas) [![Downloads](https://pepy.tech/badge/eseas/week)](https://pepy.tech/project/eseas)


 



# eseas

eseas is a Python package that acts as a wrapper for the `jwsacruncher` Java package. This tool allows users to process Demetra workspace XML files, create batch files, execute them, and collect the desired outputs into individual Excel files.

## Installation

### eseas

You can install the `eseas` package via pip:

```bash
pip install eseas -U
```

 
## Prerequisites

### jwsacruncher

`eseas` requires the `jwsacruncher` Java package. You can download it
from the [jwsacruncher GitHub releases page](https://github.com/jdemetra/jwsacruncher/releases).

### Setup Instructions

1. Download the latest release of `jwsacruncher` from the [releases page](https://github.com/jdemetra/jwsacruncher/releases).
2. Unzip the downloaded file.
3. Note the path to the `bin` directory inside the unzipped folder.

After downloading `jwsacruncher`, you need to specify its location when using the `Options` function from the `eseas` package.

## Usage

Here's an example of how to use the `eseas` package:

```python


    from eseas import Seasonal, Options
    import time

    def main():
        # Specify the path to the jwsacruncher bin directory
        java_folder = r'../../Downloads/jwsacruncher-2.2.4/bin' 

        # [Optional] Java binary folder (where the Java executable exists)
        # This will be added to the environment PATH variable if provided.
        java_bin = r'/usr/bin'

        # Folder containing Demetra XML files
        demetra_source_folder = r"./demetra_source_folder"

        # Workspace where output files will be stored
        local_folder = r"./test_out"

        options = Options(
            demetra_source_folder,
            java_folder,
            local_folder,
            result_file_names=("sa", "s_f", "cal"),  # See "Demetra Components" below
            workspace_mode=True,
            file_name_explanation=True,
            java_bin=java_bin
        )

        # Initialize the Seasonal process
        seas = Seasonal(options)

        # Execute the two-step process
        seas.part1()
        time.sleep(10)  # Wait before executing part2
        seas.part2()

    if __name__ == "__main__":
        main()


```

### Defining some parameters from .env file  (NEW in version 1.0.0 )

You can define key parameters in an `.env` file located in the current directory where you run the script.

The function first checks whether the parameters are explicitly provided.
If a parameter is not given in the function, it will automatically use the value from the `.env` file.


```plaintext
# `.env` file content (Example)

# Required if not given from function
java_folder = /Users/guest/app/jwsacruncher-2.2.6/bin
demetra_source_folder = ./eseas/data_for_testing/unix
local_folder = ./test_out

#Optional
java_bin = /usr/bin
```

### Usage: Running the Script When a `.env` File Exists

```python
from eseas import Seasonal, Options
import time

# Load options from the `.env` file
options = Options()

# Initialize and execute the seasonal adjustment process
m = Seasonal(options)
m.part1()
time.sleep(10)  # Pause before running part2
m.part2()


```
### Usage: Overwriting demetra_folder from Function Call When `.env` File Exists
If a .env file is present, you can override the demetra_folder value by passing it directly in the function call.
```python
from eseas import Seasonal, Options
import time

# Override `demetra_folder` from function call, ignoring the value in `.env`
options = Options(demetra_folder="SomeDemetraFolder")

# Initialize and execute the seasonal adjustment process
m = Seasonal(options)
m.part1()
time.sleep(10)  # Pause before running part2
m.part2()


```


## Documentation

For more detailed information, refer to the following guides:

[Documentation](https://eseas-repo.readthedocs.io/en/latest/home.html)

## How it Works

1. **Input Directory**: The user specifies the directory of the Demetra workspace where XML files are located.
2. **Batch File Creation**: The package creates batch files for all XML files in the specified directory.
3. **Execution**: It runs the batch files using the `jwsacruncher` tool.
4. **Output Collection**: The specified outputs are collected and compiled into individual Excel files for each XML file processed.



## Acknowledgments
This package (**eseas**) is an **independent Python wrapper** that interacts with the `jwsacruncher` application.  
Users must **download `jwsacruncher` separately**. This package is **not affiliated with or derived from `jwsacruncher`**.

`jwsacruncher` is a **Java-based implementation** of the .NET application **WSACruncher**. It is a command-line tool that allows users to **re-estimate all multi-processing tasks** defined in a **Demetra workspace**.  

The workspace can be generated by:
- **Demetra+ (.NET)**
- **JDemetra+ (Java)**
- **Any compatible user tool**


For more information, visit the [`jwsacruncher` GitHub repository](https://github.com/jdemetra/jwsacruncher).



## License

This project is licensed under the EUPL-1.2 License - see the [LICENSE](https://github.com/SermetPekin/eseas-repo/LICENSE) file for details.
