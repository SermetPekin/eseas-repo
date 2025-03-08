

#======================================================================
# This script was created by eseas    2025-03-08 16:52:38.108215
#   In order to reproduce you may use this template
#======================================================================
from eseas import SeasonalOptions
from eseas import Seasonal
def main():
    
    options= SeasonalOptions(
            demetra_folder="eseas/data_for_testing/unix",
            java_folder="/Users/guest/app/jwsacruncher-2.2.6/bin",
            local_folder="test_out",
            test=False,
            verbose= False,
            replace_original_files=False,
            auto_approve=False,
            result_file_names=('sa', 's_f', 'cal'),
            workspace_mode=True,
            java_bin = /usr/bin
    )
        
    m = Seasonal(options)
    m.part1()
    m.part2()
main()
        