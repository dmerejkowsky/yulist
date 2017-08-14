import attr
import bcrypt
import flask_login
import flask
import pymongo

import yulist.config
from yulist.generator import Generator


app = flask.Flask("yulist")
# pylint: disable=invalid-name
login_manager = flask_login.LoginManager()


def configure_app(*, db):
    config = yulist.config.read_conf()
    app.secret_key = config["server"]["secret_key"]
    app.db = db
    app.generator = Generator()
    login_manager.init_app(app)


USERS = dict()


@attr.s
class User:
    user_id = attr.ib()
    hashed_password = attr.ib(default=None)
    is_authenticated = attr.ib(default=False)
    is_active = attr.ib(default=True)
    is_anonymous = attr.ib(default=False)

    def get_id(self):
        return self.user_id

    @property
    def username(self):
        return self.user_id


@login_manager.user_loader
def load_user(user_id):
    matches = list(app.db.users.find({"user_id": user_id}))
    if not matches:
        return
    row = matches[0]
    if user_id not in USERS:
        res = User(row["user_id"])
        USERS[user_id] = res
    else:
        res = USERS[user_id]
    res.hashed_password = row["hashed_password"]
    return res


def do_login():
    request = flask.request
    # POST: try to log the user in
    form = request.form
    username = form.get("username")
    user = load_user(username)
    if not user:
        raise yulist.Error("User not found")
    password = form.get("password")
    if bcrypt.hashpw(password.encode(), user.hashed_password) != user.hashed_password:
        raise yulist.Error("Invalid password")
    user.is_authenticated = True
    flask_login.login_user(user, remember=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    request = flask.request
    method = request.method
    if method == "GET":
        return flask.render_template("login.html")
    try:
        do_login()
    except yulist.Error as error:
        return flask.render_template("login.html", error=error)

    return flask.redirect(flask.url_for('index'))


@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))


@app.route("/")
def index():
    return display_page("index")


@app.route("/search")
def search_form():
    pattern = flask.request.args.get("pattern")
    if pattern:
        results = list(do_search(app.db, pattern))
        return app.generator.generate_search_results(pattern, results)
    else:
        return app.generator.render("search_form", dict())


def do_search(db, pattern):
    cursor = db.items.find({"$text": {"$search": pattern}})
    for item in cursor:
        page = db.pages.find({"_id": item["page_id"]})[0]
        if can_show(page):
            page_link = page["path"]
            item["page_link"] = page_link
            yield item


def can_show(page):
    if page["private"] and not flask_login.current_user.is_authenticated:
        return False
    return True


@app.route("/<path:page_path>")
def display_page(page_path):
    db = app.db
    itemsdb = db.items
    pages = db.pages
    page = pages.find({"path": page_path})[0]
    if can_show(page):
        items = itemsdb.find({"page_id": page["_id"]})
    else:
        items = list()
    generator = app.generator
    generator.current_user = flask_login.current_user
    res = generator.generate_page(page, items)
    return res


def setup():
    client = pymongo.MongoClient()
    db = client.yulist
    configure_app(db=db)


# call setup() here for uwsgi
setup()


def main():
    app.debug = True
    app.run(port=1234)


if __name__ == "__main__":
    main()
