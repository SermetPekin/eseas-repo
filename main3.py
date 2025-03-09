from eseas import Seasonal, Options
import time

# Load options from the `.env` file
options = Options()

# Initialize and execute the seasonal adjustment process
m = Seasonal(options)
m.part1()
time.sleep(10)  # Pause before running part2
m.part2()