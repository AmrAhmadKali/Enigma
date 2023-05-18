import importlib
import itertools
import os
import re
from pathlib import Path
from typing import List

from meta.base_module import BaseModule
from meta.dict_object import DictObject


# Whatever you do, do not touch this file.
# It WILL end in a horrible bloodbath.


def flatmap(func, *iterable):
    return itertools.chain.from_iterable(map(func, *iterable))


def get_attrs(obj):
    attrs = {}
    for cls in obj.__class__.__mro__:
        attrs.update(cls.__dict__.items())
    attrs.update(obj.__class__.__dict__.items())
    return attrs


# noinspection PyUnresolvedReferences
class Registry:
    """
    Central Place for managing dependencies for the entire project.
    """
    _registry = {}
    logger = None

    @classmethod
    def inject_all(cls) -> None:
        """
        Inject Dependencies into all @instance()'s
        """
        for key in cls._registry:
            m = cls._registry[key]
            if 'inject' in get_attrs(m):
                m.inject(cls)

    @classmethod
    def pre_start_all(cls) -> None:
        """
        Run all initialisations for instances, which may be used by other modules
        """
        mods = cls.get_instance("app").modules
        for key in cls._registry:
            if str(cls._registry[key].module_name).split(".")[0] not in mods:
                continue
            m = cls._registry[key]
            if 'pre_start' in get_attrs(m):
                m.pre_start()

    @classmethod
    def start_all(cls) -> None:
        """
        Run final initialisations, different modules should not depend on stuff done in these.
        """
        mods = cls.get_instance("app").modules
        for key in cls._registry:
            if str(cls._registry[key].module_name).split(".")[0] not in mods:
                continue
            m = cls._registry[key]
            if 'start' in get_attrs(m):
                m.start()

    @classmethod
    def get_instance(cls, name: str, is_optional=False) -> BaseModule:
        """
        :param name: Name of the Module which is being requested
        :param is_optional: return None if True, otherwise throw error and exit.
        :return:
        """
        instance = cls._registry.get(name)
        if instance or is_optional:
            return instance
        else:
            raise Exception("Missing required dependency '%s'" % name)

    @classmethod
    def get_all_instances(cls) -> dict:
        return cls._registry

    @classmethod
    def add_instance(cls, name: str, inst: BaseModule, override=False) -> None:
        """
        Inject Dependencies into all @instance()'s
        :param name: Name of the Instance to be added
        :param inst: reference to the Instance which is being added
        :param override: True if an existing name with possibly other instance should be overriden.
        """
        name = cls.format_name(name)

        inst.module_name = Registry.get_module_name(inst)
        inst.module_dir = Registry.get_module_dir(inst)
        if not override and name in cls._registry:
            raise Exception("Overriding '%s' with new instance" % name)
        elif override and name not in cls._registry:
            raise Exception("No instance '%s' to override" % name)
        cls._registry[name] = inst

    @classmethod
    def format_name(cls, name: str) -> str:
        # camel-case to snake-case
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @classmethod
    def load_instances(cls, parent_dirs: List[str | Path]) -> None:
        """
        :param parent_dirs: List of Directories to check for modules
        """
        # get all subdirectories
        dirs = flatmap(lambda x: os.walk(x, followlinks=True), parent_dirs)
        dirs = filter(lambda y: not y[0].endswith("__pycache__"), dirs)

        def get_files(tup):
            return map(lambda x: os.path.join(tup[0], x), tup[2])

        # get files from subdirectories
        files = flatmap(get_files, dirs)
        files = filter(lambda z: z.endswith(".py") and not z.endswith("__init__.py"), files)

        # load files as modules
        for file in files:
            cls.load_module(file)

    @classmethod
    async def setup_storage(cls, storage: DictObject) -> None:
        """
        :param storage: Allocated storage for the connection which needs initialisation
        """
        mods = cls.get_instance("app").modules
        for key in cls._registry:
            m = cls._registry[key]
            if str(m.module_name).split(".")[0] not in mods:
                continue
            if 'setup' in get_attrs(m):
                await m.setup(storage)

    @classmethod
    def load_module(cls, file: Path) -> None:
        # strip the extension
        file = file[:-3]
        importlib.import_module(file.replace("\\", ".").replace("/", "."))

    @classmethod
    def get_module_name(cls, inst: BaseModule) -> str:
        parts = inst.__module__.split(".")
        if parts[0] == "core":
            return parts[0] + "." + parts[1]
        # last name in directory path should be first part, then the next name should be last part
        if parts[0] == "modules":
            return parts[1] + "." + parts[2]
        else:
            return ".".join(parts[:-1])

    @classmethod
    def get_module_dir(cls, inst: BaseModule) -> str:
        parts = inst.__module__.split(".")
        return "." + os.sep + os.sep.join(parts[:-1])

    @classmethod
    def clear(cls) -> None:
        """
        Reset the registry
        :return:
        """
        cls._registry = {}
