import subprocess

class MainClass():
    def __init__(self, video_url):
        self.video_url = video_url
        self.processing()
    
    def processing(self):
        cmd = "omxplayer `youtube-dl -g -f best "+self.video_url+"` -o local"
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output, error)