import jinja2


class Generator():
    def __init__(self, output_format):
        self.output_format = output_format
        loader = jinja2.PackageLoader("yulist", "templates")
        self.jinja_env = jinja2.Environment(loader=loader)

    def generate_page(self, page):
        page_data = dict()
        page_data["title"] = page["title"]
        page_data["toc"] = page.get("toc") or list()

        items = page.get("items") or list()
        processed_items = list()
        for item in items:
            out_item = self.generate_item(item)
            processed_items.append(out_item)
        page_data["items"] = processed_items

        return self.render("page", page_data)

    def generate_item(self, item):
        item_type = item["type"]
        return self.render(item_type, item)

    def render(self, template_name, data):
        template_name = template_name + "." + self.output_format
        template = self.jinja_env.get_template(template_name)
        return template.render(data)
