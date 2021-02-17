import pickle, os
import tkinter as tk
from main_menu import Main_menu


class Clip_management_page(tk.Frame):
    def __init__(self, clips_file_name, controller):
        super().__init__(controller)
        self.setup_initial_variables()
        self.controller = controller
        self.model = Clip_board_manager_model(self, clips_file_name)
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

    def create_new_clip_button(self, clip):
        clip_button = tk.Button(self)
        clip_button["text"] = clip.get_title()
        clip_button["command"] = lambda: self.model.write_to_clipboard(clip.get_message())
        clip_button.grid(column = 0, row = self.current_y, columnspan = 3)
        delete_clip_button = tk.Button(self)
        delete_clip_button["text"] = "x"
        delete_clip_button["command"] = lambda: self.model.remove_clip(clip)
        delete_clip_button.grid(column = 3, row = self.current_y)
        self.current_y += 1
        self.buttons_list.append(clip_button)
        self.buttons_list.append(delete_clip_button)

    def destroy_current_buttons(self):
        self.current_y = self.initial_y
        for button in self.buttons_list:
            button.destroy()
        self.buttons_list = []
        


class Clip_board_manager_model(object):

    def __init__(self, clip_manager_page, clips_file_name):
        self.ui = clip_manager_page
        self.load_new_clip_list(clips_file_name)

    def load_new_clip_list(self, filename):
        self.ui.destroy_current_buttons()
        self.clips_list = Clip_list(filename)
        self.populate_clip_buttons()

    def wipe_clips(self):
        self.clips_list.delete_save()
        self.ui.controller.load_main_menu()

    def remove_clip(self, clip):
        self.ui.destroy_current_buttons()
        self.clips_list.remove(clip)
        self.populate_clip_buttons()

    def write_to_clipboard(self, input_string):
        if type(input_string) != str:
            raise TypeError("Input String must be a clip")
        self.ui.clipboard_clear()
        self.ui.clipboard_append(input_string)

    def get_all_clip_messages(self):
        message_list = []
        for clip in self.clips_list:
            message_list.append(clip.get_message())
        return message_list

    def create_new_clip_button_from_clipboard(self):
        """Verifies clipboard is valid before creating a new clip button"""
        try:
            message = self.ui.clipboard_get()
            if message == "":
                return None
            elif message in self.get_all_clip_messages():
                return None
            clip = Clip(message)
            self.ui.create_new_clip_button(clip)
            self.clips_list.append(clip)
        except Exception as error:
            print(error)

    def populate_clip_buttons(self):
        for clip in self.clips_list:
            self.ui.create_new_clip_button(clip)


class Clip_list(list):

    def __init__(self, filename):
        super().__init__()
        self.filepath = './clip_files/' + filename + ".pk"
        self.load_new_clip_file()
        self.update_saved_clips()

    def load_new_clip_file(self):
        try:
            os.mkdir('./clip_files')
        except:
            1+1
        try:
            f = open(self.filepath, "rb")
            clips_list = pickle.load(f)
            super().__init__(clips_list)
            f.close()
        except Exception as err:
            self.update_saved_clips()
        self.convert_strings_to_clips()

    def update_saved_clips(self):
        f = open(self.filepath, "wb")
        pickle.dump(self, f)
        f.close()

    def convert_strings_to_clips(self):
        for i in range(len(self)):
            clip = self[i]
            if type(clip) == str:
                clipObj = Clip(clip)
                self[i] = clipObj
        self.update_saved_clips()

    def delete_save(self):
        os.remove(self.filepath)

    def append(self, item):
        super().append(item)
        self.update_saved_clips()

    def remove(self, item):
        super().remove(item)
        self.update_saved_clips()


class Clip(object):

    def __init__(self, message):
        self._message = message
        self._title = ""

    def get_title(self):
        if self._title:
            return self._title
        else:
            return self._message

    def set_title(self, title):
        if type(title) != str:
            raise TypeError
        else:
            self._title = title

    def get_message(self):
        return self._message
        
        
    
  
