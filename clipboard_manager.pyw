import pickle, os
import tkinter as tk


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clipboard Manager")
        self.current_frame = None
        self.load_clip_management_page("testing")
        

    def load_clip_management_page(self, clips_file_name):
        if self.current_frame != None:
            self.current_frame.destroy()
        c = Clip_management_page(clips_file_name, self)
        c.grid()
        self.current_frame = c
    


class Clip_management_page(tk.Frame):
    def __init__(self, clips_file_name, controller):
        super().__init__(controller)
        self.setup_initial_variables()
        self.create_create_clip_button()
        self.create_wipe_clips_button()
        self.load_new_clip_file(clips_file_name)


    def setup_initial_variables(self):
        self.initial_y = 2
        self.buttons_list = []
        self.current_y = self.initial_y
        try:
            os.mkdir('./clip_files')
            print(os.getcwd())
        except:
            1+1


    def load_new_clip_file(self, filename):
        self.destroy_current_buttons()
        self.save_file_path = './clip_files/' + filename + ".pk"
        try:
            f = open(self.save_file_path, "rb")
            self.clips_list = pickle.load(f)
            f.close()
        except:
            self.clips_list = []
            self.update_saved_clips()
        for clip in self.clips_list:
            self.create_new_clip_button(clip)
        

    def update_saved_clips(self):
        f = open(self.save_file_path, "wb")
        pickle.dump(self.clips_list, f)
        f.close()


    def wipe_clips(self):
        self.destroy_current_buttons()
        f = open(self.save_file_path, "wb")
        f.close()


    def create_create_clip_button(self):
        new_clip_button = tk.Button(self)
        new_clip_button["text"] = "<Click to create new clip>"
        new_clip_button["command"] = self.create_new_clip_button_from_clipboard
        new_clip_button.grid(column = 0, row = 0)
        clips_label = tk.Label(self)
        clips_label["text"] = "Created clips:"
        clips_label.grid(column = 0, row = 1, columnspan = 2)


    def create_wipe_clips_button(self):
        wipe_clips_button = tk.Button(self)
        wipe_clips_button["text"] = "<Click here to wipe clips>"
        wipe_clips_button["command"] = self.wipe_clips
        wipe_clips_button.grid(column = 1, row = 0)


    def create_new_clip_button(self, message):
        clip_button = tk.Button(self)
        clip_button["text"] = message
        clip_button["command"] = lambda: self.write_to_clipboard(message)
        clip_button.grid(column = 0, row = self.current_y, columnspan = 2)
        self.current_y += 1
        self.buttons_list.append(clip_button)


    def create_new_clip_button_from_clipboard(self):
        """Verifies clipboard is valid before creating a new clip button"""
        message = self.clipboard_get()
        if message == "":
            return None
        elif message in self.clips_list:
            return None
        self.create_new_clip_button(message)
        self.clips_list.append(message)
        self.update_saved_clips()


    def destroy_current_buttons(self):
        self.current_y = self.initial_y
        for button in self.buttons_list:
            button.destroy()


    def write_to_clipboard(self, input_string):
        if type(input_string) != str:
            raise TypeError("Input String must be a string")
        self.clipboard_clear()
        self.clipboard_append(input_string)


class Test(tk.Frame):
    def __init__(self):
        super().__init__()
        self.label = tk.Label(self, text="Test")
        self.label.grid(column = 0, row = 6)
        self.label = tk.Label(self, text="Test2")
        self.label.grid(column = 0, row = 5)




app = Application()
app.mainloop()

        
