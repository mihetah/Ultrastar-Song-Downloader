import asyncio
import os
import re

import requests as requests
import sacad
from pytube import YouTube, Search
from sacad import CoverImageFormat

import SongModel as Song

UNPROCESSED_PATH = 'I:/Vocaluxe/Songs/'
regex = r"\#VIDEO:.*(v=.{11})"
youtube_prefix = 'https://www.youtube.com/watch?'


def download_video(_cur_song):
    _video = YouTube(_cur_song.youtube_link, use_oauth=True, allow_oauth_cache=True)
    _video = _video.streams.get_highest_resolution()
    _out_file = _video.download(UNPROCESSED_PATH + _cur_song.folder_name + '/')
    _new_file = UNPROCESSED_PATH + _cur_song.folder_name + '/' + _cur_song.video_name
    os.rename(_out_file, _new_file)
    _cur_song.video_present = True
    return _cur_song


def download_audio(_cur_song):
    _audio_video = YouTube(_cur_song.youtube_link, use_oauth=True, allow_oauth_cache=True)
    _audio = _audio_video.streams.filter(only_audio=True).first()
    try:
        _out_file = _audio.download(UNPROCESSED_PATH + _cur_song.folder_name + '/')
        _new_file = UNPROCESSED_PATH + _cur_song.folder_name + '/' + _cur_song.folder_name + '.mp3'
        os.rename(_out_file, _new_file)
    except:
        print("FAIL")
    _cur_song.audio_present = True
    return _cur_song


def search_youtube(_cur_song, _video_file_name):
    search = Search(_video_file_name[0:-4])
    video = search.results[0]
    _youtube_link = video.watch_url
    _cur_song.youtube_link = _youtube_link
    _cur_song.youtube_id_present = True
    return _cur_song


def check_file_names(_cur_song):
    if cur_song.video_name is None:
        _cur_song.video_name = cur_song.folder_name + '.mp4'
    if cur_song.audio_name is None:
        _cur_song.audio_name = cur_song.folder_name + '.mp3'
    if cur_song.cover_name is None:
        _cur_song.cover_name = cur_song.folder_name + '.jpg'
    return _cur_song


def update_txt_file(_cur_song, _missing_video_counter, _missing_audio_counter, _missing_cover_counter):
    file_handle = open(UNPROCESSED_PATH + _cur_song.folder_name + '/' + _cur_song.txt_name, 'r')
    file_string = file_handle.read()
    file_handle.close()
    new_video_line = '#VIDEO:' + _cur_song.video_name + '\n'
    new_audio_line = '#MP3:' + _cur_song.audio_name + '\n'
    new_cover_line = '#COVER:' + _cur_song.cover_name + '\n'
    file_changed = False
    if _cur_song.video_line is None:
        # insert after title line
        file_string = file_string.replace('#TITLE:' + _cur_song.title + '\n',
                                          '#TITLE:' + _cur_song.title + '\n' + new_video_line)
        file_changed = True
        _cur_song.video_line = new_video_line
        _missing_video_counter -= 1
    elif _cur_song.video_line != new_video_line:
        file_string = file_string.replace(_cur_song.video_line, new_video_line)
        file_changed = True
        _missing_video_counter -= 1
    if _cur_song.audio_line is None:
        # insert after video line
        file_string = file_string.replace(_cur_song.video_line, _cur_song.video_line + new_audio_line)
        file_changed = True
        _missing_audio_counter -= 1
    if _cur_song.audio_line != new_audio_line:
        file_string = file_string.replace(_cur_song.audio_line, new_audio_line)
        file_changed = True
        _missing_audio_counter -= 1
    if _cur_song.cover_line is None:
        # insert before video line
        file_string = file_string.replace(new_video_line, new_cover_line + new_video_line)
        file_changed = True
        _missing_cover_counter -= 1
    elif _cur_song.cover_line != new_cover_line:
        file_string = file_string.replace(_cur_song.cover_line, new_cover_line)
        file_changed = True
        _missing_cover_counter -= 1
    if file_changed:
        file_handle = open(UNPROCESSED_PATH + _cur_song.folder_name + '/' + _cur_song.txt_name, 'w')
        file_handle.write(file_string)
        file_handle.close()
    return _missing_video_counter, _missing_audio_counter, _missing_cover_counter


if __name__ == '__main__':
    song_list = list()
    print('Found {} songs in {}'.format(len(os.listdir(UNPROCESSED_PATH)), UNPROCESSED_PATH))
    for dirs in os.listdir(UNPROCESSED_PATH):
        cur_song = Song.SongModel()
        cur_song.folder_name = dirs
        for cur_file in os.listdir(UNPROCESSED_PATH + dirs):
            if cur_file.endswith(".txt"):
                c_dict = dict()
                f = open(UNPROCESSED_PATH + dirs + "/" + cur_file)
                for line in f:
                    if line.startswith('#VIDEO'):
                        cur_song.video_line = line
                        if 'v=' in line:
                            cur_song.youtube_id_present = True
                            cur_song.youtube_link = youtube_prefix + re.match(regex, line).group(1)
                    elif line.startswith('#MP3'):
                        cur_song.audio_line = line
                    elif line.startswith('#COVER'):
                        cur_song.cover_line = line
                    elif line.startswith('#TITLE'):
                        cur_song.title = line[7:-1]
                    elif line.startswith('#ARTIST'):
                        cur_song.artist = line[8:-1]
                f.close()
                cur_song.txt_name = cur_file
            elif cur_file.endswith(".mp4") or cur_file.endswith(".avi"):
                cur_song.video_present = True
                cur_song.video_name = cur_file
            elif cur_file.endswith(".mp3"):
                cur_song.audio_present = True
                cur_song.audio_name = cur_file
            elif cur_file.endswith(".jpg") or cur_file.endswith(".png"):
                cur_song.cover_present = True
                cur_song.cover_name = cur_file
        if cur_song.txt_name is None:
            print('No txt file found for {}'.format(cur_song.folder_name))
            continue
        song_list.append(cur_song)
    missing_video_counter = len([x for x in song_list if not x.video_present])
    original_missing_video_counter = missing_video_counter
    missing_audio_counter = len([x for x in song_list if not x.audio_present])
    original_missing_audio_counter = missing_audio_counter
    missing_cover_counter = len([x for x in song_list if not x.cover_present])
    original_missing_cover_counter = missing_cover_counter
    print('Found {} songs with missing video, {} with missing audio and {} with missing cover'.format(
        missing_video_counter, missing_audio_counter, missing_cover_counter))
    for cur_song in song_list:
        # print('Downloading {}'.format(cur_song.folder_name))
        searched_youtube = False
        cur_song = check_file_names(cur_song)
        # video
        if not cur_song.video_present:
            if cur_song.youtube_id_present:
                try:
                    cur_song = download_video(cur_song)
                except Exception as e:
                    print(
                        'Failed to download video for {} trying search, exception: {}'.format(cur_song.folder_name, e))
                    cur_song = search_youtube(cur_song, cur_song.video_name)
                    searched_youtube = True
            else:
                # YouTube search
                cur_song = search_youtube(cur_song, cur_song.video_name)
                searched_youtube = True
                try:
                    cur_song = download_video(cur_song)
                except Exception as e:
                    print('Failed to download video for {}, exception: {}'.format(cur_song.folder_name, e))
                    continue
        # audio
        if not cur_song.audio_present:
            if cur_song.youtube_id_present:
                cur_song = download_audio(cur_song)
            elif not searched_youtube:
                cur_song = search_youtube(cur_song, cur_song.video_name)
                searched_youtube = True
                try:
                    cur_song = download_audio(cur_song)
                except Exception as e:
                    print('Failed to download audio for {}, exception: {}'.format(cur_song.folder_name, e))
                    continue
        # cover
        if not cur_song.cover_present:
            sources = list()
            sources.append(sacad.COVER_SOURCE_CLASSES['deezer'])
            coroutine = sacad.search_and_download(album=cur_song.title, artist=cur_song.artist,
                                                  out_filepath=UNPROCESSED_PATH + cur_song.folder_name + '/' +
                                                               cur_song.cover_name,
                                                  size=500, format=CoverImageFormat.JPEG, size_tolerance_prct=10,
                                                  source_classes=sources)
            future = asyncio.ensure_future(coroutine)
            asyncio.get_event_loop().run_until_complete(future)
            future.result()
            if cur_file in os.listdir(UNPROCESSED_PATH + cur_song.folder_name + '/'):
                if cur_file.endswith(".jpg"):
                    cur_song.cover_name = cur_file
                    cur_song.cover_present = True
            if not cur_song.cover_present:
                if cur_song.youtube_id_present:
                    thumbnail_url = YouTube(cur_song.youtube_link, use_oauth=True, allow_oauth_cache=True).thumbnail_url
                else:
                    thumbnail_url = Search(cur_song.title + ' ' + cur_song.artist).results[0].thumbnail_url
                if thumbnail_url is not None:
                    # thumbnail_url = thumbnail_url.replace('hqdefault', 'maxresdefault')
                    try:
                        # download image from url
                        r = requests.get(thumbnail_url)
                        # open method to open a file on your system and write the contents
                        with open(UNPROCESSED_PATH + cur_song.folder_name + '/' + cur_song.cover_name, "wb") as code:
                            code.write(r.content)
                        cur_song.cover_present = True
                    except Exception as e:
                        print('Failed to download cover for {}, exception: {}'.format(cur_song.folder_name, e))
                        if cur_song.youtube_id_present:
                            cur_song = search_youtube(cur_song, cur_song.video_name)
                            searched_youtube = True
                            try:
                                thumbnail_url = Search(cur_song.title + ' ' + cur_song.artist).results[0].thumbnail_url
                                # download image from url
                                r = requests.get(thumbnail_url)
                                # open method to open a file on your system and write the contents
                                with open(UNPROCESSED_PATH + cur_song.folder_name + '/' + cur_song.cover_name,
                                          "wb") as code:
                                    code.write(r.content)
                                    cur_song.cover_present = True
                            except Exception as e:
                                print('Failed to download cover for {}, exception: {}'.format(cur_song.folder_name, e))
        missing_video_counter, missing_audio_counter, missing_cover_counter = update_txt_file(cur_song,
                                                                                              missing_video_counter,
                                                                                              missing_audio_counter,
                                                                                              missing_cover_counter)
    print('Updated {} videos, {} audios and {} covers'.format(original_missing_video_counter - missing_video_counter,
                                                              original_missing_audio_counter - missing_audio_counter,
                                                              original_missing_cover_counter - missing_cover_counter))
    missing_videos = [x.folder_name for x in song_list if not x.video_present]
    missing_audios = [x.folder_name for x in song_list if not x.audio_present]
    missing_covers = [x.folder_name for x in song_list if not x.cover_present]
    # print lists pretty
    print('Missing videos: {}'.format(missing_videos))
    print('Missing audios: {}'.format(missing_audios))
    print('Missing covers: {}'.format(missing_covers))
