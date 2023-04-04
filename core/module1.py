import customtkinter
from customtkinter import CTkFrame, CTkTabview

import main
from core.base_module import Base_Module
from core.decorators import instance


@instance("addon1")
class Addon(Base_Module):
    app: main.App

    def inject(self, reg):
        self.app = reg.get_instance("app")

    def pre_start(self):
        self.tabview = CTkTabview(self.app, width=250)

    def start(self):
        # self.tabview = customtkinter.CTkTabview(self.container, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)
