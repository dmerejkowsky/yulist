import flask
import pymongo

from yulist.generator import Generator


app = flask.Flask("yulist")


def configure_app(*, db, debug):
    app.debug = debug
    app.db = db
    app.generator = Generator()


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
        page_link = page["path"]
        item["page_link"] = page_link
        yield item


@app.route("/<path:page_path>")
def display_page(page_path):
    db = app.db
    items = db.items
    pages = db.pages
    page = pages.find({"path": page_path})[0]
    matching_items = items.find({"page_id": page["_id"]})
    generator = app.generator
    res = generator.generate_page(page, matching_items)
    return res


def main():
    client = pymongo.MongoClient()
    db = client.yulist
    configure_app(db=db, debug=True)
    app.run()


if __name__ == "__main__":
    main()
