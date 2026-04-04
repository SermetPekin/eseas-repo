from eseas import Seasonal, Options

# Load options from the `.env` file
options = Options()

# Initialize and execute the seasonal adjustment process
m = Seasonal(options)
m.run()
