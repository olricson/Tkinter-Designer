from ..constants import ASSETS_PATH
from ..utils import download_image

from .node import Node
from .vector_elements import Line, Rectangle, UnknownElement

from tkdesigner.figma.elements.tk_elements import *
from tkdesigner.figma.elements.tk_elements import TextEntry as tkentry

from jinja2 import Template
from pathlib import Path


class Frame(Node):
    def __init__(self, node, figma_file, output_path, elements_pack="tk"):
        super().__init__(node)

        self.elements_pack = elements_pack

        self.width, self.height = self.size()
        self.bg_color = self.color()

        self.counter = {}

        self.figma_file = figma_file

        self.output_path: Path = output_path
        self.assets_path: Path = output_path / ASSETS_PATH

        self.output_path.mkdir(parents=True, exist_ok=True)
        self.assets_path.mkdir(parents=True, exist_ok=True)

        self.elements = [
            self.create_element(child)
            for child in self.children
            if Node(child).visible
        ]

    def create_element(self, element: Node):
        is_ctk = False
        if self.elements_pack == 'ctk':
            is_ctk = True
            from tkdesigner.figma.elements.ctk_elements import Button, Text, Image, TextEntry, Progress, Combobox

        element_name = element["name"].strip().lower().split('_')[0]
        alias = element["name"].strip().lower().split('_')[1] if '_' in element['name'] else None
        element_type = element["type"].strip().lower()

        print(
            "Creating Element "
            f"{{ name: {element_name}, type: {element_type} }}"
        )

        if element_name == "button":
            self.counter[Button] = self.counter.get(Button, 0) + 1
            ch = element.get('children')
            item_id = element["id"]
            text = [item for item in ch if item['type'] == 'TEXT'][0]
            element = [item for item in ch if item['type'] == 'RECTANGLE'][0]
            hover = [item for item in ch if item['name'] == 'hover']
            return Button(element, self, text=Text(text, self), hover=Rectangle(hover[0], self) if hover else None, id_=f"{alias or self.counter[Button]}")

        elif element_name == "progress" and is_ctk:
            self.counter[Progress] = self.counter.get(Progress, 0) + 1
            ch = element.get('children')
            foreground = [item for item in ch if item['name'] == 'foreground'][0]
            background = [item for item in ch if item['name'] == 'background'][0]
            return Progress(background, self, progress=Rectangle(foreground, self), id_=f"{alias or self.counter[Progress]}")

        elif element_name == "combobox" and is_ctk:
            self.counter[Combobox] = self.counter.get(Combobox, 0) + 1
            # ch = element.get('children')
            # foreground = [item for item in ch if item['name'] == 'foreground'][0]
            # background = [item for item in ch if item['name'] == 'background'][0]
            hover = []
            if element_type == "group":
                ch = element.get('children')
                element = [item for item in ch if item['name'].lower().strip() == 'combobox'][0]
                hover = [item for item in ch if item['name'] == 'hover']
            return Combobox(element, self, hover=Rectangle(hover[0], self) if hover else None, id_=f"{alias or self.counter[Combobox]}")


        elif element_name in ("textbox", "textarea"):
            self.counter[TextEntry] = self.counter.get(TextEntry, 0) + 1

            item_id = element["id"]
            image_url = self.figma_file.get_image(item_id)
            image_path = (
                self.assets_path / f"entry_{self.counter[TextEntry]}.png")
            download_image(image_url, image_path)

            image_path = image_path.relative_to(self.assets_path)

            if element_name == "textarea":
                return tkentry(
                    element, self, image_path=image_path, id_=f"{alias or self.counter[TextEntry]}")

            return TextEntry(
                element, self, image_path=image_path, id_=f"{alias or self.counter[TextEntry]}")

        elif element_name == "image":
            self.counter[Image] = self.counter.get(Image, 0) + 1

            item_id = element["id"]
            image_url = self.figma_file.get_image(item_id)
            image_path = self.assets_path / f"image_{self.counter[Image]}.png"
            download_image(image_url, image_path)

            image_path = image_path.relative_to(self.assets_path)

            return Image(
                element, self, image_path, id_=f"{self.counter[Image]}")

        if element_name == "rectangle" or element_type == "rectangle":
            return Rectangle(element, self)

        if element_name == "line" or element_type == "line":
            return Line(element, self)

        elif element_type == "text":
            return Text(element, self)

        else:
            print(
                f"Element with the name: `{element_name}` cannot be parsed. "
                "Would be displayed as Black Rectangle")
            return UnknownElement(element, self)

    @property
    def children(self):
        # TODO: Convert nodes to Node objects before returning a list of them.
        return self.node.get("children")

    def color(self) -> str:
        """Returns HEX form of element RGB color (str)
        """
        try:
            color = self.node["fills"][0]["color"]
            r, g, b, *_ = [int(color.get(i, 0) * 255) for i in "rgba"]
            return f"#{r:02X}{g:02X}{b:02X}"
        except Exception:
            return "#FFFFFF"

    def size(self) -> tuple:
        """Returns element dimensions as width (int) and height (int)
        """
        bbox = self.node["absoluteBoundingBox"]
        width = bbox["width"]
        height = bbox["height"]
        return int(width), int(height)

    def to_code(self, template):
        t = Template(template)
        return t.render(
            window=self, elements=self.elements, assets_path=ASSETS_PATH)


# Frame Subclasses


class Group(Frame):
    def __init__(self, node):
        super().__init__(node)


class Component(Frame):
    def __init__(self, node):
        super().__init__(node)


class ComponentSet(Frame):
    def __init__(self, node):
        super().__init__(node)


class Instance(Frame):
    def __init__(self, node):
        super().__init__(node)

    @property
    def component_id(self) -> str:
        self.node.get("componentId")
