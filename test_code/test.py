import json

# Open the file and read the data
with open('apps.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# split the data into lines
lines = data.splitlines()

# get the header and remove empty strings resulted from split
header = [h for h in lines[0].split("  ") if h]

# process each line
out = []
for line in lines[2:]:
    # split each line on two or more spaces and remove empty strings resulted from split
    items = [i for i in line.split("  ") if i]

    # Ensure there are at least 2 items (Name and Id) before processing
    if len(items) >= 2:
        # map the Id to the output list
        out.append({"Id": items[1]})

# output to json
json_data = json.dumps(out, indent=4)

# print json_data
print(json_data)

# Write the json data to a file
with open('apps.json', 'w') as file:
    file.write(json_data)
