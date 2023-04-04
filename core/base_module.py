import abc


class Base_Module(abc.ABC):
    def inject(self, reg):
        pass

    def pre_start(self):
        pass

    def start(self):
        pass