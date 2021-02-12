import tkinter as tk
from tkinter import simpledialog
import os


class Main_menu(tk.Frame):

    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.setup_buttons()
        self.setup_labels()
        self.setup_clips_list_box()
        self.create_all_clips_list_buttons()


    def setup_buttons(self):
        create_clips_set_button = tk.Button(self)
        create_clips_set_button["text"] = "Create new clips set"
        create_clips_set_button.grid(row=0, column=0)
        create_clips_set_button["command"] = self.create_clips_list_from_button


    def setup_labels(self):
        clips_label = tk.Label(self)
        clips_label["text"] = "Created clips lists:"
        clips_label.grid(row=1, column=0)


    def setup_clips_list_box(self):
        self.clips_list_frame = tk.Frame(self)
        self.clips_list_frame.grid(row=2, column=0)


    def create_clips_list_select_button(self, filename):
        """Filename should not have file extension"""
        button = tk.Button(self.clips_list_frame)
        button["text"] = filename
        button["command"] = lambda: self.controller.load_clip_management_page(filename)
        button.grid()


    def create_all_clips_list_buttons(self):
        try:
            os.chdir("clip_files")
        except:
            os.mkdir("clip_files")
        file_list = os.listdir()
        os.chdir("../")
        for file in file_list:
            if not os.path.isfile('clip_files/' + file):
                continue
            if not file.endswith(".pk"):
                continue
            name = file[:-3]
            self.create_clips_list_select_button(name)


    def create_clips_list_from_button(self):
        clipset_name = simpledialog.askstring(title = "Clipset creation",
                                              prompt = "Enter clipset name:")
        if clipset_name:
            self.create_clips_list_select_button(clipset_name)
            self.controller.load_clip_management_page(clipset_name)
        
    
        
        
