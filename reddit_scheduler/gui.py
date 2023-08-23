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
        """_summary_
        In the __init__ method the full GUI gets created, it separate the window in two frames, in the left frame, a tab gets created,
        the right frame separates to create the main GUI of the Post Scheduler
        Args:
            root (_type_): the main App, where the gui its created
            media (list): Save the paths to the photos
            self.delete_subreddit_entry: It refers to the Combobox to delete the deleted subreddits
            self.post_to_delete: It refers to the Combobox to delete the deleted posts
            self.choose_subreddit: It retrieves the data of the subreddit
            self.__user_entries (dict): Retrieve the data of the client to save data in the database
            self.__post_entries (dict): Retrieve the data of the Post to save data in the database
            self.tab_left (frame): Tab to interact with the database of Users and Subreddits
            self.frame_right (frame): Frame to interact with the database of Post Scheduler
        """
        # General Division
        self.root = root
        self.media = []
        self.delete_subreddit_entry = None
        self.post_to_delete = None
        self.__user_entries = {"ClientId": None, "ClientSecret": None, "UserAgent": None, "Password": None, "Username": None}
        self.__post_entries = {"Day":None, "Month": None, "Hour":None, "Title": None, "URL": None, "Media": [], "User":None, "Subreddit": None, "Checkbox": None}
        self.choose_subreddit = None
        self.tab_left = ctk.CTkTabview(master = root, width = 500, height = 430)
        self.tab_left.grid(row = 1, column = 1, padx = 10)

        self.frame_right = ctk.CTkFrame(master= root, width = 500, height = 450)
        self.frame_right.grid(row = 1, column = 2)
        self.db = ctrl.Controlador()

        self.post_frame = ctk.CTkFrame(master = self.frame_right)
        self.post_frame.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.subreddit_frame = self.tab_left.add("Subreddits")
        user_frame = self.tab_left.add("Users")
        self.delpost_frame = self.tab_left.add("Posts")

        post_label = ctk.CTkLabel(self.delpost_frame, text = "Delete:")
        post_label.grid(row = 1, column = 1, padx = 10, pady = 30)

        self.__frame_to_delete_post()
        add_button = ctk.CTkButton(self.delpost_frame, text = "Submit", command=self.delete_post)
        add_button.grid(row = 1, column = 3, padx = 10, pady = 10)

        # Subreddits GUI
        sbt = ctk.CTkLabel(self.subreddit_frame, text = "Add")
        sbt.grid(row = 2, column = 1, padx = 40, pady = 40)
        self.entrysub = ctk.CTkEntry(self.subreddit_frame)
        self.entrysub.grid(row = 2, column = 2, padx = 10, pady = 30)
        add_button = ctk.CTkButton(self.subreddit_frame, text = "Submit",command = self.__add_subreddit)
        add_button.grid(row = 2, column = 3, padx = 10, pady = 10)

        dele = ctk.CTkLabel(self.subreddit_frame, text = "Delete:")
        dele.grid(row = 4, column = 1, padx = 10, pady = 30)
        self.__subreddit_option_menu()
        add_button = ctk.CTkButton(self.subreddit_frame, text = "Submit", command=self.__delete_subreddit)
        add_button.grid(row = 4, column = 3, padx = 10, pady = 10)

        add_user_frame = ctk.CTkFrame(user_frame)
        add_user_frame.grid(row = 1, padx = 20, pady = 20)

        # Create the labels and add it in the tab of Users
        for i, label_text in enumerate(self.__user_entries.keys(), start=1):
            label = ctk.CTkLabel(add_user_frame, text=label_text + ":")
            label.grid(row=i, column=1, padx=5, pady=5)

            self.__user_entries[label_text] = ctk.CTkEntry(add_user_frame, width=300)
            self.__user_entries[label_text].grid(row=i, column=2, padx=5, pady=5)

        # Button to append it to the Database
        add_button = ctk.CTkButton(add_user_frame, text = "Submit", width = 300, command=self.__add_user_button)
        add_button.grid(row = 9, column = 2, padx = 5, pady = 5)

        self.us_del_frame = ctk.CTkFrame(user_frame)
        self.us_del_frame.grid(row = 2)

        # USER TO DELETE
        delelbl = ctk.CTkLabel(self.us_del_frame, text = "Delete:")
        delelbl.grid(row = 1, column = 1, padx = 20, pady = 10)

        self.user_delete_option()

        del_user_button = ctk.CTkButton(self.us_del_frame, text = "Submit", command= self.__delete_user_button)
        del_user_button.grid(row = 1, column = 3, padx = 10, pady = 10)


        ## Division for Content, calendar and entries
        self.intraframe_up = ctk.CTkFrame(master = self.post_frame, width = 500, height = 250)
        self.intraframe_up.grid(row = 1, column = 1, padx = 15, pady = 17)

        self.intraframe_down = ctk.CTkFrame(master = self.post_frame, width= 500, height= 250)
        self.intraframe_down.grid(row = 2, column = 1, padx = 15, pady = 17)

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
        self.__post_entries["Title"] = ctk.CTkEntry(master = self.intraframe_down, width = 340)
        self.__post_entries["Title"].grid(row = 1,column = 2, pady  = 10, padx = 20)


        ## Title of URL
        url = ctk.CTkLabel(master = self.intraframe_down, text = "URL:")
        url.grid(row = 2, column = 1, pady = 3, padx =10)
        self.__post_entries["URL"] = ctk.CTkEntry(master = self.intraframe_down, width = 340)
        self.__post_entries["URL"].grid(row = 2,column = 2, pady  = 10, padx = 20)

        # Option Menu Users
        users_lbl = ctk.CTkLabel(master = self.intraframe_down, text = "User:")
        users_lbl.grid(row = 4, column = 1, pady = 3, padx =10)
        self.user_option_frame()
        self.__create_subreddit_checkbox()

        ## Submit_button
        submit_scheduler = ctk.CTkButton(master = self.intraframe_down, text = "Submit", command= self.on_submit_post)
        submit_scheduler.grid(row = 6, column = 2, pady = 10)

    def user_delete_option(self):
        if isinstance(self, ctk.CTkOptionMenu):
            self.userdelete.destroy()
        self.userdelete = ctk.CTkOptionMenu(self.us_del_frame, values= self.db.show_database("Users"))
        self.userdelete.grid(row = 1, column = 2, padx = 10, pady = 10)


    def user_option_frame(self):
        if isinstance(self, ctk.CTkOptionMenu):
            self.__post_entries["User"].destroy()
        self.__post_entries["User"] = ctk.CTkOptionMenu(master = self.intraframe_down, values = self.db.show_database("Users"), width= 340)
        self.__post_entries["User"].grid(row = 5, column  = 2, pady  = 3, padx = 10)


    def __frame_to_delete_post(self):
            if isinstance(self.choose_subreddit, ctk.CTkOptionMenu):
                self.post_to_delete.destroy()
            self.post_to_delete = ctk.CTkOptionMenu(self.delpost_frame, values= self.db.show_database("Scheduler"), width= 220)
            self.post_to_delete.grid(row = 1, column = 2, padx = 10, pady = 10)


    def __subreddit_option_menu(self):
        if isinstance(self.choose_subreddit, ctk.CTkOptionMenu):
            self.sbdelete.destroy()
        self.sbdelete = ctk.CTkOptionMenu(self.subreddit_frame, values= self.db.show_database("Subreddits"))
        self.sbdelete.grid(row = 4, column = 2, padx = 10, pady = 10)


    def __create_subreddit_checkbox(self):
            if isinstance(self.choose_subreddit, ctk.CTkFrame):
                self.choose_subreddit.destroy()
            self.choose_subreddit = ctk.CTkFrame(master= self.frame_right, width = 190, height = 100)
            self.choose_subreddit.grid(row = 1,column = 2, padx = 10, pady = 10)
            _ = ctk.CTkLabel(master = self.choose_subreddit, text = "Subreddit/s:", font = ctk.CTkFont(family="Helvetica", size=14))
            _.pack(padx = 10, pady = 7)
            self.scroller = ctk.CTkScrollableFrame(master = self.choose_subreddit, orientation= "vertical", width  = 150, height= 50)
            self.scroller.pack(padx = 10, pady = 10, fill = "both")

            sb = self.db.show_database("Subreddits")
            self.__post_entries["Subreddit"] = []
            for i in range(len(sb)):
                self.__post_entries["Subreddit"].append(ctk.CTkCheckBox(master = self.scroller, text = sb[i]))
                self.__post_entries["Subreddit"][-1].pack(padx = 5, pady = 5, side = "bottom", fill = "both")
                self.__post_entries["Subreddit"][-1].pack_propagate(False)

            ## CheckBox
            self.__post_entries["Checkbox"] = (ctk.CTkCheckBox(master = self.choose_subreddit, text = "NSFW"),
                                               ctk.CTkCheckBox(master = self.choose_subreddit, text = "GIF"))

            self.__post_entries["Checkbox"][0].pack(padx = 10, pady = 10)
            self.__post_entries["Checkbox"][1].pack(padx = 10, pady = 10)


    def delete_post(self):
        """Delete a post using methods of db.py by title and date"""
        splitted = self.post_to_delete.get().split(":")
        title = splitted[2]
        date = splitted[1].split(",")[0][1:]

        self.db.delete_element((date,title[1:]),type = "Scheduler")
        self.__frame_to_delete_post()


    def calendar(self,root):
        """When the button is pressed, gui creates a new window with entries of Date,hour,year"""
        button_date = ctk.CTkButton(text ="Schedule date",master = root, command=self.__on_calendar_button_click)
        button_date.grid(row  =1, column = 1)


    def __on_calendar_button_click(self):
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

        self.__post_entries["Day"] = day
        self.__post_entries["Month"] = month
        self.__post_entries["Hour"] = hour

        day.grid(row = 1, column = 2, pady = 1.5, sticky = 'nsew')
        month.grid(row = 2, column = 2, pady = 1.5,  sticky = 'nsew')
        hour.grid(row = 3, column = 2, pady = 1.5, sticky = 'nsew')


    def __delete_subreddit(self):
        print(f"Subreddit a Borrar: {self.sbdelete.get()}")
        self.db.delete_element(self.sbdelete.get(),"Subreddits")
        self.__post_entries["User"].destroy()
        self.__subreddit_option_menu()
        self.__create_subreddit_checkbox()
        return self.sbdelete.get()


    def __add_subreddit(self):
        print(f"Subreddit agregado: {self.entrysub.get()}")
        self.db.add_element(str(self.entrysub.get()),"Subreddits")
        self.__subreddit_option_menu()
        self.__create_subreddit_checkbox()
        return self.entrysub.get()


    def __add_user_button(self):
        data = []
        for key, value in self.__user_entries.items():
            data.append(value.get())
            print(key, ":", value.get() if type(value) != list else value)
        self.db.add_element(data,"Users")
        self.__create_subreddit_checkbox()
        self.user_option_frame()
        self.user_delete_option()
        return self.__user_entries


    def __delete_user_button(self):
        print(f"User a borrar: {self.userdelete.get()}")
        self.db.delete_element(value = str(self.userdelete.get()), type = "Users")
        self.__create_subreddit_checkbox()
        self.user_option_frame()
        self.user_delete_option()
        return self.userdelete


    def on_submit_post(self):
        """When all of the data is allocated and the submit button is pressed, post data gets saved in reddit.db"""
        data = []

        try:
            for element in ["Media", "Subreddit", "Title", "URL", "Date", "Hour","User", "Checkbox"]:
                if element == "Date":
                    day = self.__post_entries["Day"].get()
                    self.__post_entries["Day"]
                    month = self.__post_entries["Month"].get()
                    data.append(f"{day}/{month}/{str(time.localtime(time.time()).tm_year)}")

                elif element == "Media":
                    cadena_files = ""
                    for file in self.__post_entries[element]:
                        cadena_files += f"@@{file}"
                    data.append(cadena_files)
                    self.__post_entries[element].clear()

                elif element == "Subreddit":
                    subreddit_text = ""
                    for checkbox in self.__post_entries["Subreddit"]:
                        if checkbox.get() == True:
                            subreddit_text += f"@@{checkbox._text}"
                    data.append(subreddit_text)

                elif element == "Checkbox":
                    nsfw = self.__post_entries["Checkbox"][0].get()
                    gif = self.__post_entries["Checkbox"][1].get()
                    data.append(f"{nsfw}{gif}")
                    self.__post_entries["Checkbox"] = None

                else:
                    data.append(self.__post_entries[element].get())
                    self.__post_entries[element] = None
        except AttributeError:
            messagebox.showwarning(message = f"You must choose a date and time")

        self.add_media_frame.forget()
        frame = ctk.CTkFrame(self.scrollable_images, width=100, height=150, fg_color= "black")
        content = ctk.CTkLabel(frame, text="",)
        frame.pack(padx=10, pady=10, fill="both", expand=True, side="right")
        self.add_media_frame.pack(padx=10, pady=10, fill="both", expand=True, side="left")

        self.db.add_element(data,type = "Scheduler")
        self.__frame_to_delete_post()
        return self.__post_entries


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

        self.media.append((frame,filename))
        self.__post_entries["Media"].append(filename)
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
        for i, (frame, _) in enumerate(self.media):
            # Frame position
            frame.pack(padx=10, pady=10, fill="both", expand=True, side="right")
        if len(self.media):
            self.add_media_frame.pack(padx=10, pady=10, fill="y", expand=True, side="right")


def get_thumbnail_path(video_path):
    """Get first frame of the video and choose it as a Thumbnail"""
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
    root.geometry(("1215x450"))
    app = App(root)
    root.mainloop()
