import subprocess
import time

import psutil
from omxplayer import OMXPlayer


class MainClass():
    def __init__(self, video_url):
        self.process_name = "omxplayer"
        self.video_url = video_url
        self.processing()

    def checkIfProcessRunning(self):
        """
        Проверка на существование процесса
        :return:
        """
        for proc in psutil.process_iter():
            try:
                if self.process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def processing(self):
        """
        - Получение потока воспроизведения с youtube-dl
        - Запуск omxplayer
        :return:
        """
        #Т.к. возникает ошибка коннекта к dbus, но при этом всё работает
        try:
            proc = subprocess.Popen(['youtube-dl', '-f', 'best', '-g', self.video_url], stdout=subprocess.PIPE)
            realurl = proc.stdout.read()
            player = OMXPlayer(realurl.decode("utf-8", "strict")[:-1], args=['-o', 'local'])
        except:
            pass
        # Необходимо для удержания очереди в FIFO
        while self.checkIfProcessRunning():
            time.sleep(3)