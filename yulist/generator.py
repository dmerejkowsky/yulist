import copy
import sys

import jinja2
import markdown


def remove_enclosing_p(html):
    return html[3:-4]


class Generator():
    def __init__(self, *, output_format, prefix="", media_url=""):
        self.output_format = output_format
        self.media_url = media_url
        self.prefix = prefix
        loader = jinja2.PackageLoader("yulist", "templates")
        self.jinja_env = jinja2.Environment(loader=loader,
                                            trim_blocks=True,
                                            lstrip_blocks=True)

    def generate_page(self, page):
        page_data = copy.copy(page)
        page_data["prefix"] = self.prefix

        intro = page.get("intro")
        if intro:
            page_data["intro"] = markdown.markdown(intro)
        outro = page.get("outro")
        if outro:
            page_data["outro"] = markdown.markdown(outro)

        toc = page.get("toc")

        if toc:
            toc_links = self.generate_toc_links(page["path"], toc)
            page_data["toc"] = [self.render("link", x) for x in toc_links]

        bread_crumbs = self.generate_bread_crumbs(page["path"])
        as_links = [self.render("link", x) for x in bread_crumbs]
        page_data["bread_crumbs"] = as_links

        items = page.get("items") or list()
        processed_items = list()
        for item in items:
            if not item.get("type"):
                sys.exit(f"Missing type for {item}")
            if item["type"] == "link":
                item["external"] = True
            out_item = self.generate_item(item)
            processed_items.append(out_item)
        page_data["items"] = processed_items

        return self.render("page", page_data)

    def generate_item(self, item):
        item_type = item["type"]
        if item_type == "markdown":
            return remove_enclosing_p(markdown.markdown(item["text"]))
        return self.render(item_type, item)

    def render(self, template_name, data):
        data["prefix"] = self.prefix
        data["media_url"] = self.media_url
        template_name = template_name + "." + self.output_format
        template = self.jinja_env.get_template(template_name)
        return template.render(data)

    def generate_bread_crumbs(self, path):
        res = [{
            "link": "/index." + self.output_format,
            "text": "home"
        }]
        for i in range(1, len(path.parts)):
            text = path.parts[i-1]
            link = "/" + "/".join(path.parts[0:i]) + "/index." + self.output_format
            res.append({"link": link, "text": text})
        return res

    def generate_toc_links(self, path, toc_entries):
        res = list()
        for entry in toc_entries:
            entry_path = entry["path"]
            entry_text = entry["text"]
            parent_str = str(path.parent)
            if parent_str == ".":
                parent_str = "/"
            else:
                parent_str = "/" + parent_str + "/"
            link = parent_str + entry_path + "." + self.output_format
            res.append({"link": link, "text": entry["text"]})
        return res
