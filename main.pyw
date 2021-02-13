import tkinter as tk
from main_menu import Main_menu
from clipboard_manager import Clip_management_page


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clipboard Manager")
        self.current_frame = None
        self.load_main_menu()
                

    def load_clip_management_page(self, clips_file_name):
        if self.current_frame != None:
            self.current_frame.destroy()
        c = Clip_management_page(clips_file_name, self)
        c.grid()
        self.current_frame = c


    def load_main_menu(self):
        if self.current_frame != None:
            self.current_frame.destroy()
        main_menu = Main_menu(self)
        main_menu.grid()
        self.current_frame = main_menu


app = Application()
app.mainloop()
