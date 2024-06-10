

#====================================================================== 
# This script was created by evdspySeas    2024-06-10 19:21:38.751352
#   In order to reproduce you may use this template 
#====================================================================== 
from evdspySeas import SeasonalOptions 
from evdspySeas import SeasonalADV
def main():
    
    options= SeasonalOptions(
            demetra_folder="./evdspySeas/data_for_testing/unix",
            java_folder="../jwsacruncher-2.2.4/bin",
            local_folder="./evdspyseas_output",
            test=False,
            verbose= False,
            replace_original_files=False,
            auto_approve=False,
            result_file_names=('sa', 's', 'cal'),
            workspace_mode=True,
    )
        
    m = SeasonalADV(options)
    m.part1()
    m.part2()
main() 
        