"""
    Клиент Telegram для добавления плейлиста воспроизведения на Raspberry Pi
"""

import time
import os
import redis
import rq
import telegram
from telegram.error import NetworkError, Unauthorized



class TelegramCli(object):
    """
    Запуск Telegram-клиента
    """

    def __init__(self, queue, token, proxy):

        self.queue = queue
        self.update_id = None
        
        if proxy is not None and proxy != "":
            request = telegram.utils.request.Request(proxy_url=proxy)
            self.bot = telegram.Bot(token, request=request)
        else:
            self.bot = telegram.Bot(token)

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
            if update.message.text == None:
                user_msg = ""
            else:
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
    # Запускаем клиент
    tg_token = os.getenv('TELEGRAM_TOKEN', None)
    tg_proxy = os.getenv('TELEGRAM_PROXY', None)
    TelegramCli(queue, tg_token, tg_proxy)

if __name__ == '__main__':
    main()
