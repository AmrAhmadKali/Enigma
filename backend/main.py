import asyncio

from meta.registry import Registry

paths = ["core"]


async def main():
    Registry.load_instances(paths)
    Registry.inject_all()
    Registry.get_instance("app").init(paths, Registry)
    await Registry.get_instance('db').connect_db()
    Registry.pre_start_all()
    Registry.start_all()
    for x, y in Registry.get_all_instances().items():
        print(f"Loaded '{x}' from '{y.module_name}'..")
    print("Starting Websocket Server...")
    await Registry.get_instance("app").startup()


if __name__ == '__main__':
    asyncio.run(main())
