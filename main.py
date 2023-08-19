import os
from pytube import YouTube
import re

import SongModel as song

UNPROCESSED_PATH = 'C:/Program Files (x86)/UltraStar WorldParty/songs/'
regex = r"\#VIDEO:.*(v=.{11})"
youtube_prefix = 'https://www.youtube.com/watch?'

if __name__ == '__main__':
    cur_dict = dict()
    song_list = list()
    for dirs in os.listdir(UNPROCESSED_PATH):
        print('Found {} entries in {}'.format(len(os.listdir(UNPROCESSED_PATH), UNPROCESSED_PATH)))
        cur_song = song.SongModel(folder_name=dirs)
        for cur_file in os.listdir(UNPROCESSED_PATH + dirs):
            if cur_file.endswith(".txt"):
                c_dict = dict()
                f = open(UNPROCESSED_PATH + dirs + "/" + cur_file)
                for line in f:
                    if line.startswith('#VIDEO'):
                        cur_song.video_line = line
                        if 'v=' in line:
                            cur_song.youtube_id_present = True
                    if line.startswith('#MP3'):
                        cur_song.audio_line = line
                    if line.startswith('#COVER'):
                        cur_song.cover_line = line
                f.close()
            elif cur_file.endswith(".mp4") or cur_file.endswith(".avi"):
                cur_song.video_present = True
                cur_song.video_name = cur_file
            elif cur_file.endswith(".mp3"):
                cur_song.audio_present = True
                cur_song.audio_name = cur_file
            elif cur_file.endswith(".jpg") or cur_file.endswith(".png"):
                cur_song.cover_present = True
                cur_song.cover_name = cur_file
        song_list.append(cur_song)
    for cur_song in song_list:
        if not cur_song.video_present:
            if cur_song.video_name is None:
                video_file_name = cur_song.folder_name + '.mp4'
            if cur_song.youtube_id_present:
                watch_id = re.match(regex, video_line).group(1)
                video_line = cur_song.video_line
                youtube_link = youtube_prefix + watch_id
                video = YouTube(youtube_link, use_oauth=True, allow_oauth_cache=True)
                try:
                    video = video.streams.get_highest_resolution()
                except:
                    print('ERROR: Ignore ' + cur_song.folder_name)
                    continue
                try:
                    out_file = video.download(UNPROCESSED_PATH + cur_song.folder_name + '/')
                    base, ext = os.path.splitext(out_file)
                    new_file = UNPROCESSED_PATH + cur_song.folder_name + '/' + cur_song.folder_name + '.mp4'
                    os.rename(out_file, new_file)
                except:
                    print("FAIL")
            else:
                # youtube search
            # download video
        # check video line


        if not cur_song.audio_present:
            #

        audio_video = YouTube(youtube_link, use_oauth=True, allow_oauth_cache=True)
        audio = audio_video.streams.filter(only_audio=True).first()
        try:
            out_file = audio.download(UNPROCESSED_PATH + cur_song.folder_name + '/')
            base, ext = os.path.splitext(out_file)
            new_file = UNPROCESSED_PATH + cur_song.folder_name + '/' + cur_song.folder_name + '.mp3'
            os.rename(out_file, new_file)
        except:
            print("FAIL")
        file_handle = open(UNPROCESSED_PATH + cur_song.folder_name + '/' + cur_song.txt_name, 'r')
        file_string = file_handle.read()
        file_handle.close()
        file_string = file_string.replace(video_line, '#VIDEO:' + cur_song.folder_name + '.mp4\n')
        file_handle = open(UNPROCESSED_PATH + cur_song.folder_name + '/' + cur_song.txt_name, 'w')
        file_handle.write(file_string)
        file_handle.close()
