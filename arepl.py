import re


input = "98239870"

pattern = r"^[189][0-9]{7}$"

match = re.match(pattern, input)

if match:
    print("Valid")
else:
    print("Invalid")
