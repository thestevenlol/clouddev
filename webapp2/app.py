from flask import Flask, render_template, request, session
from DBcm import UseDatabase
import swim_utils
import hfpy_utils

app = Flask(__name__)
app.secret_key = "ouGQUIO%^&*9SGugA2131%^&2123WU)*&^%D()DWU0a8132331(*&308AWi"

DB_CONFIG = {
        "host": "localhost",
        "database": "SwimclubDB",
        "user": "swimuser",
        "password": "swimuserpasswd"
    }


@app.get("/")
def index():

    times = list()
    with UseDatabase(DB_CONFIG) as cursor:
        _SQL = """SELECT DISTINCT DATE(ts) FROM times"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        for content in contents:
            times.append(str(content[0]).split()[0])

    return render_template("index.html", items=times)


@app.post("/get_swimmers")
def get_swimmers():
    date = request.form.get("date")

    with UseDatabase(DB_CONFIG) as cursor:
        _SQL = f"""SELECT swimmer_id FROM times WHERE DATE(ts) = '{date}'"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        swimmers = set()

        for data in contents:
            swimmer_id = data[0]

            _SQL = f"""SELECT s.name, s.age 
            FROM swimmers s 
            INNER JOIN times t ON s.id = t.swimmer_id 
            WHERE t.swimmer_id = {swimmer_id}"""

            cursor.execute(_SQL)
            swimmer_data = cursor.fetchall()
            for s_data in swimmer_data:
                txt = s_data[0] + ", " + str(s_data[1])
                swimmers.add(txt)

    swimmers = list(swimmers)
    swimmers.sort()
    return render_template("swimmers.html", items=swimmers)


@app.post("/get_events")
def get_swimmer():
    swimmer = request.form.get("swimmer")
    split_swimmer = swimmer.split(", ")
    name = split_swimmer[0]
    age = int(split_swimmer[1])

    session['swimmer_name_age'] = (name, age)

    with UseDatabase(DB_CONFIG) as cursor:
        _SQL = f"""SELECT DISTINCT e.distance, e.stroke
        FROM events e
        INNER JOIN times t ON e.id = t.event_id
        INNER JOIN swimmers s ON s.id = t.swimmer_id
        WHERE s.name = '{name}' AND s.age = {age};"""

        cursor.execute(_SQL)
        dataset = cursor.fetchall()

    items = list()
    for datapoint in dataset:
        txt = str(datapoint[0]) + "m " + datapoint[1]
        items.append(txt)

    return render_template("events.html", items=items)


@app.post("/get_chart")
def get_chart():
    data = request.form.get("event")
    split_data = data.split("m ")
    distance = int(split_data[0])
    stroke = split_data[1]
    name, age = session['swimmer_name_age']

    name, age, distance, stroke, time, converts, average = swim_utils.get_swimmers_data(name, age, distance, stroke)
    the_title = f"{name} (Under {age}) {distance} {stroke}"
    time.reverse()
    from_max = max(converts) + 50
    converts = [hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts]
    the_data = zip(converts, time)

    return render_template(
        "chart.html",
        title=the_title,
        average=average,
        data=the_data,
    )


app.run(debug=True)
