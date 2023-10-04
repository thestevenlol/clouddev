import os
import utils

def get_all_files():
    directory = "./swimdata"
    filenames = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if filename.endswith(".txt"):
                filenames.append(filename)
    
    return filenames

def get_names():
    files = get_all_files()
    names = []
    for f in files:
        name = f.split("-")[0]
        if name not in names:
            names.append(name)

    return names

def get_named_files(name):
    name = name.lower()
    files = get_all_files()
    named_files = []
    for f in files:
        if f.lower().startswith(name):
            named_files.append(f)

    return named_files

def get_data(filename):
    if not filename.endswith(".txt"):
        return None
    
    filename = filename.removesuffix(".txt")
    name = filename.split("-")[0]
    age = filename.split("-")[1]
    length = filename.split("-")[2]
    swimtype = filename.split("-")[3]

    times = []
    with open(os.path.join("./swimdata", filename + ".txt"), "r") as f:
        times = f.read().split(",")

    values = []
    for time in times:
        value = convert_time(time)
        values.append(value)

    mapped = []
    for value in values:
        converted = utils.map_value(min(values) - 50, max(values), 0, 400, value);
        formatted = "{:.2f}".format(converted)
        mapped.append(formatted)

    data = (
        name,
        age,
        length,
        swimtype,
        times,
        values,
        mapped
    )

    return data

def convert_time(time):
    mins = time.split(":")[0]
    secs = time.split(":")[1].split(".")[0]
    ms = time.split(":")[1].split(".")[1]

    return int(mins) * 6000 + int(secs) * 100 + int(ms)

file = get_named_files("darius")[0]
data = get_data(file)

head = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
"""

body = ""
title = data[0] + f"({data[1]})"
body += f"<h1>{title}</h1>"

for mapped in data[6]:
    txt = f"""
            <svg width="1000" height="50">
                <rect x="0" y="0" width="{mapped}" height="50" fill="red" />
            </svg>
          """
    body += txt


footer = """
  </body>
</html>
"""

html = head + body + footer

# clear index.html
open("index.html", "w").close()

with open("index.html", "w") as f:
    f.write(html)