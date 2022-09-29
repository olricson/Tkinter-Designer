from customtkinter import CTkTextbox

from tkdesigner.figma.vector_elements import Vector, Rectangle

TEXT_INPUT_ELEMENT_TYPES = {
    "TextArea": "CTkTextbox",
    "TextBox": "CTkEntry"
}
CTkTextbox

class Text(Vector):
    def __init__(self, node, frame):
        super().__init__(node)

        self.x, self.y = self.position(frame)
        self.width, self.height = self.size()

        self.text_color = self.color()
        self.font, self.font_size = self.font_property()
        self.text = self.characters.replace("\n", "\\n")

    @property
    def characters(self) -> str:
        string: str = self.node.get("characters")
        text_case: str = self.style.get("textCase", "ORIGINAL")

        if text_case == "UPPER":
            string = string.upper()
        elif text_case == "LOWER":
            string = string.lower()
        elif text_case == "TITLE":
            string = string.title()

        return string

    @property
    def style(self):
        # TODO: Native conversion
        return self.node.get("style")

    @property
    def character_style_overrides(self):
        return self.node.get("characterStyleOverrides")

    @property
    def style_override_table(self):
        # TODO: Native conversion
        return self.node.get("styleOverrideTable")

    def font_property(self):
        style = self.node.get("style")

        font_name = style.get("fontPostScriptName")
        if font_name is None:
            font_name = style["fontFamily"]

        font_name = font_name.replace('-', ' ')
        font_size = style["fontSize"]
        return font_name, font_size

    def to_code(self):
        return f"""
canvas.create_text(
    {self.x},
    {self.y},
    anchor="nw",
    text="{self.text}",
    fill="{self.text_color}",
    font=("{self.font}", {int(self.font_size)} * -1),
)
"""


class Button(Rectangle):
    def __init__(self, node, frame, text:Text = None, hover=None, *, id_):
        super().__init__(node, frame)
        # self.image_path = image_path
        self.id_ = id_
        self.text = text
        self.hover_color = self.color()
        if hover:
            self.hover_color = hover.color()


    def to_code(self):
        return f"""
button_{self.id_} = CTkButton(
    width={self.width},
    height={self.height},
    fg_color="{self.color()}",
    corner_radius={self.corner_radius},
    command=lambda: print("button_{self.id_} clicked"),
    text="{self.text.text}",
    text_font=("{self.text.font}", {int(self.text.font_size)} * -1),
    text_color="{self.text.color()}",
    hover_color="{self.hover_color}"
)
button_{self.id_}.place(
    x={self.x},
    y={self.y},
)
"""


class Progress(Rectangle):
    def __init__(self, node, frame, progress:Rectangle = None, *, id_):
        super().__init__(node, frame)
        # self.image_path = image_path
        self.id_ = id_
        self.progress = progress

    def to_code(self):
        return f"""
progress_{self.id_} = CTkProgressBar(
    fg_color="{self.color()}",
    width={self.width},
    height={self.height},
    corner_radius={self.corner_radius},
    progress_color="{self.progress.color()}"
)
progress_{self.id_}.place(
    x={self.x},
    y={self.y},
)
"""


class Image(Vector):
    def __init__(self, node, frame, image_path, *, id_):
        super().__init__(node)

        self.x, self.y = self.position(frame)

        width, height = self.size()
        self.x += width // 2
        self.y += height // 2

        self.image_path = image_path
        self.id_ = id_

    def to_code(self):
        return f"""
image_image_{self.id_} = PhotoImage(
    file=relative_to_assets("{self.image_path}"))
image_{self.id_} = canvas.create_image(
    {self.x},
    {self.y},
    image=image_image_{self.id_}
)
"""


class TextEntry(Vector):
    def __init__(self, node, frame, image_path, *, id_):
        super().__init__(node)

        self.id_ = id_

        self.x, self.y = self.position(frame)
        self.width, self.height = self.size()

        self.entry_type = TEXT_INPUT_ELEMENT_TYPES.get(self.get("name").split('_')[0])

    def to_code(self):
        return f"""
entry_{self.id_} = {self.entry_type}(
    fg_color="{self.color()}",
    border_width=0,
    width={self.width},
    height={self.height},
    corner_radius={self.node.get("cornerRadius", 0)},
)
entry_{self.id_}.place(
    x={self.x},
    y={self.y}
)
"""

class Combobox(Rectangle):
    def __init__(self, node, frame, hover=None, *, id_):
        super().__init__(node, frame)
        # self.image_path = image_path
        self.hover_color = self.color()
        if hover:
            self.hover_color = hover.color()
        self.id_ = id_

    def to_code(self):
        return f"""
combobox_{self.id_} = CTkOptionMenu(
    fg_color="{self.color()}",
    button_color="{self.color()}",
    button_hover_color="{self.hover_color}",
    width={self.width},
    height={self.height},
    corner_radius={self.corner_radius}
)
combobox_{self.id_}.place(
    x={self.x},
    y={self.y},
)
"""