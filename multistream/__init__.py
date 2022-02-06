import os, subprocess
import yaml
import multistream.apps as apps, multistream.nginx as nginx
from multistream.logger import logger

version = "0.0.0"

CONFIG_FILE : str = "config.yaml"
CONFIG_API_VERSION : str = "1.0"

def cli() -> None:
    main()

def main() -> None:
    rtmp_apps = []
    config_data : dict = {}

    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config_data = yaml.load(f, Loader=yaml.SafeLoader)
    else:
        logger.error("Config file not found!")
        with open(CONFIG_FILE, "w") as f:
            config_data = {
                "apiVersion": CONFIG_API_VERSION,
                "kind": "MultistreamConfig",
                "apps": [
                    {
                        "service": "twitch",
                        "stream_key": "test"
                    }
                ]
            }
            yaml.dump(config_data, f)
            logger.info("Created default config file!")
        exit(1)

    if not "apiVersion" in config_data or config_data["apiVersion"] != CONFIG_API_VERSION:
        logger.error("Configuration file is out of date. Please update the configuration file.")
        exit(1)
    
    if not "kind" in config_data or config_data["kind"] != "MultistreamConfig":
        logger.error("Configuration file is not a 'MultistreamConfig'.")
        exit(1)

    if not "apps" in config_data:
        logger.error("Configuration file does not contain an 'apps' key.")
        exit(1)
    
    for app in config_data["apps"]:
        if not "service" in app:
            logger.warn("App does not contain a 'service' key.")
            continue
        if not app["service"] in (a.service_type for a in apps.services):
            logger.warn(f"Service '{app['service']}' is not a valid service.")
            continue

        service = next(a for a in apps.services if a.service_type == app["service"])

        try:
            rtmp_app = service.new(app)
        except KeyError as e:
            logger.error(f"{app['service'].capitalize()} app is missing a '{e.args[0]}' key.")
            continue

        if rtmp_app:
            rtmp_apps.append(rtmp_app)
        else:
            logger.warn(f"Failed to create app for service '{app['service']}'.")
            continue

    config_directory = os.environ.get("NGINX_CONFIG_DIRECTORY", ".")

    config = nginx.build_config(rtmp_apps)
    with open(os.path.join(config_directory, "test.conf"), "w") as f:
        f.write(config)

    logger.info("Configuration complete, starting NGINX!")
    
    try:
        subprocess.run(["nginx", "-g", "daemon off;"])
    except FileNotFoundError:
        logger.error("NGINX not found!")
        exit(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()