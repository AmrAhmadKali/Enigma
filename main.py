# taken from: https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/complex_example.py
import tkinter
import tkinter.messagebox
import customtkinter

from core.main import App
from core.registry import Registry

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

paths = ["core"]

if __name__ == "__main__":
    Registry.load_instances(paths)
    Registry.inject_all(paths)
    Registry.get_instance("app").init(paths, Registry)
    Registry.pre_start_all()
    Registry.start_all()
    for x, y in Registry._registry.items():
        print(x, y)
    Registry.get_instance("app").mainloop()