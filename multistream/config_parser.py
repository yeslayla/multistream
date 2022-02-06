from curses import raw
import imp
import json
from multiprocessing.dummy import Array
import apps
def load_config(config_string) -> Array:
    data = []

    json_data = json.loads(config_string)
    if "Apps" in json_data:
        for raw_app in json_data["Apps"]:
            if "platform" in raw_app:
                platform = raw_app["platform"]
                name = raw_app["id"] if "id" in raw_app else None
                url = raw_app["url"] if "url" in raw_app else None
                key = raw_app["key"] if "key" in raw_app else None
                if platform == "twitch":
                    data.append(apps.RtmpTwitch(key))
                elif platform == "custom":
                    if not url or not name:
                        continue
                    data.append(apps.RtmpApplication(name, url, key))

    return data