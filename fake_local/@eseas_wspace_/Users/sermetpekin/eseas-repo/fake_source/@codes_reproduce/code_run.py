

#======================================================================
# This script was created by eseas    2026-04-04 13:31:14.617097
#   In order to reproduce you may use this template
#======================================================================
from eseas import SeasonalOptions
from eseas import Seasonal
def main():
    
    options= SeasonalOptions(
            demetra_folder="fake_source",
            java_folder="/private/var/folders/7y/qkvg04q15k78xc5kkvt0tjth0000gn/T/pytest-of-sermetpekin/pytest-20/test_auto_approve_false0",
            local_folder="fake_local",
            test=False,
            verbose= False,
            replace_original_files=False,
            auto_approve=False,
            result_file_names=('sa', 's', 'cal'),
            workspace_mode=True,
            java_bin = None
    )
        
    m = Seasonal(options)
    m.part1()
    m.part2()
main()
        