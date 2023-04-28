import abc


class BaseModule(abc.ABC):
    def inject(self, reg):
        # load all dependencies here
        pass

    def pre_start(self):
        # Module preparations before starting here; do stuff which may be required by other modules here.
        # At this stage all dependencies are resolved, but not yet initiated
        pass

    def start(self):
        # Module final loading;
        # here all dependencies are loaded and ready to go
        pass

    async def setup(self, storage):
        # prepare all required stuff inside the storage here.
        # This method gets called ONCE after opening a connection to prepare for it.
        pass
