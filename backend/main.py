import asyncio
import typing

if typing.TYPE_CHECKING:
    from core.db import DB
    from core.main import Server
from meta.registry import Registry

paths = ["core"]


async def main():
    Registry.load_instances(paths)
    Registry.inject_all()
    app: Server = Registry.get_instance("app")
    db: DB = Registry.get_instance('db')

    app.init(paths, Registry)
    await db.connect_db()
    Registry.pre_start_all()
    Registry.start_all()

    for x, y in Registry.get_all_instances().items():
        print(f"Loaded '{x}' from '{y.module_name}'..")
    print("Starting Websocket Server...")
    await app.startup()


if __name__ == '__main__':
    asyncio.run(main())
