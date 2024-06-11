### Usage 

```python

from eseas import Seasonal
from eseas import SeasonalOptions
import time 


def main(part=1):
    java_folder = r'../jwsacruncher-2.2.4/bin' 
    demetra_source_folder = r"./demetra_source_folder"
    local_folder = r"./test_out"

    options = SeasonalOptions(
             demetra_source_folder,
             java_folder,
             local_folder,
            result_file_names=("sa", "s_f", "cal",),
            workspace_mode=True,  # True
            file_name_explanation=True,  # True
    )
    seas = Seasonal(options)
    
    seas.part1()
    time.sleep(10)
    seas.part2()





if "__main__" == __name__:
    main()
    
```


- [Demetra Components](https://github.com/SermetPekin/eseas-repo/docs/demetra_components.md)
- [Readme](https://github.com/SermetPekin/eseas-repo/README.md)
  