from meta.registry import Registry
paths = ["core"]

if __name__ == "__main__":
    Registry.load_instances(paths)
    Registry.inject_all()
    Registry.get_instance("app").init(paths, Registry)
    Registry.pre_start_all()
    Registry.start_all()
    for x, y in Registry.get_all_instances().items():
        print(f"Loaded '{x}' from '{y.module_name}'..")
    print("Starting Websocket Server...")
    Registry.get_instance("app").startup()
