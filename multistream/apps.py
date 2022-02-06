import json
import requests
import multistream.nginx as nginx
from multistream.logger import logger

class RtmpApplication:

    name : str = "invalid"
    service_type : str = "custom"
    _stream_key : str = ""
    _url : str = ""

    def __init__(self, name, url, key = "") -> None:
        self.name = name
        self._url = url
        self._stream_key = key
    
    @classmethod
    def new(cls, raw_data : dict):
        return RtmpApplication(raw_data["name"], raw_data["server"], raw_data["stream_key"])

    @property
    def stream_key(self) -> str:
        return self._stream_key

    def get_url(self) -> str:
        return self._url
    
    def get_nginx_app(self) -> dict:
        return nginx.generate_app(self.name, self.get_url(), self.stream_key)


class RtmpTwitch(RtmpApplication):
    name = "twitch"
    service_type = "twitch"
    
    def __init__(self, stream_key) -> None:
        self._stream_key = stream_key

    @classmethod
    def new(cls, raw_data : dict):
        new_app = RtmpTwitch(raw_data["stream_key"])
        if "name" in raw_data:
            new_app.name = raw_data["name"]
        return new_app

    def get_ingestion_server(self) -> str:
        r = requests.get("https://ingest.twitch.tv/ingests")
        if r.status_code == 200:
            data = r.json()
            if "ingests" in data:
                if len(data["ingests"]) > 0:
                    return data["ingests"][0]["url_template"]
        logger.warn("Failed to get ingestion server! Using default.")
        return "rtmp://ord02.contribute.live-video.net/app/{stream_key}"

    def get_url(self) -> str:
        return self.get_ingestion_server().replace("{stream_key}", "")

services = [RtmpApplication, RtmpTwitch]