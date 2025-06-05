from bs4 import BeautifulSoup

class Parser:
    def __init__(self):
        pass

    def extract(self, html, selectors):
        if not html:
            raise ValueError("Empty HTML provided.")
        if not selectors or not isinstance(selectors, dict):
            raise ValueError("Invalid selectors format.")

        soup = BeautifulSoup(html, "html.parser")

        try:
            primary_key = next(iter(selectors))
            primary_selector = selectors[primary_key]["selector"]
        except (KeyError, StopIteration):
            raise ValueError("Invalid primary selector structure.")

        elements = soup.select(primary_selector)
        if not elements:
            raise ValueError(f"No elements found for selector: {primary_selector}")

        result = []

        for el in elements:
            item = {}
            for key, rule in selectors.items():
                sel = rule.get("selector")
                attr = rule.get("attr", "text")
                if not sel:
                    raise ValueError(f"Missing selector for key: {key}")
                target = el if key == primary_key else el.select_one(sel)
                if not target:
                    item[key] = None
                    continue
                if attr == "text":
                    item[key] = target.get_text(strip=True)
                else:
                    item[key] = target.get(attr)
            result.append(item)

        return result