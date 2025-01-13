import os
import random
import string

# Generate two random strings of 10 characters each
random_file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
random_app_name = 'app_' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Rename test.py to a random file name
new_file_name = f"{random_file_name}.py"
os.rename("test.py", new_file_name)

# Open the renamed file and modify the function name
with open(new_file_name, "r") as file:
    content = file.read()

content = content.replace("def app(", f"def {random_app_name}(")

with open(new_file_name, "w") as file:
    file.write(content)

# Open and edit gunicorn.service
with open("proxy_code/gunicorn.service", "r") as file:
    content = file.read()

content = content.replace("test:app", f"{random_file_name}.py:{random_app_name}")

with open("proxy_code/gunicorn.service", "w") as file:
    file.write(content)

print(f"The new file name is: {new_file_name}")
print(f"The new function name is: {random_app_name}")
print("gunicorn.service has been updated with the new file name and function name.")

