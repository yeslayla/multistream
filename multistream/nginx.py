import crossplane
from multistream.logger import logger

def nginx(directive, args=[], block=None) -> dict:
    data = {
        "directive": directive,
        "args": [args] if isinstance(args, str) else args,   
    }
    if block != None:
        data["block"] = block
    
    return data

def generate_app(id, url, streamkey) -> dict:
    return nginx("application", f"stream_{id}",
    [
        nginx("live", "on"),
        nginx("record", "off"),
        nginx("allow", ["publish", "127.0.0.1"]),
        nginx("deny", ["publish", "all"]),
        nginx("push", f"{url}{streamkey}")
    ])

def build_config(apps = []) -> dict:

    push_to_apps = []
    nginx_apps = []
    for app in apps:
        logger.info(f"Generating config for '{app.name}'...")
        nginx_apps.append(app.get_nginx_app())
        push_to_apps.append(
            nginx("push", f"rtmp://localhost/stream_{app.name}")
        )

    nginx_config = [nginx("rtmp", [], [
        nginx("server", [],
        [
            nginx("listen", "1935"),
            nginx("chunk_size", "4096"),
            nginx("notify_method", "get"),
            nginx("application", "livestream",
            [
                nginx("live", "on"),
                nginx("record", "off"),
            ] + push_to_apps),
        ] + nginx_apps)
    ])]

    return crossplane.build(nginx_config)