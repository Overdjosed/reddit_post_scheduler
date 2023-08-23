import time as time
import praw
import db as ctrl
from gui import *
# from tkinter import messagebox

if __name__ == "__main__":
    lt = time.localtime()
    controlador = ctrl.Controlador()
    posts_to_add = controlador.show_database("Scheduler", all = True)

    for tupla in posts_to_add:

        elements = {"Day":tupla[4], "Hour":tupla[5], "Title": tupla[2], "URL": tupla[3], "Media": tupla[0].split("@@"), "User":tupla[6], "Subreddit": tupla[1].split("@@"), "Checkbox": tupla[7]}
        nsfw = True if int(elements["Checkbox"][0]) == 1 else False
        gif = True if int(elements["Checkbox"][1]) == 1 else False
        dd_mm_yy = elements["Day"].split("/")

        # If Day and Year is the same
        if dd_mm_yy[0] == str(lt.tm_mday) and dd_mm_yy[1] == str(lt.tm_mon) and dd_mm_yy[2] == str(lt.tm_year):
            if lt.tm_hour in range(min(0,int(elements["Hour"].split(":")[0])-1),max(int(elements["Hour"].split(":")[0])+1,25)):
                user_dic = controlador.get_element(elements["User"], "Users")

                def upload_photos(photo_paths, title, subreddits, nsfw, gif):
                    reddit = praw.Reddit(client_id=user_dic["client_id"],
                                        client_secret=user_dic["client_secret"],
                                        username=user_dic["username"],
                                        password=user_dic["password"],
                                        user_agent=user_dic["user_agent"])
                    photos = []
                    videos = []

                    for photo_path in photo_paths:
                        # Se trata de una imagen
                        if photo_path.split(".")[-1] in App.PHOTO_FORMATS:
                            photos.append(photo_path)
                        # Se trata de un video
                        elif photo_path.split(".")[-1] in App.VIDEO_FORMATS:
                            videos.append(photo_path)

                    for subreddit in subreddits[1:]:
                        # More than one image
                        if len(photos) > 1:
                            data = [{"image_path": f, "caption": "", "outbound_url": ""} for f in photos]
                            submission = reddit.subreddit(subreddit).submit_gallery(title = title, images = data, nsfw = nsfw)
                        # Only one Image
                        elif len(photos) == 1:
                            print(title,photos[0], nsfw)
                            submission = reddit.subreddit(subreddit).submit_image(title = title, image_path = photos[0], nsfw = nsfw)
                        # Only One video
                        if len(videos) == 1:
                            submission = reddit.subreddit(subreddit).submit_video(title = title, video_path = videos[0], nsfw = nsfw,gif = gif, thumbnail_path = get_thumbnail_path(videos[0]))
                        # Error - Could not upload
                        elif len(videos) > 1:
                            raise messagebox.showwarning(message= "Reddit API Does not allow more than 1 Video per request")

                upload_photos(elements["Media"], elements["Title"], elements["Subreddit"], nsfw, gif)
                controlador.delete_element((elements["Day"], elements["Title"]), "Scheduler")

                # Remove thumbnail photo
                if path.exists(rf"{getcwd()}/my_video_frame.png"):
                    remove(rf"{getcwd()}/my_video_frame.png")


