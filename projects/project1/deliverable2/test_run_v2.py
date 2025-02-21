from deliverable2 import *

# Instantiate the URLValidator class
validator = URLValidator()

# Define user prompt and URL
user_prompt = "Is it a bad investment to buy a house as a single male under the age of 30?"
url_to_check = "https://www.quickenloans.com/learn/homes-for-single-people"

# Run the validation
result = validator.rate_url_validity(user_prompt, url_to_check)

# Print the results
import json
print(json.dumps(result, indent=2))