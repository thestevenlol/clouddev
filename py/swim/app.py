from flask import Flask, render_template
import swimming_utils

app = Flask(__name__)


@app.route("/chart")
def chart():
    person = "Darius"
    filenames = swimming_utils.get_named_files(person)
    swimming_utils.create_html(swimming_utils.get_data(filenames[0]))
    return render_template("index.html")


@app.route("/")
def index():
    return render_template("base.html", title="test")


if __name__ == "__main__":
    app.run(debug=True)
