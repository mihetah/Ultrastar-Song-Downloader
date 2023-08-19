class SongModel:
    folder_name: str = None
    txt_name: str = None
    video_name: str = None
    audio_name: str = None
    cover_name: str = None
    video_line: str = None
    audio_line: str = None
    cover_line: str = None
    video_present: bool = False
    audio_present: bool = False
    cover_present: bool = False
    youtube_id_present: bool = False
    youtube_link: str = None
    title: str = None
    artist: str = None

    def __init__(self, folder_name: str = None, txt_name: str = None, video_line: str = None, audio_line: str = None,
                 cover_line: str = None, video_present: bool = False, audio_present: bool = False,
                 cover_present: bool = False, youtube_id_present: bool = False, video_name: str = None,
                 audio_name: str = None, cover_name: str = None, youtube_link: str = None, title: str = None,
                 artist: str = None):
        self.folder_name: folder_name
        self.txt_name: txt_name
        self.video_line: video_line
        self.audio_line: audio_line
        self.cover_line: cover_line
        self.video_present: video_present
        self.audio_present: audio_present
        self.cover_present: cover_present
        self.youtube_id_present: youtube_id_present
        self.video_name: video_name
        self.audio_name: audio_name
        self.cover_name: cover_name
        self.youtube_link: youtube_link
        self.title: title
        self.artist: artist
