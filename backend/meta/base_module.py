import abc


class BaseModule(abc.ABC):
    def inject(self, reg) -> None:
        """
        Here we can load all dependencies of our module
        :param reg: Registry, which holds all instances of all modules
        """

    def pre_start(self) -> None:
        """
        Module preparations before starting here; do stuff which may be required by other modules here.
        At this stage all dependencies are resolved, but not yet initiated
        """

    def start(self) -> None:
        """
        Module final loading;
        here all dependencies are loaded and ready to go
        """

    async def setup(self, storage) -> None:
        """
        prepare all required stuff inside the storage here.
        This method gets called ONCE after opening a connection to prepare for it.
        """
