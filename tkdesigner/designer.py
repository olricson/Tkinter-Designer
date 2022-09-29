import tkdesigner.figma.endpoints as endpoints
from tkdesigner.figma.frame import Frame

from tkdesigner import template

from pathlib import Path


CODE_FILE_NAME = "gui.py"


class Designer:
    def __init__(self, token, file_key, output_path: Path, template_name='default', elements_pack='tk'):
        self.output_path = output_path
        self.figma_file = endpoints.Files(token, file_key)
        self.file_data = self.figma_file.get_file()
        self.template_name = template_name
        self.elements_pack = elements_pack

    def to_code(self) -> str:
        """Return main code.
        """
        window_data = self.file_data["document"]["children"][0]["children"][0]

        frame = Frame(window_data, self.figma_file, self.output_path, elements_pack=self.elements_pack)
        return frame.to_code(getattr(template, self.template_name))

    def design(self):
        """Write code and assets to the specified directories.
        """
        code = self.to_code()
        self.output_path.joinpath(CODE_FILE_NAME).write_text(code, encoding='UTF-8')
