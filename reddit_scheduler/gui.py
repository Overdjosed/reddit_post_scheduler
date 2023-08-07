import customtkinter as ctk
from tkinter import filedialog, messagebox
import db as ctrl
from PIL import Image
from os import getcwd, remove, path
import cv2
import time
import praw

ctk.set_appearance_mode("dark-blue")

class VideoC:
    def __init__(self, video_source = 0):
        # Open the video with cv2
        self.vid = cv2.VideoCapture(video_source)
        # Check if video is open
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Attributes
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)
        self.delay = round(1000 / self.fps)

    def get_frame(self):
        # Used tu get the next frame
        if self.vid.isOpened():
            # ret is a bool that indicates if it is open
            ret, frame = self.vid.read()
            if ret:
                # Return Frame
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                # If it is not possible to read, start again
                self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                return self.get_frame()
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

class App:
    VIDEO_FORMATS, PHOTO_FORMATS = ["mp4", "mov"], ["jpg", "jpeg", "png", "gif", "webp"]

    def __init__(self, root):
        # General Division
        self.root = root
        self.times = 0
        self.media = []
        self.images_to_delete = []
        self.user_entries = {"ClientId": None, "ClientSecret": None, "UserAgent": None, "Password": None, "Username": None}
        self.post_entries = {"Day":None, "Month": None, "Hour":None, "Title": None, "URL": None, "Media": [], "User":None, "Subreddit": None, "Checkbox": None}
        self.tab_left = ctk.CTkTabview(master = root, width = 500, height = 430)
        self.tab_left.grid(row = 1, column = 1, padx = 10)
        self.frame_right = ctk.CTkFrame(master= root, width = 500, height = 450)
        self.frame_right.grid(row = 1, column = 2)
        self.db = ctrl.Controlador()

        self.subreddit_frame = self.tab_left.add("Subreddits")
        user_frame = self.tab_left.add("Users")
        self.post_frame = self.tab_left.add("Posts")

        post_label = ctk.CTkLabel(self.post_frame, text = "Delete:")
        post_label.grid(row = 1, column = 1, padx = 10, pady = 30)
        self.post_to_delete = ctk.CTkOptionMenu(self.post_frame, values= self.db.show_database("Scheduler"), width= 220)
        self.post_to_delete.grid(row = 1, column = 2, padx = 10, pady = 10)
        add_button = ctk.CTkButton(self.post_frame, text = "Submit", command=self.delete_post) # TODO: COMMAND
        add_button.grid(row = 1, column = 3, padx = 10, pady = 10)

        # Subreddits GUI
        sbt = ctk.CTkLabel(self.subreddit_frame, text = "Add")
        sbt.grid(row = 2, column = 1, padx = 40, pady = 40)
        self.entrysub = ctk.CTkEntry(self.subreddit_frame)
        self.entrysub.grid(row = 2, column = 2, padx = 10, pady = 30)
        add_button = ctk.CTkButton(self.subreddit_frame, text = "Submit",command = self.add_subreddit) #TODO COMMAND
        add_button.grid(row = 2, column = 3, padx = 10, pady = 10)

        dele = ctk.CTkLabel(self.subreddit_frame, text = "Delete:")
        dele.grid(row = 4, column = 1, padx = 10, pady = 30)
        self.sbdelete = ctk.CTkOptionMenu(self.subreddit_frame, values= self.db.show_database("Subreddits"))
        self.sbdelete.grid(row = 4, column = 2, padx = 10, pady = 10)
        add_button = ctk.CTkButton(self.subreddit_frame, text = "Submit", command=self.delete_subreddit) # TODO: COMMAND
        add_button.grid(row = 4, column = 3, padx = 10, pady = 10)

        add_user_frame = ctk.CTkFrame(user_frame)
        add_user_frame.grid(row = 1, padx = 20, pady = 20)
        user_labels = ["ClientId", "ClientSecret", "UserAgent", "Password", "Username"]

        for i, label_text in enumerate(user_labels, start=1):
            label = ctk.CTkLabel(add_user_frame, text=label_text + ":")
            label.grid(row=i, column=1, padx=5, pady=5)

            self.user_entries[label_text] = ctk.CTkEntry(add_user_frame, width=300)
            self.user_entries[label_text].grid(row=i, column=2, padx=5, pady=5)


        add_button = ctk.CTkButton(add_user_frame, text = "Submit", width = 300, command=self.add_user_button)#TODO: COMMAND
        add_button.grid(row = 9, column = 2, padx = 5, pady = 5)

        self.us_del_frame = ctk.CTkFrame(user_frame)
        self.us_del_frame.grid(row = 2)

        # USER TO DELETE
        delelbl = ctk.CTkLabel(self.us_del_frame, text = "Delete:")
        delelbl.grid(row = 1, column = 1, padx = 20, pady = 10)

        self.userdelete = ctk.CTkOptionMenu(self.us_del_frame, values= self.db.show_database("Users"))
        self.userdelete.grid(row = 1, column = 2, padx = 10, pady = 10)

        del_user_button = ctk.CTkButton(self.us_del_frame, text = "Submit", command= self.delete_user_button)# TODO: COMMAND
        del_user_button.grid(row = 1, column = 3, padx = 10, pady = 10)



        ## Division for Content, calendar and entries
        self.intraframe_up = ctk.CTkFrame(master = self.frame_right, width = 500, height = 250)
        self.intraframe_up.grid(row = 1, column = 1, padx = 15, pady = 15)

        self.intraframe_down = ctk.CTkFrame(master = self.frame_right, width= 500, height= 250)
        self.intraframe_down.grid(row = 2, column = 1)

        ### Creating Frame for Button
        self.scrollable_images = ctk.CTkScrollableFrame(master = self.intraframe_up, orientation= "horizontal", width = 240, height= 125)
        self.scrollable_images.grid(row =1, column = 1)
        self.add_media_frame = ctk.CTkFrame(master = self.scrollable_images, width = 125, height= 125)
        self.add_media_frame.pack(pady=10, padx=10, fill="y", expand=True)

        #### Button for Content
        media_plus_img = ctk.CTkImage(Image.open("add_media.png"), size=(100, 125))
        self.add_media = ctk.CTkButton(text= "",master = self.add_media_frame,image = media_plus_img, command= self.select_file, width = 124, height = 125)
        self.add_media.pack(expand=True, fill="both")

        ## Calendar for dd/mm,hh
        self.cal = ctk.CTkFrame(master = self.intraframe_up)
        self.cal.grid(row = 1, column = 2, padx  = 10)
        self.calendar(self.cal)

        ## Title of Post
        title = ctk.CTkLabel(master = self.intraframe_down, text = "Title:")
        title.grid(row = 1, column = 1, pady = 10, padx =10)
        self.post_entries["Title"] = ctk.CTkEntry(master = self.intraframe_down, width = 340)
        self.post_entries["Title"].grid(row = 1,column = 2, pady  = 10, padx = 20)


        ## Title of URL
        url = ctk.CTkLabel(master = self.intraframe_down, text = "URL:")
        url.grid(row = 2, column = 1, pady = 3, padx =10)
        self.post_entries["URL"] = ctk.CTkEntry(master = self.intraframe_down, width = 340)
        self.post_entries["URL"].grid(row = 2,column = 2, pady  = 10, padx = 20)

        # Bombobox Menu Subreddits
        users_lbl = ctk.CTkLabel(master = self.intraframe_down, text = "Subreddit:")
        users_lbl.grid(row = 4, column = 1, pady = 3, padx =10)
        self.post_entries["Subreddit"] = ctk.CTkComboBox(master = self.intraframe_down, values = self.db.show_database("Subreddits"), width= 340)
        self.post_entries["Subreddit"].grid(row = 4, column  = 2, pady  = 10, padx = 20)

        # Option Menu Users
        users_lbl = ctk.CTkLabel(master = self.intraframe_down, text = "User:")
        users_lbl.grid(row = 5, column = 1, pady = 3, padx =10)
        self.post_entries["User"] = ctk.CTkOptionMenu(master = self.intraframe_down, values = self.db.show_database("Users"), width= 340)
        self.post_entries["User"].grid(row = 5, column  = 2, pady  = 10, padx = 20)

        ## CheckBox
        self.post_entries["Checkbox"] = ctk.CTkCheckBox(master = self.intraframe_down, text = "NSFW")
        self.post_entries["Checkbox"].grid(row = 6, column = 1, padx = 30, sticky = "nsew")

        ## Submit_button
        submit_scheduler = ctk.CTkButton(master = self.intraframe_down, text = "Submit", command= self.on_submit_post)
        submit_scheduler.grid( row = 6, column = 2, pady = 10)

    def delete_post(self):
        splitted = self.post_to_delete.get().split(":")
        splitted = splitted[1].split(",")
        self.db.delete_element(splitted[0][1:],"Scheduler")
        print(f"Scheduler a Borrar: {splitted[0][1:]}")

        self.post_to_delete.destroy()


        self.post_to_delete = ctk.CTkOptionMenu(self.post_frame, values= self.db.show_database("Scheduler"), width= 220)
        self.post_to_delete.grid(row = 1, column = 2, padx = 10, pady = 10)

    def calendar(self,root):
        button_date = ctk.CTkButton(text ="Schedule date",master = root, command=self.on_calendar_button_click)
        button_date.grid(row  =1, column = 1)

    def on_calendar_button_click(self):
        new_window = ctk.CTkFrame(self.intraframe_up)
        new_window.grid(row  =1, column = 2, padx = 5, pady = 5)

        day_descr = ctk.CTkLabel(new_window, text = "Day:")
        month_descr = ctk.CTkLabel(new_window, text = "Month:")
        hour_descr = ctk.CTkLabel(new_window, text = "Hour:")

        day_descr.grid(row = 1, column = 1, padx = 3)
        month_descr.grid(row = 2, column = 1, padx = 3)
        hour_descr.grid(row = 3, column = 1, padx = 3)

        # Use localtime to subtract past hours
        lt = time.localtime(time.time())
        day = ctk.CTkOptionMenu(master = new_window, values=[str(i) for i in range(lt.tm_mday,32)])
        month = ctk.CTkOptionMenu(master = new_window,text_color="black", values=[str(i) for i in range(lt.tm_mon,13)])
        hour = ctk.CTkOptionMenu(master = new_window,text_color="black", values=[f"{str(i)}:00" for i in range(0,24)])

        self.post_entries["Day"] = day
        self.post_entries["Month"] = month
        self.post_entries["Hour"] = hour

        day.grid(row = 1, column = 2, pady = 1.5, sticky = 'nsew')
        month.grid(row = 2, column = 2, pady = 1.5,  sticky = 'nsew')
        hour.grid(row = 3, column = 2, pady = 1.5, sticky = 'nsew')

    def delete_subreddit(self):
        print(f"Subreddit a Borrar: {self.sbdelete.get()}")
        self.db.delete_element(self.sbdelete.get(),"Subreddits")
        self.post_entries["Subreddit"].destroy()
        self.post_entries["User"].destroy()
        self.sbdelete.destroy()
        self.post_entries["Subreddit"] = ctk.CTkComboBox(master = self.intraframe_down, values = self.db.show_database("Subreddits"), width= 340)
        self.post_entries["Subreddit"].grid(row = 4, column  = 2, pady  = 3, padx = 10)
        self.post_entries["User"] = ctk.CTkOptionMenu(master = self.intraframe_down, values = self.db.show_database("Users"), width= 340)
        self.post_entries["User"].grid(row = 5, column  = 2, pady  = 3, padx = 10)
        self.sbdelete = ctk.CTkOptionMenu(self.subreddit_frame, values= self.db.show_database("Subreddits"))
        self.sbdelete.grid(row = 4, column = 2, padx = 10, pady = 10)
        return self.sbdelete.get()

    def add_subreddit(self):
        print(f"Subreddit agregado: {self.entrysub.get()}")
        self.db.add_element(str(self.entrysub.get()),"Subreddits")

        self.post_entries["Subreddit"] = ctk.CTkComboBox(master = self.intraframe_down, values = self.db.show_database("Subreddits"), width= 340)
        self.post_entries["Subreddit"].grid(row = 4, column  = 2, pady  = 3, padx = 10)
        self.sbdelete = ctk.CTkOptionMenu(self.subreddit_frame, values= self.db.show_database("Subreddits"))
        self.sbdelete.grid(row = 4, column = 2, padx = 10, pady = 10)
        return self.entrysub.get()

    def add_user_button(self):
        data = []
        for key, value in self.user_entries.items():
            data.append(value.get())
            print(key, ":", value.get() if type(value) != list else value)
        self.db.add_element(data,"Users")
        self.userdelete = ctk.CTkOptionMenu(self.us_del_frame, values= self.db.show_database("Users"))
        self.userdelete.grid(row = 1, column = 2, padx = 10, pady = 10)
        self.post_entries["Subreddit"] = ctk.CTkComboBox(master = self.intraframe_down, values = self.db.show_database("Subreddits"), width= 340)
        self.post_entries["Subreddit"].grid(row = 4, column  = 2, pady  = 3, padx = 10)
        self.post_entries["User"] = ctk.CTkOptionMenu(master = self.intraframe_down, values = self.db.show_database("Users"), width= 340)
        self.post_entries["User"].grid(row = 5, column  = 2, pady  = 3, padx = 10)
        return self.user_entries

    def delete_user_button(self):
        print(f"User a borrar: {self.userdelete.get()}")
        self.db.delete_element(value = str(self.userdelete.get()), type = "Users")
        self.post_entries["Subreddit"].destroy()
        self.post_entries["User"].destroy()
        self.userdelete.destroy()
        self.post_entries["Subreddit"] = ctk.CTkComboBox(master = self.intraframe_down, values = self.db.show_database("Subreddits"), width= 340)
        self.post_entries["Subreddit"].grid(row = 4, column  = 2, pady  = 3, padx = 10)
        self.post_entries["User"] = ctk.CTkOptionMenu(master = self.intraframe_down, values = self.db.show_database("Users"), width= 340)
        self.post_entries["User"].grid(row = 5, column  = 2, pady  = 3, padx = 10)
        self.userdelete = ctk.CTkOptionMenu(self.us_del_frame, values= self.db.show_database("Users"))
        self.userdelete.grid(row = 1, column = 2, padx = 10, pady = 10)
        return self.userdelete

    def on_submit_post(self):
        for key, value in self.post_entries.items():
            print(key, ":", value.get() if type(value) != list else value)
        data = []
        for element in ["Media", "Subreddit", "Title", "URL", "Date", "Hour","User", "Checkbox"]:

            if element == "Date":
                day = self.post_entries["Day"].get()
                self.post_entries["Day"]
                month = self.post_entries["Month"].get()
                self.post_entries["Month"]
                self.post_entries["Month"]
                data.append(f"{day}/{month}/{str(time.localtime(time.time()).tm_year)}")
            elif type(self.post_entries[element]) == list:
                cadena_files = ""
                for file in self.post_entries[element]:
                    cadena_files += f"@@{file}"
                data.append(cadena_files)
                self.post_entries[element].clear()
            else:
                data.append(self.post_entries[element].get())
                self.post_entries[element]

        self.add_media_frame.forget()
        frame = ctk.CTkFrame(self.scrollable_images, width=100, height=150, fg_color= "black")
        content = ctk.CTkLabel(frame, text="",)
        frame.pack(padx=10, pady=10, fill="both", expand=True, side="right")
        self.images_to_delete.clear()
        self.add_media_frame.pack(padx=10, pady=10, fill="both", expand=True, side="left")


        self.db.add_element(data,type = "Scheduler")
        self.post_to_delete = ctk.CTkOptionMenu(self.post_frame, values= self.db.show_database("Scheduler"), width= 220)
        self.post_to_delete.grid(row = 1, column = 2, padx = 10, pady = 10)
        return self.post_entries

    def valid_image(self, image):
        t = image.split(".")[-1]
        return ((t in App.PHOTO_FORMATS or t in App.VIDEO_FORMATS), t in App.VIDEO_FORMATS)


    def select_file(self):
        # Ask for a file
        filename = filedialog.askopenfilename()
        valid, is_video = self.valid_image(filename)

        if not valid:
            messagebox.showwarning(message = f"Non Valid Image. Format is not correct, only {App.VIDEO_FORMATS}, {App.PHOTO_FORMATS}")

        frame = ctk.CTkFrame(self.scrollable_images, width=100, height=150, fg_color= "black")
        if is_video:
            content_vid = VideoC(filename)
            content = ctk.CTkLabel(frame, text="")
            if content_vid.width/100 > content_vid.height/150:
                size = (100, 100*content_vid.height/content_vid.width)
            else:
                size = (150*content_vid.width/content_vid.height, 150)
            self.update_video(content, content_vid, size)
        else:
            image = Image.open(filename)
            if image.size[0]/100 > image.size[1]/150:
                content_img = ctk.CTkImage(image, size=(100, 100*image.size[1]/image.size[0]))
            else:
                content_img = ctk.CTkImage(image, size=(150*image.size[0]/image.size[1], 150))
            content = ctk.CTkLabel(frame, text="", image=content_img)
        self.images_to_delete.append(frame)

        self.media.append((frame,filename))
        self.post_entries["Media"].append(filename)
        content.place(relx=0.5, rely=0.5, anchor="center")
        self.reload_media()

    def update_video(self, label, vid, size):
        # Retrieve data if its possible
        ret, frame = vid.get_frame()
        if ret:
            # Make new image with the next frame
            img = ctk.CTkImage(Image.fromarray(frame), size=size)
            label.configure(image=img)
        # While possible, repeat process
        self.root.after(vid.delay, lambda: self.update_video(label, vid, size))

    def reload_media(self):
        # While is charging, packforget allows to not show frame
        self.add_media_frame.pack_forget()
        # for frame, _ in self.media:
            # frame.pack_forget()
        for i, (frame, _) in enumerate(self.media):
            # Frame position
            frame.pack(padx=10, pady=10, fill="both", expand=True, side="right")
        if len(self.media):
            self.add_media_frame.pack(padx=10, pady=10, fill="y", expand=True, side="right")


def get_thumbnail_path(video_path):
    image_path = "my_video_frame.png"
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    t_msec = 1000*(1)
    video.set(cv2.CAP_PROP_POS_MSEC, t_msec)
    ret, frame = video.read()
    cv2.imwrite(image_path, frame)
    return rf"{getcwd()}/{image_path}"


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry(("1070x450"))
    app = App(root)
    root.mainloop()
