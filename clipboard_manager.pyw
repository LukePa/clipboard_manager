import tkinter, pickle


class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clipboard Manager")
        self.create_create_clip_button()
        self.create_wipe_clips_button()
        self.save_file_name = "saved_clips.pk"
        try:
            f = open(self.save_file_name, "rb")
            self.clips_list = pickle.load(f)
            f.close()
        except:
            self.clips_list = []
            self.update_saved_clips()
        self.buttons_list = []
        self.current_y = 2
        for clip in self.clips_list:
            self.create_new_clip_button(clip)



    def update_saved_clips(self):
        f = open(self.save_file_name, "wb")
        pickle.dump(self.clips_list, f)
        f.close()
        


    def create_create_clip_button(self):
        self.new_clip_button = tkinter.Button()
        self.new_clip_button["text"] = "<Click to create new clip>"
        self.new_clip_button["command"] = self.create_new_clip_button_from_clipboard
        self.new_clip_button.grid(column = 0, row = 0)
        self.clips_label = tkinter.Label()
        self.clips_label["text"] = "Created clips:"
        self.clips_label.grid(column = 0, row = 1, columnspan = 2)


    def create_wipe_clips_button(self):
        self.wipe_clips_button = tkinter.Button()
        self.wipe_clips_button["text"] = "<Click here to wipe clips>"
        self.wipe_clips_button["command"] = self.destroy_current_buttons
        self.wipe_clips_button.grid(column = 1, row = 0)


    def destroy_current_buttons(self):
        self.current_y = 2
        self.wipe_clips()
        for button in self.buttons_list:
            button.destroy()
        

    def wipe_clips(self):
        f = open(self.save_file_name, "wb")
        f.close()


    def write_to_clipboard(self, input_string):
        if type(input_string) != str:
            raise TypeError("Input String must be a string")
        self.clipboard_clear()
        self.clipboard_append(input_string)


    def create_new_clip_button_from_clipboard(self):
        message = self.clipboard_get()
        if message == "":
            return None
        elif message in self.clips_list:
            return None
        self.create_new_clip_button(message)
        self.clips_list.append(message)
        self.update_saved_clips()


    def create_new_clip_button(self, message):
        clip_button = tkinter.Button()
        clip_button["text"] = message
        clip_button["command"] = lambda: self.write_to_clipboard(message)
        clip_button.grid(column = 0, row = self.current_y, columnspan = 2)
        self.current_y += 1
        self.buttons_list.append(clip_button)





app = Application()
app.mainloop()

        
