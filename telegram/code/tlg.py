import os
import time

import redis
import rq
import telegram
from telegram.error import NetworkError, Unauthorized


class TelegramCli:
    """Telegram CLI for launching youtube-dl on RPI"""

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
            if update.message.text is None:
                user_msg = ""
            else:
                user_msg = update.message.text

            if user_msg == "/start":
                string = "Welcome to Demka's house\nGive me YouTube's video link 📼"
                update.message.reply_text(string)

            elif "youtube.com" in user_msg or "youtu.be" in user_msg:
                self.queue.enqueue("video_player.MainClass", user_msg, timeout=-1)
                update.message.reply_text("Added video to the queue 😉")

            else:
                update.message.reply_text("Wrong URL 😕")


def main():

    # rq connector
    queue = rq.Queue("youtube", connection=redis.Redis.from_url("redis://redis:6379/0"))

    tg_token = os.getenv("TELEGRAM_TOKEN", None)
    tg_proxy = os.getenv("TELEGRAM_PROXY", None)
    TelegramCli(queue, tg_token, tg_proxy)


if __name__ == "__main__":
    main()
