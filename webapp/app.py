from flask import Flask, render_template, request, session  # from module import Class.

import hfpy_utils
import swim_utils
import os
import secrets


app = Flask(__name__)
app.secret_key = str(secrets.token_hex)

"""
Requirements:
- Display an ordered list of swimmers in a select list.
- When a swimmer is selected, display their events.
- When an event is selected, open their chart in a new tab.
- Once tested, deploy on PythonAnywhere, configure account settings to set teacher to barryp.
"""


@app.get("/")
def index():
    files = os.listdir("swimdata")
    files.remove(".DS_Store")
    swimmers = []
    for f in files:
        f.removesuffix(".txt")
        split = f.split("-")
        name = split[0]
        if name not in swimmers:
            swimmers.append(name)

        swimmers.sort()

    return render_template("index.html", title="Swimmer Charts", swimmers=swimmers)


@app.post("/events")
def events():
    session["swimmer"] = request.form["swimmers"]

    files = os.listdir("swimdata")
    files.remove(".DS_Store")

    swimmer_files = []
    for f in files:
        if session["swimmer"] in f:
            swimmer_files.append(f.removesuffix(".txt"))

    events = []
    for f in swimmer_files:
        event = f"{f.split('-')[2]} {f.split('-')[3]}"
        events.append(event)

    return render_template("events.html", swimmer=session["swimmer"], events=events)


@app.post("/chart")
def display_chart():
    session["event"] = request.form["events"]

    files = os.listdir("swimdata")
    files.remove(".DS_Store")

    event = session["event"]
    event = event.replace(" ", "-")

    swimmer = session["swimmer"]

    filename = ""
    for f in files:
        if swimmer in f and event in f:
            filename = str(f)

    (
        name,
        age,
        distance,
        stroke,
        the_times,
        converts,
        the_average,
    ) = swim_utils.get_swimmers_data(filename)

    the_title = f"{name} (Under {age}) {distance} {stroke}"
    from_max = max(converts) + 50
    the_converts = [hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts]

    the_data = zip(the_converts, the_times)

    return render_template(
        "chart.html",
        title=the_title,
        average=the_average,
        data=the_data,
    )


if __name__ == "__main__":
    app.run(debug=True)  # Starts a local (test) webserver, and waits... forever.
