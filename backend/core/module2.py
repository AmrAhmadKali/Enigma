from meta.base_module import BaseModule
from meta.decorators import instance


@instance("thisisarandommod")
class Addon2(BaseModule):
    pass
