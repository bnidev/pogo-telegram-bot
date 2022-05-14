# Pokemon Go Telegram Bot

## Requirements

**Python 3** and the following modules

- [requests](https://pypi.org/project/requests/)
- [geopy](https://pypi.org/project/geopy/)
- [python-telegram-bot](https://pypi.org/project/python-telegram-bot/)

Run `pip install -r requirements.txt` to install all requirements.

## Setup

Rename `config_template.json` to `config.json` and add your information.

- [How the Telegram Bot API works](https://core.telegram.org/bots)
- [How to find your channel id](https://gist.github.com/mraaroncruz/e76d19f7d61d59419002db54030ebe35)

## Usage

Run `cmbot.py` to start the bot.

## Running as daemon process in the background

Using a process manager like [PM2](https://pm2.keymetrics.io/) enables you to run the bot as a deamon process in the background.
Run `pm2 start cmbot.py --interpreter python3` to start the bot with PM2.
