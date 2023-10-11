# Written by Jack Foley, C00274246

import os
import utils

# Gets all raw files from the swimdata dir.
def get_all_files():
    directory = "./swimdata"
    filenames = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if filename.endswith(".txt"):
                filenames.append(filename)
    
    return filenames

# Gets the names of all swimmers from the files.
def get_names():
    files = get_all_files()
    names = []
    for f in files:
        name = f.split("-")[0]
        if name not in names:
            names.append(name)

    return names

# Gets all files with for a swimmer.
def get_named_files(name):
    name = name.lower()
    files = get_all_files()
    named_files = []
    for f in files:
        if f.lower().startswith(name):
            named_files.append(f)

    return named_files

# Gets the data from a file.
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
        converted = utils.map_value(value, 0, max(values) + 50, 0, 500);
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

# Converts time to an integer value.
def convert_time(time):

    if ':' in time:
        mins = time.split(":")[0]
        secs = time.split(":")[1].split(".")[0]
        ms = time.split(":")[1].split(".")[1]
    else:
        mins = 0
        secs = time.split(".")[0]
        ms = time.split(".")[1]


    return int(mins) * 6000 + int(secs) * 100 + int(ms)

# Builds the HTML page from the data
def create_html(data: tuple):
    head = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Document</title>
        <style>
            .container {
                display: flex;
                height: 100%;
                width: 100%;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 0;
                margin: 0;
            }

            .bars {
                display: flex;
                flex-direction: column;
                padding: 0;
                margin: 0;
                width: 100%;
                justify-content: center;
                align-items: center;
            }

            .bar {
                display: flex;
                flex-direction: row;
                justify-content: space-around;
                
                @media only screen and (max-width: 1000px) {
                    min-width: 70%;
                    width: 80%;
                }

                @media only screen and (max-width: 650px) {
                    width: 100%;
                }

                min-width: 50%;
                max-width: 100%;
                padding: 0;
                margin: 0;
            }
        </style>
    </head>
    <body>
    <div class="container">
        <div class="bars">
    """

    body = ""
    title = data[0] + f", {data[1]}"
    body += f"<h1>{title}</h1>"
    subtitle = f"<h2>{data[2]} {data[3]}</h2>"
    body += subtitle


    for mapped, time in zip(data[6], data[4]):
        txt = f"""
            <div class="bar">
                <svg width="500" height="50">
                    <rect x="0" y="0" width="{mapped}" height="50" fill="red" />
                </svg>
                <p>{time}</p>
            </div>
            """
        body += txt


    footer = """
        </div>
    </body>
    </html>
    """

    return head + body + footer