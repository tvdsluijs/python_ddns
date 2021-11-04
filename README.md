# Welcome to Python Auto DDNS 👋
![Version](https://img.shields.io/badge/version-1-blue.svg?cacheSeconds=2592000)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)
[![Twitter: sffdfsfd](https://img.shields.io/twitter/follow/itheo_tech.svg?style=social)](https://twitter.com/itheo_tech)

Script to set your home (or business) IP address via cloudflare dns on A-record domain record.

Specially used when you do not have a fixed IP address.

This script checks your current IP address by using the Amazon service checkip.amazonaws.com. The service checkip.amazonaws.com provides the public IP address of the client making the request. Please be sure that your device running this script is not behind a VPN.

## Installation

do a git clone
```bash
git clone git@github.com:tvdsluijs/python_ddns.git
```

Go into the folder that was created
```bash
cd python_ddns
```

Create an environment when needed within the folder
```bash
# macOS/Linux
# You may need to run sudo apt-get install python3-venv first
python3 -m venv .venv

# Windows
# You can also use py -3 -m venv .venv
python -m venv .venv
```

Then install the needed requirements with
```bash
pip install -r requirements.txt
```

Create a config.ini from the config_sample.ini

> NOTICE: KEEP your zone_id and API-Key to yourself!!!! Do not share with anyone!!!

With the following information

* zone_id =
* api_token =
* ip_address_type = A
* dns_name =

## Prerequisites

For this script to work your need:
1. A cloudflare account (pick the free one)
2. Set a A-record, with current ip address to the desired domain / subdomain
3. A zone_id, can be found on the right side of the screen when you scroll down
4. A API-Key, also found on right side of screen, make sure the API-key is able to edit the DNS

## Usage

```sh
python ddns.py
```

That's all folks!

## Docker environment

> Notice! Before building and running the Dockerfile please create your own config.ini file with the right information

You can als run a docker instance with this script (as you like running Dockers)

This docker is running the Alpine Python framework. It's smaller than 80Mb, so lightweight (the normal python mage is 980mb)! Great to run on a Raspberry Pi.

To create the Docker environment (I assume you already have docker running) do:

```bash
docker build -t auto_ddns .
```

The docker build command builds Docker images from a Dockerfile and a “context”. A build’s context is the set of files located in the specified PATH or URL. The build process can refer to any of the files in the context. For example, your build can use a COPY instruction to reference a file in the context.

To run the docker (on the background) do:

```bash
docker run -d auto_ddns
```

That's all folks!


## Author

👤 **Theo van der Sluijs**

* Website: https://itheo.tech
* Twitter: [@itheo_tech](https://twitter.com/itheo_tech)
* Github: [@tvdsluijs](https://github.com/tvdsluijs)
* LinkedIn: [@tvandersluijs](https://www.linkedin.com/in/tvandersluijs/)

## Show your support

Give a ⭐️ if this project helped you! And a donation is always very welcome! (Just to buy a cup of coffee!)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update or create tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
