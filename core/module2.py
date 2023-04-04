import customtkinter
import main
from core.base_module import Base_Module
from core.decorators import instance


@instance("thisisarandommod")
class Addon2(Base_Module):
    app: main.App

    def inject(self, reg):
        self.app = reg.get_instance("app")

    def pre_start(self):
        self.entry = customtkinter.CTkEntry(self.app, placeholder_text="CTkEntry")
        self.main_button_1 = customtkinter.CTkButton(master=self.app, fg_color="transparent", border_width=2,
                                             text_color=("gray10", "#DCE4EE"))
        self.textbox = customtkinter.CTkTextbox(self.app, width=250)
    def start(self):
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")


        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox

        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")


