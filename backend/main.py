# taken from: https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py
from meta.registry import Registry
paths = ["core"]

if __name__ == "__main__":
    Registry.load_instances(paths)
    Registry.inject_all(paths)
    Registry.get_instance("app").init(paths, Registry)
    Registry.pre_start_all()
    Registry.start_all()
    for x, y in Registry._registry.items():
        print(f"Loading '{x}' from '{y.module_name}'..")
    print("Starting Websocket Server...")
    Registry.get_instance("app").startup()