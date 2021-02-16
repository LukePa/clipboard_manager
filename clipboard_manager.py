import pickle, os
import tkinter as tk
from main_menu import Main_menu


class Clip_management_page(tk.Frame):
    def __init__(self, clips_file_name, controller):
        super().__init__(controller)
        self.setup_initial_variables()
        self.controller = controller
        self.model = clip_board_manager_model(self, clips_file_name)
        self.create_create_clip_button()
        self.create_wipe_clips_button()
        self.create_main_menu_button()


    def setup_initial_variables(self):
        self.initial_y = 2
        self.buttons_list = []
        self.current_y = self.initial_y


    def create_create_clip_button(self):
        new_clip_button = tk.Button(self)
        new_clip_button["text"] = "<Click to create new clip>"
        new_clip_button["command"] = self.model.create_new_clip_button_from_clipboard
        new_clip_button.grid(column = 0, row = 0)
        clips_label = tk.Label(self)
        clips_label["text"] = "Created clips:"
        clips_label.grid(column = 0, row = 1, columnspan = 3)


    def create_wipe_clips_button(self):
        wipe_clips_button = tk.Button(self)
        wipe_clips_button["text"] = "<Click here to wipe clips>"
        wipe_clips_button["command"] = self.model.wipe_clips
        wipe_clips_button.grid(column = 1, row = 0)


    def create_main_menu_button(self):
        main_menu_button = tk.Button(self)
        main_menu_button["text"] = "<Click here to select a clipset>"
        main_menu_button["command"] = self.controller.load_main_menu
        main_menu_button.grid(column=2, row = 0)


    def create_new_clip_button(self, message):
        clip_button = tk.Button(self)
        clip_button["text"] = message
        clip_button["command"] = lambda: self.model.write_to_clipboard(message)
        clip_button.grid(column = 0, row = self.current_y, columnspan = 3)
        delete_clip_button = tk.Button(self)
        delete_clip_button["text"] = "x"
        delete_clip_button["command"] = lambda: self.model.remove_clip(message)
        delete_clip_button.grid(column = 3, row = self.current_y)
        self.current_y += 1
        self.buttons_list.append(clip_button)
        self.buttons_list.append(delete_clip_button)
        

    def destroy_current_buttons(self):
        self.current_y = self.initial_y
        for button in self.buttons_list:
            button.destroy()
        self.buttons_list = []
        

    



class clip_board_manager_model(object):

    def __init__(self, clip_manager_page, clips_file_name):
        self.ui = clip_manager_page
        self.setup_initial_variables()
        self.load_new_clip_file(clips_file_name)
        

    def setup_initial_variables(self):
        self.clips_list = []
        try:
            os.mkdir('./clip_files')
        except:
            1+1


    def load_new_clip_file(self, filename):
        self.ui.destroy_current_buttons()
        self.save_file_path = './clip_files/' + filename + ".pk"
        try:
            f = open(self.save_file_path, "rb")
            self.clips_list = pickle.load(f)
            f.close()
        except:
            self.clips_list = []
            self.update_saved_clips()
        self.populate_clip_buttons()


    def update_saved_clips(self):
        f = open(self.save_file_path, "wb")
        pickle.dump(self.clips_list, f)
        f.close()


    def wipe_clips(self):
        os.remove(self.save_file_path)
        self.ui.controller.load_main_menu()


    def remove_clip(self, clip_str):
        self.ui.destroy_current_buttons()
        self.clips_list.remove(clip_str)
        self.update_saved_clips()
        self.populate_clip_buttons()


    def write_to_clipboard(self, input_string):
        if type(input_string) != str:
            raise TypeError("Input String must be a string")
        self.ui.clipboard_clear()
        self.ui.clipboard_append(input_string)


    def create_new_clip_button_from_clipboard(self):
        """Verifies clipboard is valid before creating a new clip button"""
        try:
            message = self.ui.clipboard_get()
            if message == "":
                return None
            elif message in self.clips_list:
                return None
            self.ui.create_new_clip_button(message)
            self.clips_list.append(message)
            self.update_saved_clips()
        except:
            1+1


    def populate_clip_buttons(self):
        for clip in self.clips_list:
            self.ui.create_new_clip_button(clip)
        
    
  
