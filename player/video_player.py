import subprocess
from omxplayer import OMXPlayer

class MainClass():
    def __init__(self, video_url):
        self.video_url = video_url
        self.processing()
    
    def processing(self):
        
        proc = subprocess.Popen(['youtube-dl','-f','best', '-g', self.video_url], stdout=subprocess.PIPE)
        realurl=proc.stdout.read()
        player = OMXPlayer(realurl.decode("utf-8", "strict")[:-1],args=['-o', 'local'])