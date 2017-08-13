import copy
import sys

import jinja2
import markdown


class Generator():
    def __init__(self, *, media_url=""):
        self.media_url = media_url
        loader = jinja2.PackageLoader("yulist", "templates")
        self.jinja_env = jinja2.Environment(loader=loader,
                                            trim_blocks=True,
                                            lstrip_blocks=True)

    def generate_page(self, page):
        page_data = copy.copy(page)

        page_data["intro"] = self.get_intro(page)
        page_data["outro"] = self.get_outro(page)
        page_data["toc"] = self.get_toc(page)
        page_data["bread_crumbs"] = self.get_bread_crumbs(page)
        page_data["items"] = self.get_items(page)

        return self.render("page", page_data)

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
            parent_str = str(page["path"].parent)
            if parent_str == ".":
                parent_str = "/"
            else:
                parent_str = "/" + parent_str + "/"
            link = parent_str + entry_path + ".html"
            links.append({"link": link, "text": entry["text"]})
        return [self.render("link", x) for x in links]

    def get_bread_crumbs(self, page):
        links = [{
            "link": "/index.html",
            "text": "home"
        }]
        page_parts = page["path"].parts
        for i in range(1, len(page_parts)):
            text = page_parts[i-1]
            link = "/" + "/".join(page_parts[0:i]) + "/index.html"
            links.append({"link": link, "text": text})
        res = [self.render("link", x) for x in links]
        return res

    def get_items(self, page):
        items = page.get("items") or list()
        processed_items = list()
        for item in items:
            if not item.get("type"):
                sys.exit(f"Missing type for {item}")
            if item["type"] == "link":
                item["external"] = True
            out_item = self.process_item(item)
            processed_items.append(out_item)
        return processed_items

    def process_item(self, item):
        item_type = item["type"]
        return self.render(item_type, item)

    def render(self, template_name, data):
        data["media_url"] = self.media_url
        template_name = template_name + ".html"
        template = self.jinja_env.get_template(template_name)
        return template.render(data)
