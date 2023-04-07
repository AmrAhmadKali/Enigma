from core import main
from meta.decorators import instance

from meta.base_module import BaseModule


@instance("addon1")
class Addon(BaseModule):
    app: main.Server

    def inject(self, reg):
        self.app = reg.get_instance("app")

    def pre_start(self):
        pass

    def start(self):
        pass
