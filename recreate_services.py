import os
import random
import string

# Generate random string of 10 characters each
random_app_name = 'app_' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))

new_file_name = 'proxy.py'
# Open the renamed file and modify the function name
with open(new_file_name, "r") as file:
    content = file.read()

content = content.replace("fetch", random_app_name)

with open(new_file_name, "w") as file:
    file.write(content)

print(f"The new function name is: {random_app_name}")

