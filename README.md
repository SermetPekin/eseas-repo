[![Python package](https://github.com/SermetPekin/eseas-repo/actions/workflows/python-package.yml/badge.svg?branch=main&1)](https://github.com/SermetPekin/eseas-repo/actions/workflows/python-package.yml)


[![PyPI](https://img.shields.io/pypi/v/eseas?1)](https://img.shields.io/pypi/v/eseas?1)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/eseas)](https://pypi.org/project/eseas/)
[![Downloads](https://static.pepy.tech/badge/eseas?1)](https://pepy.tech/project/eseas?1)
[![Downloads](https://static.pepy.tech/badge/eseas/month?1)](https://pepy.tech/project/eseas?1)
[![Downloads](https://pepy.tech/badge/eseas/week?1)](https://pepy.tech/project/eseas?1)



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
    demetra_source_folder = r"./demetra_source_folder"
    local_folder = r"./test_out"

    options = Options(
        demetra_source_folder,
        java_folder,
        local_folder,
        result_file_names=("sa", "s_f", "cal"), # *1
        workspace_mode=True,
        file_name_explanation=True,
    )
    # Note (1)
    # result_file_names see full list of result types from Demetra Components below

    seas = Seasonal(options)

    seas.part1()
    time.sleep(10)
    seas.part2()

if __name__ == "__main__":
    main()
```

## Documentation

For more detailed information, refer to the following guides:

- [Demetra Components](https://github.com/SermetPekin/eseas-repo/blob/main/docs/demetra_components.md)
- [Usage Guide](https://github.com/SermetPekin/eseas-repo/blob/main/docs/usage.md)

## How it Works

1. **Input Directory**: The user specifies the directory of the Demetra workspace where XML files are located.
2. **Batch File Creation**: The package creates batch files for all XML files in the specified directory.
3. **Execution**: It runs the batch files using the `jwsacruncher` tool.
4. **Output Collection**: The specified outputs are collected and compiled into individual Excel files for each XML file processed.

## Acknowledgments

Special thanks to the creators of the `jwsacruncher` Java package, which is integral to the functionality of `eseas`. For more information, visit the [jwsacruncher GitHub repository](https://github.com/jdemetra/jwsacruncher).

## About jwsacruncher

`jwsacruncher` is a Java implementation of the .NET application "WSACruncher". It is a console tool that re-estimates all the multi-processing defined in a workspace. The workspace can be generated by Demetra+ (.NET), JDemetra+ (Java), or any user tool. For more information, visit the [jwsacruncher GitHub repository](https://github.com/jdemetra/jwsacruncher).

## License

This project is licensed under the EUPL-1.2 License - see the [LICENSE](https://github.com/SermetPekin/eseas-repo/LICENSE) file for details.
