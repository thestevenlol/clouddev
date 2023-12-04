from flask import Flask, render_template, request
from DBcm import UseDatabase

app = Flask(__name__)

DB_CONFIG = {
        "host": "localhost",
        "database": "swimmers_webapp",
        "user": "admin",
        "password": "swimmerspwd"
    }


@app.get("/")
def index():

    times = list()
    with UseDatabase(DB_CONFIG) as cursor:
        _SQL = """SELECT DISTINCT ts FROM times"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        for content in contents:
            times.append(content[0])

    return render_template("index.html", items=times)


@app.post("/get_swimmers")
def get_swimmers():
    date = request.form.get("date")

    with UseDatabase(DB_CONFIG) as cursor:
        _SQL = f"""SELECT * FROM times WHERE ts = '{date}'"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()

    return date


app.run(debug=True)
