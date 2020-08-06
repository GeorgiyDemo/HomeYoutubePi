import subprocess
import time

import psutil
from omxplayer import OMXPlayer


class MainClass:
    def __init__(self, video_url):
        self.process_name = "omxplayer"
        self.video_url = video_url
        self.processing()

    def checkIfProcessRunning(self):
        """
        - Checker for excecuting proc
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
        - Get videostream from youtube-dl
        - Launch omxplayer
        :return:
        """
        # It can't connect to dbus sometimes, looks good
        try:
            proc = subprocess.Popen(
                ["youtube-dl", "-f", "best", "-g", self.video_url],
                stdout=subprocess.PIPE,
            )
            realurl = proc.stdout.read()
            OMXPlayer(realurl.decode("utf-8", "strict")[:-1], args=["-o", "local"])
        except:
            pass
        # for FIFO queue
        while self.checkIfProcessRunning():
            time.sleep(3)
