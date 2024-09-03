from pytube import YouTube
from tqdm import tqdm
from pytube import Playlist
import os
from moviepy.editor import *
from time import time


def check_high_res(youtubeObject):
    res_set = set()
    for i in youtubeObject.streams:
        temp_res = str(i).split(" ")[3][5:][:-1]
        if "video/mp4" in str(i).split(" ")[2]:
            try:
                res_set.add(int(temp_res[:-1]))
            except:
                pass
    return max(res_set)

def check_high_audio(youtubeObject):
    res_set = set()
    for i in youtubeObject.streams:
        temp_res = str(i).split(" ")[3][5:][:-1]
        if "audio/mp4" in str(i).split(" ")[2]:
            try:
                res_set.add(int(temp_res[:-4]))
            except:
                pass
            
    return max(res_set)

def Download(link):
    path = "temp_youtube_video"
    dir_list = os.listdir(path)
    for i in dir_list:
        os.remove(path + "/" + i)

    youtubeObject = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    
    highest_res = check_high_res(youtubeObject)

    for i in youtubeObject.streams:
        temp = str(i).split(" ")
        if temp[3][5:][:-1] == str(highest_res) + "p" and "mp4" in temp[2]:
            itag = temp[1][6:-1]
            break

    youtubeObject_itag = youtubeObject.streams.get_by_itag(itag)

    try:
        youtubeObject_itag.download(output_path="temp_youtube_video")
    except Exception as e:
        print(e)
        print("An error has occurred")
        return False





    path = "temp_youtube_audio"
    dir_list = os.listdir(path)
    for i in dir_list:
        os.remove(path + "/" + i)

    audio_res = check_high_audio(youtubeObject)
    for i in youtubeObject.streams:
        temp = str(i).split(" ")
        if temp[3][5:][:-1] == str(audio_res) + "kbps" and "mp4" in temp[2]:
            itag = temp[1][6:-1]
            break
    
    youtubeObject_itag = youtubeObject.streams.get_by_itag(itag)

    try:
        youtubeObject_itag.download(output_path="temp_youtube_audio")
    except Exception as e:
        print(e)
        print("An error has occurred")
        return False

    # Load the mp4 file
    dir_list = os.listdir(path)
    video = AudioFileClip(f"{path}/{dir_list[0]}")

    # Extract audio from video
    inital_time = time()
    video.write_audiofile(f"{path}/{dir_list[0][:-4]}.mp3", logger = None)
    print(f"Time taken for mp4 to mp3: {time() - inital_time}")

    for i in dir_list:
        if ".mp4" in i:
            os.remove(path + "/" + i)

    return True

def combine_video_and_audio(main_file_path):
    video_path = "temp_youtube_video"
    audio_path = "temp_youtube_audio"
    video_file = os.listdir(video_path)[0]
    audio_file = os.listdir(audio_path)[0]
    my_clip = VideoFileClip(f"{video_path}/{video_file}")
    audio_background = AudioFileClip(f"{audio_path}/{audio_file}")
    final_clip = my_clip.set_audio(audio_background)
    inital_time = time()
    final_clip.write_videofile(f"{main_file_path}/{video_file}", threads = 16, preset = "ultrafast", logger = None)
    print(f"Time taken for combining: {time() - inital_time}")

video_dict = {
    "打泥泥": "https://www.youtube.com/playlist?list=PLOyOeaYn_3iNogEqWE35NDNinkyjMbE1x",
    }

for key, value in video_dict.items():
    os.mkdir(key)

    yt_play = Playlist(value)
    links = []
    for i in yt_play.videos:
        links.append(i.watch_url)

    counter = 0
    for link in links:
        if Download(link):
            combine_video_and_audio(key)
            pass
        else:
            print(link)
        counter += 1
        print(f"Downloaded {counter}/{len(links)} videos")

        