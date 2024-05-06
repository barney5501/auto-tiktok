import os
import random
from pytube import YouTube, Playlist
from moviepy.editor import VideoFileClip, clips_array

def download_vid(video):
    files = os.listdir('clips')
    vid_name = 1 if len(files)==0 else sorted([int(name.split('.')[0]) for name in os.listdir('.')])[-1]+1
    if type(video) == str:
        video = YouTube(video)
    try:
        video.streams.first().download('clips', filename=f'{vid_name}.mp4')
    except:
        print(video.title, video.age_restricted)
        return None
    return vid_name

def add_game(vid_name):
    yt_vid = VideoFileClip(f'clips/{vid_name}.mp4')
    yt_vid.resize((720,800))

    games = os.listdir('games')
    game = random.choice(games)
    game = VideoFileClip(f'games/{game}').without_audio()
    game = game.subclip(0,yt_vid.duration)
    game = game.resize((720,480))

    export_vid = clips_array([[yt_vid], [game]])

    return export_vid

def upload_to_tiktok(vid_name):
    pass


def vid_pipeline(source):
    vid_name = download_vid(source)
    if not vid_name:
        return
    vid = add_game(vid_name)
    vid.write_videofile(f'output/o{vid_name}.mp4')
    upload_to_tiktok(vid_name)

def run_playlist(playlist_url):
    playlist = Playlist(playlist_url)
    for video in playlist.videos:
        if not video.age_restricted:
            vid_pipeline(video)

def main():
    playlist = "https://www.youtube.com/playlist?list=PLyGzpAS2-Hqyn9Hx7d4-d_XIPinfMeG4e" #pjamas
    run_playlist(playlist)

if __name__ == '__main__':
    main()