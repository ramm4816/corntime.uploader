import requests, time

class test:
    def __init__(self) -> None:
        
        self.filmix_headers =  {
            'Cache-Control': 'no-cache',
            'cookie': 'dle_user_id=825356; dle_password=8ff78a9e53c673a21c6b354c7cb865a5; remember_me=1; _ga=GA1.1.890962328.1671787536; dle_hash=8959a02cdd197fc3992abe5737a535b2; _ga_GYLWSWSZ3C=GS1.1.1674399214.24.0.1674399214.0.0.0; x-a-key=sinatra; FILMIXNET=3b563ieqmrrfvi7c23l21qstgc; ishimura=260ff49b34a54f611f116eb366e5312a3b88db0d',
            'x-requested-with': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded'
        }


    def get_playlist(self, post_id):
        res = requests.request("POST", proxies={'https': f'http://1c5cM8:Lrv4GD@107.152.153.214:9911'}, timeout=5, url=f'https://filmix.zone/api/movies/player-data?t={round(time.time()*1000)}', data=f'post_id={post_id}&showfull=true', headers=self.filmix_headers)                        
        player_info = res.json()
        print(player_info)

test = test()
test.get_playlist(138052)