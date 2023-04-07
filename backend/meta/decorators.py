# taken from: https://stackoverflow.com/a/26151604/280574
from meta.registry import Registry


def parameterized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parameterized
def instance(cls, name=None, override=False):
    instance_name = name if name else cls.__name__
    Registry.add_instance(instance_name, cls(), override)
    return cls
