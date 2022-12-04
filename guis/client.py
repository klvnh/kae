import aiohttp

class Client:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.spotify_token = ''
        self.url = 'https://api.spotify.com/v1/me/player/currently-playing'
        self.refresh_token = 'AQC6KGOD0lyxyGRfJhcNFIM9JgoxtKvySRxJiC92EkbsnRjePeUR1d3lR9SPQl9KcAJiv0sVCI08lKYYrGt1dEm7wNVB_NfV9pAv7nc3lTiLrffqlQ8Yt0nH2Ulz_rS3qto'
        self.base_64 = 'N2M3NjFhZjU5M2U3NDY3YWIzZDZjYmY5NzljMTg1Njk6NDdlNGQxNzc0ZGZmNDE1ZGE3NWU1MDFjNDgwNzM5ZjY='

    async def get_current_track(self):
        response = await self.session.get(self.url, headers={'Authorization': f'Bearer {self.spotify_token}'})
        json_resp = await response.json()
        track_name = json_resp['item']['name']
        artists = [artist for artist in json_resp['item']['artists']]
        link = json_resp['item']['external_urls']['spotify']
        artist_names = ', '.join([artist['name'] for artist in artists])
        track_cover =  json_resp['item']['album']['images'][0]['url']
        duration = json_resp['item']['duration_ms']
        current_duration = json_resp['progress_ms']
        is_playing = json_resp['is_playing']
        current_track_info = {'link': link, 
                            'track_name': track_name, 
                            'track_cover': track_cover, 
                            'artists': artist_names, 
                            'duration': duration, 
                            'current_duration': current_duration, 
                            'is_playing': is_playing}

        await self.session.close()
        return current_track_info


    async def refresh(self):
        query = 'https://accounts.spotify.com/api/token'
        response = await self.session.post(query,data={f"grant_type": 'refresh_token', 'refresh_token': {self.refresh_token}}, headers={'Authorization': 'Basic ' + self.base_64})
        response_json = await response.json()
        self.spotify_token = response_json['access_token']