![Release](https://img.shields.io/github/v/release/meteoritesolutions/multistream)
[![Publish Release](https://github.com/meteoritesolutions/multistream/actions/workflows/release.yaml/badge.svg)](https://github.com/meteoritesolutions/multistream/actions/workflows/release.yaml)

# Multistream

## Requirements

- Python 3.9+

- [NGINX](https://nginx.org/) 1.19+

- [NGINX RTMP Module](https://github.com/arut/nginx-rtmp-module)

## Installing

```bash
pip install multistream
```

## Usage

Once installed, you can run Multistream with the `multistream` command!

```bash
# Set directory in which generated config will be placed 
export NGINX_CONFIG_DIRECTORY="/etc/nginx/conf.d/"

multistream
```

If everything is configured properly, you'll have a `RTMP` server running on `127.0.0.1`. You can set your streaming software to point at `rtmp://127.0.0.1/livestream` and go LIVE!
