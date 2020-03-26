from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
    file = open('raceSchedule.csv', 'r')
    races = file.readlines()
    table = []
    for race in races:
        r = race.split(',')
        map(str.strip, r)

        table.append(r)


    title = "Pinewood Derby"
    #table = [["1", "2", "3"], ["a", "b", "c"], ["d", "e", "f"]]
    return render_template("index.html", title = title, table=table)


if __name__ == "__main__":
    Bootstrap(app)
    app.run(host='0.0.0.0')