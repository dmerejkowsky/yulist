import flask


app = flask.Flask("yulist")


@app.route("/")
def index():
    return "Welcome to yulist"


if __name__ == "__main__":
    app.debug = True
    app.run()
