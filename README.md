# eseas

eseas is a Python package that acts as a wrapper for the `jwsacruncher` Java package. This tool allows users to process Demetra workspace XML files, create batch files, execute them, and collect the desired outputs into individual Excel files.

## Installation

### eseas

You can install the `eseas` package via pip:

```bash
pip install eseas
```

Alternatively, you can install it from a local wheel file:

```bash
pip install ./eseas-0.1.0-py3-none-any.whl
```

### jwsacruncher

The `jwsacruncher` tool is required for this package to function. You can download the latest release of `jwsacruncher` from the [jdemetra releases](https://github.com/jdemetra/jwsacruncher/releases/tag/v2.2.4).

```bash
# Download jwsacruncher
cd jdemetra/jswacruncher
```

After downloading `jwsacruncher`, you need to specify its location when using the `SeasonalOptions` function from the `eseas` package.

## Usage

Here's an example of how to use the `eseas` package:

```python
from eseas import Seasonal, SeasonalOptions
import time

def main():
    # Specify the path to the jwsacruncher bin directory
    java_folder = r'../jwsacruncher-2.2.4/bin'
    demetra_source_folder = r"./demetra_source_folder"
    local_folder = r"./test_out"

    options = SeasonalOptions(
        demetra_source_folder,
        java_folder,
        local_folder,
        result_file_names=("sa", "s_f", "cal"),
        workspace_mode=True,
        file_name_explanation=True,
    )
    seas = Seasonal(options)
    
    seas.part1()
    time.sleep(10)
    seas.part2()

if __name__ == "__main__":
    main()
```

## Documentation

For more detailed information, refer to the following guides:

- [Demetra Components](https://github.com/SermetPekin/eseas-repo/docs/demetra_components.md)
- [Usage Guide](https://github.com/SermetPekin/eseas-repo/docs/usage.md)

## How it Works

1. **Input Directory**: The user specifies the directory of the Demetra workspace where XML files are located.
2. **Batch File Creation**: The package creates batch files for all XML files in the specified directory.
3. **Execution**: It runs the batch files using the `jwsacruncher` tool.
4. **Output Collection**: The specified outputs are collected and compiled into individual Excel files for each XML file processed.

## About jwsacruncher

`jwsacruncher` is a Java implementation of the .NET application "WSACruncher". It is a console tool that re-estimates all the multi-processing defined in a workspace. The workspace can be generated by Demetra+ (.NET), JDemetra+ (Java), or any user tool. For more information, visit the [jwsacruncher GitHub repository](https://github.com/jdemetra/jwsacruncher).

## License

This project is licensed under the EUPL-1.2 License - see the [LICENSE](https://github.com/SermetPekin/eseas-repo/LICENSE) file for details.

