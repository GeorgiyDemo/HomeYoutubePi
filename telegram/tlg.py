"""
    Клиент Telegram для добавления плейлиста воспроизведения на Raspberry Pi
"""

import time

import redis
import rq
import telegram
import yaml
from telegram.error import NetworkError, Unauthorized


class GetSettingsClass(object):
    """
    Чтение настроек с yaml
    """

    def __init__(self):
        self.get_settings()

    def get_settings(self):
        with open("./yaml/settings.yml", 'r') as stream:
            self.c = yaml.safe_load(stream)


class TelegramCli(object):
    """
    Запуск Telegram-клиента
    """

    def __init__(self, queue, token, proxy):

        self.queue = queue
        request = telegram.utils.request.Request(proxy_url=proxy)

        self.update_id = None
        self.bot = telegram.Bot(token, request=request)

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

        for update in self.bot.get_updates(offset=self.update_id, timeout=10):
            self.update_id = update.update_id + 1
            user_msg = update.message.text

            if user_msg == "/start":
                update.message.reply_text("Привет, добро пожаловать в коммуналку Демы\nСкинь ссылку на видос YouTube")
                self.bot.sendPhoto(chat_id=update.message.chat.id,
                                   photo='https://sun9-37.userapi.com/c857624/v857624432/10708d/u7yl1BWKmDY.jpg')

            elif "youtube.com" in user_msg or "youtu.be" in user_msg:
                self.queue.enqueue('video_player.MainClass', user_msg, timeout=-1)
                update.message.reply_text("Добавили видео в очередь 😉")


def main():
    # Подключение очереди rq
    queue = rq.Queue('youtube', connection=redis.Redis.from_url('redis://redis:6379/0'))
    # Получаем настройки бота
    obj = GetSettingsClass()
    # Запускаем клиент
    TelegramCli(queue, obj.c["telegram_token"], obj.c["proxy_str"])


if __name__ == '__main__':
    main()
