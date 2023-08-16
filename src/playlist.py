from src.video import Video
from datetime import timedelta
import isodate


class PlayList(Video):
    def __init__(self, playlist_id):
        playlists = super().get_service().playlists().list(id=playlist_id,
                                                           part='id,snippet',
                                                           ).execute()
        self.playlist_id = playlist_id
        self.title = playlists['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlists['items'][0]['id']}"
        playlist_videos = super().get_service().playlistItems().list(playlistId=playlist_id,
                                                                     part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()
        playlist_video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.video_response = super().get_service().videos().list(part='contentDetails,statistics',
                                                             id=','.join(playlist_video_ids)
                                                             ).execute()

    @property
    def total_duration(self):
        """
        Возвращает общее время всех видео в плейлисте
        """
        total_duration = timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        likes_count = 0
        for video in self.video_response['items']:
            if likes_count < int(video['statistics']['likeCount']):
                likes_count = int(video['statistics']['likeCount'])
                best_video_id = video['id']

        return f"https://youtu.be/{best_video_id}"
