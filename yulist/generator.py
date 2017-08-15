import copy
import itertools
import pathlib

import jinja2
import markdown


class Generator():
    def __init__(self):
        loader = jinja2.PackageLoader("yulist", "templates")
        self.jinja_env = jinja2.Environment(loader=loader,
                                            trim_blocks=True,
                                            lstrip_blocks=True,
                                            extensions=["jinja2_slug.SlugExtension"])
        self.current_user = None

    def generate_page(self, page, items):
        page_data = copy.copy(page)

        page_data["intro"] = self.get_intro(page)
        page_data["outro"] = self.get_outro(page)
        page_data["toc"] = self.get_toc(page)
        page_data["bread_crumbs"] = self.get_bread_crumbs(page)
        items = self.get_items(items)
        by_section = itertools.groupby(items, lambda x: x.get("section"))
        page_data["items"] = by_section
        return self.render("page", page_data)

    def generate_search_results(self, pattern, items):
        generated_items = self.get_items(items)
        data = dict()
        data["pattern"] = pattern
        data["results"] = generated_items
        return self.render("search_results", data)

    @staticmethod
    def get_intro(page):
        intro = page.get("intro")
        if intro:
            return markdown.markdown(intro)

    @staticmethod
    def get_outro(page):
        outro = page.get("outro")
        if outro:
            return markdown.markdown(outro)

    def get_toc(self, page):
        toc = page.get("toc")
        if not toc:
            return None
        links = list()
        for entry in toc:
            entry_path = entry["path"]
            parent_str = str(pathlib.Path(page["path"]).parent)
            if parent_str == ".":
                parent_str = "/"
            else:
                parent_str = "/" + parent_str + "/"
            link = parent_str + entry_path
            links.append({"link": link, "text": entry["text"]})
        return [self.render("link", x) for x in links]

    def get_bread_crumbs(self, page):
        links = [{
            "link": "/index",
            "text": "home"
        }]
        page_parts = pathlib.Path(page["path"]).parts
        for i in range(1, len(page_parts)):
            text = page_parts[i-1]
            link = "/" + "/".join(page_parts[0:i]) + "/index"
            links.append({"link": link, "text": text})
        res = [self.render("link", x) for x in links]
        return res

    def get_items(self, items):
        processed_items = list()
        for item in items:
            if not item.get("type"):
                raise Exception("Missing type for %s" % item)
            if item["type"] == "link":
                item["external"] = True
            out_item = self.process_item(item)
            processed_items.append(out_item)
        return processed_items

    def process_item(self, item):
        item_type = item["type"]
        inner_html = self.render(item_type, item)
        item["inner_html"] = inner_html
        return item

    def render(self, template_name, data):
        data["current_user"] = self.current_user
        template_name = template_name + ".html"
        template = self.jinja_env.get_template(template_name)
        return template.render(data)
