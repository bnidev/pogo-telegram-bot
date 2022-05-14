# Pokemon Go Telegram Bot

## Requirements

- **Python 3** and the following modules
- [requests](https://pypi.org/project/requests/)
- [geopy](https://pypi.org/project/geopy/)
- [python-telegram-bot](https://pypi.org/project/python-telegram-bot/)

Run `pip install -r requirements.txt` to install all requirements.

## Start

Run `cmbot.py` to start the bot.

## Running as daemon process in the background

Using a process manager like [PM2](https://pm2.keymetrics.io/) enables you to run the bot as a deamon process in the background.
Run `pm2 start cmbot.py --interpreter python3` to start the bot with PM2.
