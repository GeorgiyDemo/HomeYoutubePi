"""
    Клиент Telegram для добавления плейлиста восроизведения на Raspberry Pi
"""

import rq
import telegram
import time
import yaml

from telegram.error import NetworkError, Unauthorized


class GetSettingsClass(object):
    """
    Класс для чтения настроек с yaml
    """

    def __init__(self):
        self.get_settings()

    def get_settings(self):
        with open("./yaml/settings.yml", 'r') as stream:
            self.c = yaml.safe_load(stream)


class TelegramCli(object):

    def __init__(self, token, admin_list):

        self.update_id = None
        self.bot = telegram.Bot(token)
        self.admin_list = admin_list
        try:
            self.update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            self.update_id = None

        while True:
            try:
                self.handler()
            except NetworkError:
                time.sleep(1)
            except Unauthorized:
                self.update_id += 1


    def handler(self):
        p_mode = telegram.ParseMode.HTML
        for update in self.bot.get_updates(offset=self.update_id, timeout=10):
            self.update_id = update.update_id + 1

            if update.message.text == "/start":
                    update.message.reply_text("Привет",parse_mode=p_mode)2

def main():
    obj = GetSettingsClass()
    TelegramCli(obj.c["telegram_token"], obj.c["telegram_admins"])


if __name__ == '__main__':
    main()
